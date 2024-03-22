import os
import django
import json
import psycopg2

# Define your PostgreSQL connection details
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'task_app.settings')
django.setup()

from quotes_task.models import Quote, Tag, Author
{"_id":{"$oid":"65ea5023dd13bcbc30e8aa99"},"full_name":"J.K. Rowling","born_date":"July 31, 1965","born_location":"in Yate, South Gloucestershire, England, The United Kingdom","description":"Description"}

{"_id":{"$oid":"65ea50eb4a839b2b68785200"},"tags":["change","deep-thoughts","thinking","world"],"author_name":{"$oid":"65ea5023dd13bcbc30e8aa98"},"quote_text":"Quote text"}