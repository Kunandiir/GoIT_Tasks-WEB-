
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from mongoengine import *
import json


# Your connection code
uri = "mongodb+srv://testuser:XLvxVCakGPtvmeSx@testdb.qksxmsr.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))

register_connection(alias='default', name='Task_8', host=uri)
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


# Author model
class Author(Document):
    fullname = StringField(required=True)
    born_date = StringField()
    born_location = StringField()
    description = StringField()

# Quote model
class Quote(Document):
    tags = ListField(StringField())
    author = ReferenceField(Author)
    quote = StringField()

#Load json files 
def load_data():
    with open('Task_8/authors.json', 'r', encoding='utf-8') as f:
        authors_data = json.load(f)

    with open('Task_8/quotes.json', 'r', encoding='utf-8') as f:
        quotes_data = json.load(f)


    for author in authors_data:
        a = Author(**author)
        a.save()

    for quote in quotes_data:
        author = Author.objects(fullname=quote['author']).first()
        del quote['author']  # Remove the 'author' key from the quote dictionary
        q = Quote(author=author, **quote)
        q.save()


def main():
    # Search 
    while True:
        command = input('Enter command: ')
        if command.startswith('name:'):
            name = command.split(':')[1].strip()
            author = Author.objects(fullname=name).first()
            if author:
                quotes = Quote.objects(author=author)
                for quote in quotes:
                    print(quote.quote)
        elif command.startswith('tag:'):
            tag = command.split(':')[1].strip()
            quotes = Quote.objects(tags=tag)
            for quote in quotes:
                print(quote.quote)
        elif command.startswith('tags:'):
            tags = command.split(':')[1].split(',')
            tags = [tag.strip() for tag in tags]  # Remove spaces
            quotes = Quote.objects(tags__in=tags)
            for quote in quotes:
                print(quote.quote)
        elif command == 'exit':
            break

if __name__ == "__main__":
    #load_data()
    main()