"""
Main script for processing images with Mistral Vision API
Generates descriptions for images and adds them to EXIF metadata
"""
import os
import sys
from datetime import datetime
from mistral_vision import MistralVisionClient
from image_metadata import ImageMetadataHandler
from config import IMAGE_FOLDER, SUPPORTED_FORMATS, LOG_FOLDER


class OutputLogger:
    """Captures terminal output and writes to both console and log file"""
    
    def __init__(self, log_file):
        self.terminal = sys.stdout
        self.log = open(log_file, 'w', encoding='utf-8')
        
        # Write header
        self.log.write(f"Image Processing Log - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        self.log.write("="*80 + "\n\n")
        self.log.flush()
        
    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)
        self.log.flush()
    
    def flush(self):
        self.terminal.flush()
        self.log.flush()
    
    def close(self):
        self.log.write("\n" + "="*80 + "\n")
        self.log.write(f"Processing ended at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        self.log.close()


def setup_logging():
    """
    Set up logging to both file and console
    Creates a timestamped log file in the logs folder
    Returns the logger instance
    """
    # Create logs folder if it doesn't exist
    os.makedirs(LOG_FOLDER, exist_ok=True)
    
    # Create timestamped log filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = os.path.join(LOG_FOLDER, f"image_processing_{timestamp}.txt")
    
    # Create and return logger
    logger = OutputLogger(log_filename)
    print(f"Logging to: {log_filename}\n")
    
    return logger


def process_images(image_folder=IMAGE_FOLDER):
    """
    Process all images in the specified folder
    
    Args:
        image_folder: Path to the folder containing images
    """
    # Initialize clients
    vision_client = MistralVisionClient()
    metadata_handler = ImageMetadataHandler()
    
    # Check if folder exists
    if not os.path.exists(image_folder):
        print(f"Error: Folder '{image_folder}' does not exist!")
        return
    
    # Get all image files
    image_files = [
        f for f in os.listdir(image_folder)
        if f.lower().endswith(SUPPORTED_FORMATS)
    ]
    
    if not image_files:
        print(f"No images found in '{image_folder}'")
        return
    
    print(f"Found {len(image_files)} images to process\n")
    
    # Process each image
    for idx, filename in enumerate(image_files, 1):
        full_path = os.path.join(image_folder, filename)
        print(f"[{idx}/{len(image_files)}] Processing: {filename}")
        
        try:
            # Get description from Mistral Vision API
            description = vision_client.get_image_description(full_path)
            print(f"  Description: {description}")
            
            # Add description to metadata
            metadata_handler.add_description_to_metadata(full_path, description)
            print()
            
        except Exception as e:
            print(f"  ✗ Error processing {filename}: {e}\n")
    
    print("\nProcessing complete!")


if __name__ == "__main__":
    # Set up logging
    logger = setup_logging()
    
    # Redirect stdout to logger
    sys.stdout = logger
    
    try:
        # Run the main process
        process_images()
    finally:
        # Restore stdout and close logger
        sys.stdout = logger.terminal
        logger.close()
        print(f"\nLog saved successfully!")
