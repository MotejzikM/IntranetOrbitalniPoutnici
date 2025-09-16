from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from .models import Page
from .forms import PageForm
from diskuze.models import Diskuze
from diskuze.forms import ZpravaForm
from django_comments.views.comments import post_comment
from django.http import HttpResponseRedirect

from rest_framework import viewsets
from .serializers import PageSerializer

class PageViewSet(viewsets.ModelViewSet):
    queryset = Page.objects.all()
    serializer_class = PageSerializer


def custom_post_comment(request, *args, **kwargs):
    if request.user.is_authenticated and request.method == "POST":
        # vytvoříme mutable copy POST dat
        data = request.POST.copy()
        data['name'] = request.user.get_full_name() or request.user.username
        data['email'] = request.user.email
        request.POST = data
    return post_comment(request, *args, **kwargs)

@login_required
def page_detail(request, slug):
    page = get_object_or_404(Page, slug=slug)
    return render(request, 'pages/page_detail.html', {'page': page, 'object': page, 'user': request.user})

@login_required
def edit_page(request, slug):
    page = get_object_or_404(Page, slug=slug)
    if request.method == 'POST':
        form = PageForm(request.POST, instance=page)
        if form.is_valid():
            form.save(commit=False)
            page.slug = slugify(page.title)

            while Page.objects.filter(slug=page.slug).exists():
                page.slug = f"{page.slug}-{Page.objects.filter(slug=page.slug).count() + 1}"

            page.updated_by = request.user
            page.save()
            
            return redirect('pages:page_detail', slug=page.slug)
    else:
        form = PageForm(instance=page)
    return render(request, 'pages/edit_page.html', {'form': form, 'page': page})

@login_required
def page_list(request):
    pages = Page.objects.all()
    return render(request, 'pages/page_list.html', {'pages': pages})

@login_required
def add_page(request):
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            page = form.save(commit=False)
            page.slug = slugify(page.title)
            
            while Page.objects.filter(slug=page.slug).exists():
                page.slug = f"{page.slug}-{Page.objects.filter(slug=page.slug).count() + 1}"

            page.updated_by = request.user

            print(page.slug, request.user)

            page.save()

            return redirect('pages:page_detail', slug=page.slug)
    else:
        form = PageForm()
    return render(request, 'pages/add_page.html', {'form': form})