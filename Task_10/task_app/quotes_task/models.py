from django.db import models

# Create your models here.
class Author(models.Model):
    full_name = models.CharField(max_length=100)
    born_date = models.CharField(max_length=100)
    born_location = models.CharField(max_length=100)
    description = models.TextField()

class Tag(models.Model):
    name = models.TextField(max_length=50, null=False, unique=True)

class Quote(models.Model):
    quote_text = models.TextField()
    #author = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, blank=True, null=True, default=None)
    tags = models.ManyToManyField(Tag)

