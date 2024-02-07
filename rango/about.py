from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from rango.models import Category, Page
from rango.forms import CategoryForm
from rango.forms import PageForm
from django.shortcuts import redirect
from django.shortcuts import reverse
from rango.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime

def visitor_cookie_handler(request, response):
    # Use cookies.get() to get the visits cookie.
    # If the cookie exists, the value returned is casted to an integer.
    # If the cookie doesn't exist, then the default value of 1 is used.
    visits = int(request.COOKIES.get('visits', '1'))

    last_visit_cookie = request.COOKIES.get('last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')

    # If it's been more than a day since the last visit...
    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        # Update the last visit cookie now that we have updated the count
        response.set_cookie('last_visit', str(datetime.now()))
    else:
        # Set the last visit cookie
        response.set_cookie('last_visit', last_visit_cookie)

    # Update/set the visits cookie
    response.set_cookie('visits', visits)
    request.session['visits'] = visits 
    request.session['last_visit'] = str(datetime.now())

def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    
    # Update the context dictionary
    context_dict = {'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!',
                    'categories': category_list,
                    'pages': page_list}
    response = render(request, 'rango/index.html', context=context_dict)
    # Call the helper function to handle the visitor cookie
    visitor_cookie_handler(request, response)
    return response
    
def about(request):
    # Call the function to handle the visitor cookie
    
    visits = request.session['visits']

    context_dict = {'visits': visits}
    response = render(request, 'rango/about.html', context=context_dict)
    visitor_cookie_handler(request,response)
    return response
