from typing import List, Dict
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator
from recllm.models.rec_llm import RecLLM
from recllm.utils.youtube_api import YouTubeAPI
from recllm.utils.profile_store import ProfileStore
from dotenv import load_dotenv
from huggingface_hub import login
import os
from fastapi.middleware.cors import CORSMiddleware
import logging

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Login to Hugging Face
login(token=os.getenv("HUGGING_FACE_HUB_TOKEN"))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

rec_llm = RecLLM(model_name="google/gemma-2b-it")
youtube_api = YouTubeAPI()

# Initialize profile store
profile_store = ProfileStore()

class Message(BaseModel):
    role: str
    content: str

    @field_validator('role')
    @classmethod
    def validate_role(cls, v: str) -> str:
        if v not in ['user', 'assistant', 'system']:
            raise ValueError('Role must be either user, assistant, or system')
        return v

    @field_validator('content')
    @classmethod
    def validate_content(cls, v: str) -> str:
        if not v.strip():
            raise ValueError('Content cannot be empty')
        return v.strip()

class ConversationRequest(BaseModel):
    user_id: str
    messages: List[Message]

class RecommendationResponse(BaseModel):
    response: str
    recommendations: List[Dict]
    explanation: str

@app.post("/api/chat", response_model=RecommendationResponse)
async def chat_endpoint(request: ConversationRequest) -> RecommendationResponse:
    """Handle chat messages and return personalised video recommendations."""
    try:
        # Get or create user profile using profile store
        user_profile = profile_store.get_profile(request.user_id)

        # Extract profile aspects relevant to current conversation context
        conversation_context = "\n".join(
            [f"{msg.role}: {msg.content}" for msg in request.messages]
        )
        relevant_profile = user_profile.get_relevant_profile_aspects(
            conversation_context,
            rec_llm
        )

        # Convert Pydantic models to dictionaries for the LLM functions
        messages_dict = [
            {"role": msg.role, "content": msg.content}
            for msg in request.messages
        ]

        # Generate contextual search query
        search_query = rec_llm.generate_search_query(
            messages_dict,
            relevant_profile
        )
        
        # Retrieve + Rank candidate videos
        video_candidates = youtube_api.search_videos(search_query)
        ranked_videos = rec_llm.rank_videos(
            video_candidates,
            conversation_context,
            relevant_profile
        )

        # Generate response
        response = rec_llm.generate_recommendation_response(
            messages_dict,
            ranked_videos,
            relevant_profile
        )

        explanation = "Here's why I recommended these videos:\n"
        for video in ranked_videos[:3]:
            explanation += f"\n{video['title']}: {video['explanation']}"

        # Save profile after updates
        profile_store.save_profile(request.user_id, user_profile)
        
        return RecommendationResponse(
            response=response,
            recommendations=ranked_videos[:5],
            explanation=explanation
        )

    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/feedback")
async def feedback_endpoint(
    user_id: str,
    video_id: str,
    feedback_type: str,
    feedback_value: float
) -> Dict[str, str]:
    """Handle user feedback and update user profile accordingly."""
    try:
        user_profile = profile_store.get_profile(user_id)
        
        video_details = youtube_api.get_video_details(video_id)
        
        if video_details:
            # Record video in user's watch history
            user_profile.add_to_watch_history(video_details)
            
            # Update profile based on feedback
            user_profile.update_profile_from_feedback(
                video_details,
                feedback_type,
                feedback_value,
                rec_llm
            )
            
        # Save profile after updates
        profile_store.save_profile(user_id, user_profile)
            
        return {"status": "success"}
        
    except Exception as e:
        logger.error(f"Error in feedback endpoint: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    return {"message": "RecLLM API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860) 