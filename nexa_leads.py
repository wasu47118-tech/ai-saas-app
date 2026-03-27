import streamlit as st
import pandas as pd
import datetime
import hashlib
import json
import os
import random
import uuid
from datetime import timedelta
import time
import re

# ============================================
# NEXA LEADS - AI POWERED LEAD GENERATION
# LOAN & CREDIT CARD LEADS
# MULTI-COMPANY SUPPORT
# ============================================

# ============================================
# HIDE STREAMLIT UI
# ============================================

st.set_page_config(
    page_title="NEXA LEADS | AI Lead Gen",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

hide_streamlit_style = """
<style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stAppDeployButton {display: none;}
    .stActionButton {display: none;}
    .stToolbar {display: none;}
    .stStatusWidget {display: none;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# ============================================
# CONFIGURATION
# ============================================

YOUR_EMAIL = "wasu47118@gmail.com"
YOUR_PHONE = "8439049681"
YOUR_UPI = "nexatech@okhdfcbank"

# Pricing Plans (per month)
PRICING_PLANS = {
    "basic": {
        "name": "Basic Plan",
        "price": 4999,
        "leads_limit": 500,
        "companies": 1,
        "features": ["500 leads/month", "Basic AI Scoring", "Email Support"]
    },
    "professional": {
        "name": "Professional Plan",
        "price": 14999,
        "leads_limit": 2000,
        "companies": 3,
        "features": ["2000 leads/month", "Advanced AI Scoring", "Auto Follow-up", "WhatsApp Support", "3 Companies"]
    },
    "enterprise": {
        "name": "Enterprise Plan",
        "price": 49999,
        "leads_limit": 10000,
        "companies": 10,
        "features": ["10000 leads/month", "AI Premium Scoring", "SMS/WhatsApp/Email", "Priority Support", "API Access", "10 Companies"]
    }
}

# Lead Sources
LEAD_SOURCES = {
    "google_ads": "Google Ads",
    "facebook": "Facebook",
    "instagram": "Instagram",
    "whatsapp": "WhatsApp",
    "website": "Website Form",
    "referral": "Referral",
    "qr_code": "QR Code",
    "email": "Email Campaign"
}

# Loan Types
LOAN_TYPES = [
    "Personal Loan",
    "Home Loan",
    "Car Loan",
    "Business Loan",
    "Education Loan",
    "Credit Card",
    "Gold Loan",
    "Loan Against Property"
]

# ============================================
# DATABASE INIT
# ============================================

def init_database():
    """Initialize all data structures"""
    return {
        'companies': [],
        'leads': [],
        'assignments': [],
        'followups': [],
        'transactions': []
    }

if 'leads_db' not in st.session_state:
    st.session_state.leads_db = init_database()
    
    # Demo companies
    st.session_state.leads_db['companies'] = [
        {'id': 1, 'name': 'HDFC Bank', 'email': 'hdfc@example.com', 'plan': 'enterprise', 'leads_used': 150, 'leads_limit': 10000, 'active': True, 'created': '2026-01-01'},
        {'id': 2, 'name': 'ICICI Bank', 'email': 'icici@example.com', 'plan': 'professional', 'leads_used': 450, 'leads_limit': 2000, 'active': True, 'created': '2026-02-01'},
        {'id': 3, 'name': 'SBI Card', 'email': 'sbi@example.com', 'plan': 'basic', 'leads_used': 120, 'leads_limit': 500, 'active': True, 'created': '2026-03-01'},
    ]
    
    # Demo leads
    st.session_state.leads_db['leads'] = [
        {'id': 1, 'name': 'Rajesh Sharma', 'phone': '9876543210', 'email': 'rajesh@example.com', 'loan_type': 'Home Loan', 'amount': 5000000, 'income': 150000, 'city': 'Mumbai', 'source': 'google_ads', 'score': 85, 'created': '2026-03-27', 'assigned_to': 1, 'status': 'new'},
        {'id': 2, 'name': 'Priya Singh', 'phone': '8765432109', 'email': 'priya@example.com', 'loan_type': 'Personal Loan', 'amount': 500000, 'income': 50000, 'city': 'Delhi', 'source': 'facebook', 'score': 72, 'created': '2026-03-26', 'assigned_to': 2, 'status': 'contacted'},
        {'id': 3, 'name': 'Amit Kumar', 'phone': '7654321098', 'email': 'amit@example.com', 'loan_type': 'Car Loan', 'amount': 1000000, 'income': 80000, 'city': 'Bangalore', 'source': 'website', 'score': 91, 'created': '2026-03-25', 'assigned_to': 1, 'status': 'interested'},
    ]

# ============================================
# AI LEAD SCORING
# ============================================

def calculate_lead_score(loan_amount, monthly_income, city):
    """AI based lead scoring (0-100)"""
    score = 0
    
    # Income to loan ratio (higher income = better score)
    income_ratio = loan_amount / monthly_income if monthly_income > 0 else 0
    if income_ratio <= 30:
        score += 40
    elif income_ratio <= 50:
        score += 30
    elif income_ratio <= 80:
        score += 20
    else:
        score += 10
    
    # City tier scoring
    tier1_cities = ['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Hyderabad', 'Pune', 'Kolkata', 'Ahmedabad']
    tier2_cities = ['Jaipur', 'Lucknow', 'Nagpur', 'Indore', 'Bhopal', 'Surat', 'Vadodara']
    
    if city in tier1_cities:
        score += 30
    elif city in tier2_cities:
        score += 20
    else:
        score += 10
    
    # Loan type scoring
    if loan_amount <= 500000:
        score += 10
    elif loan_amount <= 2000000:
        score += 15
    elif loan_amount <= 5000000:
        score += 20
    else:
        score += 25
    
    return min(score, 100)

# ============================================
# LEAD CAPTURE FORM
# ============================================

def show_lead_capture():
    """Public lead capture form"""
    st.markdown("""
    <style>
        .lead-form {
            max-width: 600px;
            margin: 2rem auto;
            padding: 2rem;
            background: white;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }
        .form-title {
            text-align: center;
            margin-bottom: 2rem;
        }
        .form-title h1 {
            color: #1e3c72;
            font-size: 2rem;
        }
        .form-title p {
            color: #666;
        }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="lead-form">
        <div class="form-title">
            <h1>🎯 Get Best Loan Offers</h1>
            <p>Fill the form and get instant offers from top banks</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("lead_capture_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Full Name *")
            phone = st.text_input("Phone Number *")
            email = st.text_input("Email Address *")
            city = st.text_input("City *")
        
        with col2:
            loan_type = st.selectbox("Loan Type *", LOAN_TYPES)
            loan_amount = st.number_input("Loan Amount Required (₹) *", min_value=10000, value=500000, step=50000)
            monthly_income = st.number_input("Monthly Income (₹) *", min_value=5000, value=50000, step=5000)
            source = st.selectbox("How did you hear about us?", list(LEAD_SOURCES.keys()), format_func=lambda x: LEAD_SOURCES[x])
        
        agree = st.checkbox("I agree to receive offers from partner banks")
        
        submitted = st.form_submit_button("Get Best Offers →", use_container_width=True, type="primary")
        
        if submitted:
            if name and phone and email and city and agree:
                # Calculate AI score
                score = calculate_lead_score(loan_amount, monthly_income, city)
                
                # Find available companies with remaining leads
                available_companies = [c for c in st.session_state.leads_db['companies'] 
                                      if c['active'] and c['leads_used'] < c['leads_limit']]
                
                if available_companies:
                    # Assign to company with least leads used (fair distribution)
                    best_company = min(available_companies, key=lambda x: x['leads_used'])
                    
                    # Create lead
                    lead = {
                        'id': len(st.session_state.leads_db['leads']) + 1,
                        'name': name,
                        'phone': phone,
                        'email': email,
                        'loan_type': loan_type,
                        'amount': loan_amount,
                        'income': monthly_income,
                        'city': city,
                        'source': source,
                        'score': score,
                        'created': str(datetime.date.today()),
                        'assigned_to': best_company['id'],
                        'status': 'new'
                    }
                    st.session_state.leads_db['leads'].append(lead)
                    
                    # Update company leads count
                    for c in st.session_state.leads_db['companies']:
                        if c['id'] == best_company['id']:
                            c['leads_used'] += 1
                    
                    # Create assignment record
                    assignment = {
                        'id': len(st.session_state.leads_db['assignments']) + 1,
                        'lead_id': lead['id'],
                        'company_id': best_company['id'],
                        'assigned_at': str(datetime.datetime.now()),
                        'status': 'new'
                    }
                    st.session_state.leads_db['assignments'].append(assignment)
                    
                    st.success(f"✅ Thank you! Your lead has been shared with {best_company['name']}")
                    st.balloons()
                    st.info("📞 Our partner bank will contact you within 24 hours")
                else:
                    st.error("Sorry! All partner banks have reached their lead limit for today. Please try again tomorrow.")
            else:
                st.error("Please fill all required fields and agree to terms")

# ============================================
# COMPANY DASHBOARD
# ============================================

def show_company_dashboard(company):
    """Dashboard for logged in company"""
    
    # Company leads
    company_leads = [l for l in st.session_state.leads_db['leads'] if l.get('assigned_to') == company['id']]
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); padding: 1.5rem; border-radius: 15px; margin-bottom: 1.5rem;">
        <h1 style="color: white; margin: 0;">🏢 {company['name']}</h1>
        <p style="color: #ccc;">Plan: {PRICING_PLANS[company['plan']]['name']} | Leads Used: {company['leads_used']}/{company['leads_limit']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Leads", len(company_leads))
    with col2:
        new_leads = len([l for l in company_leads if l.get('status') == 'new'])
        st.metric("New Leads", new_leads)
    with col3:
        interested = len([l for l in company_leads if l.get('status') == 'interested'])
        st.metric("Interested", interested)
    with col4:
        avg_score = sum(l.get('score', 0) for l in company_leads) / len(company_leads) if company_leads else 0
        st.metric("Avg Score", f"{avg_score:.0f}")
    
    st.markdown("---")
    
    # Lead table
    st.markdown("### 📋 Your Leads")
    
    if company_leads:
        lead_data = []
        for lead in company_leads:
            lead_data.append({
                'ID': lead['id'],
                'Name': lead['name'],
                'Phone': lead['phone'],
                'Loan Type': lead['loan_type'],
                'Amount': f"₹{lead['amount']:,}",
                'Score': f"{lead['score']}%",
                'Status': lead['status'].upper(),
                'Created': lead['created']
            })
        
        df = pd.DataFrame(lead_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Lead details expander
        with st.expander("🔍 View Lead Details"):
            selected_id = st.selectbox("Select Lead ID", [l['id'] for l in company_leads])
            lead = next((l for l in company_leads if l['id'] == selected_id), None)
            
            if lead:
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**Name:** {lead['name']}")
                    st.markdown(f"**Phone:** {lead['phone']}")
                    st.markdown(f"**Email:** {lead['email']}")
                    st.markdown(f"**City:** {lead['city']}")
                with col2:
                    st.markdown(f"**Loan Type:** {lead['loan_type']}")
                    st.markdown(f"**Amount:** ₹{lead['amount']:,}")
                    st.markdown(f"**Income:** ₹{lead['income']:,}")
                    st.markdown(f"**AI Score:** {lead['score']}%")
                
                st.markdown("### Update Status")
                new_status = st.selectbox("Status", ["new", "contacted", "interested", "not_interested", "converted", "lost"])
                if st.button("Update Status"):
                    for l in st.session_state.leads_db['leads']:
                        if l['id'] == lead['id']:
                            l['status'] = new_status
                            st.success("Status updated!")
                            st.rerun()
    else:
        st.info("No leads assigned yet")

# ============================================
# ADMIN DASHBOARD
# ============================================

def show_admin_dashboard():
    """Admin dashboard (you)"""
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); padding: 1.5rem; border-radius: 15px; margin-bottom: 1.5rem;">
        <h1 style="color: white;">👑 ADMIN DASHBOARD</h1>
        <p style="color: #ccc;">NEXA LEADS Management System</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "🏢 Companies", "🎯 Leads", "💰 Billing"])
    
    with tab1:
        total_leads = len(st.session_state.leads_db['leads'])
        total_companies = len(st.session_state.leads_db['companies'])
        total_revenue = sum(c['leads_used'] * 50 for c in st.session_state.leads_db['companies'])  # Example: ₹50 per lead
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Leads", total_leads)
        with col2:
            st.metric("Active Companies", total_companies)
        with col3:
            st.metric("Estimated Revenue", f"₹{total_revenue:,}")
        
        # Lead source chart
        st.markdown("### Lead Sources")
        source_counts = {}
        for lead in st.session_state.leads_db['leads']:
            src = LEAD_SOURCES.get(lead.get('source', 'website'), lead.get('source', 'Other'))
            source_counts[src] = source_counts.get(src, 0) + 1
        
        if source_counts:
            st.bar_chart(source_counts)
        
        # Loan type distribution
        st.markdown("### Loan Type Distribution")
        loan_counts = {}
        for lead in st.session_state.leads_db['leads']:
            loan = lead.get('loan_type', 'Other')
            loan_counts[loan] = loan_counts.get(loan, 0) + 1
        
        if loan_counts:
            st.bar_chart(loan_counts)
    
    with tab2:
        st.markdown("### Companies")
        
        companies_df = pd.DataFrame(st.session_state.leads_db['companies'])
        st.dataframe(companies_df, use_container_width=True, hide_index=True)
        
        st.markdown("### ➕ Add New Company")
        with st.form("add_company"):
            col1, col2 = st.columns(2)
            with col1:
                company_name = st.text_input("Company Name")
                company_email = st.text_input("Email")
            with col2:
                plan = st.selectbox("Plan", list(PRICING_PLANS.keys()), format_func=lambda x: PRICING_PLANS[x]['name'])
                leads_limit = PRICING_PLANS[plan]['leads_limit']
                st.info(f"Lead Limit: {leads_limit} per month")
            
            if st.form_submit_button("Add Company"):
                new_company = {
                    'id': len(st.session_state.leads_db['companies']) + 1,
                    'name': company_name,
                    'email': company_email,
                    'plan': plan,
                    'leads_used': 0,
                    'leads_limit': leads_limit,
                    'active': True,
                    'created': str(datetime.date.today())
                }
                st.session_state.leads_db['companies'].append(new_company)
                st.success(f"Company {company_name} added!")
                st.rerun()
    
    with tab3:
        st.markdown("### All Leads")
        leads_df = pd.DataFrame(st.session_state.leads_db['leads'])
        if not leads_df.empty:
            st.dataframe(leads_df, use_container_width=True, hide_index=True)
            
            # Export option
            if st.button("📥 Export to CSV"):
                csv = leads_df.to_csv(index=False)
                st.download_button("Download CSV", csv, "nexa_leads.csv", "text/csv")
        else:
            st.info("No leads yet")
    
    with tab4:
        st.markdown("### Billing & Payments")
        
        st.markdown("#### Pricing Plans")
        for plan_id, plan in PRICING_PLANS.items():
            st.markdown(f"""
            <div style="border: 1px solid #ddd; border-radius: 10px; padding: 1rem; margin: 0.5rem 0;">
                <h3>{plan['name']}</h3>
                <p><b>₹{plan['price']}/month</b></p>
                <p>{', '.join(plan['features'])}</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("#### Payment QR")
        st.info(f"UPI: {YOUR_UPI}")
        st.info(f"Phone: {YOUR_PHONE}")

# ============================================
# COMPANY LOGIN
# ============================================

def show_company_login():
    """Company login page"""
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0;">
        <h1>🏢 Company Login</h1>
        <p>Access your lead dashboard</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("login_form"):
        email = st.text_input("Email Address")
        password = st.text_input("Password", type="password")
        
        if st.form_submit_button("Login", use_container_width=True):
            # Simple password check (demo - in production, use proper auth)
            companies = st.session_state.leads_db['companies']
            company = next((c for c in companies if c['email'] == email), None)
            
            if company and email == company['email']:
                st.session_state.logged_in_company = company
                st.rerun()
            else:
                st.error("Invalid credentials. Demo: use company email")

# ============================================
# MAIN APP
# ============================================

# Initialize session state
if 'logged_in_company' not in st.session_state:
    st.session_state.logged_in_company = None

if 'admin_mode' not in st.session_state:
    st.session_state.admin_mode = False

# Sidebar navigation
with st.sidebar:
    st.markdown("### 🎯 NEXA LEADS")
    st.markdown("AI Lead Generation System")
    st.markdown("---")
    
    if st.session_state.logged_in_company:
        st.success(f"Logged in as: {st.session_state.logged_in_company['name']}")
        if st.button("🚪 Logout"):
            st.session_state.logged_in_company = None
            st.rerun()
    else:
        mode = st.radio("Mode", ["🏠 Lead Capture", "🏢 Company Login", "👑 Admin"], label_visibility="collapsed")
    
    st.markdown("---")
    st.markdown(f"""
    <div style="font-size: 0.7rem; text-align: center;">
        <b>NEXA LEADS</b><br>
        © 2026 Enterprise Edition<br>
        Support: 8439049681
    </div>
    """, unsafe_allow_html=True)

# Page routing
if st.session_state.logged_in_company:
    show_company_dashboard(st.session_state.logged_in_company)
elif st.session_state.admin_mode or (not st.session_state.logged_in_company and mode == "👑 Admin"):
    st.session_state.admin_mode = True
    show_admin_dashboard()
elif mode == "🏢 Company Login":
    show_company_login()
else:
    show_lead_capture()
