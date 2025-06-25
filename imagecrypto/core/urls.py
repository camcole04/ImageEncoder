from django.urls import path
from . import views

urlpatterns = [
    path('vigenere/', views.vigenere_view, name='vigenere'),
    path('upload_image/', views.upload_image, name='upload_image'),
    path('encrypt_image/', views.encrypt_image, name='encrypt_image'),
    path('decrypt_image/', views.decrypt_image, name='decrypt_image'),
]
