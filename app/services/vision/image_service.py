from PIL import Image
import io
import base64

class ImageService:
    @staticmethod
    def preprocess_image(image_bytes: bytes):
        # Vision preprocessing is now in classifier.py
        return image_bytes
    
    @staticmethod
    def decode_base64(base64_str: str):
        # Remove data URL prefix if present
        if ',' in base64_str:
            base64_str = base64_str.split(',')[1]
        return base64.b64decode(base64_str)
