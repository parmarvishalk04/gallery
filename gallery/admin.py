# gallery/admin.py
from django.contrib import admin
from .models import Photo

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'date_posted')
    list_filter = ('date_posted', 'user')
    search_fields = ('title', 'description')
    date_hierarchy = 'date_posted'
    ordering = ('-date_posted',)