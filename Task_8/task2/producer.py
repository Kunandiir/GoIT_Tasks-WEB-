# producer.py
import pika
from mongoengine import *
from faker import Faker
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


# Connection code
uri = "mongodb+srv://testuser:XLvxVCakGPtvmeSx@testdb.qksxmsr.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))

connect(alias='default', name='Task_8', host=uri)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Define models
class Contact(Document):
    fullname = StringField(required=True)
    email = StringField(required=True)
    phone_number = StringField()
    message_sent = BooleanField(default=False)
    preferred_contact = StringField(choices=['email', 'sms'])


def main():

    # Declare queues
    channel.queue_declare(queue='email_contacts')
    channel.queue_declare(queue='sms_contacts')

    # Generate contacts and publish to the queue
    fake = Faker()
    for _ in range(100):
        contact = Contact(fullname=fake.name(), email=fake.email(), phone_number=fake.phone_number(), preferred_contact=fake.random_element(['email', 'sms']))
        contact.save()

        if contact.preferred_contact == 'email':
            channel.basic_publish(exchange='', routing_key='email_contacts', body=str(contact.id))
        else:
            channel.basic_publish(exchange='', routing_key='sms_contacts', body=str(contact.id))

    connection.close()

if __name__ == "__main__":
    main()
