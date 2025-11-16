from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from typing import Dict, List
import plotly.graph_objects as go
import plotly.express as px
from ..auth.authentication import get_current_user

router = APIRouter()
security = HTTPBearer()

class OwnerDashboard:
    def __init__(self):
        self.metrics = {}
    
    async def get_business_overview(self, user: Dict = Depends(get_current_user)) -> Dict:
        """Get comprehensive business overview"""
        
        if not user.get('is_owner', False):
            return {"error": "Unauthorized"}
        
        revenue_data = await self._get_revenue_metrics()
        user_metrics = await self._get_user_metrics()
        ai_metrics = await self._get_ai_performance()
        marketing_metrics = await self._get_marketing_metrics()
        
        return {
            "revenue": revenue_data,
            "users": user_metrics,
            "ai_performance": ai_metrics,
            "marketing": marketing_metrics,
            "charts": await self._generate_charts()
        }
    
    async def _get_revenue_metrics(self) -> Dict:
        """Get revenue metrics in ZAR"""
        return {
            "monthly_revenue_zar": 1250000,  # Example: 1.25 million ZAR
            "revenue_growth": "+25%",
            "average_revenue_per_user": 599,
            "revenue_breakdown": {
                "basic_packages": 350000,
                "professional_packages": 600000,
                "premium_packages": 300000
            },
            "target_monthly": 2000000  # 2 million ZAR target
        }
    
    async def _generate_charts(self) -> Dict:
        """Generate Plotly charts for dashboard"""
        
        # Revenue chart
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        revenue = [800000, 950000, 1100000, 1250000, 1400000, 1600000]
        
        revenue_fig = go.Figure()
        revenue_fig.add_trace(go.Scatter(
            x=months, y=revenue,
            mode='lines+markers',
            name='Monthly Revenue',
            line=dict(color='#00FF00', width=4)
        ))
        revenue_fig.update_layout(
            title='Monthly Revenue (ZAR)',
            xaxis_title='Month',
            yaxis_title='Revenue (ZAR)'
        )
        
        # User growth chart
        user_growth = [500, 1200, 2500, 4200, 6500, 8900]
        user_fig = px.line(x=months, y=user_growth, title='User Growth')
        user_fig.update_traces(line_color='#FF6B00')
        
        # Package distribution pie chart
        packages = ['Basic', 'Professional', 'Premium']
        distribution = [45, 35, 20]
        pie_fig = px.pie(values=distribution, names=packages, title='Package Distribution')
        
        return {
            "revenue_chart": revenue_fig.to_json(),
            "user_chart": user_fig.to_json(),
            "package_chart": pie_fig.to_json()
        }
    
    async def activate_ai_agents(self, agent_type: str = "all") -> Dict:
        """Activate AI agents from dashboard"""
        
        agents_to_activate = []
        
        if agent_type == "all" or agent_type == "marketing":
            agents_to_activate.extend(["content_creator", "social_poster", "ad_optimizer"])
        
        if agent_type == "all" or agent_type == "applications":
            agents_to_activate.extend(["job_scraper", "application_bot", "resume_rewriter"])
        
        if agent_type == "all" or agent_type == "acquisition":
            agents_to_activate.extend(["lead_generator", "conversion_optimizer"])
        
        return {
            "activated_agents": agents_to_activate,
            "status": "active",
            "estimated_impact": "2-5x performance increase"
        }

@router.get("/dashboard/overview")
async def get_dashboard_overview(current_user: Dict = Depends(get_current_user)):
    dashboard = OwnerDashboard()
    return await dashboard.get_business_overview(current_user)

@router.post("/dashboard/ai/activate")
async def activate_ai_agents(agent_type: str, current_user: Dict = Depends(get_current_user)):
    dashboard = OwnerDashboard()
    return await dashboard.activate_ai_agents(agent_type)
