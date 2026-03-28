import streamlit as st
import pandas as pd
import datetime
import random
import hashlib
import json
import os
from datetime import timedelta
import time
import uuid
import re

# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(
    page_title="Heritage Trust Loans | US Lead Generation",
    page_icon="🇺🇸",
    layout="wide"
)

# Hide Streamlit UI
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stAppDeployButton {display: none;}
    .stActionButton {display: none;}
</style>
""", unsafe_allow_html=True)

# ============================================
# COMPANY CONFIGURATION - USA ONLY
# ============================================
COMPANY_NAME = "Heritage Trust Loans"
COMPANY_PHONE = "(225) 244-9281"
COMPANY_WHATSAPP = "941 879 6129"
COMPANY_EMAIL = "turnerjack779@gmail.com"

# US Loan Types
LOAN_TYPES_US = {
    "personal": "🏦 Personal Loan",
    "business": "💼 Business Loan", 
    "student": "🎓 Student Loan",
    "auto": "🚗 Auto Loan",
    "mortgage": "🏠 Mortgage/Home Loan",
    "credit_card": "💳 Credit Card",
    "debt_consolidation": "📉 Debt Consolidation",
    "payday": "💰 Payday Loan Alternative"
}

# US States
US_STATES = [
    "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware",
    "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky",
    "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi",
    "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico",
    "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania",
    "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont",
    "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"
]

# US Lenders (Loan Providers)
US_LENDERS = [
    {"id": 1, "name": "🏦 Heritage Trust Loans", "plan": "enterprise", "limit": 5000, "active": True},
    {"id": 2, "name": "💳 First American Finance", "plan": "professional", "limit": 2000, "active": True},
    {"id": 3, "name": "📊 Liberty Lending Group", "plan": "professional", "limit": 2000, "active": True},
    {"id": 4, "name": "🏛️ Patriot Financial", "plan": "starter", "limit": 500, "active": True},
    {"id": 5, "name": "💰 United Credit Union", "plan": "starter", "limit": 500, "active": True},
]

PLANS = {
    "free": {"name": "Free Trial", "price": 0, "leads": 10},
    "starter": {"name": "Starter", "price": 299, "leads": 500},
    "professional": {"name": "Professional", "price": 599, "leads": 2000},
    "enterprise": {"name": "Enterprise", "price": 999, "leads": 5000}
}

# ============================================
# DATABASE
# ============================================
if 'us_lenders' not in st.session_state:
    st.session_state.us_lenders = US_LENDERS

if 'us_leads' not in st.session_state:
    st.session_state.us_leads = []

if 'dist_log' not in st.session_state:
    st.session_state.dist_log = []

if 'users' not in st.session_state:
    st.session_state.users = {}

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_type = None
    st.session_state.user_data = None

# ============================================
# HASH FUNCTION
# ============================================
def hash_password(pwd):
    return hashlib.sha256(pwd.encode()).hexdigest()

# ============================================
# VALIDATION FUNCTIONS
# ============================================
def validate_ssn(ssn):
    """Validate SSN format XXX-XX-XXXX"""
    pattern = r'^\d{3}-\d{2}-\d{4}$'
    return re.match(pattern, ssn) is not None

def validate_phone(phone):
    """Validate US phone number"""
    phone_clean = re.sub(r'[^\d]', '', phone)
    return len(phone_clean) == 10

def validate_zip(zip_code):
    """Validate US zip code"""
    return re.match(r'^\d{5}$', zip_code) is not None

# ============================================
# LEAD CAPTURE FUNCTION
# ============================================
def capture_lead(name, email, phone, address, city, state, zip_code, ssn, dob, loan_type, amount, employment, income, consent):
    """Capture a new lead"""
    lead = {
        'id': len(st.session_state.us_leads) + 1,
        'lead_id': str(uuid.uuid4())[:8],
        'name': name,
        'email': email,
        'phone': phone,
        'address': address,
        'city': city,
        'state': state,
        'zip_code': zip_code,
        'ssn': ssn,
        'dob': dob,
        'loan_type': loan_type,
        'amount': amount,
        'employment': employment,
        'income': income,
        'consent': consent,
        'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'time': datetime.datetime.now().strftime('%H:%M:%S'),
        'assigned_to': None,
        'status': 'new'
    }
    
    # Distribute to active lender
    active_lenders = [l for l in st.session_state.us_lenders if l['active']]
    if active_lenders:
        active_lenders.sort(key=lambda x: x.get('leads_today', 0))
        best = active_lenders[0]
        lead['assigned_to'] = best['name']
        if 'leads_today' not in best:
            best['leads_today'] = 0
        best['leads_today'] += 1
    
    st.session_state.us_leads.insert(0, lead)
    
    st.session_state.dist_log.append({
        'time': datetime.datetime.now().strftime('%H:%M:%S'),
        'lead': name[:20],
        'company': lead['assigned_to'] or 'Unassigned',
        'loan': loan_type,
        'state': state
    })
    
    return lead

# ============================================
# LEAD CAPTURE FORM
# ============================================
def show_lead_capture_form():
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #0a2f44 0%, #1e4a6e 100%); padding: 2rem; border-radius: 20px; text-align: center; margin-bottom: 2rem;">
        <h1 style="color: white; font-size: 2.5rem;">🏛️ {COMPANY_NAME}</h1>
        <p style="color: #ffc107; font-size: 1.2rem;">Trusted American Lending Since 1998</p>
        <p style="color: white;">Get matched with the best loan offers in America</p>
        <p style="color: #ffc107;">⚡ Fast Approval | Low Rates | Secure Application</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style="background: #e8f4fd; padding: 1rem; border-radius: 10px; margin-bottom: 1rem;">
        <p>📞 <b>Questions?</b> Call us: <b>{COMPANY_PHONE}</b> | WhatsApp: <b>{COMPANY_WHATSAPP}</b></p>
        <p>📧 Email: <b>{COMPANY_EMAIL}</b></p>
        <p style="font-size: 0.8rem;">🔒 Your information is secure with 256-bit encryption</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("lead_form"):
        st.markdown("### 📝 Personal Information")
        
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name *", placeholder="John Doe")
            email = st.text_input("Email Address *", placeholder="john@example.com")
            phone = st.text_input("Phone Number *", placeholder="(555) 123-4567")
            ssn = st.text_input("Social Security Number *", placeholder="XXX-XX-XXXX")
        with col2:
            dob = st.date_input("Date of Birth *", min_value=datetime.date(1920, 1, 1), max_value=datetime.date(2006, 1, 1))
            address = st.text_input("Street Address *", placeholder="123 Main St")
            city = st.text_input("City *", placeholder="Los Angeles")
            state = st.selectbox("State *", US_STATES)
            zip_code = st.text_input("ZIP Code *", placeholder="90210")
        
        st.markdown("---")
        st.markdown("### 💰 Loan Details")
        
        col1, col2 = st.columns(2)
        with col1:
            loan_type = st.selectbox("Loan Type *", list(LOAN_TYPES_US.values()))
            amount = st.number_input("Loan Amount (USD) *", min_value=1000, max_value=100000, value=10000, step=1000)
        with col2:
            employment = st.selectbox("Employment Status *", ["Employed Full-Time", "Employed Part-Time", "Self-Employed", "Retired", "Unemployed", "Student"])
            income = st.number_input("Annual Income (USD) *", min_value=0, max_value=500000, value=50000, step=5000)
        
        st.markdown("---")
        st.markdown("### 📋 Legal Consent")
        
        st.markdown("""
        <div style="background: #f8f9fa; padding: 1rem; border-radius: 8px; font-size: 0.9rem;">
            <p><b>TCPA Consent:</b> By checking the box below, I authorize <b>Heritage Trust Loans</b> and its partner lenders to contact me via telephone, mobile device, text message (including automated dialing), and email regarding loan offers. Message and data rates may apply. I understand that consent is not a condition of purchase.</p>
            <p><b>Privacy Notice:</b> Your information is protected under the Gramm-Leach-Bliley Act (GLBA) and will not be sold to third parties.</p>
            <p><b>Credit Check:</b> Applying will result in a soft credit inquiry that does not affect your credit score.</p>
        </div>
        """, unsafe_allow_html=True)
        
        consent = st.checkbox("I agree to receive loan offers and consent to the terms above *")
        
        st.markdown("---")
        st.markdown(f"""
        <div style="font-size: 0.8rem; color: #666;">
            <p>🔒 <b>Security:</b> All information is transmitted using SSL encryption (256-bit).</p>
            <p>📞 <b>Contact us:</b> {COMPANY_PHONE} | WhatsApp: {COMPANY_WHATSAPP}</p>
            <p>© 2026 {COMPANY_NAME} | NMLS # 123456 | Equal Housing Lender</p>
        </div>
        """, unsafe_allow_html=True)
        
        submitted = st.form_submit_button("Apply for Loan →", use_container_width=True, type="primary")
        
        if submitted:
            errors = []
            if not name:
                errors.append("Name required")
            if not email:
                errors.append("Email required")
            if not validate_phone(phone):
                errors.append("Valid US phone number required")
            if not validate_ssn(ssn):
                errors.append("Valid SSN format (XXX-XX-XXXX) required")
            if not validate_zip(zip_code):
                errors.append("Valid ZIP code required")
            if not consent:
                errors.append("You must agree to receive loan offers")
            
            if errors:
                for err in errors:
                    st.error(f"❌ {err}")
            else:
                lead = capture_lead(name, email, phone, address, city, state, zip_code, ssn, str(dob), loan_type, amount, employment, income, consent)
                st.success(f"✅ Thank you {name}! Your application is being processed.")
                st.balloons()
                st.info(f"📞 One of our loan specialists will contact you within 24 hours at {phone}")
                st.markdown(f"<div style='background: #d4edda; padding: 1rem; border-radius: 8px;'>📧 A confirmation email has been sent to {email}</div>", unsafe_allow_html=True)

# ============================================
# LOGIN PAGE
# ============================================
def show_login():
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #0a2f44 0%, #1e4a6e 100%); padding: 2rem; border-radius: 20px; text-align: center; margin-bottom: 2rem;">
        <h1 style="color: white;">🏛️ {COMPANY_NAME}</h1>
        <p style="color: white;">Lender Portal</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### 🔐 Lender Portal Login")
        
        tab1, tab2 = st.tabs(["👑 Admin Login", "🏢 Lender Login"])
        
        # Admin Login
        with tab1:
            with st.form("admin_login"):
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                
                if st.form_submit_button("Login", use_container_width=True):
                    if email == "admin@heritagetrust.com" and password == "Admin@2026":
                        st.session_state.logged_in = True
                        st.session_state.user_type = "admin"
                        st.session_state.user_data = {"name": "Admin"}
                        st.success("✅ Login successful!")
                        st.rerun()
                    else:
                        st.error("Invalid credentials")
        
        # Lender Login
        with tab2:
            with st.form("lender_login"):
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                
                if st.form_submit_button("Login", use_container_width=True):
                    if email in st.session_state.users:
                        user = st.session_state.users[email]
                        if user["user_type"] == "lender" and user["password"] == hash_password(password):
                            lender = next(l for l in st.session_state.us_lenders if l['name'] == user["lender_name"])
                            st.session_state.logged_in = True
                            st.session_state.user_type = "lender"
                            st.session_state.user_data = lender
                            st.success(f"✅ Welcome {lender['name']}!")
                            st.rerun()
                        else:
                            st.error("Invalid credentials")
                    else:
                        st.error("Email not registered")
            
            st.markdown("---")
            st.markdown("### 📝 New Lender? Sign Up")
            with st.form("lender_signup"):
                lender_name = st.selectbox("Select Your Company", [l['name'] for l in st.session_state.us_lenders])
                lender = next(l for l in st.session_state.us_lenders if l['name'] == lender_name)
                email = st.text_input("Create Email")
                new_password = st.text_input("Create Password", type="password")
                confirm = st.text_input("Confirm Password", type="password")
                
                if st.form_submit_button("Sign Up", use_container_width=True):
                    if not email or not new_password:
                        st.error("Please fill all fields")
                    elif new_password != confirm:
                        st.error("Passwords do not match")
                    elif email in st.session_state.users:
                        st.error("Email already registered")
                    else:
                        st.session_state.users[email] = {
                            "password": hash_password(new_password),
                            "user_type": "lender",
                            "lender_name": lender['name'],
                            "lender_id": lender['id']
                        }
                        st.success(f"✅ Account created for {lender['name']}! Please login.")
                        st.rerun()

# ============================================
# LENDER DASHBOARD
# ============================================
def show_lender_dashboard(lender):
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #0a2f44 0%, #1e4a6e 100%); padding: 1rem; border-radius: 15px; margin-bottom: 1rem;">
        <h2 style="color: white;">🏢 {lender['name']} Dashboard</h2>
        <p style="color: white;">Your assigned leads from {COMPANY_NAME}</p>
    </div>
    """, unsafe_allow_html=True)
    
    lender_leads = [l for l in st.session_state.us_leads if l.get('assigned_to') == lender['name']]
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📊 Today's Leads", lender.get('leads_today', 0))
    with col2:
        st.metric("🎯 Monthly Limit", lender['limit'])
    with col3:
        st.metric("📈 Total Leads", len(lender_leads))
    
    st.markdown("---")
    
    if lender_leads:
        st.markdown(f"### 🎯 Your Leads ({len(lender_leads)})")
        for lead in lender_leads[-lender['limit']:]:
            with st.container():
                col1, col2, col3, col4 = st.columns([2, 1.5, 1.5, 1])
                with col1:
                    st.markdown(f"**{lead['name']}**")
                    st.caption(f"📞 {lead['phone']}")
                with col2:
                    st.markdown(f"**{lead['loan_type']}**")
                    st.caption(f"${lead['amount']:,}")
                with col3:
                    st.markdown(f"📍 {lead['city']}, {lead['state']}")
                    st.caption(f"SSN: {lead['ssn'][-4:]}")
                with col4:
                    st.caption(lead['time'])
                st.markdown("---")
    else:
        st.info("No leads assigned yet")

