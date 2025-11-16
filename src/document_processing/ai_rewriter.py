import openai
from langchain.schema import Document
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from pydantic_ai import Agent
from ..config import settings

class ResumeRewriter:
    def __init__(self):
        self.llm = ChatOpenAI(
            openai_api_key=settings.OPENAI_API_KEY,
            model_name="gpt-4",
            temperature=0.3
        )
        self.agent = Agent(
            model='openai:gpt-4',
            system_prompt="You are an expert resume writer and career coach."
        )
    
    async def rewrite_resume(self, original_resume: str, target_industry: str = None) -> dict:
        """Rewrite resume using AI to optimize for ATS systems and modern hiring practices"""
        
        prompt = PromptTemplate(
            template="""Rewrite and optimize the following resume for modern hiring practices and ATS systems.
            Focus on:
            1. Action-oriented language
            2. Quantifiable achievements
            3. Relevant keywords for {industry}
            4. Professional formatting
            5. Clear hierarchy and readability
            
            Original Resume:
            {resume}
            
            Return ONLY the rewritten resume without any additional text:""",
            input_variables=["resume", "industry"]
        )
        
        chain = LLMChain(llm=self.llm, prompt=prompt)
        rewritten = await chain.arun(resume=original_resume, industry=target_industry or "general")
        
        # Generate multiple versions for different job types
        versions = await self._create_targeted_versions(rewritten)
        
        return {
            "optimized": rewritten,
            "versions": versions,
            "analysis": await self._analyze_resume(rewritten)
        }
    
    async def _create_targeted_versions(self, resume: str) -> dict:
        """Create different resume versions for various job types"""
        versions = {}
        job_types = ["technical", "managerial", "creative", "executive"]
        
        for job_type in job_types:
            prompt = f"Adapt this resume for a {job_type} role, emphasizing relevant skills and experience:\n\n{resume}"
            versions[job_type] = await self.llm.apredict(prompt)
        
        return versions
    
    async def _analyze_resume(self, resume: str) -> dict:
        """Analyze resume strength and provide recommendations"""
        analysis_prompt = f"""Analyze this resume and provide a JSON response with:
        - overall_score (0-100)
        - strengths (list)
        - improvement_areas (list)
        - ats_compatibility_score (0-100)
        - keyword_density_analysis
        
        Resume:
        {resume}"""
        
        analysis = await self.llm.apredict(analysis_prompt)
        return self._parse_analysis(analysis)
