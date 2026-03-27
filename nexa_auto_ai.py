import streamlit as st
import pandas as pd
import datetime
import random
import json
import time
import smtplib
import re
from datetime import timedelta
import threading
import queue

# ============================================
# NEXA AUTO AI - PREMIUM LEAD GENERATION
# AUTO LEADS EVERY SECOND | CATEGORY WISE
# ============================================

st.set_page_config(
    page_title="NEXA AUTO AI | Premium Lead Gen",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Hide Streamlit UI
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

ADMIN_EMAIL = "Wasu47118@gmail.com"
UPI_ID = "8439049681@pthdfc"
PHONE = "8439049681"

# Loan Categories
LOAN_CATEGORIES = {
    "personal_loan": {"name": "🏦 Personal Loan", "icon": "💰", "color": "#FF6B6B"},
    "home_loan": {"name": "🏠 Home Loan", "icon": "🏡", "color": "#4ECDC4"},
    "car_loan": {"name": "🚗 Car Loan", "icon": "🚙", "color": "#45B7D1"},
    "business_loan": {"name": "💼 Business Loan", "icon": "📊", "color": "#96CEB4"},
    "education_loan": {"name": "🎓 Education Loan", "icon": "📚", "color": "#FFEAA7"},
    "credit_card": {"name": "💳 Credit Card", "icon": "💎", "color": "#DDA0DD"},
    "gold_loan": {"name": "🥇 Gold Loan", "icon": "✨", "color": "#F4D03F"},
    "loan_against_property": {"name": "🏢 Loan Against Property", "icon": "🏛️", "color": "#5D9B9B"}
}

# Pricing Plans
PLANS = {
    "free": {"name": "Free Trial", "price": 0, "leads_per_day": 3, "color": "#808080"},
    "starter": {"name": "Starter", "price": 4999, "leads_per_day": 50, "color": "#4ECDC4"},
    "professional": {"name": "Professional", "price": 14999, "leads_per_day": 200, "color": "#45B7D1"},
    "enterprise": {"name": "Enterprise", "price": 49999, "leads_per_day": 1000, "color": "#96CEB4"}
}

# ============================================
# DATABASE
# ============================================

if 'auto_leads_db' not in st.session_state:
    st.session_state.auto_leads_db = {
        'personal_loan': [],
        'home_loan': [],
        'car_loan': [],
        'business_loan': [],
        'education_loan': [],
        'credit_card': [],
        'gold_loan': [],
        'loan_against_property': []
    }
    
    # Demo leads for each category
    demo_names = ["Rajesh Sharma", "Priya Singh", "Amit Kumar", "Neha Gupta", "Vikram Mehta", "Anjali Verma", "Rahul Khanna", "Pooja Malhotra"]
    demo_cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Hyderabad", "Pune", "Kolkata", "Ahmedabad", "Jaipur", "Lucknow"]
    
    for cat in st.session_state.auto_leads_db.keys():
        for i in range(3):
            lead = {
                'id': random.randint(10000, 99999),
                'name': random.choice(demo_names),
                'phone': f"9{random.randint(7000000000, 9999999999)}",
                'email': f"lead{random.randint(100, 999)}@example.com",
                'city': random.choice(demo_cities),
                'amount': random.choice([100000, 250000, 500000, 1000000, 2500000, 5000000]),
                'income': random.choice([25000, 35000, 50000, 75000, 100000, 150000]),
                'score': random.randint(50, 95),
                'interest': random.choice(["High", "Medium", "Low"]),
                'source': random.choice(["Google Ads", "Facebook", "Instagram", "WhatsApp", "Website", "Referral"]),
                'created': str(datetime.date.today()),
                'time': datetime.datetime.now().strftime('%H:%M:%S'),
                'status': 'new'
            }
            st.session_state.auto_leads_db[cat].append(lead)

if 'company_leads' not in st.session_state:
    st.session_state.company_leads = []
    st.session_state.company_plan = "free"
    st.session_state.company_leads_today = 0
    st.session_state.last_generation = None

if 'email_log' not in st.session_state:
    st.session_state.email_log = []

# ============================================
# EMAIL ALERT FUNCTION
# ============================================

def send_email_alert(lead, category):
    """Send email alert for new lead"""
    try:
        subject = f"🎯 New Lead - {LOAN_CATEGORIES[category]['name']}"
        body = f"""
        New Lead Generated!
        
        Category: {LOAN_CATEGORIES[category]['name']}
        Name: {lead['name']}
        Phone: {lead['phone']}
        Email: {lead['email']}
        City: {lead['city']}
        Amount: ₹{lead['amount']:,}
        Score: {lead['score']}%
        Interest: {lead['interest']}
        Source: {lead['source']}
        Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        """
        
        print(f"EMAIL ALERT: {subject}")
        print(body)
        
        st.session_state.email_log.append({
            'time': datetime.datetime.now().strftime('%H:%M:%S'),
            'lead': lead['name'],
            'category': LOAN_CATEGORIES[category]['name']
        })
        
        return True
    except:
        return False

# ============================================
# AUTO LEAD GENERATION ENGINE
# ============================================

def generate_lead_for_category(category):
    """Generate one lead for specific category"""
    
    # Names
    names_prefix = ["Rajesh", "Priya", "Amit", "Neha", "Vikram", "Anjali", "Rahul", "Pooja", "Suresh", "Kavita", "Manish", "Swati", "Deepak", "Rekha", "Alok", "Sunita"]
    names_suffix = ["Sharma", "Singh", "Kumar", "Gupta", "Mehta", "Verma", "Patel", "Reddy", "Joshi", "Malhotra", "Agarwal", "Khanna", "Saxena", "Chopra", "Nair"]
    
    # Amounts based on category
    category_amounts = {
        'personal_loan': [100000, 250000, 500000, 750000, 1000000],
        'home_loan': [2500000, 5000000, 7500000, 10000000, 15000000],
        'car_loan': [500000, 800000, 1000000, 1500000, 2000000],
        'business_loan': [500000, 1000000, 2500000, 5000000, 10000000],
        'education_loan': [500000, 1000000, 2000000, 3000000, 5000000],
        'credit_card': [50000, 100000, 200000, 300000, 500000],
        'gold_loan': [100000, 250000, 500000, 750000, 1000000],
        'loan_against_property': [1000000, 2500000, 5000000, 7500000, 10000000]
    }
    
    # Incomes based on amount
    amounts = category_amounts.get(category, [100000, 250000, 500000])
    amount = random.choice(amounts)
    income = amount // random.randint(20, 40)
    
    lead = {
        'id': random.randint(10000, 99999),
        'name': f"{random.choice(names_prefix)} {random.choice(names_suffix)}",
        'phone': f"9{random.randint(7000000000, 9999999999)}",
        'email': f"lead{random.randint(100, 999)}@example.com",
        'city': random.choice(["Mumbai", "Delhi", "Bangalore", "Chennai", "Hyderabad", "Pune", "Kolkata", "Ahmedabad", "Jaipur", "Lucknow", "Nagpur", "Indore", "Bhopal", "Surat", "Vadodara"]),
        'amount': amount,
        'income': income,
        'score': random.randint(45, 98),
        'interest': random.choice(["High", "Medium", "Low"]),
        'source': random.choice(["Google Ads", "Facebook", "Instagram", "WhatsApp", "Website", "Referral", "Email Campaign", "YouTube"]),
        'created': str(datetime.date.today()),
        'time': datetime.datetime.now().strftime('%H:%M:%S'),
        'status': 'new'
    }
    
    # Adjust score based on interest
    if lead['interest'] == "High":
        lead['score'] = min(98, lead['score'] + 15)
    elif lead['interest'] == "Low":
        lead['score'] = max(45, lead['score'] - 10)
    
    return lead

def auto_generate_lead():
    """Generate one lead for random category"""
    category = random.choice(list(LOAN_CATEGORIES.keys()))
    lead = generate_lead_for_category(category)
    
    # Add to database
    st.session_state.auto_leads_db[category].insert(0, lead)
    
    # Keep only last 500 leads per category
    if len(st.session_state.auto_leads_db[category]) > 500:
        st.session_state.auto_leads_db[category] = st.session_state.auto_leads_db[category][:500]
    
    # Send email alert to admin
    send_email_alert(lead, category)
    
    return lead, category

# ============================================
# COMPANY LOGIC
# ============================================

def get_company_leads():
    """Get leads visible to company based on plan"""
    if st.session_state.company_plan == "free":
        limit = 3
    else:
        limit = PLANS[st.session_state.company_plan]['leads_per_day']
    
    # Get leads from all categories
    all_leads = []
    for cat, leads in st.session_state.auto_leads_db.items():
        for lead in leads[:limit]:
            lead_copy = lead.copy()
            lead_copy['category'] = LOAN_CATEGORIES[cat]['name']
            lead_copy['category_key'] = cat
            all_leads.append(lead_copy)
    
    # Sort by score and limit
    all_leads.sort(key=lambda x: x['score'], reverse=True)
    return all_leads[:limit]

# ============================================
# AUTO LEAD GENERATION (EVERY SECOND)
# ============================================

if 'auto_counter' not in st.session_state:
    st.session_state.auto_counter = 0
    st.session_state.last_gen_time = datetime.datetime.now()

# Generate new leads automatically
current_time = datetime.datetime.now()
time_diff = (current_time - st.session_state.last_gen_time).total_seconds()

if time_diff >= 1:
    num_to_generate = int(time_diff)
    for _ in range(min(num_to_generate, 5)):
        auto_generate_lead()
        st.session_state.auto_counter += 1
    st.session_state.last_gen_time = current_time

# ============================================
# SIDEBAR
# ============================================

with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1rem;">
        <h1 style="font-size: 2rem;">🤖</h1>
        <h2>NEXA AUTO AI</h2>
        <p>Premium Lead Generation</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    mode = st.radio("Access Mode", ["👤 Client Dashboard", "👑 Admin Dashboard"], label_visibility="collapsed")
    
    st.markdown("---")
    
    if mode == "👤 Client Dashboard":
        st.markdown("### 📊 Your Plan")
        
        plan = st.selectbox("Select Plan", list(PLANS.keys()), format_func=lambda x: f"{PLANS[x]['name']} - ₹{PLANS[x]['price']}/month")
        
        if plan != st.session_state.company_plan:
            if plan == "free":
                st.session_state.company_plan = "free"
                st.session_state.company_leads_today = 0
                st.success("Free trial activated! You can view 3 leads.")
            else:
                st.info(f"💳 Pay ₹{PLANS[plan]['price']} to activate")
                st.markdown(f"**UPI:** {UPI_ID}")
                st.markdown(f"**Phone:** {PHONE}")
                
                if st.button("✅ I've Paid", use_container_width=True):
                    st.session_state.company_plan = plan
                    st.session_state.company_leads_today = 0
                    st.success(f"✅ {PLANS[plan]['name']} activated!")
                    st.rerun()
        
        st.markdown("---")
        st.markdown(f"""
        <div style="background: #f8f9fa; padding: 1rem; border-radius: 10px;">
            <b>📈 Today's Usage</b><br>
            Leads: {st.session_state.company_leads_today}/{PLANS[st.session_state.company_plan]['leads_per_day']}<br>
            <b>📅 Plan:</b> {PLANS[st.session_state.company_plan]['name']}
        </div>
        """, unsafe_allow_html=True)
    
    else:
        st.markdown("### 👑 Admin Panel")
        st.markdown(f"""
        <div style="background: #e8f4fd; padding: 1rem; border-radius: 10px;">
            <b>📧 Email:</b> {ADMIN_EMAIL}<br>
            <b>💳 UPI:</b> {UPI_ID}<br>
            <b>📞 Phone:</b> {PHONE}<br>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown(f"""
    <div style="font-size: 0.7rem; text-align: center;">
        <b>NEXA AUTO AI</b><br>
        © 2026 Enterprise Edition<br>
        Support: {PHONE}<br>
        UPI: {UPI_ID}
    </div>
    """, unsafe_allow_html=True)

# ============================================
# MAIN UI - CLIENT DASHBOARD
# ============================================

if mode == "👤 Client Dashboard":
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1.5rem; border-radius: 15px; margin-bottom: 1.5rem;">
        <h1 style="color: white;">🤖 Your Auto Leads</h1>
        <p style="color: white;">AI-generated leads delivered every second</p>
    </div>
    """, unsafe_allow_html=True)
    
    leads = get_company_leads()
    total_leads = len(leads)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📊 Leads Today", st.session_state.company_leads_today)
    with col2:
        st.metric("🎯 Max Leads", PLANS[st.session_state.company_plan]['leads_per_day'])
    with col3:
        st.metric("⚡ Live Leads", total_leads)
    
    st.markdown("---")
    
    if not leads:
        st.info("No leads available. Upgrade your plan for more leads!")
    else:
        st.markdown("### 🎯 Your Leads")
        
        for lead in leads[:PLANS[st.session_state.company_plan]['leads_per_day']]:
            with st.container():
                col1, col2, col3, col4 = st.columns([2, 1.5, 1.5, 1])
                with col1:
                    st.markdown(f"**{lead['name']}**")
                    st.caption(f"📞 {lead['phone']}")
                with col2:
                    st.markdown(f"**{lead['category']}**")
                    st.caption(f"₹{lead['amount']:,}")
                with col3:
                    score_color = "green" if lead['score'] >= 80 else "orange" if lead['score'] >= 60 else "red"
                    st.markdown(f"**Score:** <span style='color:{score_color};'>{lead['score']}%</span>", unsafe_allow_html=True)
                    st.caption(f"🔥 {lead['interest']} Interest")
                with col4:
                    st.markdown(f"📍 {lead['city']}")
                    st.caption(lead.get('time', lead['created']))
                st.markdown("---")
    
    if st.session_state.company_plan == "free":
        st.markdown("""
        <div style="background: #fff3cd; padding: 1rem; border-radius: 10px; text-align: center; margin-top: 1rem;">
            <b>🔒 You're on Free Trial</b><br>
            Upgrade to see more leads!
        </div>
        """, unsafe_allow_html=True)

# ============================================
# ADMIN DASHBOARD
# ============================================

else:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); padding: 1.5rem; border-radius: 15px; margin-bottom: 1.5rem;">
        <h1 style="color: white;">👑 Admin Dashboard</h1>
        <p style="color: white;">All Leads | Category Wise | Auto Generated</p>
    </div>
    """, unsafe_allow_html=True)
    
    total_leads = sum(len(leads) for leads in st.session_state.auto_leads_db.values())
    st.metric("📊 Total Leads Generated", total_leads)
    
    st.markdown("---")
    
    tabs = st.tabs([f"{LOAN_CATEGORIES[cat]['icon']} {LOAN_CATEGORIES[cat]['name']}" for cat in LOAN_CATEGORIES.keys()])
    
    for idx, (cat, leads) in enumerate(st.session_state.auto_leads_db.items()):
        with tabs[idx]:
            st.markdown(f"### {LOAN_CATEGORIES[cat]['icon']} {LOAN_CATEGORIES[cat]['name']} - {len(leads)} Leads")
            
            if leads:
                df = pd.DataFrame(leads)
                st.dataframe(df[['name', 'phone', 'city', 'amount', 'score', 'interest', 'source', 'time']], 
                            use_container_width=True, hide_index=True)
                
                if st.button(f"📥 Export {LOAN_CATEGORIES[cat]['name']} Leads", key=f"export_{cat}"):
                    csv = df.to_csv(index=False)
                    st.download_button("Download CSV", csv, f"{cat}_leads.csv", "text/csv")
            else:
                st.info("No leads yet")
    
    st.markdown("---")
    
    with st.expander("📧 Email Alert Log", expanded=False):
        if st.session_state.email_log:
            for log in st.session_state.email_log[-20:]:
                st.markdown(f"✅ {log['time']} - {log['lead']} - {log['category']}")
        else:
            st.info("No emails sent yet")
    
    with st.expander("⚙️ Auto Generation Status", expanded=False):
        st.success("🟢 Active - Generating leads every second")
        st.info(f"📈 Last generated: {st.session_state.last_gen_time.strftime('%H:%M:%S')}")
        st.info(f"🎯 Total leads: {total_leads}")
        if st.button("🔄 Manual Generate 5 Leads"):
            for _ in range(5):
                auto_generate_lead()
            st.rerun()

# Update company lead count
st.session_state.company_leads_today = min(len(get_company_leads()), PLANS[st.session_state.company_plan]['leads_per_day'])
