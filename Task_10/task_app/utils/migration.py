import os
import django
from mongoengine import *

from pymongo import MongoClient
# Define your PostgreSQL connection details
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_app.settings')
django.setup()

from quotes_task.models import Quote, Tag, Author


quotes = Quote.objects.all()
print(quotes.de)
for quote in quotes:
    quote.
'''
url = "mongodb+srv://testuser:y2H_Q5At4P5HB3B@testdb.qksxmsr.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(url)

#register_connection(alias='default', name='Task_8', host=url)
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


db = client.Task_8

authors = db.author.find()

for author in authors:
    Author.objects.get_or_create(
        full_name=author['full_name'],
        born_date=author['born_date'] ,
        born_location=author['born_location'] ,
        description=author['description'] 
    )


quotes = db.quote.find()


for quote in quotes:
    tags = []
    for tag in quote['tags']:
        t, *_ = Tag.objects.get_or_create(name=tag)
        tags.append(t)

    exist_quote = bool(len(Quote.objects.filter(quote_text=quote['quote_text'])))

    if not exist_quote:
        try:
            print(quote['author_name'])
            author = db.authors.find_one({'_id': quote['author_name']})
            a = Author.objects.get(full_name=author['full_name'])
            q = Quote.objects.create(
                quote_text=quote['quote_text'],
                author=a
                
            )
            for tag in tags:
                q.tags.add(tag)
        except:
            pass'''