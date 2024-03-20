from django.shortcuts import render,redirect
from .forms import QuoteForm, AuthorForm
from .models import Quote,Author

# Create your views here.

def index(request):
    return render(request, template_name='quotes_task/index.html', context={'msg':'Hello World'})


def add_quote(request):
    form = QuoteForm(instance=Quote())
    if request.method == 'POST':
        form = QuoteForm(request.POST, instance=Quote())
        
        if form.is_valid():
            quote = form.save()
            
            
            author_name = form.cleaned_data['author']
            author = Author.objects.get(full_name=author_name)
            # Associate the author with the quote
            
            quote.author = author
            quote.save()
            return redirect(to='quotes_task:home')
    return render(request, template_name='quotes_task/add_quote.html', context={'form': form})



def add_author(request):
    form = AuthorForm(instance=Author())
    if request.method == 'POST':
        form = AuthorForm(request.POST, instance=Author())
        if form.is_valid():
            form.save()
            return redirect(to='quotes_task:home')
    return render(request, template_name='quotes_task/add_author.html', context={'form': form})
