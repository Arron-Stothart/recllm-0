import gradio as gr
from typing import List, Dict
from recllm.models.rec_llm import RecLLM
from recllm.models.user_profile import UserProfile
from recllm.utils.youtube_api import YouTubeAPI
from dotenv import load_dotenv

load_dotenv()

# rec_llm = RecLLM()
# youtube_api = YouTubeAPI()

# Store user profiles in memory
user_profiles: Dict[str, UserProfile] = {}

# Custom CSS to emulate YouTube's style
CUSTOM_CSS = """
/* Full page sizing */
.gradio-container {
    width: 100% !important;
    height: 100vh !important;
    margin: 0 !important;
    padding: 0 !important;
}

#component-0 { /* Main container */
    width: 100% !important;
    height: 100vh !important;
    margin: 0 !important;
    padding: 0 !important;
    background-color: #f9f9f9;
}

.youtube-header {
    background-color: white;
    padding: 12px 24px;
    border-bottom: 1px solid #e5e5e5;
    position: sticky;
    top: 0;
    z-index: 100;
    display: flex;
    align-items: center;
    gap: 10px;
}

.youtube-logo {
    margin-right: 40px;
}

.logo-container {
    display: flex;
    align-items: center;
    white-space: nowrap;
}

.logo-container svg {
    min-width: 90px;
    height: 20px;
    flex-shrink: 0;
    margin-right: 1px;
}

.logo-container span {
    color: #282828;
    font-size: 20px;
    font-weight: 500;
}

.search-container {
    flex: 0 1 732px;
}

.search-box-wrapper {
    width: 100%;
    position: relative;
}

.search-input {
    width: 100% !important;
    border: 1px solid #ccc !important;
    border-radius: 9999px !important;
    padding: 0 16px !important;
    height: 40px !important;
    font-size: 16px !important;
    background: #f8f8f8 !important;
    box-shadow: none !important;
}

.search-input:focus {
    border-color: #065fd4 !important;
    outline: none !important;
    background: white !important;
}

.search-box-wrapper > div {
    border: none !important;
    background: none !important;
    box-shadow: none !important;
}

/* Ensure main content uses remaining height */
.main-content {
    display: flex;
    padding: 24px;
    gap: 24px;
    height: calc(100vh - 65px); /* Subtract header height */
    overflow-y: auto;
}

.chat-container {
    flex: 1;
    max-width: 800px;
    background: white;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
}

.video-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 16px;
    padding: 16px;
}

.video-card {
    background: white;
    border-radius: 12px;
    overflow: hidden;
    transition: transform 0.2s;
}

.video-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.video-thumbnail {
    width: 100%;
    aspect-ratio: 16/9;
    object-fit: cover;
}

.video-info {
    padding: 12px;
}

.video-title {
    font-weight: 500;
    margin-bottom: 8px;
}

.channel-name {
    color: #606060;
    font-size: 14px;
}

.chatbot {
    border: none !important;
    background: transparent !important;
}

.message {
    padding: 12px 16px !important;
    border-radius: 18px !important;
    margin-bottom: 8px !important;
}

.user-message {
    background: #e3f2fd !important;
}

.bot-message {
    background: #f5f5f5 !important;
}

.clear-button {
    background: #f2f2f2 !important;
    border-radius: 18px !important;
    color: #606060 !important;
    font-size: 14px !important;
}
"""

