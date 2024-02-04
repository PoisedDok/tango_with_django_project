from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from rango import about
from rango.models import Category, Page
from rango.forms import CategoryForm
from rango.forms import PageForm
from django.shortcuts import redirect
from django.shortcuts import reverse


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

def add_category(request):
    form = CategoryForm()
    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)
            # Now that the category is saved, we could confirm this.
            # For now, just redirect the user back to the index view.
            return redirect('/rango/')
        else:
            # The supplied form contained errors -
            # just print them to the terminal.
            print(form.errors)
    # Will handle the bad form, new form, or no form supplied cases.
    # Render the form with error messages (if any).
    return render(request, 'rango/add_category.html', {'form': form})

def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    if category is None:
        return redirect('/rango/')
    
    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()
                return redirect(reverse('rango:show_category', kwargs={'category_name_slug': category_name_slug}))
        else:
            print(form.errors)
    
    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context=context_dict)
