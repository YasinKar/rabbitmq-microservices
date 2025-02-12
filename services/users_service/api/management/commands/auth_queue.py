import json
import pika
import signal
from django.core.management.base import BaseCommand
import pika.exceptions
from utils.validate_token import validate_token
from django.conf import settings

class Command(BaseCommand):
    help = 'Starts the RabbitMQ consumer for auth_queue'

    def handle(self, *args, **kwargs):
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host='rabbitmq',
                    credentials=pika.PlainCredentials('admin', 'admin')
                )
            )
            channel = connection.channel()
            channel.queue_declare(queue='auth_queue', durable=True)

            def callback(ch, method, properties, body):
                data = json.loads(body)
                token = data.get("token")
                
                response = validate_token(token)

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

            channel.basic_consume(queue='auth_queue', on_message_callback=callback, auto_ack=False)
            print(" [*] Users Service is waiting for messages...")

            # Handling graceful shutdown
            def graceful_exit(sig, frame):
                print("Closing connection...")
                connection.close()
                exit(0)

            signal.signal(signal.SIGINT, graceful_exit)
            signal.signal(signal.SIGTERM, graceful_exit)

            channel.start_consuming()

        except pika.exceptions.AMQPConnectionError as e:
            print(f"Failed to connect to RabbitMQ: {e}")