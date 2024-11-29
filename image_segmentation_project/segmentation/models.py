from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ImagePair(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    original_image = models.ImageField(upload_to='original_images/')
    segmented_image = models.ImageField(upload_to='segmented_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    processing_time = models.FloatField(null=True, blank=True)  # in seconds
    accuracy = models.FloatField(null=True, blank=True)  # percentage
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Image pair {self.id} by {self.user.username}"