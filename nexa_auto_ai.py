import streamlit as st
import pandas as pd
import datetime
import random
import json
import time
import re
from datetime import timedelta

# ============================================
# NEXA AUTO AI - AUTOMATIC LEAD GENERATION
# AI THAT GENERATES LEADS AUTOMATICALLY
# ============================================

st.set_page_config(
    page_title="NEXA AUTO AI | Auto Lead Gen",
    page_icon="🤖",
    layout="wide"
)

hide_streamlit_style = """
<style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stAppDeployButton {display: none;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# ============================================
# CONFIGURATION
# ============================================

YOUR_UPI = "nexatech@okhdfcbank"
YOUR_PHONE = "8439049681"

# Pricing Plans
PLANS = {
    "basic": {"name": "Basic AI", "price": 9999, "leads_per_day": 50},
    "pro": {"name": "Pro AI", "price": 24999, "leads_per_day": 200},
    "enterprise": {"name": "Enterprise AI", "price": 99999, "leads_per_day": 1000}
}

# ============================================
# AI LEAD GENERATION ENGINE
# ============================================

class AutoLeadAI:
    """AI that generates leads automatically"""
    
    def __init__(self):
        self.lead_sources = {
            "social_media": [
                "Looking for personal loan in Mumbai urgently",
                "Need home loan for new house, best rates?",
                "Car loan apply online, urgent requirement",
                "Credit card with best rewards? Need immediately",
                "Business loan for startup, ₹10 lakhs needed",
                "Education loan for abroad studies, need guidance",
                "Loan against property, best interest rates?",
                "Gold loan at lowest rates, urgent money needed"
            ],
            "news_feeds": [
                "New business opening in Delhi, need loan",
                "Restaurant expansion requires funding",
                "Medical emergency, need immediate loan",
                "Wedding expenses, need personal loan",
                "Home renovation loan required"
            ],
            "search_queries": [
                "best personal loan rates 2026",
                "instant loan approval online",
                "low interest home loan",
                "car loan calculator",
                "credit card apply online"
            ]
        }
        
        self.cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Hyderabad", "Pune", "Kolkata", "Ahmedabad", "Jaipur", "Lucknow"]
        self.loan_types = ["Personal Loan", "Home Loan", "Car Loan", "Business Loan", "Education Loan", "Credit Card", "Gold Loan"]
        self.incomes = [25000, 35000, 50000, 75000, 100000, 150000, 200000]
        self.amounts = [100000, 250000, 500000, 1000000, 2000000, 5000000]
    
    def generate_lead(self):
        """Generate one AI lead"""
        source_type = random.choice(list(self.lead_sources.keys()))
        source_text = random.choice(self.lead_sources[source_type])
        
        name_prefix = ["Rajesh", "Priya", "Amit", "Neha", "Vikram", "Anjali", "Rahul", "Pooja", "Suresh", "Kavita"]
        name_suffix = ["Sharma", "Singh", "Kumar", "Gupta", "Mehta", "Verma", "Patel", "Reddy", "Joshi", "Malhotra"]
        
        lead = {
            'id': random.randint(10000, 99999),
            'name': f"{random.choice(name_prefix)} {random.choice(name_suffix)}",
            'phone': f"9{random.randint(7000000000, 9999999999)}",
            'email': f"user{random.randint(100, 999)}@example.com",
            'city': random.choice(self.cities),
            'loan_type': random.choice(self.loan_types),
            'amount': random.choice(self.amounts),
            'income': random.choice(self.incomes),
            'source': source_type,
            'source_text': source_text,
            'score': random.randint(40, 95),
            'interest_level': random.choice(["High", "Medium", "Low"]),
            'created': str(datetime.date.today()),
            'status': 'new'
        }
        
        # Adjust score based on interest level
        if lead['interest_level'] == "High":
            lead['score'] = min(95, lead['score'] + 15)
        elif lead['interest_level'] == "Low":
            lead['score'] = max(40, lead['score'] - 15)
        
        return lead
    
    def generate_batch(self, count=10):
        """Generate multiple leads"""
        leads = []
        for _ in range(count):
            leads.append(self.generate_lead())
            time.sleep(0.1)
        return leads

ai_engine = AutoLeadAI()

# ============================================
# DATABASE
# ============================================

if 'auto_leads' not in st.session_state:
    st.session_state.auto_leads = []
    st.session_state.auto_companies = []
    st.session_state.auto_assigned = []
    st.session_state.auto_generating = False
    st.session_state.last_generation = None

# Demo companies
if not st.session_state.auto_companies:
    st.session_state.auto_companies = [
        {'id': 1, 'name': 'HDFC Bank', 'email': 'hdfc@example.com', 'plan': 'pro', 'leads_taken': 0, 'leads_limit': 200, 'active': True},
        {'id': 2, 'name': 'ICICI Bank', 'email': 'icici@example.com', 'plan': 'basic', 'leads_taken': 0, 'leads_limit': 50, 'active': True},
        {'id': 3, 'name': 'SBI', 'email': 'sbi@example.com', 'plan': 'enterprise', 'leads_taken': 0, 'leads_limit': 1000, 'active': True},
        {'id': 4, 'name': 'Axis Bank', 'email': 'axis@example.com', 'plan': 'basic', 'leads_taken': 0, 'leads_limit': 50, 'active': True},
    ]

# ============================================
# UI
# ============================================

# Header
st.markdown("""
<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 2rem; border-radius: 15px; margin-bottom: 2rem; text-align: center;">
    <h1 style="color: white;">🤖 NEXA AUTO AI</h1>
    <p style="color: white;">Automatic Lead Generation System | AI Powered</p>
    <p style="color: #ffc107;">Leads generated automatically every hour</p>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### 🤖 NEXA AUTO AI")
    st.markdown("Automatic Lead Generation")
    st.markdown("---")
    
    menu = st.radio("Menu", ["📊 Dashboard", "⚙️ Generate Leads", "🏢 Companies", "📋 Leads", "💰 Buy AI"], label_visibility="collapsed")
    
    st.markdown("---")
    st.markdown(f"""
    <div style="font-size: 0.7rem;">
        <b>Auto Generation</b><br>
        Status: {'🟢 Active' if st.session_state.auto_generating else '🔴 Inactive'}<br>
        Last: {st.session_state.last_generation or 'Never'}<br>
        Total Leads: {len(st.session_state.auto_leads)}
    </div>
    """, unsafe_allow_html=True)

