# RecLLM - Conversational YouTube Recommendations

RecLLM is an AI-powered conversational YouTube recommendation engine that provides personalized video suggestions through natural language interaction.

## Features

- Natural language conversation interface
- Personalized video recommendations based on user preferences
- Integration with YouTube Data API
- Beautiful web interface powered by Gradio

## Deployment on Hugging Face Spaces

1. Create a new Space on Hugging Face:
   - Go to https://huggingface.co/spaces
   - Click "Create new Space"
   - Choose "Docker" as the SDK
   - Set the Space hardware to "CPU" (or GPU if needed)

2. Configure environment variables:
   - Add your `YOUTUBE_API_KEY` to the Space's secrets
   - The app will automatically use this key for YouTube API requests

3. Upload the code:
   ```bash
   git clone https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME
   # Copy your RecLLM files to the cloned directory
   git add .
   git commit -m "Initial commit"
   git push
   ```

4. The Space will automatically build and deploy your app

## Local Development

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up environment variables:
   ```bash
   echo "YOUTUBE_API_KEY=your_api_key_here" > .env
   ```

3. Run the app:
   ```bash
   python -m recllm.app
   ```

## Architecture

- `app.py`: Main Gradio web interface
- `models/rec_llm.py`: Core recommendation model
- `models/user_profile.py`: User profile management
- `utils/youtube_api.py`: YouTube Data API integration

## License

MIT License 