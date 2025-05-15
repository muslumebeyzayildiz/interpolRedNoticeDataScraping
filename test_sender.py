import pika
import json

# RabbitMQ bağlantısı
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='interpol_notices', durable=True)

# Test verisi
test_notice = {
    "entity_id": "2014/26942",  # Dikkat! Mevcut bir entity_id
    "forename": "ATIA UPDATED TEST",  # forename farklı
    "name": "MEKY",
    "date_of_birth": "1992/01/15",
    "age": 33,
    "sex": "",
    "nationalities": "EG",
    "detail_link": "https://ws-public.interpol.int/notices/v1/red/2014-26942"
}

# Mesajı RabbitMQ kuyruğuna gönder
channel.basic_publish(
    exchange='',
    routing_key='interpol_notices',
    body=json.dumps(test_notice),
    properties=pika.BasicProperties(delivery_mode=2)  # mesaj kalıcı olsun
)

print("Test mesajı gönderildi! ✅")

connection.close()