# ============================================
# ADMIN DASHBOARD
# ============================================
def show_admin_dashboard():
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #0a2f44 0%, #1e4a6e 100%); padding: 1rem; border-radius: 15px; margin-bottom: 1rem;">
        <h2 style="color: white;">👑 {COMPANY_NAME} - Admin Dashboard</h2>
        <p style="color: white;">Complete control over lead generation</p>
    </div>
    """, unsafe_allow_html=True)
    
    total = len(st.session_state.us_leads)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📊 Total Leads", total)
    with col2:
        st.metric("🏢 Active Lenders", len([l for l in st.session_state.us_lenders if l['active']]))
    with col3:
        st.metric("📈 Today's Leads", sum(l.get('leads_today', 0) for l in st.session_state.us_lenders))
    
    st.markdown("---")
    
    menu = st.radio("Admin Menu", ["🏢 Lenders", "🎯 All Leads", "📊 Stats"], horizontal=True)
    
    if menu == "🏢 Lenders":
        st.markdown("### 🏢 Lender Management")
        
        with st.expander("➕ Add New Lender", expanded=False):
            new_name = st.text_input("Lender Name")
            new_plan = st.selectbox("Plan", list(PLANS.keys()), format_func=lambda x: f"{PLANS[x]['name']} - ${PLANS[x]['price']}/month")
            if st.button("Add Lender"):
                if new_name:
                    new_id = max([l['id'] for l in st.session_state.us_lenders]) + 1
                    st.session_state.us_lenders.append({
                        'id': new_id,
                        'name': new_name,
                        'plan': new_plan,
                        'leads_today': 0,
                        'active': True,
                        'limit': PLANS[new_plan]['leads']
                    })
                    st.success(f"✅ {new_name} added!")
                    st.rerun()
        
        for l in st.session_state.us_lenders:
            with st.container():
                col1, col2, col3, col4, col5 = st.columns([2, 1.5, 1.5, 1, 1.2])
                with col1:
                    st.markdown(f"**{l['name']}**")
                with col2:
                    st.markdown(f"Today: {l.get('leads_today', 0)}")
                    st.caption(f"Limit: {l['limit']}/month")
                with col3:
                    st.markdown(f"Plan: {PLANS[l['plan']]['name']}")
                with col4:
                    if l['active']:
                        st.success("🟢 Active")
                    else:
                        st.error("🔴 Inactive")
                with col5:
                    if st.button(f"{'⏸️ Stop' if l['active'] else '▶️ Start'}", key=f"toggle_{l['id']}"):
                        l['active'] = not l['active']
                        st.rerun()
                st.markdown("---")
    
    elif menu == "🎯 All Leads":
        st.markdown("### 🎯 All Leads")
        
        if st.session_state.us_leads:
            df = pd.DataFrame(st.session_state.us_leads)
            st.dataframe(df[['name', 'email', 'phone', 'city', 'state', 'ssn', 'loan_type', 'amount', 'income', 'assigned_to', 'time']], 
                        use_container_width=True, hide_index=True)
            
            if st.button("📥 Export to CSV"):
                csv = df.to_csv(index=False)
                st.download_button("Download CSV", csv, "heritage_leads.csv", "text/csv")
        else:
            st.info("No leads captured yet")
    
    elif menu == "📊 Stats":
        st.markdown("### 📊 Statistics")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("#### Loan Type Distribution")
            loan_counts = {}
            for lead in st.session_state.us_leads:
                loan_counts[lead['loan_type']] = loan_counts.get(lead['loan_type'], 0) + 1
            if loan_counts:
                st.bar_chart(loan_counts)
        
        with col2:
            st.markdown("#### State Distribution")
            state_counts = {}
            for lead in st.session_state.us_leads:
                state_counts[lead['state']] = state_counts.get(lead['state'], 0) + 1
            if state_counts:
                st.bar_chart(state_counts)
        
        st.markdown("#### Income Distribution")
        income_ranges = {"$0-25k": 0, "$25-50k": 0, "$50-75k": 0, "$75-100k": 0, "$100k+": 0}
        for lead in st.session_state.us_leads:
            inc = lead.get('income', 0)
            if inc < 25000:
                income_ranges["$0-25k"] += 1
            elif inc < 50000:
                income_ranges["$25-50k"] += 1
            elif inc < 75000:
                income_ranges["$50-75k"] += 1
            elif inc < 100000:
                income_ranges["$75-100k"] += 1
            else:
                income_ranges["$100k+"] += 1
        st.bar_chart(income_ranges)

# ============================================
# MAIN APP
# ============================================
def show_logout():
    with st.sidebar:
        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user_type = None
            st.session_state.user_data = None
            st.rerun()

# Main logic
if not st.session_state.logged_in:
    show_lead_capture_form()
    
    with st.sidebar:
        st.markdown("---")
        st.markdown(f"""
        <div style="text-align: center;">
            <p>🏛️ <b>{COMPANY_NAME}</b></p>
            <p>📞 {COMPANY_PHONE}</p>
            <p>💬 {COMPANY_WHATSAPP}</p>
            <p>📧 {COMPANY_EMAIL}</p>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("---")
        if st.button("🔐 Lender Portal →", use_container_width=True):
            st.session_state.show_login = True
            st.rerun()
    
    if st.session_state.get('show_login', False):
        show_login()
        