def process_message(
    message: str,
    history: List[List[str]],
    user_id: str = "default_user"
) -> tuple[str, List[Dict]]:
    """Process a message and return response with recommendations."""
    # try:
    #     # Convert history to message format
    #     messages = []
    #     for h in history:
    #         messages.extend([
    #             {"role": "user", "content": h[0]},
    #             {"role": "assistant", "content": h[1]}
    #         ])
    #     messages.append({"role": "user", "content": message})
        
    #     # Get or create user profile
    #     if user_id not in user_profiles:
    #         user_profiles[user_id] = UserProfile(user_id)
    #     user_profile = user_profiles[user_id]
        
    #     # Update profile and get relevant aspects
    #     conversation_context = "\n".join(
    #         [f"{msg['role']}: {msg['content']}" for msg in messages]
    #     )
    #     relevant_profile = user_profile.get_relevant_profile_aspects(
    #         conversation_context,
    #         rec_llm
    #     )
        
    #     # Generate search query and get recommendations
    #     search_query = rec_llm.generate_search_query(messages, relevant_profile)
    #     video_candidates = youtube_api.search_videos(search_query)
    #     ranked_videos = rec_llm.rank_videos(
    #         video_candidates,
    #         conversation_context,
    #         relevant_profile
    #     )
        
    #     # Generate response
    #     response = rec_llm.generate_recommendation_response(
    #         messages,
    #         ranked_videos,
    #         relevant_profile
    #     )
        
    #     # Format video recommendations for display
    #     video_html = "<div style='margin-top: 20px'>"
    #     for video in ranked_videos[:5]:
    #         video_html += f"""
    #         <div style='margin-bottom: 20px; padding: 10px; border: 1px solid #ddd; border-radius: 8px;'>
    #             <img src='{video["thumbnail"]}' style='width: 200px; border-radius: 4px;'>
    #             <h3>{video["title"]}</h3>
    #             <p><strong>Channel:</strong> {video["channel_title"]}</p>
    #             <p><strong>Views:</strong> {video["view_count"]}</p>
    #             <p><strong>Why this video:</strong> {video.get("explanation", "")}</p>
    #             <a href='https://youtube.com/watch?v={video["id"]}' target='_blank'>
    #                 Watch on YouTube
    #             </a>
    #         </div>
    #         """
    #     video_html += "</div>"
        
    #     return response + video_html, ranked_videos[:5]
        
    # except Exception as e:
    #     return f"Error: {str(e)}", []
    
    try:
        return f"Echo: {message}", []  # Simple echo response
    except Exception as e:
        return f"Error: {str(e)}", []

# Create Gradio interface
with gr.Blocks(css=CUSTOM_CSS) as demo:
    with gr.Row(elem_classes="youtube-header"):
        gr.HTML("""
            <div class="youtube-logo">
                <div class="logo-container">
                    <svg viewBox="0 0 90 20" preserveAspectRatio="xMidYMid meet">
                        <g viewBox="0 0 90 20">
                            <path d="M27.9727 3.12324C27.6435 1.89323 26.6768 0.926623 25.4468 0.597366C23.2197 2.24288e-07 14.285 0 14.285 0C14.285 0 5.35042 2.24288e-07 3.12323 0.597366C1.89323 0.926623 0.926623 1.89323 0.597366 3.12324C2.24288e-07 5.35042 0 10 0 10C0 10 2.24288e-07 14.6496 0.597366 16.8768C0.926623 18.1068 1.89323 19.0734 3.12323 19.4026C5.35042 20 14.285 20 14.285 20C14.285 20 23.2197 20 25.4468 19.4026C26.6768 19.0734 27.6435 18.1068 27.9727 16.8768C28.5701 14.6496 28.5701 10 28.5701 10C28.5701 10 28.5677 5.35042 27.9727 3.12324Z" fill="#FF0000"></path>
                            <path d="M11.4253 14.2854L18.8477 10.0004L11.4253 5.71533V14.2854Z" fill="white"></path>
                        </g>
                    </svg>
                    <span>RecLLM</span>
                </div>
            </div>
        """)
        with gr.Column(elem_classes="search-container"):
            with gr.Row(elem_classes="search-box-wrapper"):
                msg = gr.Textbox(
                    placeholder="Ask for video recommendations...",
                    show_label=False,
                    container=False,  # Important: removes default container
                    elem_classes="search-input"
                )
    
    with gr.Row(elem_classes="main-content"):
        with gr.Column(elem_classes="chat-container"):
            chatbot = gr.Chatbot(
                elem_classes=["chatbot"],
                show_label=False,
                height=500
            )
            clear = gr.Button("Clear", elem_classes="clear-button")

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