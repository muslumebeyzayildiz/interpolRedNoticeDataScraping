# Kuyruğa veri gönderme fonksiyonu
import pika
import json
import os

def get_channel():
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=os.getenv("RABBITMQ_HOST", "localhost"),
        port=int(os.getenv("RABBITMQ_PORT", 5672))
    ))
    channel = connection.channel()
    channel.queue_declare(queue='interpol_notices', durable=True)
    return connection, channel

def send_to_queue(notice):
    connection, channel = get_channel()
    message = json.dumps(notice)
    channel.basic_publish(
        exchange='',
        routing_key='interpol_notices',
        body=message,
        properties=pika.BasicProperties(delivery_mode=2)  # mesaj kalıcı olsun
    )
    connection.close()
