import os
import pika
import mysql.connector
from mysql.connector import Error

# Connect to RabbitMQ
credentials = pika.PlainCredentials('guest', 'guest')
parameters = pika.ConnectionParameters('rabbitmq', 5672, '/', credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

# Declare the 'dfs' exchange and the queue
channel.exchange_declare(exchange='dfs', exchange_type='topic')
result = channel.queue_declare('', exclusive=True)
queue_name = result.method.queue

# Bind the queue to the 'dfs' exchange
channel.queue_bind(exchange='dfs', queue=queue_name, routing_key='#')

# Connect to MySQL
def create_db_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host='mysql-dfs',
            user='root',
            password='my-secret-pw',
            database='dfs'
        )
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

# Callback function to process messages
def callback(ch, method, properties, body):
    message = body.decode()
    print("Received message:", message)
    file_data = message.split(',')

    db_conn = create_db_connection()
    cursor = db_conn.cursor()
    
    try:
        cursor.execute("""
            INSERT INTO file_metadata (filename, filepath, filesize)
            VALUES (%s, %s, %s)
        """, (file_data[0], file_data[1], file_data[2]))
        db_conn.commit()
        print("File metadata saved to MySQL")
    except Error as e:
        print(f"Error saving file metadata: {e}")

    cursor.close()
    db_conn.close()

# Start consuming messages
print("Subscriber is waiting for messages...")
channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()

# Close the RabbitMQ connection
connection.close()
