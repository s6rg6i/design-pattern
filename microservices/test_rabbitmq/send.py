import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')
for i in range(7, 10):
    s = f'Hello {i} World!'
    sb = s.encode("utf-8")
    channel.basic_publish(exchange='', routing_key='hello', body=sb)
    print(f" [x] Sent {sb}")
connection.close()
