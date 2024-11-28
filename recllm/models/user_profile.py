from typing import List, Dict
import json
from datetime import datetime
from recllm.prompts.templates import (
    PREFERENCE_EXTRACTION_PROMPT,
    PROFILE_INTEGRATION_PROMPT,
    FEEDBACK_INTEGRATION_PROMPT,
    PROFILE_MERGE_PROMPT
)

class UserProfile:
    def __init__(self, user_id: str):
        self.user_id = user_id
        # Interpretable natural language user profiles
        self.profile_description = "" 
        # Imitation of user watch history NOTE: Not fully implemented
        self.watch_history: List[Dict] = []
        self.last_updated = datetime.now()
    
    def update_profile_from_conversation(
        self,
        conversation_history: List[Dict[str, str]],
        llm_model
    ):
        """Extract and update profile description from conversation using LLM."""
        # Generate profile insights from conversation
        conv_str = "\n".join([
            f"{msg['role']}: {msg['content']}"
            for msg in conversation_history
        ])
        prompt = PREFERENCE_EXTRACTION_PROMPT.format(
            conversation_history=conv_str
        )
        new_insights = llm_model.generate_response([{"role": "system", "content": prompt}])
        
        # Combine existing profile with new insights
        if self.profile_description:
            merge_prompt = PROFILE_MERGE_PROMPT.format(
                current_profile=self.profile_description,
                new_insights=new_insights
            )
            
            self.profile_description = llm_model.generate_response(
                [{"role": "system", "content": merge_prompt}]
            )
        else:
            self.profile_description = new_insights
        
        self.last_updated = datetime.now()
    
    def add_to_watch_history(self, video_data: Dict):
        """Add a video to the user's watch history."""
        watch_entry = {
            **video_data,
            "watched_at": datetime.now().isoformat()
        }
        self.watch_history.append(watch_entry)
    
    def get_relevant_profile_aspects(
        self,
        context: str,
        llm_model
    ) -> str:
        """Extract relevant aspects of the user profile for the current context."""
        prompt = PROFILE_INTEGRATION_PROMPT.format(
            user_profile=self.profile_description,
            context=context
        )
        
        return llm_model.generate_response([{"role": "system", "content": prompt}])
    
    def update_profile_from_feedback(
        self,
        video_details: Dict,
        feedback_type: str,
        feedback_value: float,
        llm_model
    ):
        """Update profile based on feedback using LLM."""
        # Generate profile insights from feedback
        prompt = FEEDBACK_INTEGRATION_PROMPT.format(
            video_details=video_details,
            feedback_type=feedback_type,
            feedback_value=feedback_value,
            current_preferences=self.profile_description
        )
        
        new_insights = llm_model.generate_response([{"role": "system", "content": prompt}])
        
        # Merge new insights with existing profile
        if self.profile_description:
            merge_prompt = PROFILE_MERGE_PROMPT.format(
                current_profile=self.profile_description,
                new_insights=new_insights
            )
            
            self.profile_description = llm_model.generate_response(
                [{"role": "system", "content": merge_prompt}]
            )
        else:
            self.profile_description = new_insights
        
        self.last_updated = datetime.now()
    
    def to_dict(self) -> dict:
        """Convert profile to dictionary for storage."""
        return {
            "user_id": self.user_id,
            "profile_description": self.profile_description,
            "watch_history": self.watch_history,
            "last_updated": self.last_updated.isoformat()
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "UserProfile":
        """Create profile from dictionary."""
        profile = cls(data["user_id"])
        profile.profile_description = data["profile_description"]
        profile.watch_history = data["watch_history"]
        profile.last_updated = datetime.fromisoformat(data["last_updated"])
        
        return profile 