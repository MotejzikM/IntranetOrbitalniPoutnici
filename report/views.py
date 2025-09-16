from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from pages.models import Page

# Create your views here.

@login_required
def index(request):
    """
    Render the main page of the report application.
    """

    pages = Page.objects.all()

    return render(request, 'report/index.html', {'pages': pages})