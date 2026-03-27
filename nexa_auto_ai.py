import streamlit as st
import pandas as pd
import datetime
import random
from datetime import timedelta

st.set_page_config(page_title="NEXA AUTO AI", page_icon="🤖", layout="wide")

# Hide Streamlit UI
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stAppDeployButton {display: none;}
</style>
""", unsafe_allow_html=True)

# Configuration
ADMIN_EMAIL = "Wasu47118@gmail.com"
UPI_ID = "8439049681@pthdfc"
PHONE = "8439049681"

LOAN_CATEGORIES = {
    "personal_loan": "🏦 Personal Loan",
    "home_loan": "🏠 Home Loan", 
    "car_loan": "🚗 Car Loan",
    "business_loan": "💼 Business Loan",
    "credit_card": "💳 Credit Card"
}

PLANS = {
    "free": {"name": "Free Trial", "price": 0, "leads_per_day": 3},
    "starter": {"name": "Starter", "price": 4999, "leads_per_day": 50},
    "professional": {"name": "Professional", "price": 14999, "leads_per_day": 200},
    "enterprise": {"name": "Enterprise", "price": 49999, "leads_per_day": 1000}
}

# Database
if 'companies' not in st.session_state:
    st.session_state.companies = [
        {'id': 1, 'name': 'HDFC Bank', 'plan': 'professional', 'leads_today': 0, 'leads_limit': 200, 'active': True},
        {'id': 2, 'name': 'ICICI Bank', 'plan': 'starter', 'leads_today': 0, 'leads_limit': 50, 'active': True},
        {'id': 3, 'name': 'SBI Card', 'plan': 'free', 'leads_today': 0, 'leads_limit': 3, 'active': True},
    ]

if 'leads' not in st.session_state:
    st.session_state.leads = []
    for i in range(5):
        st.session_state.leads.append({
            'id': i, 'name': f'Lead {i}', 'phone': '9876543210', 'loan_type': 'Personal Loan',
            'amount': 500000, 'score': random.randint(50, 95), 'city': 'Mumbai',
            'assigned_to': None, 'time': datetime.datetime.now().strftime('%H:%M:%S')
        })

# ============================================
# SIDEBAR
# ============================================

with st.sidebar:
    st.markdown("### 🤖 NEXA AUTO AI")
    st.markdown("---")
    
    # Simple radio - CLEARLY VISIBLE
    st.markdown("### 🔑 ACCESS MODE")
    mode = st.radio("", ["👤 CLIENT DASHBOARD", "👑 ADMIN DASHBOARD"], index=0)
    
    st.markdown("---")
    
    if mode == "👤 CLIENT DASHBOARD":
        company_names = [c['name'] for c in st.session_state.companies]
        selected_company = st.selectbox("Select Company", company_names)
        current_company = next(c for c in st.session_state.companies if c['name'] == selected_company)
        
        st.markdown(f"""
        **{current_company['name']}**  
        Plan: {PLANS[current_company['plan']]['name']}  
        Leads: {current_company['leads_today']}/{current_company['leads_limit']}  
        Status: {'🟢 Active' if current_company['active'] else '🔴 Inactive'}
        """)
        
        if current_company['plan'] == 'free':
            st.markdown("---")
            st.markdown("### 💰 Upgrade")
            if st.button("📊 Starter - ₹4,999/month"):
                st.info(f"Pay to UPI: {UPI_ID}")
    else:
        st.markdown("### 👑 ADMIN")
        st.markdown(f"📧 {ADMIN_EMAIL}")
        st.markdown(f"💳 {UPI_ID}")
        st.markdown(f"📞 {PHONE}")

# ============================================
# MAIN CONTENT
# ============================================

if mode == "👤 CLIENT DASHBOARD":
    st.markdown("### 🤖 Your Leads")
    company_leads = [l for l in st.session_state.leads if l.get('assigned_to') == current_company['name']]
    
    if company_leads:
        for lead in company_leads[:PLANS[current_company['plan']]['leads_per_day']]:
            st.markdown(f"""
            **{lead['name']}** | {lead['loan_type']} | ₹{lead['amount']:,} | Score: {lead['score']}%
            """)
    else:
        st.info("No leads assigned yet")

else:
    st.markdown("### 👑 ADMIN DASHBOARD")
    
    tab1, tab2, tab3 = st.tabs(["📊 Companies", "🎯 Leads", "📈 Stats"])
    
    with tab1:
        st.markdown("### Companies")
        for c in st.session_state.companies:
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.markdown(f"**{c['name']}** - {PLANS[c['plan']]['name']}")
            with col2:
                st.markdown(f"Leads: {c['leads_today']}/{c['leads_limit']}")
            with col3:
                if st.button(f"{'⏸️ Stop' if c['active'] else '▶️ Start'}", key=f"btn_{c['id']}"):
                    c['active'] = not c['active']
                    st.rerun()
        
        with st.expander("➕ Add Company"):
            new_name = st.text_input("Company Name")
            new_plan = st.selectbox("Plan", list(PLANS.keys()), format_func=lambda x: PLANS[x]['name'])
            if st.button("Add"):
                st.session_state.companies.append({
                    'id': len(st.session_state.companies)+1,
                    'name': new_name,
                    'plan': new_plan,
                    'leads_today': 0,
                    'leads_limit': PLANS[new_plan]['leads_per_day'],
                    'active': True
                })
                st.rerun()
    
    with tab2:
        st.markdown("### All Leads")
        df = pd.DataFrame(st.session_state.leads)
        st.dataframe(df[['name', 'loan_type', 'amount', 'score', 'city']], use_container_width=True)
    
    with tab3:
        total = len(st.session_state.leads)
        assigned = len([l for l in st.session_state.leads if l.get('assigned_to')])
        st.metric("Total Leads", total)
        st.metric("Assigned", assigned)
