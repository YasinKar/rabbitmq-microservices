import pika
import json
import uuid
import time
from django.conf import settings

class OrderCreatedProducer:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=settings.RABBITMQ_HOST,
                credentials=pika.PlainCredentials(settings.RABBITMQ_USERNAME, settings.RABBITMQ_PASSWORD)
            )
        )
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='order_created_queue', durable=True)

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(queue=self.callback_queue, on_message_callback=self.on_response, auto_ack=True)
        self.response = None
        self.corr_id = None

    def on_response(self, ch, method, properties, body):
        if self.corr_id == properties.correlation_id:
            self.response = json.loads(body)

    def order_created(self, product_id, quantity, timeout=5):
        self.response = None
        self.corr_id = str(uuid.uuid4())

        self.channel.basic_publish(
            exchange='', 
            routing_key='order_created_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
                content_type='application/json'
            ),
            body=json.dumps({"product_id": product_id, "quantity" : quantity})
        )

        start_time = time.time()
        while self.response is None:
            self.connection.process_data_events()
            if time.time() - start_time > timeout:
                print("Timeout: No response received.")
                return None
        return self.response

    def __del__(self):
        self.connection.close()