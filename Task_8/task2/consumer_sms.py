
import pika
from mongoengine import *
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


# Define modelsS
class Contact(Document):
    fullname = StringField(required=True)
    email = StringField(required=True)
    phone_number = StringField()
    message_sent = BooleanField(default=False)
    preferred_contact = StringField(choices=['email', 'sms'])
    
# Message handler
def callback(ch, method, properties, body):
    contact = Contact.objects(id=body.decode()).first()
    if contact and contact.preferred_contact == 'sms':
        # Simulate sending an SMS
        print(f'Sending SMS to {contact.fullname} ({contact.phone_number})')
        contact.message_sent = True
        contact.save()

# Listen to the SMS queue
channel.basic_consume(queue='sms_contacts', on_message_callback=callback, auto_ack=True)

print('Waiting for SMS contacts. To exit press CTRL+C')
channel.start_consuming()
