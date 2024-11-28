from typing import List, Dict, Optional
import torch
import torch.nn as nn
from transformers import AutoModelForCausalLM, AutoTokenizer
from recllm.prompts.templates import (
    MAIN_CONVERSATION_PROMPT,
    SEARCH_QUERY_PROMPT,
    RANKING_PROMPT,
    RESPONSE_GENERATION_PROMPT
)
import logging

class RecLLM(nn.Module):
    def __init__(
        self,
        model_name: str = "google/gemma-2-2b-it",
        device: str = "cpu"
    ):
        super().__init__()
        self.device = device
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            device_map=None,
            torch_dtype=torch.float32,
            low_cpu_mem_usage=True
        ).to(device)
        
    def generate_response(
        self,
        conversation_history: List[Dict[str, str]],
        user_profile: Optional[Dict] = None,
        max_length: int = 512
    ) -> str:
        """Generate a response based on conversation history and user profile."""
        try:
            conv_str = "\n".join([
                f"{msg['role']}: {msg['content']}"
                for msg in conversation_history[:-1]  # Exclude the last message
            ])
            
            user_message = conversation_history[-1]["content"] if conversation_history else ""
            
            prompt = MAIN_CONVERSATION_PROMPT.format(
                user_profile=str(user_profile or {}),
                conversation_history=conv_str,
                user_message=user_message
            )
            
            inputs = self.tokenizer(
                prompt,
                return_tensors="pt",
                truncation=True,
                max_length=max_length
            ).to(self.device)
            
            outputs = self.model.generate(
                **inputs,
                max_length=max_length,
                num_return_sequences=1,
                temperature=0.7,
                do_sample=True,
                pad_token_id=self.tokenizer.eos_token_id
            )
            
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            return self._extract_response(response)
            
        except Exception as e:
            logging.error(f"Error in generate_response: {str(e)}", exc_info=True)
            return f"I apologize, but I encountered an error: {str(e)}"
    
    def generate_search_query(
        self,
        conversation_history: List[Dict[str, str]],
        user_profile: Optional[Dict] = None
    ) -> str:
        """Generate a search query for YouTube based on conversation context."""
        conv_str = "\n".join([
            f"{msg['role']}: {msg['content']}"
            for msg in conversation_history
        ])
        
        prompt = SEARCH_QUERY_PROMPT.format(
            user_profile=str(user_profile or {}),
            conversation_history=conv_str
        )
        
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        outputs = self.model.generate(
            **inputs,
            max_length=256,
            num_return_sequences=1,
            temperature=0.2
        )
        
        query = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return query.strip()
    
    def rank_videos(
        self,
        video_candidates: List[Dict],
        conversation_context: str,
        user_profile: Optional[Dict] = None
    ) -> List[Dict]:
        """Rank video candidates based on conversation context and user profile."""
        ranked_videos = []
        for video in video_candidates:
            prompt = RANKING_PROMPT.format(
                video_title=video.get("title", ""),
                video_description=video.get("description", ""),
                channel_title=video.get("channel_title", ""),
                user_profile=str(user_profile or {}),
                conversation_context=conversation_context
            )
            
            inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
            outputs = self.model.generate(
                **inputs,
                max_length=512,
                num_return_sequences=1,
                temperature=0.3
            )
            
            response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            try:
                lines = response.strip().split("\n")
                score = float(lines[0])
                explanation = "\n".join(lines[1:])
            except Exception as e:
                score = 0.0
                explanation = f"Failed to generate explanation: {e}"
            
            ranked_videos.append({
                **video,
                "score": score,
                "explanation": explanation
            })
        
        ranked_videos.sort(key=lambda x: x["score"], reverse=True)
        return ranked_videos
    
    def generate_recommendation_response(
        self,
        conversation_history: List[Dict[str, str]],
        recommendations: List[Dict],
        user_profile: Optional[Dict] = None
    ) -> str:
        """Generate a natural language response with recommendations."""
        conv_str = "\n".join([
            f"{msg['role']}: {msg['content']}"
            for msg in conversation_history
        ])
        
        rec_str = "\n".join([
            f"Title: {video['title']}\nExplanation: {video['explanation']}"
            for video in recommendations[:5]  # Top 5 recommendations
        ])
        
        prompt = RESPONSE_GENERATION_PROMPT.format(
            user_profile=str(user_profile or {}),
            conversation_history=conv_str,
            recommendations=rec_str
        )
        
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.device)
        outputs = self.model.generate(
            **inputs,
            max_length=1024,
            num_return_sequences=1,
            temperature=0.7
        )
        
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response.strip()
    
    def _extract_response(self, generated_text: str) -> str:
        """Extract the relevant response from the generated text."""
        response = generated_text.split("Assistant: ")[-1].strip()
        return response