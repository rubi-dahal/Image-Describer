# 🗣️ See it, Say it

An AI-powered Streamlit application that analyzes images and describes them out loud in your preferred language.

## Features

- **Image Captioning**: Automatically generates accurate descriptions of uploaded or captured images
- **Visual Question Answering**: Ask specific questions about images and get AI-powered answers
- **Multi-Language Support**: Translate descriptions to Hindi, French, Spanish, or German
- **Text-to-Speech**: Listen to descriptions in your selected language
- **Flexible Input**: Upload images or capture photos directly using your device camera
- **Audio Download**: Save generated audio descriptions as MP3 files

## Supported Languages

- English (default)
- Hindi
- French
- Spanish
- German

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup

1. Clone or download this project
2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - **Windows**:
     ```bash
     venv\Scripts\activate
     ```
   - **macOS/Linux**:
     ```bash
     source venv/bin/activate
     ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

2. The application will open in your browser (typically at `http://localhost:8501`)

3. **Choose an image source**:
   - Upload a photo from your device
   - Or capture a photo using your camera

4. **Optional: Ask a question** - If you'd like to know something specific about the image

5. **Select your preferred language** - Choose the language for the audio output

6. Wait for the AI to analyze the image and generate audio

7. **Listen or download** - Play the audio or download it as an MP3 file

## How It Works

1. **Image Understanding**: Uses the Salesforce BLIP model for image captioning and visual question answering
2. **Translation**: Employs Helsinki-NLP's MarianMT models for language translation
3. **Text-to-Speech**: Converts translated text to speech using Google Text-to-Speech (gTTS)

## Technologies Used

- **Streamlit** - Web app framework
- **Hugging Face Transformers** - Pre-trained AI models for vision and language tasks
- **PyTorch** - Deep learning framework
- **Pillow** - Image processing
- **gTTS** - Google Text-to-Speech integration

## Requirements

- streamlit >= 1.28.0
- transformers >= 4.30.0
- torch >= 2.0.0
- Pillow >= 9.0.0
- gtts >= 2.3.0

## Performance Notes

- First run will download pre-trained models (~2-3 GB) - this may take a few minutes
- Subsequent runs use cached models for faster processing
- Image processing and model inference typically take 5-30 seconds depending on your hardware

## Troubleshooting

### Models Not Downloading
- Ensure you have a stable internet connection
- Check available disk space (at least 3-4 GB recommended)

### GPU Support
- For faster processing, install GPU-enabled PyTorch:
  ```bash
  pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
  ```

### Audio Generation Issues
- Requires internet connection for gTTS to work
- Check your internet connectivity if audio generation fails

## License

This project uses open-source models and libraries. Refer to individual license agreements for model usage.

## Support

For issues or questions, please refer to the documentation of the individual libraries used:
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Hugging Face Documentation](https://huggingface.co/docs)
- [gTTS Documentation](https://gtts.readthedocs.io/)
