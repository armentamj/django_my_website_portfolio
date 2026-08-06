# Create your views here.
from django.shortcuts import render

# This function handles requests to your main landing page (the root URL)
def home(request):
    # It tells Django to look for 'index.html' inside your homepage templates folder
    return render(request, 'homepage/home.html')

# This function handles requests to the legal/impressum page
def impressum(request):
    # It serves the 'impressum.html' file when the user visits /impressum/
    return render(request, 'homepage/impressum.html')

def datenschutzerklärung(request):
    # It serves the 'impressum.html' file when the user visits /datenschutzerklärung/
     return render(request, 'homepage/datenschutzerklärung.html')
