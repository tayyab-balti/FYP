from django import forms
from .models import ImagePair

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = ImagePair
        fields = ('original_image',)