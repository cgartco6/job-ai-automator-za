from twilio.rest import Client
from fastapi import APIRouter
from typing import Dict
import asyncio

router = APIRouter()

class WhatsAppService:
    def __init__(self):
        self.client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        self.whatsapp_number = "whatsapp:+14155238886"  # Twilio WhatsApp number
    
    async def send_interview_invite(self, user_phone: str, interview_details: Dict) -> Dict:
        """Send interview invitation via WhatsApp"""
        
        message_body = f"""
🎉 *INTERVIEW INVITATION* 🎉

Dear Applicant,

You've been invited for an interview!

*Position:* {interview_details['position']}
*Company:* {interview_details['company']}
*Date:* {interview_details['date']}
*Time:* {interview_details['time']}
*Location:* {interview_details['location']}

Please confirm your attendance by replying YES or NO.

Best regards,
AI Job Assistant
        """
        
        try:
            message = self.client.messages.create(
                body=message_body,
                from_=self.whatsapp_number,
                to=f"whatsapp:{user_phone}"
            )
            
            return {
                "success": True,
                "message_sid": message.sid,
                "status": message.status,
                "platform": "whatsapp"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "platform": "whatsapp"
            }
    
    async def send_application_update(self, user_phone: str, update_data: Dict) -> Dict:
        """Send application status update"""
        
        if update_data['status'] == 'applied':
            message = f"✅ Job applied: {update_data['job_title']} at {update_data['company']}"
        elif update_data['status'] == 'interview':
            message = f"🎉 Interview scheduled: {update_data['job_title']} on {update_data['date']}"
        elif update_data['status'] == 'offer':
            message = f"🏆 JOB OFFER: {update_data['job_title']} - {update_data['salary']}"
        else:
            message = f"📊 Application update: {update_data['message']}"
        
        return await self._send_message(user_phone, message)
    
    async def create_whatsapp_me_link(self, user_id: str) -> str:
        """Create WhatsApp me link for direct contact"""
        pre-filled_message = f"Hello! I'm interested in learning more about AI Job Automator services. User ID: {user_id}"
        
        encoded_message = pre-filled_message.replace(' ', '%20')
        return f"https://wa.me/27600123456?text={encoded_message}"
