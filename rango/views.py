from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from rango import about
from rango.models import Category, Page


def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]

    context_dict = {'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!',
                    'categories': category_list,
                    'pages': page_list}

    return render(request, 'rango/index.html', context=context_dict)

    
def about(request):
    context_dict = {'boldmessage': 'Contact, Email, Fax'}
    return render(request, 'rango/about.html', context=context_dict)
    

def show_category(request, category_name_slug):
    # Get the category object or raise a 404 error if not found
    category = get_object_or_404(Category, slug=category_name_slug)

    # Get all the pages associated with this category
    pages = Page.objects.filter(category=category)

    # Create a context dictionary to pass to the template
    context_dict = {}
    context_dict['category'] = category
    context_dict['pages'] = pages

    # Return a rendered response using the category.html template
    return render(request, 'rango/category.html', context=context_dict)
