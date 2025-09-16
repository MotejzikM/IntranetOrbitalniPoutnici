from django.shortcuts import render, redirect
from .forms import ZpravaForm, DiskuzeForm
from .models import Diskuze
from django.contrib.auth.decorators import login_required

from rest_framework import viewsets
from .models import Zprava, Diskuze
from .serializers import DiskuzeSerializer, ZpravaSerializer

# Create your views here.

class DiskuzeViewSet(viewsets.ModelViewSet):
    queryset = Diskuze.objects.all()
    serializer_class = DiskuzeSerializer

class ZpravaViewSet(viewsets.ModelViewSet):
    queryset = Zprava.objects.all()
    serializer_class = ZpravaSerializer

@login_required
def diskuze_index(request):
    return render(request, 'diskuze/index.html')

@login_required
def diskuze_detail(request, id):
    # Placeholder for discussion detail view
    diskuze = Diskuze.objects.get(id=id)
    return render(request, 'diskuze/detail.html', {
        'diskuze': diskuze,
        'zprava_form': ZpravaForm(),
    })

@login_required
def add_message(request, id):
    # Placeholder for adding a message to a discussion
    if request.method == 'POST':
        form = ZpravaForm(request.POST)
        if form.is_valid():
            zprava = form.save(commit=False)
            zprava.autor = request.user
            zprava.save()

            # najdi diskuzi podle id a přidej zprávu
            diskuze = Diskuze.objects.get(id=id)
            diskuze.zpravy.add(zprava)

            return redirect('diskuze:diskuze_detail', id=id)
    else:
        form = ZpravaForm()
    return render(request, 'diskuze/add_message.html', {'form': form, 'id': id})

@login_required
def index(request):
    """
    Render the main page of the discussion application.
    """
    discussions = Diskuze.objects.all().order_by('datum_zahajeni')
    return render(request, 'diskuze/index.html', {
        'discussions': discussions,
        'new_discussion_form': DiskuzeForm(),
    })

@login_required
def add_discussion(request):
    """
    Handle the addition of a new discussion.
    """
    if request.method == 'POST':
        nazev = request.POST.get('nazev')
        popis = request.POST.get('popis', '')
        
        diskuze = Diskuze.objects.create(
            nazev=nazev,
            popis=popis
        )
        return redirect('diskuze:diskuze_detail', id=diskuze.id)
    
    return render(request, 'diskuze/add_discussion.html')

def delete_discussion(request, id):
    """
    Handle the deletion of a discussion.
    """
    diskuze = Diskuze.objects.get(id=id)
    if request.method == 'POST':
        diskuze.delete()
        return redirect('diskuze:index')
    
    return render(request, 'diskuze/delete_discussion.html', {'diskuze': diskuze})