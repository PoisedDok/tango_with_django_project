from django.shortcuts import render
from django.http import HttpResponse

def about(request):
    context_dict = {'boldmessage': 'Contact, Email, Fax'}
    return render(request, 'rango/about.html', context=context_dict)