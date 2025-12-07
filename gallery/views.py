# gallery/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Photo
from .forms import PhotoForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def home(request):
    # Get all photos ordered by date (newest first)
    photos_list = Photo.objects.select_related('user').order_by('-date_posted')
    
    # Pagination - 12 photos per page
    paginator = Paginator(photos_list, 12)
    page = request.GET.get('page')
    
    try:
        photos = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        photos = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results
        photos = paginator.page(paginator.num_pages)
    
    return render(request, 'gallery/home.html', {
        'photos': photos,
        'is_paginated': photos.has_other_pages(),
        'page_obj': photos  # For template pagination
    })

@login_required
def upload_photo(request):
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.user = request.user
            photo.save()
            messages.success(request, 'Your photo has been uploaded!')
            return redirect('gallery:home')
    else:
        form = PhotoForm()
    return render(request, 'gallery/upload.html', {'form': form})

def photo_detail(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    return render(request, 'gallery/photo_detail.html', {'photo': photo})

@login_required
def delete_photo(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    if photo.user != request.user:
        messages.error(request, 'You are not authorized to delete this photo.')
        return redirect('gallery:home')
    
    if request.method == 'POST':
        photo.delete()
        messages.success(request, 'Photo has been deleted.')
        return redirect('gallery:home')
    
    return render(request, 'gallery/confirm_delete.html', {'photo': photo})