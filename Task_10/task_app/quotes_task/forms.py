
from django.forms import ModelForm, CharField, TextInput, DateField, DateInput
from .models import Quote, Author
from django import forms

class QuoteForm(ModelForm):
    quote_text = CharField(max_length=600, min_length=3, required=True, widget=TextInput(attrs={'class': 'form-control'}))
    author = CharField(max_length=100, required=True, widget=TextInput (attrs={'class': 'form-control'}))
    tags = CharField(widget=TextInput(attrs={'class': 'form-control'}))


    class Meta:
        model = Quote
        fields = ['quote_text', 'author', 'tags']

    def clean_author(self):
        author_name = self.cleaned_data.get('author')
        try:
            Author.objects.get(full_name=author_name)
            #raise forms.ValidationError(f"Author '{Author.objects.get(full_name=author_name)}'  ")
        except Author.DoesNotExist:
            raise forms.ValidationError(f"Author '{author_name}' does not exist. Consider adding a new author.")
        return author_name
    
    
class AuthorForm(ModelForm):
    full_name = CharField(max_length=100, min_length=3, required=True, widget=TextInput(attrs={'class': 'form-control'}))
    born_date = DateField(required=True, widget=DateInput (attrs={'type': 'date'}))
    born_location = CharField(max_length=100, widget=TextInput(attrs={'class': 'form-control'}))
    
    description = CharField(max_length=1000, widget=TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Author
        fields = ['full_name', 'born_date', 'born_location', 'description']
