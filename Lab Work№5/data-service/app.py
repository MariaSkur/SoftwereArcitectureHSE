import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='rabbitmq')
)

channel = connection.channel()

channel.queue_declare(queue='process')

def callback(ch, method, properties, body):
    print("Processing:", body)

channel.basic_consume(
    queue='process',
    on_message_callback=callback,
    auto_ack=True
)

print("Waiting for messages")

channel.start_consuming()
