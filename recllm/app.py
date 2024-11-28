import gradio as gr
from typing import List, Dict
from recllm.models.rec_llm import RecLLM
from recllm.models.user_profile import UserProfile
from recllm.utils.youtube_api import YouTubeAPI
from dotenv import load_dotenv

load_dotenv()

rec_llm = RecLLM()
youtube_api = YouTubeAPI()

# Store user profiles in memory
user_profiles: Dict[str, UserProfile] = {}

def process_message(
    message: str,
    history: List[List[str]],
    user_id: str = "default_user"
) -> tuple[str, List[Dict]]:
    """Process a message and return response with recommendations."""
    try:
        # Convert history to message format
        messages = []
        for h in history:
            messages.extend([
                {"role": "user", "content": h[0]},
                {"role": "assistant", "content": h[1]}
            ])
        messages.append({"role": "user", "content": message})
        
        # Get or create user profile
        if user_id not in user_profiles:
            user_profiles[user_id] = UserProfile(user_id)
        user_profile = user_profiles[user_id]
        
        # Update profile and get relevant aspects
        conversation_context = "\n".join(
            [f"{msg['role']}: {msg['content']}" for msg in messages]
        )
        relevant_profile = user_profile.get_relevant_profile_aspects(
            conversation_context,
            rec_llm
        )
        
        # Generate search query and get recommendations
        search_query = rec_llm.generate_search_query(messages, relevant_profile)
        video_candidates = youtube_api.search_videos(search_query)
        ranked_videos = rec_llm.rank_videos(
            video_candidates,
            conversation_context,
            relevant_profile
        )
        
        # Generate response
        response = rec_llm.generate_recommendation_response(
            messages,
            ranked_videos,
            relevant_profile
        )
        
        # Format video recommendations for display
        video_html = "<div style='margin-top: 20px'>"
        for video in ranked_videos[:5]:
            video_html += f"""
            <div style='margin-bottom: 20px; padding: 10px; border: 1px solid #ddd; border-radius: 8px;'>
                <img src='{video["thumbnail"]}' style='width: 200px; border-radius: 4px;'>
                <h3>{video["title"]}</h3>
                <p><strong>Channel:</strong> {video["channel_title"]}</p>
                <p><strong>Views:</strong> {video["view_count"]}</p>
                <p><strong>Why this video:</strong> {video.get("explanation", "")}</p>
                <a href='https://youtube.com/watch?v={video["id"]}' target='_blank'>
                    Watch on YouTube
                </a>
            </div>
            """
        video_html += "</div>"
        
        return response + video_html, ranked_videos[:5]
        
    except Exception as e:
        return f"Error: {str(e)}", []

# Create Gradio interface
with gr.Blocks(css="footer {visibility: hidden}") as demo:
    gr.Markdown("# RecLLM - AI YouTube Recommendations")
    gr.Markdown("""
    Have a conversation with RecLLM to get personalized YouTube video recommendations.
    Tell it about your interests, ask for specific types of content, or get recommendations
    based on your mood and preferences.
    """)
    
    chatbot = gr.Chatbot(height=400)
    msg = gr.Textbox(label="Your message", placeholder="What kind of videos are you interested in?")
    clear = gr.Button("Clear")
    
    def user(message, history):
        return "", history + [[message, None]]
    
    def bot(history):
        response, _ = process_message(history[-1][0], history[:-1])
        history[-1][1] = response
        return history
    
    msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(
        bot, chatbot, chatbot
    )
    clear.click(lambda: None, None, chatbot, queue=False)

if __name__ == "__main__":
    demo.launch() 