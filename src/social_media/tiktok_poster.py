import asyncio
from typing import Dict
import aiohttp

class TikTokPoster:
    def __init__(self):
        self.api_url = "https://open.tiktokapis.com/v2/post/publish/inbox/video/"
    
    async def post_video(self, video_data: Dict) -> Dict:
        """Post video to TikTok automatically"""
        
        # Prepare video content
        payload = {
            "video_url": video_data['video_url'],
            "description": self._build_description(video_data),
            "privacy_level": "PUBLIC_TO_EVERYONE",
            "disable_duet": False,
            "disable_comment": False,
            "disable_stitch": False
        }
        
        headers = {
            "Authorization": f"Bearer {video_data['access_token']}",
            "Content-Type": "application/json"
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.post(self.api_url, json=payload, headers=headers) as response:
                if response.status == 200:
                    result = await response.json()
                    return {
                        "success": True,
                        "video_id": result['data']['id'],
                        "share_url": result['data']['share_url'],
                        "platform": "tiktok"
                    }
                else:
                    return {
                        "success": False,
                        "error": await response.text(),
                        "platform": "tiktok"
                    }
    
    def _build_description(self, video_data: Dict) -> str:
        """Build engaging TikTok description"""
        description = video_data.get('script_hook', '')
        description += f"\n\n{video_data.get('call_to_action', 'Find your dream job today!')}"
        description += f"\n\n{''.join([f'#{tag} ' for tag in video_data.get('hashtags', [])])}"
        return description

class SocialMediaManager:
    def __init__(self):
        self.tiktok_poster = TikTokPoster()
        self.facebook_poster = FacebookPoster()
        self.instagram_poster = InstagramPoster()
    
    async def post_to_all_platforms(self, content_package: Dict) -> Dict:
        """Post content to all social media platforms simultaneously"""
        
        results = {}
        
        # Post to TikTok
        if content_package.get('post_to_tiktok', True):
            results['tiktok'] = await self.tiktok_poster.post_video(content_package)
        
        # Post to Instagram
        if content_package.get('post_to_instagram', True):
            results['instagram'] = await self.instagram_poster.post_reel(content_package)
        
        # Post to Facebook
        if content_package.get('post_to_facebook', True):
            results['facebook'] = await self.facebook_poster.post_video(content_package)
        
        return results
    
    async def schedule_daily_posts(self, themes: List[str]) -> Dict:
        """Schedule daily social media posts"""
        scheduled_posts = {}
        
        for i, theme in enumerate(themes):
            # Create content for each theme
            content = await self.content_generator.create_complete_reel(theme)
            
            # Schedule posting
            post_time = self._calculate_post_time(i)
            scheduled_posts[post_time] = content
        
        return scheduled_posts
