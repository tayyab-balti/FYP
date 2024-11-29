from django.shortcuts import render, redirect, get_object_or_404
from .utils import call_huggingface_segmentation
from .forms import ImageUploadForm
from django.db import models
from django.db.models import Avg 
from .models import ImagePair
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, FileResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os

# @login_required(login_url='login')
# def upload_image (request):
#     if request.method == 'POST':
#         form = ImageUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             # Save the uploaded image to the media directory
#             uploaded_file = request.FILES['image']
#             fs = FileSystemStorage()
#             file_path = fs.save(uploaded_file.name, uploaded_file)
#             full_path = fs.path(file_path)

#             try:
#                 # Call the Hugging Face API for segmentation
#                 api_response = call_huggingface_segmentation(full_path)
#                 print("API Response:", api_response)  # Debugging
#                 if "data" in api_response and api_response['data']:
#                     segmented_image_data = api_response['data'][0]['segmentation']  # Extract segmentation info
                
#                     # Save the segmented image to media/segmented_images
#                     segmented_image_path = os.path.join(settings.MEDIA_ROOT, 'segmented_images', uploaded_file.name)
#                     with open(segmented_image_path, 'wb') as f:
#                         f.write(segmented_image_data)  # Save the binary segmented image
#                 else:
#                     raise Exception("Segmentation output is missing in the API response")
                
#                 # Save the image pair in the database
#                 image_pair = ImagePair(
#                     user=request.user,
#                     original_image=uploaded_file,
#                     segmented_image=os.path.relpath(segmented_image_path, settings.MEDIA_ROOT),  # Relative path
#                     processing_time=api_response['data'][0].get('processing_time', 0.5),  # Example metric
#                     accuracy=api_response['data'][0].get('accuracy', 99.0)  # Example metric
#                 )
#                 image_pair.save()

#                 # Redirect to the My Images page
#                 return redirect('my_images')

#             except Exception as e:
#                 print("API Call Failed:", str(e))  # Debugging
#                 return render(request, 'segmentation/error.html', {"error": str(e)})

#     else:
#         form = ImageUploadForm()
#     return render(request, 'segmentation/upload_image.html', {'form': form})


# --------------------------------------------------
@login_required(login_url='login')
def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Create ImagePair instance
            image_pair = ImagePair(
                user=request.user,
                original_image=request.FILES['image']
            )
            
            # Save the ImagePair instance
            image_pair.save()
            
            # Make prediction using the segmentation model
            results, processing_time = call_huggingface_segmentation(image_pair)
            
            # Save metrics
            image_pair.processing_time = processing_time
            image_pair.save()
            
            return redirect('my_images')
    else:
        form = ImageUploadForm()
    return render(request, 'segmentation/upload_image.html', {'form': form})
# --------------------------------------------------

@login_required(login_url='login')
def MyImages(request):
    images = ImagePair.objects.filter(user=request.user)
    return render(request, 'segmentation/my_images.html', {'images': images})

@login_required(login_url='login')
def view_image(request, image_id, image_type):
    image_pair = get_object_or_404(ImagePair, id=image_id, user=request.user)
    if image_type == 'original':
        image = image_pair.original_image
    else:
        image = image_pair.segmented_image
    return FileResponse(image.open(), content_type='image/jpeg')

@login_required(login_url='login')
def download_image(request, image_id, image_type):
    image_pair = get_object_or_404(ImagePair, id=image_id, user=request.user)
    if image_type == 'original':
        image = image_pair.original_image
    else:
        image = image_pair.segmented_image
    response = FileResponse(image.open(), as_attachment=True)
    response['Content-Disposition'] = f'attachment; filename="{image.name}"'
    return response

@login_required(login_url='login')
def delete_image(request, image_id):
    if request.method == 'POST':
        image_pair = get_object_or_404(ImagePair, id=image_id, user=request.user)
        image_pair.delete()
    return redirect('image_gallery')

@login_required(login_url='login')
def performance_metrics(request):
    # Get user's images
    user_images = ImagePair.objects.filter(user=request.user)
    
    # Get the last 3 processing times and accuracies
    processed_images = user_images.exclude(processing_time=None).order_by('-created_at')[:3]
    
    # Calculate averages
    avg_processing_time = processed_images.aggregate(Avg('processing_time'))['processing_time__avg']
    avg_accuracy = processed_images.aggregate(Avg('accuracy'))['accuracy__avg']

    context = {
        'processed_images': processed_images,
        'avg_processing_time': round(avg_processing_time, 3) if avg_processing_time else None,
        'avg_accuracy': round(avg_accuracy, 1) if avg_accuracy else None,
        'total_images': user_images.count(),
        'images_with_metrics': processed_images.count(),
    }
    return render(request, 'segmentation/performance.html', context)

@login_required(login_url='login')
def FeedbackPage(request):
    if request.method == 'POST':
        feed_back = request.POST.get('feedback')
        # Here you would typically save the feedback to a database or handle it as needed
        return HttpResponse("Thank you for your feedback!")

    return render(request, 'segmentation/feedback.html')

# -------------------
@login_required
def image_gallery(request):
    images = ImagePair.objects.filter(user=request.user)
    return render(request, 'segmentation/image_gallery.html', {'images': images})

# -------------------