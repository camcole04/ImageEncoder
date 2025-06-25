import os
import django
import json
from django.test import TestCase, Client
from django.urls import reverse

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'imagecrypto.settings')
django.setup()

class ImageCryptoTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.encrypt_url = reverse('encrypt_image')
        self.decrypt_url = reverse('decrypt_image')
        self.key = "testkey123"
        self.pixel_array = [10,20,30,40,50,60,70,80,90,100,110,120,130,140,150,160]

    def test_encrypt_image_success(self):
        response = self.client.post(self.encrypt_url, data=json.dumps({
            "pixel_array": self.pixel_array,
            "key": self.key
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'success')
        self.assertIn('encrypted_pixels', data)
        self.assertIsInstance(data['encrypted_pixels'], list)

    def test_encrypt_image_missing_data(self):
        response = self.client.post(self.encrypt_url, data=json.dumps({
            "key": self.key
        }), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertEqual(data['status'], 'error')

    def test_decrypt_image_success(self):
        # First encrypt
        encrypt_response = self.client.post(self.encrypt_url, data=json.dumps({
            "pixel_array": self.pixel_array,
            "key": self.key
        }), content_type='application/json')
        encrypted_pixels = encrypt_response.json().get('encrypted_pixels')

        # Then decrypt
        decrypt_response = self.client.post(self.decrypt_url, data=json.dumps({
            "encrypted_array": encrypted_pixels,
            "key": self.key
        }), content_type='application/json')
        self.assertEqual(decrypt_response.status_code, 200)
        data = decrypt_response.json()
        self.assertEqual(data['status'], 'success')
        self.assertIn('decrypted_pixels', data)
        self.assertEqual(data['decrypted_pixels'], self.pixel_array)

    def test_decrypt_image_missing_data(self):
        response = self.client.post(self.decrypt_url, data=json.dumps({
            "key": self.key
        }), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data = response.json()
        self.assertEqual(data['status'], 'error')

    def test_decrypt_image_invalid_method(self):
        response = self.client.get(self.decrypt_url)
        self.assertEqual(response.status_code, 405)
        data = response.json()
        self.assertEqual(data['status'], 'error')

    def test_encrypt_image_invalid_method(self):
        response = self.client.get(self.encrypt_url)
        self.assertEqual(response.status_code, 405)
        data = response.json()
        self.assertEqual(data['status'], 'error')
