from datetime import datetime
from typing import Dict, List
import jinja2
import os

class ComplianceGeneratorZA:
    def __init__(self):
        self.template_loader = jinja2.FileSystemLoader(searchpath="./templates")
        self.template_env = jinja2.Environment(loader=self.template_loader)
        
    async def generate_compliance_documents(self, company_info: Dict) -> Dict[str, str]:
        """Generate all required compliance documents for South Africa"""
        
        documents = {}
        
        # Privacy Policy compliant with POPIA
        documents["privacy_policy"] = await self._generate_popia_privacy_policy(company_info)
        
        # Terms of Service
        documents["terms_of_service"] = await self._generate_terms_of_service(company_info)
        
        # Data Processing Agreement
        documents["data_processing_agreement"] = await self._generate_data_processing_agreement(company_info)
        
        # Consumer Protection Act compliance
        documents["cpa_compliance"] = await self._generate_cpa_compliance(company_info)
        
        # Electronic Communications and Transactions Act
        documents["ect_act_compliance"] = await self._generate_ect_act_compliance(company_info)
        
        return documents
    
    async def _generate_popia_privacy_policy(self, company_info: Dict) -> str:
        """Generate POPIA compliant privacy policy"""
        
        template = self.template_env.get_template("privacy_policy_za.j2")
        
        return template.render(
            company_name=company_info.get("name", "AI Job Automator South Africa"),
            registration_number=company_info.get("registration_number", "2024/123456/07"),
            physical_address=company_info.get("address", "123 Main Street, Johannesburg, 2000"),
            email=company_info.get("email", "info@jobautomator.co.za"),
            phone=company_info.get("phone", "+27 11 123 4567"),
            effective_date=datetime.now().strftime("%Y-%m-%d"),
            data_officer=company_info.get("data_officer", "Data Protection Officer")
        )
    
    async def _generate_terms_of_service(self, company_info: Dict) -> str:
        """Generate terms of service compliant with South African law"""
        
        template = self.template_env.get_template("terms_of_service_za.j2")
        
        return template.render(
            company_name=company_info.get("name", "AI Job Automator South Africa"),
            website_url=company_info.get("website", "https://jobautomator.co.za"),
            support_email=company_info.get("support_email", "support@jobautomator.co.za"),
            effective_date=datetime.now().strftime("%Y-%m-%d")
        )
    
    async def _generate_data_processing_agreement(self, company_info: Dict) -> str:
        """Generate data processing agreement for POPIA compliance"""
        
        template = self.template_env.get_template("data_processing_agreement.j2")
        
        return template.render(
            company_name=company_info.get("name", "AI Job Automator South Africa"),
            registration_number=company_info.get("registration_number", "2024/123456/07"),
            effective_date=datetime.now().strftime("%Y-%m-%d")
        )
    
    async def _generate_cpa_compliance(self, company_info: Dict) -> str:
        """Generate Consumer Protection Act compliance document"""
        
        template = self.template_env.get_template("cpa_compliance.j2")
        
        return template.render(
            company_name=company_info.get("name", "AI Job Automator South Africa"),
            registration_number=company_info.get("registration_number", "2024/123456/07"),
            physical_address=company_info.get("address", "123 Main Street, Johannesburg, 2000"),
            effective_date=datetime.now().strftime("%Y-%m-%d")
        )
    
    async def _generate_ect_act_compliance(self, company_info: Dict) -> str:
        """Generate Electronic Communications and Transactions Act compliance"""
        
        template = self.template_env.get_template("ect_act_compliance.j2")
        
        return template.render(
            company_name=company_info.get("name", "AI Job Automator South Africa"),
            website_url=company_info.get("website", "https://jobautomator.co.za"),
            email=company_info.get("email", "info@jobautomator.co.za"),
            effective_date=datetime.now().strftime("%Y-%m-%d")
        )
    
    async def generate_employment_contract_template(self, job_details: Dict) -> str:
        """Generate South African employment contract template"""
        
        template = self.template_env.get_template("employment_contract_za.j2")
        
        return template.render(
            company_name=job_details.get("company_name"),
            employee_name=job_details.get("employee_name"),
            position=job_details.get("position"),
            start_date=job_details.get("start_date"),
            salary=job_details.get("salary"),
            location=job_details.get("location"),
            working_hours=job_details.get("working_hours", "09:00 - 17:00"),
            notice_period=job_details.get("notice_period", "1 month")
        )

# Create template directory and files if they don't exist
def create_compliance_templates():
    """Create default compliance templates"""
    templates_dir = "templates"
    os.makedirs(templates_dir, exist_ok=True)
    
    # Privacy Policy Template
    privacy_policy_template = """
PRIVACY POLICY
In compliance with the Protection of Personal Information Act (POPIA)

1. Introduction
{{ company_name }} (Registration Number: {{ registration_number }}) is committed to protecting your personal information.

2. Information We Collect
- Personal identification information
- Resume and employment history
- Educational qualifications
- Contact details

3. How We Use Your Information
- To provide job application services
- To match you with potential employers
- To communicate with you about opportunities
- For compliance with South African laws

4. Data Security
We implement appropriate technical and organizational measures to protect your personal information.

5. Your Rights
You have the right to:
- Access your personal information
- Correct inaccurate information
- Object to processing
- Lodge a complaint with the Information Regulator

Contact Information:
Data Protection Officer: {{ data_officer }}
Email: {{ email }}
Phone: {{ phone }}
Address: {{ physical_address }}

Effective Date: {{ effective_date }}
"""
    
    with open(f"{templates_dir}/privacy_policy_za.j2", "w") as f:
        f.write(privacy_policy_template)
    
    # Similar templates would be created for other documents...
