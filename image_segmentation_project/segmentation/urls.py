from django.urls import path
from . import views

urlpatterns = [
    path('my-site/', views.upload_image , name="mysite"),
    path('my-images/', views.MyImages, name="my_images"),
    path('gallery/', views.image_gallery, name='image_gallery'),   #
    
    path('view/<int:image_id>/<str:image_type>/', views.view_image, name='view_image'),
    path('download/<int:image_id>/<str:image_type>/', views.download_image, name='download_image'),
    path('delete/<int:image_id>/', views.delete_image, name='delete_image'),

    path('performance-metrics', views.performance_metrics, name='performance_metrics'),
    path('feedback/', views.FeedbackPage, name="feedback"),
]
