from typing import List, Dict, Optional
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os
from dotenv import load_dotenv

load_dotenv()

class YouTubeAPI:
    def __init__(self, api_key: Optional[str] = None):
        """Initialize YouTube API client."""
        self.api_key = api_key or os.getenv("YOUTUBE_API_KEY")
        if not self.api_key:
            raise ValueError("YouTube API key is required")
        
        self.youtube = build("youtube", "v3", developerKey=self.api_key)
    
    def search_videos(
        self,
        query: str,
        max_results: int = 10,
        region_code: str = "US",
        relevance_language: str = "en"
    ) -> List[Dict]:
        """Search for videos using the YouTube Data API."""
        # TODO: Hybridise with Filmot API subtitle search
        try:
            search_response = self.youtube.search().list(
                q=query,
                part="id,snippet",
                maxResults=max_results,
                type="video",
                regionCode=region_code,
                relevanceLanguage=relevance_language
            ).execute()
            
            videos = []
            for item in search_response.get("items", []):
                video_id = item["id"]["videoId"]
                
                # Get additional video details
                video_response = self.youtube.videos().list(
                    part="snippet,statistics,contentDetails",
                    id=video_id
                ).execute()
                
                if video_response["items"]:
                    video_data = video_response["items"][0]
                    videos.append({
                        "id": video_id,
                        "title": video_data["snippet"]["title"],
                        "description": video_data["snippet"]["description"],
                        "thumbnail": video_data["snippet"]["thumbnails"]["medium"]["url"],
                        "channel_title": video_data["snippet"]["channelTitle"],
                        "published_at": video_data["snippet"]["publishedAt"],
                        "view_count": video_data["statistics"].get("viewCount", "0"),
                        "like_count": video_data["statistics"].get("likeCount", "0"),
                        "duration": video_data["contentDetails"]["duration"]
                    })
            
            return videos
            
        except HttpError as e:
            print(f"An HTTP error {e.resp.status} occurred: {e.content}")
            return []
    
    def get_video_details(self, video_id: str) -> Optional[Dict]:
        """Get detailed information about a specific video."""
        try:
            video_response = self.youtube.videos().list(
                part="snippet,statistics,contentDetails",
                id=video_id
            ).execute()
            
            if video_response["items"]:
                video_data = video_response["items"][0]
                return {
                    "id": video_id,
                    "title": video_data["snippet"]["title"],
                    "description": video_data["snippet"]["description"],
                    "thumbnail": video_data["snippet"]["thumbnails"]["medium"]["url"],
                    "channel_title": video_data["snippet"]["channelTitle"],
                    "published_at": video_data["snippet"]["publishedAt"],
                    "view_count": video_data["statistics"].get("viewCount", "0"),
                    "like_count": video_data["statistics"].get("likeCount", "0"),
                    "duration": video_data["contentDetails"]["duration"]
                }
            
            return None
            
        except HttpError as e:
            print(f"An HTTP error {e.resp.status} occurred: {e.content}")
            return None 