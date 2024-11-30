from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, FileResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
# from huggingface_hub import Client
from transformers import AutoModelForSequenceClassification #
from .models import ImagePair 
from .forms import ImageUploadForm
import logging
from django.core.files import File
from django.core.files.base import ContentFile #
import tempfile

def website(request):
    """
    Render the main website page with example images and navigation.
    """
    return render(request, 'segmentation/website.html')

def check_demo(request):
    """
    Render the upload page with an empty form for image segmentation.
    """
    return render(request, 'segmentation/upload_image.html', {
        'form': ImageUploadForm(),
        'original_image': None
    })

@login_required(login_url='login')
def upload_image(request):
    """
    Handle image upload, display, and segmentation process.
    """
    if request.method == 'POST':
        # Get the uploaded image
        original_image = request.FILES.get('original_image')
        
        if not original_image:
            return render(request, 'segmentation/upload_image.html', {
                'form': ImageUploadForm(),
                'error': 'Please upload an image.'
            })

        try:
            # Validate file type and size
            valid_extensions = ['.jpg', '.jpeg', '.png', '.webp']
            max_file_size = 10 * 1024 * 1024  # 10MB

            # Check file extension
            if not any(original_image.name.lower().endswith(ext) for ext in valid_extensions):
                raise ValidationError(f'Invalid file type. Supported types: {", ".join(valid_extensions)}')
            
            # Check file size
            if original_image.size > max_file_size:
                raise ValidationError('File too large. Maximum size is 10MB.')

            # Perform segmentation using Hugging Face
            try:
                client = Client("fcakyon/yolov8-segmentation")
                
                # Save the uploaded image temporarily
                with tempfile.NamedTemporaryFile(delete=False, suffix=original_image.name.split('.')[-1]) as temp_file:
                    for chunk in original_image.chunks():
                        temp_file.write(chunk)
                    temp_file_path = temp_file.name

                # Perform segmentation
                result = client.predict(
                    image=temp_file_path,
                    model_name="yolov8m-seg.pt",
                    image_size=640,
                    conf_threshold=0.25,
                    iou_threshold=0.45,
                    api_name="/predict"
                )

                # Ensure the result is valid
                if not result or len(result) == 0:
                    raise ValueError("No segmentation result returned")

                # Save segmented image
                segmented_filename = f'segmented_{original_image.name}'
                segmented_content = ContentFile(result[0])

                # Create ImagePair
                image_pair = ImagePair.objects.create(
                    user=request.user,
                    original_image=original_image,
                    accuracy=80.0,
                    processing_time=2.5
                )
                
                # Save segmented image separately to avoid potential issues
                image_pair.segmented_image.save(segmented_filename, segmented_content)
                image_pair.save()

                # Redirect to MyImages view
                return redirect('my_images')

            except Exception as e:
                logging.error(f"Segmentation error: {e}")
                return render(request, 'segmentation/upload_image.html', {
                    'form': ImageUploadForm(),
                    'error': f'Error processing image: {str(e)}'
                })

        except ValidationError as e:
            return render(request, 'segmentation/upload_image.html', {
                'form': ImageUploadForm(),
                'error': str(e)
            })

    # GET request
    return render(request, 'segmentation/upload_image.html', {
        'form': ImageUploadForm(),
    })

@login_required(login_url='login')
def my_images(request):
    """
    Display user's uploaded and segmented images.
    Filters out entries with missing images.
    """
    # Get all image pairs for the current user, with valid images
    image_pairs = ImagePair.objects.filter(
        user=request.user, 
        original_image__isnull=False
    ).order_by('-created_at')
    
    return render(request, 'segmentation/my_images.html', {
        'image_pairs': image_pairs
    })
# --------------------------------------------------

@login_required(login_url='login')
def view_image(request, image_id, image_type):
    image_pair = ImagePair.objects.get(id=image_id)
    if image_type == 'original':
        image = image_pair.original_image
    else:
        image = image_pair.segmented_image
    return render(request, 'segmentation/view_image.html', {'image': image})

@login_required(login_url='login')
def download_image(request, image_id, image_type):
    image_pair = ImagePair.objects.get(id=image_id)
    if image_type == 'original':
        image = image_pair.original_image
    else:
        image = image_pair.segmented_image
    response = HttpResponse(image.read(), content_type='image/jpeg')
    response['Content-Disposition'] = f'attachment; filename="{image.name}"'
    return response

@login_required(login_url='login')
def delete_image_pair(request, image_id):
    # Get the image pair
    image_pair = get_object_or_404(ImagePair, pk=image_id)
    # Delete the original image
    image_pair.original_image.delete()
    # Delete the segmented image
    if image_pair.segmented_image:
        image_pair.segmented_image.delete()
    # Delete the image pair
    image_pair.delete()
    return redirect('my_images')

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