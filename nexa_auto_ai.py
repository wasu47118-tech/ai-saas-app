import streamlit as st
import pandas as pd
import datetime
import random
from datetime import timedelta
import hashlib

# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(
    page_title="NEXA AUTO AI | Lead Management",
    page_icon="🤖",
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
# CONFIGURATION
# ============================================
ADMIN_EMAIL = "admin@nexa.com"
ADMIN_PASSWORD = "admin123"
UPI_ID = "8439049681@pthdfc"
PHONE = "8439049681"

LOAN_CATEGORIES = {
    "personal": "🏦 Personal Loan",
    "home": "🏠 Home Loan",
    "car": "🚗 Car Loan",
    "business": "💼 Business Loan",
    "education": "🎓 Education Loan",
    "credit_card": "💳 Credit Card",
    "gold": "🥇 Gold Loan"
}

PLANS = {
    "free": {"name": "🔥 Free Trial", "price": 0, "leads": 3},
    "starter": {"name": "📊 Starter", "price": 4999, "leads": 50},
    "professional": {"name": "⚡ Professional", "price": 14999, "leads": 200},
    "enterprise": {"name": "👑 Enterprise", "price": 49999, "leads": 1000}
}

# Client credentials
CLIENT_CREDENTIALS = {
    "hdfc@nexa.com": {"password": "hdfc123", "company_id": 1, "name": "🏦 HDFC Bank"},
    "icici@nexa.com": {"password": "icici123", "company_id": 2, "name": "🏧 ICICI Bank"},
    "sbi@nexa.com": {"password": "sbi123", "company_id": 3, "name": "💳 SBI Card"},
    "axis@nexa.com": {"password": "axis123", "company_id": 4, "name": "🏛️ Axis Bank"},
    "kotak@nexa.com": {"password": "kotak123", "company_id": 5, "name": "🏢 Kotak Bank"},
}

# ============================================
# DATABASE
# ============================================
if 'companies' not in st.session_state:
    st.session_state.companies = [
        {'id': 1, 'name': '🏦 HDFC Bank', 'plan': 'professional', 'leads_today': 0, 'leads_total': 0, 'active': True, 'limit': 200},
        {'id': 2, 'name': '🏧 ICICI Bank', 'plan': 'starter', 'leads_today': 0, 'leads_total': 0, 'active': True, 'limit': 50},
        {'id': 3, 'name': '💳 SBI Card', 'plan': 'free', 'leads_today': 0, 'leads_total': 0, 'active': True, 'limit': 3},
        {'id': 4, 'name': '🏛️ Axis Bank', 'plan': 'starter', 'leads_today': 0, 'leads_total': 0, 'active': True, 'limit': 50},
        {'id': 5, 'name': '🏢 Kotak Bank', 'plan': 'enterprise', 'leads_today': 0, 'leads_total': 0, 'active': True, 'limit': 1000},
    ]

if 'leads' not in st.session_state:
    st.session_state.leads = []
    names = ["Rajesh Sharma", "Priya Singh", "Amit Kumar", "Neha Gupta", "Vikram Mehta", "Anjali Verma", "Rahul Khanna", "Pooja Malhotra"]
    cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Hyderabad", "Pune", "Kolkata", "Ahmedabad"]
    
    for i in range(50):
        cat = random.choice(list(LOAN_CATEGORIES.keys()))
        st.session_state.leads.append({
            'id': i+1,
            'name': random.choice(names),
            'phone': f"9{random.randint(7000000000, 9999999999)}",
            'email': f"lead{i+1}@example.com",
            'city': random.choice(cities),
            'loan_type': LOAN_CATEGORIES[cat],
            'amount': random.choice([100000, 250000, 500000, 1000000, 2500000, 5000000]),
            'income': random.choice([25000, 35000, 50000, 75000, 100000]),
            'score': random.randint(45, 98),
            'interest': random.choice(["🔥 High", "⭐ Medium", "💤 Low"]),
            'source': random.choice(["Google Ads", "Facebook", "Instagram", "WhatsApp", "Website"]),
            'created': str(datetime.date.today()),
            'time': datetime.datetime.now().strftime('%H:%M:%S'),
            'assigned_to': None,
            'assigned_name': None
        })

if 'dist_log' not in st.session_state:
    st.session_state.dist_log = []

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_type = None
    st.session_state.user_data = None

