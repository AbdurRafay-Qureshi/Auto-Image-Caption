"""
Configuration settings for the image description pipeline
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Mistral API Configuration
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
if not MISTRAL_API_KEY:
    raise ValueError("MISTRAL_API_KEY not found in environment variables. Please check your .env file.")

MISTRAL_MODEL = os.getenv("MISTRAL_MODEL", "mistral-small-latest")

# Image Processing Configuration
IMAGE_FOLDER = os.getenv("IMAGE_FOLDER")
if not IMAGE_FOLDER:
    raise ValueError("IMAGE_FOLDER not found in environment variables. Please check your .env file.")

# Logs folder (created at runtime in project directory)
LOG_FOLDER = "logs"

SUPPORTED_FORMATS = (".jpg", ".jpeg", ".png", ".webp")
