from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import shutil
import os

from .auth.authentication import get_current_user
from .ai_agents.agent_orchestrator import AgentOrchestrator
from .location_za.location_matcher import LocationMatcher
from .social_media.whatsapp_integration import WhatsAppService
from .owners_dashboard.dashboard import OwnerDashboard
from .auth.payment_zar import ZARPaymentProcessor, PAYMENT_PACKAGES

app = FastAPI(title="AI Job Application Automator - South Africa", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/marketing", StaticFiles(directory="marketing_content"), name="marketing")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

security = HTTPBearer()
payment_processor = ZARPaymentProcessor()
whatsapp_service = WhatsAppService()
location_matcher = LocationMatcher()

@app.post("/register-za")
async def register_user_za(
    email: str = Form(...),
    password: str = Form(...),
    full_name: str = Form(...),
    province: str = Form(...),
    city: str = Form(...),
    phone: str = Form(...)
):
    """South Africa specific registration"""
    return await create_za_user(email, password, full_name, province, city, phone)

@app.post("/add-custom-location")
async def add_custom_location(
    location_name: str = Form(...),
    location_type: str = Form("town"),
    current_user: dict = Depends(get_current_user)
):
    """Add custom location and auto-detect province"""
    result = location_matcher.add_custom_location(location_name, location_type)
    return result

@app.post("/create-payment-intent")
async def create_payment_intent_zar(
    package: str = Form(...),
    current_user: dict = Depends(get_current_user)
):
    """Create payment intent in ZAR"""
    if package not in PAYMENT_PACKAGES:
        raise HTTPException(status_code=400, detail="Invalid package")
    
    amount = PAYMENT_PACKAGES[package]["price_zar"]
    return await payment_processor.create_payment_intent(amount, current_user['id'], package)

@app.get("/whatsapp-link")
async def get_whatsapp_link(current_user: dict = Depends(get_current_user)):
    """Get personalized WhatsApp me link"""
    link = await whatsapp_service.create_whatsapp_me_link(current_user['id'])
    return {"whatsapp_link": link}

@app.post("/generate-marketing-content")
async def generate_marketing_content(
    theme: str = Form(...),
    platform: str = Form("tiktok"),
    current_user: dict = Depends(get_current_user)
):
    """Generate HD marketing content"""
    if not current_user.get('is_owner', False):
        raise HTTPException(status_code=403, detail="Owner access required")
    
    content_creator = ContentGenerator()
    content = await content_creator.generate_marketing_content(theme, platform)
    return content

@app.get("/owners/dashboard")
async def owners_dashboard(current_user: dict = Depends(get_current_user)):
    """Owner's dashboard with business metrics"""
    dashboard = OwnerDashboard()
    return await dashboard.get_business_overview(current_user)

@app.post("/activate-acquisition-campaign")
async def activate_acquisition_campaign(
    target_count: int = Form(2000),
    days: int = Form(7),
    current_user: dict = Depends(get_current_user)
):
    """Activate customer acquisition campaign"""
    if not current_user.get('is_owner', False):
        raise HTTPException(status_code=403, detail="Owner access required")
    
    acquisition_agent = TargetAcquisitionAgent()
    return await acquisition_agent.acquire_customers(target_count, days)

# South Africa Compliance Endpoints
@app.get("/compliance-documents")
async def get_compliance_documents(current_user: dict = Depends(get_current_user)):
    """Generate South Africa compliance documents"""
    compliance_generator = ComplianceGeneratorZA()
    documents = await compliance_generator.generate_all_documents()
    return documents

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
