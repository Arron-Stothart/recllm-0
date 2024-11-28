from typing import List, Dict
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from recllm.models.rec_llm import RecLLM
from recllm.models.user_profile import UserProfile
from recllm.utils.youtube_api import YouTubeAPI
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
rec_llm = RecLLM()
youtube_api = YouTubeAPI()

# Store user profiles in memory TODO: Gradio compatability
user_profiles: Dict[str, UserProfile] = {}

class Message(BaseModel):
    role: str
    content: str

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
        # Get or create user profile
        if request.user_id not in user_profiles:
            user_profiles[request.user_id] = UserProfile(request.user_id)
        user_profile = user_profiles[request.user_id]

        # Extract profile aspects relevant to current conversation context
        conversation_context = "\n".join(
            [f"{msg.role}: {msg.content}" for msg in request.messages]
        )
        relevant_profile = user_profile.get_relevant_profile_aspects(
            conversation_context,
            rec_llm
        )

        # Generate contextual search query
        search_query = rec_llm.generate_search_query(
            request.messages,
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
            request.messages,
            ranked_videos,
            relevant_profile
        )

        explanation = "Here's why I recommended these videos:\n"
        for video in ranked_videos[:3]:
            explanation += f"\n{video['title']}: {video['explanation']}"

        return RecommendationResponse(
            response=response,
            recommendations=ranked_videos[:5],
            explanation=explanation
        )

    except Exception as e:
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
        if user_id not in user_profiles:
            raise HTTPException(status_code=404, detail="User not found")
        
        user_profile = user_profiles[user_id]
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
            
        return {"status": "success"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860) 