# ============================================
# LEAD DISTRIBUTION
# ============================================
def distribute_lead(lead):
    active = [c for c in st.session_state.companies if c['active'] and c['leads_today'] < c['limit']]
    if not active:
        lead['assigned_name'] = "📦 Unassigned"
        return lead
    
    active.sort(key=lambda x: x['leads_today'])
    best = active[0]
    
    lead['assigned_to'] = best['id']
    lead['assigned_name'] = best['name']
    
    for c in st.session_state.companies:
        if c['id'] == best['id']:
            c['leads_today'] += 1
            c['leads_total'] += 1
    
    st.session_state.dist_log.append({
        'time': datetime.datetime.now().strftime('%H:%M:%S'),
        'lead': lead['name'][:15],
        'company': best['name'],
        'loan': lead['loan_type'],
        'score': lead['score']
    })
    return lead

# Distribute existing leads
for lead in st.session_state.leads:
    if not lead.get('assigned_name'):
        distribute_lead(lead)

# ============================================
# LOGIN PAGE
# ============================================
def show_login():
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); padding: 2rem; border-radius: 20px; text-align: center; margin-bottom: 2rem;">
        <h1 style="color: white;">🤖 NEXA AUTO AI</h1>
        <p style="color: white;">Lead Generation System</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### 🔐 Login to Access")
        
        tab1, tab2 = st.tabs(["👑 Admin Login", "🏢 Client Login"])
        
        with tab1:
            with st.form("admin_login"):
                email = st.text_input("Email", value="admin@nexa.com")
                password = st.text_input("Password", type="password", value="admin123")
                
                if st.form_submit_button("Login as Admin", use_container_width=True):
                    if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
                        st.session_state.logged_in = True
                        st.session_state.user_type = "admin"
                        st.session_state.user_data = {"name": "Admin", "email": ADMIN_EMAIL}
                        st.success("✅ Admin login successful!")
                        st.rerun()
                    else:
                        st.error("Invalid admin credentials")
        
        with tab2:
            with st.form("client_login"):
                email = st.text_input("Company Email", placeholder="hdfc@nexa.com")
                password = st.text_input("Password", type="password", placeholder="hdfc123")
                
                if st.form_submit_button("Login as Client", use_container_width=True):
                    if email in CLIENT_CREDENTIALS and password == CLIENT_CREDENTIALS[email]["password"]:
                        company_id = CLIENT_CREDENTIALS[email]["company_id"]
                        company = next(c for c in st.session_state.companies if c['id'] == company_id)
                        st.session_state.logged_in = True
                        st.session_state.user_type = "client"
                        st.session_state.user_data = company
                        st.success(f"✅ Welcome {company['name']}!")
                        st.rerun()
                    else:
                        st.error("Invalid client credentials")
        
        st.markdown("---")
        st.markdown("### 📝 Demo Credentials")
        st.markdown("**Admin:** admin@nexa.com / admin123")
        st.markdown("**Client:** hdfc@nexa.com / hdfc123")

# ============================================
# LOGOUT BUTTON
# ============================================
def show_logout():
    with st.sidebar:
        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.session_state.user_type = None
            st.session_state.user_data = None
            st.rerun()

# ============================================
# CLIENT DASHBOARD
# ============================================
def show_client_dashboard(company):
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1rem; border-radius: 15px; margin-bottom: 1rem;">
        <h2 style="color: white;">👤 {company['name']} Dashboard</h2>
        <p style="color: white;">Your assigned leads appear here</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats
    col1, col2, col3, col4 = st.columns(4)
    company_leads = [l for l in st.session_state.leads if l.get('assigned_name') == company['name']]
    
    with col1:
        st.metric("📊 Today's Leads", company['leads_today'])
    with col2:
        st.metric("🎯 Daily Limit", company['limit'])
    with col3:
        st.metric("📈 Total Leads", company['leads_total'])
    with col4:
        avg_score = sum(l['score'] for l in company_leads[-10:]) // 10 if company_leads else 0
        st.metric("⭐ Avg Score", f"{avg_score}%")
    
    st.markdown("---")
    st.markdown(f"### 🎯 Your Leads ({len(company_leads)} total)")
    
    if company_leads:
        for lead in company_leads[-company['limit']:]:
            with st.container():
                col1, col2, col3, col4 = st.columns([2, 1.5, 1.5, 1])
                with col1:
                    st.markdown(f"**{lead['name']}**")
                    st.caption(f"📞 {lead['phone']}")
                with col2:
                    st.markdown(f"**{lead['loan_type']}**")
                    st.caption(f"₹{lead['amount']:,}")
                with col3:
                    color = "green" if lead['score'] >= 80 else "orange" if lead['score'] >= 60 else "red"
                    st.markdown(f"**Score:** <span style='color:{color};'>{lead['score']}%</span>", unsafe_allow_html=True)
                    st.caption(f"{lead['interest']}")
                with col4:
                    st.markdown(f"📍 {lead['city']}")
                    st.caption(lead['time'])
                st.markdown("---")
    else:
        st.info("No leads assigned yet. Leads will appear here automatically!")
    
    # Upgrade option for free plan
    if company['plan'] == 'free':
        st.markdown("---")
        st.markdown("### 💎 Upgrade Your Plan")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("📊 Starter - ₹4,999/month (50 leads/day)", use_container_width=True):
                st.info(f"💳 Pay ₹4,999 to UPI: {UPI_ID}")
                st.success("✅ After payment, contact support to activate")
        with col2:
            if st.button("⚡ Professional - ₹14,999/month (200 leads/day)", use_container_width=True):
                st.info(f"💳 Pay ₹14,999 to UPI: {UPI_ID}")
                st.success("✅ After payment, contact support to activate")

