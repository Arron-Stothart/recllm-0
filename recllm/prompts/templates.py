# System prompts
# TODO: Experiment with all of these + check user/assistant formatting is valid for model #PromptEngineering😚

MAIN_CONVERSATION_PROMPT = """You are RecLLM, a helpful and engaging YouTube video recommendation assistant. 
Your goal is to understand the user's interests and preferences to provide personalized video recommendations.
Always be friendly, concise, and natural in your responses.

User Profile:
{user_profile}

Previous conversation:
{conversation_history}

User: {user_message}
Assistant:"""

SEARCH_QUERY_PROMPT = """Based on the conversation and user profile, generate a YouTube search query that will find relevant videos.
Consider the user's preferred content style, depth, and format.

User Profile:
{user_profile}

Conversation:
{conversation_history}

Generate a search query (only the query, no explanations):"""

RANKING_PROMPT = """Rate how well this video matches the user's interests, preferred content style, and learning preferences.
Consider factors like video length, presentation style, and depth of content.
Provide a score from 0 to 1 (1 being perfect match) and a brief explanation.

Video:
Title: {video_title}
Description: {video_description}
Channel: {channel_title}

User Profile:
{user_profile}

Conversation Context:
{conversation_context}

Provide rating and explanation in this format:
[score]
[explanation]"""

PREFERENCE_EXTRACTION_PROMPT = """Based on the conversation, describe the user's content preferences and interests.
Consider:
- Topics and subjects they're interested in
- Preferred content style (entertaining, academic, practical, etc.)
- Preferred video length and depth
- Learning style and pace
- Production quality preferences
- Language and presentation style preferences

Conversation:
{conversation_history}

Generate a natural, coherent description of the user's preferences:"""

PROFILE_MERGE_PROMPT = """Merge these two user profile descriptions into a single, coherent profile.
Remove redundancy, resolve any contradictions, and maintain the most current and relevant information.
The merged profile should capture the user's content preferences, interests, and viewing habits comprehensively.

Current profile:
{current_profile}

New insights:
{new_insights}

Generate a concise, coherent profile that combines both descriptions:"""

PROFILE_INTEGRATION_PROMPT = """Given the user profile and current conversation context, extract the most relevant aspects of their preferences.
Focus on aspects that would help find the most suitable videos for the current context.

User Profile:
{user_profile}

Current Context:
{context}

Describe the relevant preferences:"""

RESPONSE_GENERATION_PROMPT = """Generate a natural, engaging response that introduces the recommended videos.
Explain how each recommendation aligns with the user's content preferences and interests.
Be concise but informative.

User Profile:
{user_profile}

Conversation History:
{conversation_history}

Top Recommendations:
{recommendations}

Generate response (be natural and conversational):"""

FEEDBACK_INTEGRATION_PROMPT = """Based on the user's feedback on this video, update our understanding of their preferences.
Consider how this feedback reveals their content preferences, interests, and viewing habits.

Video Details:
{video_details}

Feedback Type: {feedback_type}
Feedback Value: {feedback_value}

Current User Profile:
{current_preferences}

Generate an updated profile description:""" 