"""
Standalone metadata checker for images
Verifies that descriptions were correctly added to image metadata
"""
import os
import sys
import piexif
from PIL import Image


def check_image_metadata(file_path):
    """
    Check and display metadata from an image file
    
    Args:
        file_path: Path to the image file
    """
    print(f"\n{'='*60}")
    print(f"Checking: {os.path.basename(file_path)}")
    print(f"{'='*60}")
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return False
    
    file_ext = os.path.splitext(file_path)[1].lower()
    
    try:
        if file_ext in ['.jpg', '.jpeg', '.webp']:
            # Check EXIF data for JPEG/WebP
            exif_data = piexif.load(file_path)
            
            # Check ImageDescription in 0th IFD
            desc = exif_data['0th'].get(piexif.ImageIFD.ImageDescription)
            
            if desc:
                description_text = desc.decode('utf-8') if isinstance(desc, bytes) else desc
                print(f"✅ FOUND DESCRIPTION (EXIF):")
                print(f"   {description_text}")
            else:
                print("❌ No 'ImageDescription' found in EXIF 0th IFD.")
            
            # Also check UserComment (sometimes models write here)
            comment = exif_data['Exif'].get(piexif.ExifIFD.UserComment)
            if comment:
                comment_text = comment.decode('utf-8') if isinstance(comment, bytes) else comment
                print(f"✅ FOUND USER COMMENT (EXIF):")
                print(f"   {comment_text}")
            
            return desc is not None
            
        elif file_ext == '.png':
            # Check PNG text chunks
            img = Image.open(file_path)
            
            if hasattr(img, 'text') and img.text:
                print("✅ FOUND PNG METADATA:")
                for key, value in img.text.items():
                    print(f"   {key}: {value}")
                
                # Specifically check for description fields
                desc_fields = ['Description', 'ImageDescription']
                found = False
                for field in desc_fields:
                    if field in img.text:
                        found = True
                        break
                
                return found
            else:
                print("❌ No PNG text chunks found.")
                return False
        
        else:
            # Check for sidecar file
            sidecar_path = f"{file_path}.description.txt"
            if os.path.exists(sidecar_path):
                with open(sidecar_path, 'r', encoding='utf-8') as f:
                    description = f.read().strip()
                print(f"✅ FOUND DESCRIPTION (sidecar file):")
                print(f"   {description}")
                return True
            else:
                print(f"❌ No sidecar file found: {sidecar_path}")
                return False
                
    except Exception as e:
        print(f"❌ Error reading metadata: {e}")
        return False


def check_folder_metadata(folder_path, supported_formats=('.jpg', '.jpeg', '.png', '.webp')):
    """
    Check metadata for all images in a folder
    
    Args:
        folder_path: Path to the folder containing images
        supported_formats: Tuple of supported file extensions
    """
    if not os.path.exists(folder_path):
        print(f"❌ Folder not found: {folder_path}")
        return
    
    # Get all image files
    image_files = [
        f for f in os.listdir(folder_path)
        if f.lower().endswith(supported_formats)
    ]
    
    if not image_files:
        print(f"No images found in '{folder_path}'")
        return
    
    print(f"\n{'#'*60}")
    print(f"Checking {len(image_files)} images in: {folder_path}")
    print(f"{'#'*60}")
    
    success_count = 0
    fail_count = 0
    
    for filename in sorted(image_files):
        full_path = os.path.join(folder_path, filename)
        result = check_image_metadata(full_path)
        
        if result:
            success_count += 1
        else:
            fail_count += 1
    
    # Summary
    print(f"\n{'='*60}")
    print(f"SUMMARY:")
    print(f"  ✅ Success: {success_count}/{len(image_files)}")
    print(f"  ❌ Failed:  {fail_count}/{len(image_files)}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # User provided a path
        path = sys.argv[1]
        
        if os.path.isfile(path):
            # Single file
            check_image_metadata(path)
        elif os.path.isdir(path):
            # Folder
            check_folder_metadata(path)
        else:
            print(f"❌ Invalid path: {path}")
            print("\nUsage:")
            print("  Check single file:  python check_metadata.py path/to/image.jpg")
            print("  Check folder:       python check_metadata.py path/to/folder")
    else:
        # No arguments - check default folder
        default_folder = "C:/Users/sprin/OneDrive/Desktop/visionLLM/images"
        
        print("No path specified. Checking default folder...")
        print(f"To check a specific file or folder, use:")
        print(f"  python check_metadata.py <path>\n")
        
        if os.path.exists(default_folder):
            check_folder_metadata(default_folder)
        else:
            print(f"❌ Default folder not found: {default_folder}")
            print("\nUsage:")
            print("  Check single file:  python check_metadata.py path/to/image.jpg")
            print("  Check folder:       python check_metadata.py path/to/folder")
