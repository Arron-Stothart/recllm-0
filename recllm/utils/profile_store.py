import os
import json
from typing import Dict
from recllm.models.user_profile import UserProfile

class ProfileStore:
    def __init__(self):
        # Use /tmp for storage in container
        self.storage_dir = "/tmp/profiles"
        os.makedirs(self.storage_dir, exist_ok=True)
        self._cache: Dict[str, UserProfile] = {}

    def get_profile(self, user_id: str) -> UserProfile:
        """Get or create a user profile."""
        if user_id in self._cache:
            return self._cache[user_id]

        profile_path = os.path.join(self.storage_dir, f"{user_id}.json")
        
        if os.path.exists(profile_path):
            try:
                with open(profile_path, 'r') as f:
                    data = json.load(f)
                profile = UserProfile.from_dict(data)
            except Exception:
                profile = UserProfile(user_id)
        else:
            profile = UserProfile(user_id)
        
        self._cache[user_id] = profile
        return profile

    def save_profile(self, user_id: str, profile: UserProfile):
        """Save a user profile to storage."""
        profile_path = os.path.join(self.storage_dir, f"{user_id}.json")
        
        try:
            with open(profile_path, 'w') as f:
                json.dump(profile.to_dict(), f)
            self._cache[user_id] = profile
        except Exception as e:
            print(f"Error saving profile: {e}") 