"""
Mistral Vision API integration for image description generation
"""
import base64
from io import BytesIO
import os
import random
import time
from mistralai.client import Mistral
from mistralai.client.errors.sdkerror import SDKError
from config import MISTRAL_API_KEY, MISTRAL_MODEL
from PIL import Image


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
        self.max_retries = int(os.getenv("MISTRAL_MAX_RETRIES", "3"))
        self.retry_delay_seconds = float(os.getenv("MISTRAL_RETRY_DELAY_SECONDS", "2"))
        self.min_seconds_between_requests = float(
            os.getenv("MISTRAL_MIN_SECONDS_BETWEEN_REQUESTS", "0")
        )
        self._last_request_ts = None
        self.image_max_side = int(os.getenv("MISTRAL_IMAGE_MAX_SIDE", "1024"))
        self.image_quality = int(os.getenv("MISTRAL_IMAGE_QUALITY", "85"))
    
    def encode_image_to_base64(self, image_path):
        """
        Encode image to base64 data URI
        
        Args:
            image_path: Path to the image file
            
        Returns:
            str: Base64 encoded data URI
        """
        # Downscale/compress before sending to reduce input size and "vision token" usage.
        # This does NOT modify the original file on disk.
        try:
            with Image.open(image_path) as img:
                width, height = img.size
                if max(width, height) > self.image_max_side:
                    scale = self.image_max_side / float(max(width, height))
                    new_w = max(1, int(width * scale))
                    new_h = max(1, int(height * scale))
                    img = img.resize((new_w, new_h), Image.LANCZOS)

                # Ensure JPEG-compatible mode.
                if img.mode in ("RGBA", "LA"):
                    bg = Image.new("RGB", img.size, (255, 255, 255))
                    bg.paste(img, mask=img.split()[-1])
                    img = bg
                else:
                    img = img.convert("RGB")

                buf = BytesIO()
                img.save(buf, format="JPEG", quality=self.image_quality, optimize=True)
                encoded = base64.b64encode(buf.getvalue()).decode("utf-8")
                mime_type = "image/jpeg"
                return f"data:{mime_type};base64,{encoded}"
        except Exception:
            # Fallback: raw encoding based on extension.
            with open(image_path, "rb") as image_file:
                encoded = base64.b64encode(image_file.read()).decode("utf-8")

            if image_path.lower().endswith(".png"):
                mime_type = "image/png"
            elif image_path.lower().endswith(".jpg") or image_path.lower().endswith(".jpeg"):
                mime_type = "image/jpeg"
            elif image_path.lower().endswith(".webp"):
                mime_type = "image/webp"
            else:
                mime_type = "image/jpeg"  # default

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
        
        last_error = None
        for attempt in range(self.max_retries + 1):
            try:
                if self.min_seconds_between_requests and self._last_request_ts is not None:
                    elapsed = time.time() - self._last_request_ts
                    if elapsed < self.min_seconds_between_requests:
                        time.sleep(self.min_seconds_between_requests - elapsed)

                response = self.client.chat.complete(model=self.model, messages=messages)
                self._last_request_ts = time.time()
                description = response.choices[0].message.content
                return description.strip()
            except SDKError as e:
                last_error = e
                # Only retry on rate limiting. Other errors should surface immediately.
                if getattr(e, "status_code", None) != 429:
                    raise

                # Prefer provider-provided Retry-After header (seconds). If it's absent/unparseable,
                # fall back to exponential backoff.
                retry_after_s = None
                try:
                    headers = getattr(e, "headers", {}) or {}
                    ra = headers.get("retry-after")
                    if ra is not None:
                        retry_after_s = float(ra)
                except Exception:
                    retry_after_s = None

                # Backoff and retry for rate limiting.
                if attempt >= self.max_retries:
                    break

                delay = self.retry_delay_seconds * (2 ** attempt)
                if retry_after_s is not None:
                    delay = max(delay, retry_after_s)

                # Small jitter to avoid herd effects if you run multiple instances.
                delay = delay * random.uniform(0.9, 1.1)
                print(
                    f"  Rate limited (429). Waiting {delay:.1f}s... "
                    f"(attempt {attempt+1}/{self.max_retries+1})"
                )
                time.sleep(delay)

        # If we exhausted retries, surface the last error.
        raise last_error
