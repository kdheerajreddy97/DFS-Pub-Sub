import os
import pika
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

# Connect to RabbitMQ
credentials = pika.PlainCredentials('guest', 'guest')
parameters = pika.ConnectionParameters('rabbitmq', 5672, '/', credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

# Declare the 'dfs' exchange
channel.exchange_declare(exchange='dfs', exchange_type='topic')

# Endpoint to upload a file
@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file:
        # Save the file to the shared storage
        filepath = os.path.join('/data', file.filename)
        file.save(filepath)

        # Publish a message with the file metadata
        metadata = {
            'filename': file.filename,
            'filepath': filepath,
            'filesize': os.path.getsize(filepath),
        }
        channel.basic_publish(
            exchange='dfs',
            routing_key='file.upload',
            body=json.dumps(metadata)
        )
        return jsonify(success=True, message='File uploaded and message published')
    else:
        return jsonify(success=False, message='No file provided'), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
