# gallery/signals.py
from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Photo

@receiver(post_delete, sender=Photo)
def delete_photo_file(sender, instance, **kwargs):
    """
    Deletes the image file from the filesystem when the corresponding Photo object is deleted.
    """
    if instance.image:
        instance.image.delete(save=False)