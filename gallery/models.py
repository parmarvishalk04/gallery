# gallery/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Photo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='photos/%Y/%m/%d/')
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        # Delete the image file when the photo is deleted
        self.image.delete()
        super().delete(*args, **kwargs)