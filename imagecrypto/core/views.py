from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.views.decorators.csrf import csrf_exempt
import json
from core.crypto import aes_encrypt_text, aes_decrypt_text, aes_encrypt_image, aes_decrypt_image

# Create your views here.
def members(request):
  template = loader.get_template('myfirst.html')
  return HttpResponse(template.render())

def vigenere_view(request):
    encrypted_text = ""
    decrypted_text = ""
    if request.method == "POST":
        plain_text = request.POST.get("plain_text", "")
        cipher_text = request.POST.get("cipher_text", "")
        key = request.POST.get("key", "")
        if plain_text and key:
            encrypted_text = aes_encrypt_text(plain_text, key)

        if cipher_text and key:
            decrypted_text = aes_decrypt_text(cipher_text, key)

    context = {
        'encrypted_text': encrypted_text,
        'decrypted_text': decrypted_text,
    }
    return render(request, 'myfirst.html', context)

@csrf_exempt
def upload_image(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            image_data = data.get('image_data', None)
            if image_data:
                # For now, just acknowledge receipt of image data
                return JsonResponse({'status': 'success', 'message': 'Image received'})
            else:
                return JsonResponse({'status': 'error', 'message': 'No image data found'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

@csrf_exempt
def encrypt_image(request):
    if request.method != "POST":
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
    try:
        data = json.loads(request.body)
        pixel_array = data.get('pixel_array', None)
        key = data.get('key', "")
        if pixel_array is not None and key:
            encrypted_pixels = aes_encrypt_image(pixel_array, key)
            return JsonResponse({'status': 'success', 'encrypted_pixels': encrypted_pixels})
        else:
            return JsonResponse({'status': 'error', 'message': 'Missing pixel array or key'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

@csrf_exempt
def decrypt_image(request):
    if request.method != "POST":
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)
    try:
        data = json.loads(request.body)
        encrypted_array = data.get('encrypted_array', None)
        key = data.get('key', "")
        if encrypted_array is not None and key:
            decrypted_pixels = aes_decrypt_image(encrypted_array, key)
            return JsonResponse({'status': 'success', 'decrypted_pixels': decrypted_pixels})
        else:
            return JsonResponse({'status': 'error', 'message': 'Missing encrypted array or key'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
