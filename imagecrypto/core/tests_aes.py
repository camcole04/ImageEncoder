from django.test import TestCase, Client
import json
from core.crypto import aes_encrypt_text, aes_decrypt_text, aes_encrypt_image, aes_decrypt_image

class AESCipherTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.key = "thisisaverysecurekey1234567890"
        self.plain_text = "Hello World"
        self.pixel_array = [10, 20, 30, 40, 50, 60, 70, 80]

    def test_text_encryption_decryption(self):
        encrypted = aes_encrypt_text(self.plain_text, self.key)
        decrypted = aes_decrypt_text(encrypted, self.key)
        self.assertEqual(decrypted, self.plain_text)

    def test_image_encryption_decryption(self):
        encrypted = aes_encrypt_image(self.pixel_array, self.key)
        decrypted = aes_decrypt_image(encrypted, self.key)
        self.assertEqual(decrypted, self.pixel_array)

    def test_vigenere_view_encrypt_decrypt(self):
        # Test encrypt text via view
        response = self.client.post('/vigenere/', {'plain_text': self.plain_text, 'key': self.key})
        self.assertEqual(response.status_code, 200)
        self.assertIn('encrypted_text', response.context)
        encrypted_text = response.context['encrypted_text']
        self.assertTrue(encrypted_text)

        # Test decrypt text via view
        response = self.client.post('/vigenere/', {'cipher_text': encrypted_text, 'key': self.key})
        self.assertEqual(response.status_code, 200)
        self.assertIn('decrypted_text', response.context)
        decrypted_text = response.context['decrypted_text']
        self.assertEqual(decrypted_text, self.plain_text)

    def test_encrypt_image_endpoint(self):
        # Test image encryption endpoint
        response = self.client.post('/encrypt_image/', json.dumps({'pixel_array': self.pixel_array, 'key': self.key}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'success')
        encrypted_pixels = data['encrypted_pixels']
        self.assertIsInstance(encrypted_pixels, list)
        self.assertTrue(len(encrypted_pixels) > 0)

    def test_encrypt_image_missing_data(self):
        # Missing pixel_array
        response = self.client.post('/encrypt_image/', json.dumps({'key': self.key}), content_type='application/json')
        self.assertEqual(response.status_code, 400)

        # Missing key
        response = self.client.post('/encrypt_image/', json.dumps({'pixel_array': self.pixel_array}), content_type='application/json')
        self.assertEqual(response.status_code, 400)
