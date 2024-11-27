---
title: RecLLM-HF
emoji: 🎥
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: "3.50.2"
python_version: "3.10"
app_file: recllm/app.py
pinned: false
---

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference

# RecLLM-HF - Conversational YouTube Recommendations

RecLLM is an AI-powered conversational YouTube recommendation engine that provides personalized video suggestions through natural language interaction.

## Features

- Natural language conversation interface
- Personalized video recommendations based on user preferences
- Integration with YouTube Data API
- Beautiful web interface powered by Gradio

## Usage

Simply type your interests or what kind of videos you're looking for in the chat interface. RecLLM will understand your preferences and provide personalized YouTube video recommendations with explanations.

Example prompts:
- "I'm interested in learning about quantum computing"
- "Show me some relaxing nature documentaries"
- "Find me tutorials on Python machine learning"

## Environment Variables

This Space requires the following environment variable:
- `YOUTUBE_API_KEY`: Your YouTube Data API key

Add this to your Space's secrets in the Settings tab.

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