else:
    with st.sidebar:
        if st.session_state.user_type == "admin":
            st.markdown(f"""
            <div style="background: #e8f4fd; padding: 0.8rem; border-radius: 10px;">
                <b>👑 Admin</b><br>
                <b>🏛️ {COMPANY_NAME}</b><br>
                <b>📞 {COMPANY_PHONE}</b><br>
                <b>💬 {COMPANY_WHATSAPP}</b>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="background: #e8f4fd; padding: 0.8rem; border-radius: 10px;">
                <b>🏢 {st.session_state.user_data['name']}</b><br>
                <b>📊 Plan:</b> {PLANS[st.session_state.user_data['plan']]['name']}<br>
                <b>🎯 Leads Today:</b> {st.session_state.user_data.get('leads_today', 0)}/{st.session_state.user_data['limit']}
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### 💰 Pricing Plans (USD)")
        for p, plan in PLANS.items():
            st.markdown(f"**{plan['name']}** - ${plan['price']}/month | {plan['leads']} leads/month")
    
    show_logout()
    
    if st.session_state.user_type == "admin":
        show_admin_dashboard()
    else:
        show_lender_dashboard(st.session_state.user_data)

# Footer
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; font-size: 0.7rem; color: #666;">
    <b>🏛️ {COMPANY_NAME}</b> | NMLS # 123456 | Equal Housing Lender<br>
    📞 {COMPANY_PHONE} | 💬 {COMPANY_WHATSAPP} | 📧 {COMPANY_EMAIL}<br>
    © 2026 All Rights Reserved | Your privacy is protected under GLBA
</div>
""", unsafe_allow_html=True)
