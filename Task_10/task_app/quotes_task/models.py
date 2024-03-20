from django.db import models

# Create your models here.
class Author(models.Model):
    full_name = models.CharField(max_length=100)
    born_date = models.DateField()
    born_location = models.CharField(max_length=100)
    description = models.TextField()



class Quote(models.Model):
    quote_text = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    tags = models.CharField(max_length=255, blank=True)


    def save(self, *args, **kwargs):
        # Convert the comma-separated tags to a list
        self.tags = [tag.strip() for tag in self.tags.split(",")]
        super().save(*args, **kwargs)

    def get_tags_list(self):
        # Retrieve the tags as a list
        return self.tags
