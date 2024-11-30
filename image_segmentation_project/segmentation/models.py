# models.py
from django.db import models
from django.contrib.auth.models import User

class ImagePair(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    original_image = models.ImageField(upload_to='original_images/')
    segmented_image = models.ImageField(upload_to='segmented_images/', null=True, blank=True)
    accuracy = models.FloatField(default=0.0)  # Set a default value here
    processing_time = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image Pair for {self.user.username} - {self.created_at}"