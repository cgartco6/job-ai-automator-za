import openai
from langchain.agents import AgentType, initialize_agent
from langchain.tools import Tool
from langchain.memory import ConversationBufferMemory
from pydantic_ai import Agent
from ..config import settings

class ApplicationAgent:
    def __init__(self):
        self.llm = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.agent = Agent(
            model='openai:gpt-4',
            system_prompt="""You are an expert job application assistant. Your role is to:
            1. Analyze job descriptions and match them with candidate profiles
            2. Generate personalized cover letters and application responses
            3. Adapt resumes for specific job applications
            4. Provide application strategy recommendations
            5. Handle follow-up communications"""
        )
        
        self.memory = ConversationBufferMemory()
    
    async def generate_cover_letter(self, job_data: dict, candidate_profile: dict, resume_text: str) -> str:
        """Generate personalized cover letter for a job application"""
        
        prompt = f"""
        Generate a compelling cover letter for the following job opportunity:
        
        Job Title: {job_data.get('title')}
        Company: {job_data.get('company')}
        Job Description: {job_data.get('description', '')}
        
        Candidate Profile:
        - Skills: {', '.join(candidate_profile.get('skills', []))}
        - Experience: {candidate_profile.get('experience')} years
        - Education: {candidate_profile.get('education')}
        
        Resume Highlights:
        {resume_text[:1000]}
        
        Create a professional, engaging cover letter that:
        1. Addresses the hiring manager personally if possible
        2. Highlights relevant skills and experience
        3. Shows enthusiasm for the specific role and company
        4. Includes specific accomplishments and quantifiable results
        5. Is tailored to the job description
        
        Keep it concise (under 400 words) and impactful.
        """
        
        response = await self.llm.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a professional career coach and resume writer."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1000,
            temperature=0.7
        )
        
        return response.choices[0].message.content
    
    async def customize_resume(self, original_resume: str, job_description: str) -> str:
        """Customize resume for a specific job application"""
        
        prompt = f"""
        Customize this resume to better match the job description:
        
        ORIGINAL RESUME:
        {original_resume}
        
        JOB DESCRIPTION:
        {job_description}
        
        Please:
        1. Emphasize relevant skills and experience
        2. Incorporate keywords from the job description
        3. Reorder sections to highlight most relevant qualifications
        4. Maintain truthfulness while optimizing presentation
        
        Return only the customized resume text.
        """
        
        response = await self.llm.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000,
            temperature=0.3
        )
        
        return response.choices[0].message.content
