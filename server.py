import requests
from flask import Flask, Request, request
from flask_sslify import SSLify

import config
from bot import webhook_handler

app = Flask(__name__)
ssl = SSLify(app)


@app.route('/' + config.WEBHOOK_SECRET, methods=['POST'])
def webhook():
    request_data = request.stream.read().decode('utf-8')
    webhook_handler(request_data)
    requests.post(
        'https://amojo.amocrm.ru/~external/hooks/telegram?t=5753300022:AAEbXFH4y3ye1Ku2MAn6LHJn43TN6H5gSpc&', 
        data=request_data
    )
    return 'ok', 200
