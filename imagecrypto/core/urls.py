from django.urls import path
from . import views

urlpatterns = [
    path('', views.starting_page, name='starting_page'),
    path('text_encryption/', views.vigenere_view, name='text_encryption'),
    path('image_encryption/', views.image_encryption_view, name='image_encryption'),
    path('upload_image/', views.upload_image, name='upload_image'),
    path('encrypt_image/', views.encrypt_image, name='encrypt_image'),
    path('decrypt_image/', views.decrypt_image, name='decrypt_image'),
]
