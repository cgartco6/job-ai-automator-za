import openai
from typing import List, Dict
import asyncio
from ..config import settings

class ContentGenerator:
    def __init__(self):
        self.openai_client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
    
    async def generate_marketing_content(self, theme: str, platform: str) -> Dict:
        """Generate HD marketing content for different platforms"""
        
        if platform == "tiktok":
            return await self._generate_tiktok_content(theme)
        elif platform == "instagram":
            return await self._generate_instagram_content(theme)
        elif platform == "facebook":
            return await self._generate_facebook_content(theme)
        else:
            return await self._generate_generic_content(theme)
    
    async def _generate_tiktok_content(self, theme: str) -> Dict:
        """Generate TikTok shorts content"""
        prompt = f"""
        Create a viral TikTok short script about job searching in South Africa with theme: {theme}
        
        Include:
        - Engaging hook (first 3 seconds)
        - Problem statement
        - Solution (our platform)
        - Call to action
        - Trending hashtags for South Africa
        - Background music suggestions
        
        Make it entertaining, fast-paced, and relatable for South African job seekers.
        """
        
        response = await self.openai_client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a viral TikTok content creator specializing in career content for South African audience."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000
        )
        
        script = response.choices[0].message.content
        
        # Generate video description
        video_prompt = f"Create a HD video showing: {script}"
        
        return {
            "platform": "tiktok",
            "script": script,
            "hashtags": ["#jobs", "#career", "#southafrica", "#hiring", "#jobsearch", "#careertok"],
            "video_prompt": video_prompt,
            "duration": "15-30 seconds"
        }
    
    async def generate_voiceover(self, script: str, language: str = "en-ZA") -> str:
        """Generate South African accent voiceover"""
        # Integration with voice generation API
        voiceover_prompt = f"""
        Generate a natural South African English voiceover for this script:
        {script}
        
        Requirements:
        - Clear South African accent
        - Professional but friendly tone
        - Moderate pace
        - HD audio quality
        """
        
        return await self._generate_audio(voiceover_prompt, language)
    
    async def generate_hd_image(self, prompt: str) -> str:
        """Generate HD marketing images"""
        response = await self.openai_client.images.generate(
            model="dall-e-3",
            prompt=f"HD professional marketing image: {prompt}. Style: modern, professional, South African context, high quality",
            size="1024x1024",
            quality="hd",
            n=1
        )
        
        return response.data[0].url
    
    async def create_complete_reel(self, theme: str) -> Dict:
        """Create complete social media reel with all assets"""
        content = await self.generate_marketing_content(theme, "instagram")
        voiceover = await self.generate_voiceover(content['script'])
        image_url = await self.generate_hd_image(content['video_prompt'])
        
        return {
            "theme": theme,
            "script": content['script'],
            "voiceover": voiceover,
            "thumbnail": image_url,
            "hashtags": content['hashtags'],
            "platforms": ["instagram", "tiktok", "facebook"],
            "status": "ready_for_posting"
        }
