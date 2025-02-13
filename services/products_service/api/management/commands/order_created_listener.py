import json
import pika
import pika.exceptions
import signal
from django.core.management.base import BaseCommand
from django.conf import settings
from api.models import Product
from api.serializers import ProductSerializer

class Command(BaseCommand):
    help = 'Starts the RabbitMQ consumer for order_created_queue'

    def handle(self, *args, **kwargs):
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=settings.RABBITMQ_HOST,
                    credentials=pika.PlainCredentials(settings.RABBITMQ_USERNAME, settings.RABBITMQ_PASSWORD)
                )
            )
            channel = connection.channel()
            channel.queue_declare(queue='order_created_queue', durable=True)

            def callback(ch, method, properties, body):
                data = json.loads(body)
                product_id = data.get("product_id")
                quantity = data.get("quantity")

                try:
                    product = Product.objects.get(id=product_id)
                    product_serializer = ProductSerializer(product).data
                    if product.stock < quantity:
                        response = {"exists": True, "product" : product_serializer, "stock_updated" : False}
                    else :
                        product.stock -= quantity
                        product.save()
                        self.stdout.write(
                            self.style.SUCCESS(f"Product stock updated/product_id : {product.id}, stock : {product.stock}"),
                            ending='/'
                        )
                        response = {"exists": True, "product" : product_serializer, "stock_updated" : True}
                except Product.DoesNotExist:
                    response = {"exists": False}

                ch.basic_publish(
                    exchange='',
                    routing_key=properties.reply_to,
                    body=json.dumps(response),
                    properties=pika.BasicProperties(
                        correlation_id=properties.correlation_id,
                        content_type='application/json'
                    )
                )
                ch.basic_ack(delivery_tag=method.delivery_tag)

            channel.basic_consume(queue='order_created_queue', on_message_callback=callback, auto_ack=False)
            self.stdout.write(
                self.style.NOTICE('order_created_queue is waiting for messages...')
            )

            # Handling graceful shutdown
            def graceful_exit(sig, frame):
                self.stdout.write(
                    self.style.ERROR("Closing connection...")
                )
                connection.close()
                exit(0)

            signal.signal(signal.SIGINT, graceful_exit)
            signal.signal(signal.SIGTERM, graceful_exit)

            channel.start_consuming()

        except pika.exceptions.AMQPConnectionError as e:
            self.stdout.write(
                self.style.ERROR(f"Failed to connect to RabbitMQ: {e}")
            )