from django.urls import path
from . import views

urlpatterns = [
    path('my-site/', views.website, name="mysite"),
    path('upload_image/', views.upload_image, name='upload_image'),    #
    path('check_demo/', views.check_demo, name='check_demo'),
    # path('segmentation/', views.upload_and_segment, name='upload_and_segment'),
    path('my-images/', views.my_images, name='my_images'),
    path('gallery/', views.image_gallery, name='image_gallery'),   #
    
    path('view-image/<int:image_id>/<str:image_type>/', views.view_image, name='view_image'),
    path('download-image/<int:image_id>/<str:image_type>/', views.download_image, name='download_image'),
    path('delete-image-pair/<int:image_id>/', views.delete_image_pair, name='delete_image_pair'),

    path('performance-metrics', views.performance_metrics, name='performance_metrics'),
    path('feedback/', views.FeedbackPage, name="feedback"),
]
    