# ============================================
# ADMIN DASHBOARD
# ============================================
def show_admin_dashboard():
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); padding: 1rem; border-radius: 15px; margin-bottom: 1rem;">
        <h2 style="color: white;">👑 ADMIN DASHBOARD</h2>
        <p style="color: white;">Complete system control</p>
    </div>
    """, unsafe_allow_html=True)
    
    total = len(st.session_state.leads)
    assigned = len([l for l in st.session_state.leads if l.get('assigned_name') and l['assigned_name'] != "📦 Unassigned"])
    unassigned = total - assigned
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📊 Total Leads", total)
    with col2:
        st.metric("✅ Assigned", assigned)
    with col3:
        st.metric("⏳ Unassigned", unassigned)
    with col4:
        st.metric("🏢 Active Companies", len([c for c in st.session_state.companies if c['active']]))
    
    st.markdown("---")
    
    # Top Menu for Admin
    menu = st.radio("Admin Menu", ["🏢 Companies", "🎯 All Leads", "📈 Stats"], horizontal=True)
    
    if menu == "🏢 Companies":
        st.markdown("### 🏢 Company Management")
        
        # Add company
        with st.expander("➕ Add New Company", expanded=False):
            col1, col2 = st.columns(2)
            with col1:
                new_name = st.text_input("Company Name")
            with col2:
                new_plan = st.selectbox("Select Plan", list(PLANS.keys()), format_func=lambda x: f"{PLANS[x]['name']} - ₹{PLANS[x]['price']}/month")
            
            if st.button("✅ Add Company", use_container_width=True):
                if new_name:
                    new_id = max([c['id'] for c in st.session_state.companies]) + 1
                    st.session_state.companies.append({
                        'id': new_id,
                        'name': new_name,
                        'plan': new_plan,
                        'leads_today': 0,
                        'leads_total': 0,
                        'active': True,
                        'limit': PLANS[new_plan]['leads']
                    })
                    st.success(f"✅ {new_name} added successfully!")
                    st.rerun()
                else:
                    st.error("Please enter company name")
        
        # Company list
        for c in st.session_state.companies:
            with st.container():
                col1, col2, col3, col4, col5 = st.columns([2, 1.5, 1.5, 1, 1.2])
                with col1:
                    st.markdown(f"**{c['name']}**")
                    st.caption(f"Plan: {PLANS[c['plan']]['name']}")
                with col2:
                    st.markdown(f"Today: {c['leads_today']}")
                    st.caption(f"Limit: {c['limit']}/day")
                with col3:
                    st.markdown(f"Total: {c['leads_total']}")
                with col4:
                    if c['active']:
                        st.success("🟢 Active")
                    else:
                        st.error("🔴 Inactive")
                with col5:
                    if st.button(f"{'⏸️ Stop' if c['active'] else '▶️ Start'}", key=f"toggle_{c['id']}"):
                        c['active'] = not c['active']
                        st.rerun()
                
                if st.button(f"📊 Update Plan", key=f"plan_{c['id']}"):
                    with st.popover(f"Update {c['name']} Plan"):
                        new_plan = st.selectbox("Select Plan", list(PLANS.keys()), format_func=lambda x: PLANS[x]['name'], key=f"select_{c['id']}")
                        if st.button("Confirm Update"):
                            c['plan'] = new_plan
                            c['limit'] = PLANS[new_plan]['leads']
                            st.success(f"✅ {c['name']} updated to {PLANS[new_plan]['name']}")
                            st.rerun()
                st.markdown("---")
    
    elif menu == "🎯 All Leads":
        st.markdown("### 🎯 All Leads")
        
        # Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            company_filter = st.selectbox("Filter by Company", ["All"] + [c['name'] for c in st.session_state.companies])
        with col2:
            score_filter = st.selectbox("Filter by Score", ["All", "High (80+)", "Medium (60-79)", "Low (<60)"])
        with col3:
            loan_filter = st.selectbox("Filter by Loan", ["All"] + list(LOAN_CATEGORIES.values()))
        
        filtered = st.session_state.leads.copy()
        if company_filter != "All":
            filtered = [l for l in filtered if l.get('assigned_name') == company_filter]
        if score_filter == "High (80+)":
            filtered = [l for l in filtered if l['score'] >= 80]
        elif score_filter == "Medium (60-79)":
            filtered = [l for l in filtered if 60 <= l['score'] < 80]
        elif score_filter == "Low (<60)":
            filtered = [l for l in filtered if l['score'] < 60]
        if loan_filter != "All":
            filtered = [l for l in filtered if l['loan_type'] == loan_filter]
        
        if filtered:
            df = pd.DataFrame(filtered)
            st.dataframe(df[['name', 'phone', 'city', 'loan_type', 'amount', 'score', 'interest', 'assigned_name', 'time']], 
                        use_container_width=True, hide_index=True)
            
            if st.button("📥 Export to CSV"):
                csv = df.to_csv(index=False)
                st.download_button("Download CSV", csv, "leads_export.csv", "text/csv")
        else:
            st.info("No leads found")
    
    elif menu == "📈 Stats":
        st.markdown("### 📈 Statistics")
        
        # Loan type distribution
        st.markdown("#### 📊 Loan Type Distribution")
        loan_counts = {}
        for lead in st.session_state.leads:
            loan_counts[lead['loan_type']] = loan_counts.get(lead['loan_type'], 0) + 1
        st.bar_chart(loan_counts)
        
        # Company distribution
        st.markdown("#### 🏢 Company Distribution")
        company_counts = {}
        for lead in st.session_state.leads:
            name = lead.get('assigned_name', 'Unassigned')
            company_counts[name] = company_counts.get(name, 0) + 1
        st.bar_chart(company_counts)
        
        # Score distribution
        st.markdown("#### 📈 Score Distribution")
        score_ranges = {"High (80-100)": 0, "Medium (60-79)": 0, "Low (0-59)": 0}
        for lead in st.session_state.leads:
            if lead['score'] >= 80:
                score_ranges["High (80-100)"] += 1
            elif lead['score'] >= 60:
                score_ranges["Medium (60-79)"] += 1
            else:
                score_ranges["Low (0-59)"] += 1
        st.bar_chart(score_ranges)

# ============================================
# MAIN
# ============================================
if not st.session_state.logged_in:
    show_login()
else:
    # Sidebar info
    with st.sidebar:
        if st.session_state.user_type == "admin":
            st.markdown(f"""
            <div style="background: #e8f4fd; padding: 0.8rem; border-radius: 10px;">
                <b>👑 Logged in as:</b> Admin<br>
                <b>📧 Email:</b> {ADMIN_EMAIL}<br>
                <b>💳 UPI:</b> {UPI_ID}<br>
                <b>📞 Support:</b> {PHONE}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="background: #e8f4fd; padding: 0.8rem; border-radius: 10px;">
                <b>🏢 Company:</b> {st.session_state.user_data['name']}<br>
                <b>📊 Plan:</b> {PLANS[st.session_state.user_data['plan']]['name']}<br>
                <b>🎯 Leads Today:</b> {st.session_state.user_data['leads_today']}/{st.session_state.user_data['limit']}
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### 💰 Pricing Plans")
        for p, plan in PLANS.items():
            st.markdown(f"**{plan['name']}** - ₹{plan['price']}/month | {plan['leads']} leads/day")
    
    # Show logout button
    show_logout()
    
    # Show appropriate dashboard
    if st.session_state.user_type == "admin":
        show_admin_dashboard()
    else:
        show_client_dashboard(st.session_state.user_data)
