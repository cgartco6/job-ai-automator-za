import React, { useState, useEffect } from 'react';
import { PieChart, BarChart, TrendingUp, Users, DollarSign, Activity } from 'lucide-react';

const OwnerDashboard = () => {
    const [metrics, setMetrics] = useState(null);
    const [activeTab, setActiveTab] = useState('overview');

    useEffect(() => {
        fetchDashboardData();
    }, []);

    const fetchDashboardData = async () => {
        const response = await fetch('/owners/dashboard', {
            headers: { 'Authorization': `Bearer ${localStorage.getItem('token')}` }
        });
        const data = await response.json();
        setMetrics(data);
    };

    const activateAIAgents = async (agentType) => {
        const response = await fetch('/owners/dashboard/ai/activate', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${localStorage.getItem('token')}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ agent_type: agentType })
        });
        const result = await response.json();
        alert(`AI Agents Activated: ${result.activated_agents.join(', ')}`);
    };

    if (!metrics) return <div>Loading...</div>;

    return (
        <div className="owner-dashboard">
            <div className="dashboard-header">
                <h1>Business Intelligence Dashboard</h1>
                <div className="revenue-display">
                    <DollarSign className="icon" />
                    <span className="revenue-amount">
                        ZAR {metrics.revenue?.monthly_revenue_zar?.toLocaleString()}
                    </span>
                    <span className="revenue-growth positive">
                        {metrics.revenue?.revenue_growth}
                    </span>
                </div>
            </div>

            <div className="metrics-grid">
                <div className="metric-card">
                    <Users className="icon" />
                    <div className="metric-info">
                        <h3>Total Users</h3>
                        <span className="metric-value">{metrics.users?.total_users}</span>
                        <span className="metric-change positive">+{metrics.users?.daily_signups} today</span>
                    </div>
                </div>

                <div className="metric-card">
                    <DollarSign className="icon" />
                    <div className="metric-info">
                        <h3>Monthly Revenue</h3>
                        <span className="metric-value">
                            ZAR {metrics.revenue?.monthly_revenue_zar?.toLocaleString()}
                        </span>
                        <span className="metric-change positive">
                            Target: ZAR {metrics.revenue?.target_monthly?.toLocaleString()}
                        </span>
                    </div>
                </div>

                <div className="metric-card">
                    <Activity className="icon" />
                    <div className="metric-info">
                        <h3>AI Performance</h3>
                        <span className="metric-value">{metrics.ai_performance?.success_rate}%</span>
                        <span className="metric-change">
                            {metrics.ai_performance?.applications_today} apps today
                        </span>
                    </div>
                </div>

                <div className="metric-card">
                    <TrendingUp className="icon" />
                    <div className="metric-info">
                        <h3>Customer Acquisition</h3>
                        <span className="metric-value">{metrics.marketing?.daily_acquisitions}</span>
                        <span className="metric-change positive">
                            CPA: ZAR {metrics.marketing?.cost_per_acquisition}
                        </span>
                    </div>
                </div>
            </div>

            <div className="ai-control-panel">
                <h2>AI Agent Control Center</h2>
                <div className="ai-buttons">
                    <button onClick={() => activateAIAgents('marketing')} className="ai-btn marketing">
                        Activate Marketing AI
                    </button>
                    <button onClick={() => activateAIAgents('applications')} className="ai-btn applications">
                        Activate Application AI
                    </button>
                    <button onClick={() => activateAIAgents('acquisition')} className="ai-btn acquisition">
                        Activate Acquisition AI
                    </button>
                    <button onClick={() => activateAIAgents('all')} className="ai-btn all">
                        ACTIVATE ALL AI
                    </button>
                </div>
            </div>

            <div className="charts-section">
                <h2>Business Analytics</h2>
                <div className="charts-grid">
                    <div className="chart-container">
                        <h3>Revenue Growth</h3>
                        {/* Revenue chart would be rendered here */}
                    </div>
                    <div className="chart-container">
                        <h3>User Distribution</h3>
                        {/* Pie chart would be rendered here */}
                    </div>
                </div>
            </div>
        </div>
    );
};

export default OwnerDashboard;
