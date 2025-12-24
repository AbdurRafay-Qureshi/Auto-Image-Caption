# Auto-Image-Caption - AI-Powered Image Description Generator

> **Transform your images into searchable, organized masterpieces!** 📸

We’ve all been there: scrolling through a folder of 500 images titled "IMG_8432," trying to remember which one was from that specific shoot or vacation. It’s a mess, and let’s be honest—no one has the time to manually tag every single photo.

I built Auto-Image-Caption to solve exactly that. It uses Mistral’s Vision AI to "look" at your photos and write detailed descriptions directly into the metadata. It makes your library searchable and organized without you having to lift a finger. Your future self will definitely thank you for this one.

---

## Features

-  **AI-Powered Descriptions** - Uses Mistral’s Vision AI to actually "see" your photos and describe them in plain English. No more generic tags; you get real context.
-  **Metadata Embedding** - Descriptions are baked directly into the image files (EXIF/metadata). It works seamlessly with JPEGs, PNGs, and WebPs, so the info stays with the photo wherever it goes.
-  **Automatic Logging** - Every run is timestamped and logged. You’ll always know exactly which folders you’ve already tackled and when.
-  **Metadata Verification** - Includes a handy `check_metadata.bat` script so you can double-check that your descriptions were saved correctly without opening every file.
-  **One-Click Execution** - Just double-click `run.bat` and let the magic happen!
-  **Multiple Format Support** - Whether your library is full of `.jpg`, `.jpeg`, `.png`, or `.webp`, we’ve got you covered.

---

## Quick Start

### Prerequisites

- Python 3.8+ installed
- A Mistral API key ([Get one here](https://console.mistral.ai/))

### One-Click Setup & Run (Windows)

1. **Clone this repository:**
   ```bash
   https://github.com/AbdurRafay-Qureshi/Auto-Image-Caption.git
   cd Auto-Image-Caption
   ```

2. **Set up your API key:**
   
   Copy the example environment file:
   ```bash
   copy .env.example .env
   ```
   
   Open `.env` and add your Mistral API key:
   ```env
   MISTRAL_API_KEY=your_api_key_here
   MISTRAL_MODEL=mistral-small-latest
   IMAGE_FOLDER=C:/path/to/your/images
   ```

3. **Install dependencies & run:**
   
   Just double-click `requirements.bat` for installing libraries and then double click `run.bat` - it handles everything!
   
   Or manually:
   ```bash
   pip install -r requirements.txt
   python main.py
   ```

That's it! Your images will be processed, descriptions will be embedded, and everything will be logged.

---

## Project Structure

```
Auto-Image-Caption/
├── 📄 main.py                   # Main script - runs the image processing pipeline
├── ⚙️ config.py                 # Configuration settings (loads from .env)
├── 🤖 mistral_vision.py         # Mistral Vision API client
├── 🏷️ image_metadata.py         # Metadata handler for images
├── 🔍 check_metadata.py         # Verify metadata was added successfully
├── 📝 logger.py                 # Standalone logger (optional wrapper)
├── 📋 requirements.txt           # Python dependencies
├── 🔐 .env                      # Your API keys (NEVER commit this!)
├── 📝 .env.example              # Template for environment variables
├── 🚫 .gitignore                # Keeps secrets safe
├── ▶️ run.bat                   # One-click installer & runner (Windows)
├── 📂 images/                   # Place your images here
├── 📂 logs/                     # Processing logs (auto-created)
└── 📖 README.md                 # You are here!
```

---

## How It Works

1. **Image Discovery** - Scans the `images/` folder for supported file types
2. **AI Processing** - Sends each image to Mistral Vision API for analysis
3. **Description Generation** - Receives detailed, natural-language descriptions
4. **Metadata Embedding** - Embeds descriptions into image metadata
5. **Logging** - Saves log of all operations to `logs/` folder just in case.

All output is displayed in your terminal **and** saved to log files for future reference!

---

## Usage Examples

### Process Images
```bash
python main.py
```
Or double-click run.bat

### Check Metadata
Verify that descriptions were successfully embedded:
```bash
python check_metadata.py
```
Or just double-click metadata_checker.bat. It'll check whether the description been added to pictures metadata.

### View Logs
All logs are saved in `logs/` folder with timestamps:
```
logs/
├── image_processing_20251224_202033.txt
├── image_processing_20251224_203145.txt
└── ...
```

---

## Configuration

All configuration is done through the `.env` file:

| Variable | Description | Example |
|----------|-------------|---------|
| `MISTRAL_API_KEY` | Your Mistral API key (required) | `IK1E2yeSqM8cYA0mHw...` |
| `MISTRAL_MODEL` | Mistral model to use | `mistral-small-latest` |
| `IMAGE_FOLDER` | Path to your images folder | `C:/Users/you/Pictures` |

The `logs/` folder location is hardcoded to the project directory and created automatically at runtime.

---

## Supported Image Formats

| Format | Extension | Metadata Method |
|--------|-----------|-----------------|
| **JPEG** | `.jpg`, `.jpeg` | EXIF tag 270 (ImageDescription) |
| **PNG** | `.png` | PNG text chunks |
| **WebP** | `.webp` | EXIF metadata |
| **Others** | Any | Sidecar `.txt` files |
---

## Troubleshooting

### "MISTRAL_API_KEY not found in environment variables"
→ Make sure you've created a `.env` file and added your API key.

### "No images found in folder"
→ Check that your `IMAGE_FOLDER` path in `.env` is correct and contains supported image formats.

### Images not getting descriptions
→ Verify your Mistral API key is valid and has credits remaining.

---

## Contributing

Contributions are welcome! Feel free to:
- Report bugs
- Suggest new features
- Submit pull requests

---

## License

This project is open source and available under the MIT License.

---


<div align="center">
</div>
