"""
Image metadata operations for adding descriptions to image files
Supports JPEG (EXIF), PNG (text chunks), and other formats
"""
from PIL import Image, PngImagePlugin
import os


class ImageMetadataHandler:
    """Handler for reading and writing image metadata"""
    
    @staticmethod
    def add_description_to_metadata(image_path, description):
        """
        Add description to image metadata
        Supports JPEG (EXIF) and PNG (text chunks)
        
        Args:
            image_path: Path to the image file
            description: Description text to add to metadata
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            img = Image.open(image_path)
            file_ext = os.path.splitext(image_path)[1].lower()
            
            if file_ext in ['.jpg', '.jpeg']:
                # JPEG: Use EXIF metadata
                exif_dict = img.getexif()
                exif_dict[270] = description  # EXIF tag 270 = ImageDescription
                img.save(image_path, exif=exif_dict, quality=95)
                print(f"✓ Updated (EXIF): {image_path}")
                
            elif file_ext == '.png':
                # PNG: Use PNG text chunks
                metadata = PngImagePlugin.PngInfo()
                
                # Preserve existing metadata
                if hasattr(img, 'text') and img.text:
                    for key, value in img.text.items():
                        metadata.add_text(key, value)
                
                # Add description
                metadata.add_text("Description", description)
                metadata.add_text("ImageDescription", description)
                
                img.save(image_path, pnginfo=metadata, optimize=True)
                print(f"✓ Updated (PNG): {image_path}")
                
            elif file_ext == '.webp':
                # WebP: Use EXIF metadata
                exif_dict = img.getexif()
                exif_dict[270] = description
                img.save(image_path, exif=exif_dict, quality=95)
                print(f"✓ Updated (WebP): {image_path}")
                
            else:
                # For other formats, save as a sidecar text file
                sidecar_path = f"{image_path}.description.txt"
                with open(sidecar_path, 'w', encoding='utf-8') as f:
                    f.write(description)
                print(f"✓ Updated (sidecar): {sidecar_path}")
            
            return True
            
        except Exception as e:
            print(f"✗ Error updating {image_path}: {e}")
            return False
    
    @staticmethod
    def get_description_from_metadata(image_path):
        """
        Read description from image metadata
        
        Args:
            image_path: Path to the image file
            
        Returns:
            str: Description from metadata, or empty string if not found
        """
        try:
            img = Image.open(image_path)
            file_ext = os.path.splitext(image_path)[1].lower()
            
            if file_ext in ['.jpg', '.jpeg', '.webp']:
                # JPEG/WebP: Read from EXIF
                exif_dict = img.getexif()
                description = exif_dict.get(270, "")
                return description
                
            elif file_ext == '.png':
                # PNG: Read from text chunks
                if hasattr(img, 'text'):
                    return img.text.get("Description", img.text.get("ImageDescription", ""))
                return ""
                
            else:
                # Check for sidecar file
                sidecar_path = f"{image_path}.description.txt"
                if os.path.exists(sidecar_path):
                    with open(sidecar_path, 'r', encoding='utf-8') as f:
                        return f.read().strip()
                return ""
                
        except Exception as e:
            print(f"✗ Error reading {image_path}: {e}")
            return ""
