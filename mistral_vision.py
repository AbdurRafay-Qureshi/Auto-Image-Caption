"""
Mistral Vision API integration for image description generation
"""
import base64
from mistralai import Mistral
from config import MISTRAL_API_KEY, MISTRAL_MODEL


class MistralVisionClient:
    """Client for interacting with Mistral Vision API"""
    
    def __init__(self, api_key=None, model=None):
        """
        Initialize Mistral client
        
        Args:
            api_key: Mistral API key (defaults to config value)
            model: Model name (defaults to config value)
        """
        self.api_key = api_key or MISTRAL_API_KEY
        self.model = model or MISTRAL_MODEL
        self.client = Mistral(api_key=self.api_key)
    
    def encode_image_to_base64(self, image_path):
        """
        Encode image to base64 data URI
        
        Args:
            image_path: Path to the image file
            
        Returns:
            str: Base64 encoded data URI
        """
        with open(image_path, "rb") as image_file:
            encoded = base64.b64encode(image_file.read()).decode('utf-8')
        
        # Determine MIME type based on file extension
        if image_path.lower().endswith('.png'):
            mime_type = 'image/png'
        elif image_path.lower().endswith('.jpg') or image_path.lower().endswith('.jpeg'):
            mime_type = 'image/jpeg'
        elif image_path.lower().endswith('.webp'):
            mime_type = 'image/webp'
        else:
            mime_type = 'image/jpeg'  # default
        
        return f"data:{mime_type};base64,{encoded}"
    
    def get_image_description(self, image_path):
        """
        Send local image to Mistral and get description
        
        Args:
            image_path: Path to the image file
            
        Returns:
            str: Description of the image
        """
        # Encode image as base64 data URI
        image_data_uri = self.encode_image_to_base64(image_path)
        
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Describe this image in detail. Do not include 'this image shows' type of words in the beginning. just straight up description."},
                    {"type": "image_url", "image_url": image_data_uri}
                ]
            }
        ]
        
        response = self.client.chat.complete(model=self.model, messages=messages)
        description = response.choices[0].message.content
        return description.strip()
