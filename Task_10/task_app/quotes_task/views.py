from django.shortcuts import render, redirect, get_object_or_404
from .forms import QuoteForm, AuthorForm
from .models import Quote,Author,Tag
from django.core.paginator import Paginator
# Create your views here.

def index(request):
    all_quotes = Quote.objects.all()
    paginator = Paginator(all_quotes, 10)
    page_number = request.GET.get('page', 1)
    quotes = paginator.get_page(page_number)

    return render(request, template_name='quotes_task/index.html', context={'quotes': quotes})

def author_show(request, author_id):

    author = get_object_or_404(Author, pk=author_id)
    return render(request, 'quotes_task/author_show.html', {'author': author})



def add_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            # Split comma-separated tags
            tags_from_form = form.cleaned_data['tags']
            tags_list = [tag.strip() for tag in tags_from_form.split(",")]

            # Create or retrieve Tag instances
            tag_instances = []
            for tag_name in tags_list:
                try:
                    tag_instance = Tag.objects.get(name=tag_name)
                except Tag.DoesNotExist:
                    # Tag doesn't exist, create a new one
                    tag_instance = Tag.objects.create(name=tag_name)
                tag_instances.append(tag_instance)

            # Associate the tags with the quote
            quote_instance = form.save(commit=False)
            quote_instance.save()
            quote_instance.tags.set(tag_instances)

            # Redirect to a success page or display a success message
            return redirect(to='quotes_task:home')
    else:
        form = QuoteForm()

    return render(request, template_name='quotes_task/add_quote.html', context={'form': form})



def add_author(request):
    form = AuthorForm(instance=Author())
    if request.method == 'POST':
        form = AuthorForm(request.POST, instance=Author())
        if form.is_valid():
            form.save()
            return redirect(to='quotes_task:home')
    return render(request, template_name='quotes_task/add_author.html', context={'form': form})
