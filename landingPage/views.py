from django.shortcuts import render

# Create your views here.


def landingView(request):
    return render(request, 'index.html')

def contactView(request):
    return render(request, 'contact.html')