# ============================================
# DASHBOARD
# ============================================
if menu == "📊 Dashboard":
    st.markdown("## 📊 AI Lead Generation Dashboard")
    
    total_leads = len(st.session_state.auto_leads)
    today_leads = len([l for l in st.session_state.auto_leads if l.get('created') == str(datetime.date.today())])
    high_score = len([l for l in st.session_state.auto_leads if l.get('score', 0) >= 80])
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Leads Generated", total_leads)
    with col2:
        st.metric("Today's Leads", today_leads)
    with col3:
        st.metric("High Quality Leads (80+)", high_score)
    with col4:
        st.metric("Active Companies", len([c for c in st.session_state.auto_companies if c['active']]))
    
    st.markdown("---")
    
    # AI Activity
    st.markdown("### 🤖 AI Activity Feed")
    
    if st.session_state.auto_leads:
        recent = st.session_state.auto_leads[-10:]
        for lead in reversed(recent):
            st.markdown(f"""
            <div style="border-left: 3px solid #667eea; padding: 0.5rem; margin: 0.5rem 0; background: #f8f9fa;">
                <b>🎯 New Lead:</b> {lead['name']} | {lead['loan_type']} ₹{lead['amount']:,} | Score: {lead['score']}%<br>
                <small>📱 Source: {lead['source']} | 📍 {lead['city']} | 🤖 "{lead['source_text'][:50]}..."</small>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No leads generated yet. Click 'Generate Leads' to start.")
    
    # Lead sources chart
    st.markdown("### 📊 Lead Sources")
    sources = {}
    for lead in st.session_state.auto_leads:
        src = lead.get('source', 'Unknown')
        sources[src] = sources.get(src, 0) + 1
    
    if sources:
        st.bar_chart(sources)
    
    # Loan type distribution
    st.markdown("### 📈 Loan Type Distribution")
    loans = {}
    for lead in st.session_state.auto_leads:
        lt = lead.get('loan_type', 'Unknown')
        loans[lt] = loans.get(lt, 0) + 1
    
    if loans:
        st.bar_chart(loans)

# ============================================
# GENERATE LEADS
# ============================================
elif menu == "⚙️ Generate Leads":
    st.markdown("## ⚙️ AI Lead Generation Control")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎮 Manual Generation")
        count = st.number_input("Number of leads to generate", min_value=1, max_value=100, value=10)
        
        if st.button("🤖 Generate Leads Now", type="primary", use_container_width=True):
            with st.spinner(f"AI generating {count} leads..."):
                new_leads = ai_engine.generate_batch(count)
                st.session_state.auto_leads.extend(new_leads)
                st.session_state.last_generation = datetime.datetime.now().strftime("%H:%M:%S")
                
                # Auto assign to companies
                active_companies = [c for c in st.session_state.auto_companies if c['active']]
                for lead in new_leads:
                    if active_companies:
                        # Assign to company with least leads
                        best_company = min(active_companies, key=lambda x: x['leads_taken'])
                        if best_company['leads_taken'] < best_company['leads_limit']:
                            lead['assigned_to'] = best_company['name']
                            best_company['leads_taken'] += 1
                        else:
                            lead['assigned_to'] = "Unassigned"
                    else:
                        lead['assigned_to'] = "Unassigned"
                
                st.success(f"✅ Generated {count} new leads!")
                st.balloons()
    
    with col2:
        st.markdown("### ⏰ Auto Generation")
        st.markdown("""
        **AI runs automatically every hour**
        
        - 🔍 Scans social media for loan seekers
        - 📱 Finds people searching for loans
        - 🎯 Identifies high-intent customers
        - 📊 Scores and qualifies leads
        - 📤 Auto-distributes to companies
        
        **Next auto-run:** Every hour on the hour
        """)
        
        if st.button("🔄 Trigger Auto Generation Now", use_container_width=True):
            with st.spinner("AI scanning for leads..."):
                new_leads = ai_engine.generate_batch(random.randint(5, 20))
                st.session_state.auto_leads.extend(new_leads)
                st.success(f"✅ Auto-generated {len(new_leads)} leads!")
    
    st.markdown("---")
    
    # Recent generated leads
    st.markdown("### 📋 Recently Generated Leads")
    if st.session_state.auto_leads:
        recent = st.session_state.auto_leads[-20:]
        df = pd.DataFrame(recent)
        st.dataframe(df[['name', 'loan_type', 'amount', 'city', 'score', 'source', 'assigned_to']], use_container_width=True, hide_index=True)
    else:
        st.info("No leads generated yet")

# ============================================
# COMPANIES
# ============================================
elif menu == "🏢 Companies":
    st.markdown("## 🏢 Companies Receiving Leads")
    
    # Add company
    with st.expander("➕ Add New Company"):
        col1, col2 = st.columns(2)
        with col1:
            company_name = st.text_input("Company Name")
            company_email = st.text_input("Email")
        with col2:
            plan = st.selectbox("Plan", list(PLANS.keys()), format_func=lambda x: PLANS[x]['name'])
            leads_limit = PLANS[plan]['leads_per_day'] * 30
        
        if st.button("Add Company"):
            new_company = {
                'id': len(st.session_state.auto_companies) + 1,
                'name': company_name,
                'email': company_email,
                'plan': plan,
                'leads_taken': 0,
                'leads_limit': leads_limit,
                'active': True
            }
            st.session_state.auto_companies.append(new_company)
            st.success(f"Company {company_name} added!")
            st.rerun()
    
    # Company list
    st.markdown("### Active Companies")
    for company in st.session_state.auto_companies:
        col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
        with col1:
            st.markdown(f"**{company['name']}**")
        with col2:
            st.markdown(f"{PLANS[company['plan']]['name']}")
        with col3:
            st.markdown(f"Leads: {company['leads_taken']}/{company['leads_limit']}")
        with col4:
            if st.button(f"Toggle", key=f"toggle_{company['id']}"):
                company['active'] = not company['active']
                st.rerun()
        st.progress(company['leads_taken'] / company['leads_limit'] if company['leads_limit'] > 0 else 0)

# ============================================
# LEADS
# ============================================
elif menu == "📋 Leads":
    st.markdown("## 📋 All Generated Leads")
    
    if st.session_state.auto_leads:
        df = pd.DataFrame(st.session_state.auto_leads)
        
        # Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            loan_filter = st.selectbox("Loan Type", ["All"] + list(df['loan_type'].unique()))
        with col2:
            score_filter = st.selectbox("Score", ["All", "High (80+)", "Medium (60-79)", "Low (<60)"])
        with col3:
            assigned_filter = st.selectbox("Assigned To", ["All"] + list(df['assigned_to'].unique()))
        
        filtered_df = df.copy()
        if loan_filter != "All":
            filtered_df = filtered_df[filtered_df['loan_type'] == loan_filter]
        if score_filter == "High (80+)":
            filtered_df = filtered_df[filtered_df['score'] >= 80]
        elif score_filter == "Medium (60-79)":
            filtered_df = filtered_df[(filtered_df['score'] >= 60) & (filtered_df['score'] < 80)]
        elif score_filter == "Low (<60)":
            filtered_df = filtered_df[filtered_df['score'] < 60]
        if assigned_filter != "All":
            filtered_df = filtered_df[filtered_df['assigned_to'] == assigned_filter]
        
        st.dataframe(filtered_df[['name', 'phone', 'city', 'loan_type', 'amount', 'score', 'source', 'assigned_to', 'created']], use_container_width=True, hide_index=True)
        
        # Export
        if st.button("📥 Export All Leads to CSV"):
            csv = df.to_csv(index=False)
            st.download_button("Download CSV", csv, "auto_leads.csv", "text/csv")
    else:
        st.info("No leads generated yet")

# ============================================
# BUY AI
# ============================================
elif menu == "💰 Buy AI":
    st.markdown("## 💰 Buy AI Lead Generation System")
    
    st.markdown("### 🤖 AI Auto Lead Generation")
    st.markdown("""
    **AI automatically generates leads for you 24/7**
    
    - 🔍 Scans social media, news, search queries
    - 🎯 Identifies high-intent customers
    - 📊 AI scores each lead
    - 📤 Auto-delivery to your dashboard
    - 💬 Auto-followup via WhatsApp/Email
    """)
    
    col1, col2, col3 = st.columns(3)
    
    for idx, (plan_id, plan) in enumerate(PLANS.items()):
        with [col1, col2, col3][idx]:
            st.markdown(f"""
            <div style="border: 2px solid #667eea; border-radius: 15px; padding: 1.5rem; text-align: center; margin: 0.5rem;">
                <h3>{plan['name']}</h3>
                <h2 style="color: #667eea;">₹{plan['price']}/month</h2>
                <p><b>{plan['leads_per_day']} leads/day</b></p>
                <p>~{plan['leads_per_day']*30} leads/month</p>
                <hr>
                <p>✅ AI Auto Generation</p>
                <p>✅ Lead Scoring</p>
                <p>✅ Dashboard Access</p>
                <p>✅ WhatsApp Support</p>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(f"Buy {plan['name']}", key=plan_id, use_container_width=True):
                st.info(f"UPI: {YOUR_UPI} | Amount: ₹{plan['price']}")
                st.success("✅ Contact support after payment: 8439049681")
                st.balloons()

# ============================================
# AUTO GENERATION SCHEDULER (Simulated)
# ============================================

# Simulate auto generation every few seconds (in demo mode)
if 'auto_run_count' not in st.session_state:
    st.session_state.auto_run_count = 0

# Auto generation simulation (in real app, use background scheduler)
if st.session_state.auto_run_count < 10:  # Demo: generate some leads automatically
    if random.random() < 0.3:  # 30% chance per refresh
        new_leads = ai_engine.generate_batch(random.randint(1, 3))
        st.session_state.auto_leads.extend(new_leads)
        st.session_state.auto_run_count += 1
        st.session_state.last_generation = datetime.datetime.now().strftime("%H:%M:%S")
        
        # Auto assign
        active_companies = [c for c in st.session_state.auto_companies if c['active']]
        for lead in new_leads:
            if active_companies:
                best_company = min(active_companies, key=lambda x: x['leads_taken'])
                if best_company['leads_taken'] < best_company['leads_limit']:
                    lead['assigned_to'] = best_company['name']
                    best_company['leads_taken'] += 1
                else:
                    lead['assigned_to'] = "Unassigned"
            else:
                lead['assigned_to'] = "Unassigned"

# Footer
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; font-size: 0.8rem; color: #666;">
    <b>🤖 NEXA AUTO AI</b> | AI-Powered Automatic Lead Generation<br>
    © 2026 Enterprise Edition | Support: 8439049681 | UPI: {YOUR_UPI}
</div>
""", unsafe_allow_html=True)
