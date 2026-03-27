import streamlit as st
import pandas as pd
import datetime
import random
import json
import time
from datetime import timedelta

# ============================================
# NEXA AUTO AI - COMPANY MANAGEMENT SYSTEM
# LEAD DISTRIBUTION | PURCHASE | CONTROL
# ============================================

st.set_page_config(
    page_title="NEXA AUTO AI | Lead Management",
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
    "personal_loan": {"name": "🏦 Personal Loan", "icon": "💰"},
    "home_loan": {"name": "🏠 Home Loan", "icon": "🏡"},
    "car_loan": {"name": "🚗 Car Loan", "icon": "🚙"},
    "business_loan": {"name": "💼 Business Loan", "icon": "📊"},
    "education_loan": {"name": "🎓 Education Loan", "icon": "📚"},
    "credit_card": {"name": "💳 Credit Card", "icon": "💎"},
    "gold_loan": {"name": "🥇 Gold Loan", "icon": "✨"},
    "loan_against_property": {"name": "🏢 Loan Against Property", "icon": "🏛️"}
}

# Pricing Plans
PLANS = {
    "free": {"name": "Free Trial", "price": 0, "leads_per_day": 3, "color": "gray"},
    "starter": {"name": "Starter", "price": 4999, "leads_per_day": 50, "color": "blue"},
    "professional": {"name": "Professional", "price": 14999, "leads_per_day": 200, "color": "green"},
    "enterprise": {"name": "Enterprise", "price": 49999, "leads_per_day": 1000, "color": "purple"}
}

# ============================================
# DATABASE
# ============================================

# Companies Database
if 'companies_db' not in st.session_state:
    st.session_state.companies_db = [
        {
            'id': 1,
            'name': 'HDFC Bank',
            'email': 'hdfc@example.com',
            'plan': 'professional',
            'leads_today': 0,
            'leads_total': 0,
            'active': True,
            'created': '2026-01-01',
            'leads_limit': 200
        },
        {
            'id': 2,
            'name': 'ICICI Bank',
            'email': 'icici@example.com',
            'plan': 'starter',
            'leads_today': 0,
            'leads_total': 0,
            'active': True,
            'created': '2026-02-01',
            'leads_limit': 50
        },
        {
            'id': 3,
            'name': 'SBI Card',
            'email': 'sbi@example.com',
            'plan': 'free',
            'leads_today': 0,
            'leads_total': 0,
            'active': True,
            'created': '2026-03-01',
            'leads_limit': 3
        },
        {
            'id': 4,
            'name': 'Axis Bank',
            'email': 'axis@example.com',
            'plan': 'starter',
            'leads_today': 0,
            'leads_total': 0,
            'active': True,
            'created': '2026-03-15',
            'leads_limit': 50
        },
        {
            'id': 5,
            'name': 'Kotak Mahindra',
            'email': 'kotak@example.com',
            'plan': 'enterprise',
            'leads_today': 0,
            'leads_total': 0,
            'active': True,
            'created': '2026-03-20',
            'leads_limit': 1000
        }
    ]

# Leads Database
if 'all_leads' not in st.session_state:
    st.session_state.all_leads = []
    
    # Demo leads
    names = ["Rajesh Sharma", "Priya Singh", "Amit Kumar", "Neha Gupta", "Vikram Mehta", "Anjali Verma", "Rahul Khanna", "Pooja Malhotra"]
    cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Hyderabad", "Pune", "Kolkata", "Ahmedabad"]
    
    for i in range(20):
        cat = random.choice(list(LOAN_CATEGORIES.keys()))
        lead = {
            'id': random.randint(10000, 99999),
            'name': random.choice(names),
            'phone': f"9{random.randint(7000000000, 9999999999)}",
            'email': f"lead{random.randint(100, 999)}@example.com",
            'city': random.choice(cities),
            'loan_type': LOAN_CATEGORIES[cat]['name'],
            'loan_category': cat,
            'amount': random.choice([100000, 250000, 500000, 1000000, 2500000, 5000000]),
            'income': random.choice([25000, 35000, 50000, 75000, 100000]),
            'score': random.randint(50, 95),
            'interest': random.choice(["High", "Medium", "Low"]),
            'source': random.choice(["Google Ads", "Facebook", "Instagram", "Website"]),
            'created': str(datetime.date.today()),
            'time': datetime.datetime.now().strftime('%H:%M:%S'),
            'assigned_to': None,
            'assigned_name': None,
            'status': 'new'
        }
        st.session_state.all_leads.append(lead)

# Lead Distribution Log
if 'distribution_log' not in st.session_state:
    st.session_state.distribution_log = []

# ============================================
# LEAD DISTRIBUTION ENGINE
# ============================================

def distribute_lead(lead):
    """Auto distribute lead to active company"""
    active_companies = [c for c in st.session_state.companies_db if c['active'] and c['leads_today'] < c['leads_limit']]
    
    if not active_companies:
        lead['assigned_to'] = None
        lead['assigned_name'] = "Unassigned"
        return lead
    
    # Round robin distribution (fair)
    active_companies.sort(key=lambda x: x['leads_today'])
    best_company = active_companies[0]
    
    lead['assigned_to'] = best_company['id']
    lead['assigned_name'] = best_company['name']
    lead['status'] = 'assigned'
    
    # Update company stats
    for c in st.session_state.companies_db:
        if c['id'] == best_company['id']:
            c['leads_today'] += 1
            c['leads_total'] += 1
    
    # Log distribution
    st.session_state.distribution_log.append({
        'time': datetime.datetime.now().strftime('%H:%M:%S'),
        'lead': lead['name'],
        'company': best_company['name'],
        'loan_type': lead['loan_type'],
        'score': lead['score']
    })
    
    return lead

def auto_generate_lead():
    """Generate one new lead"""
    cat = random.choice(list(LOAN_CATEGORIES.keys()))
    
    names_prefix = ["Rajesh", "Priya", "Amit", "Neha", "Vikram", "Anjali", "Rahul", "Pooja", "Suresh", "Kavita", "Manish", "Swati", "Deepak", "Rekha", "Alok", "Sunita"]
    names_suffix = ["Sharma", "Singh", "Kumar", "Gupta", "Mehta", "Verma", "Patel", "Reddy", "Joshi", "Malhotra", "Agarwal", "Khanna", "Saxena", "Chopra", "Nair"]
    cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Hyderabad", "Pune", "Kolkata", "Ahmedabad", "Jaipur", "Lucknow", "Nagpur", "Indore", "Bhopal", "Surat", "Vadodara"]
    
    amount_options = {
        'personal_loan': [100000, 250000, 500000, 750000, 1000000],
        'home_loan': [2500000, 5000000, 7500000, 10000000, 15000000],
        'car_loan': [500000, 800000, 1000000, 1500000, 2000000],
        'business_loan': [500000, 1000000, 2500000, 5000000, 10000000],
        'education_loan': [500000, 1000000, 2000000, 3000000, 5000000],
        'credit_card': [50000, 100000, 200000, 300000, 500000],
        'gold_loan': [100000, 250000, 500000, 750000, 1000000],
        'loan_against_property': [1000000, 2500000, 5000000, 7500000, 10000000]
    }
    
    amount = random.choice(amount_options.get(cat, [100000, 250000, 500000]))
    income = amount // random.randint(20, 40)
    
    lead = {
        'id': random.randint(10000, 99999),
        'name': f"{random.choice(names_prefix)} {random.choice(names_suffix)}",
        'phone': f"9{random.randint(7000000000, 9999999999)}",
        'email': f"lead{random.randint(100, 999)}@example.com",
        'city': random.choice(cities),
        'loan_type': LOAN_CATEGORIES[cat]['name'],
        'loan_category': cat,
        'amount': amount,
        'income': income,
        'score': random.randint(45, 98),
        'interest': random.choice(["High", "Medium", "Low"]),
        'source': random.choice(["Google Ads", "Facebook", "Instagram", "WhatsApp", "Website", "Referral"]),
        'created': str(datetime.date.today()),
        'time': datetime.datetime.now().strftime('%H:%M:%S'),
        'assigned_to': None,
        'assigned_name': None,
        'status': 'new'
    }
    
    # Distribute
    lead = distribute_lead(lead)
    
    return lead

# ============================================
# AUTO GENERATION (EVERY SECOND)
# ============================================

if 'last_gen_time' not in st.session_state:
    st.session_state.last_gen_time = datetime.datetime.now()
    st.session_state.gen_counter = 0

current_time = datetime.datetime.now()
time_diff = (current_time - st.session_state.last_gen_time).total_seconds()

if time_diff >= 1:
    num_to_gen = min(int(time_diff), 3)
    for _ in range(num_to_gen):
        new_lead = auto_generate_lead()
        st.session_state.all_leads.insert(0, new_lead)
        st.session_state.gen_counter += 1
    st.session_state.last_gen_time = current_time

# ============================================
# SIDEBAR
# ============================================

with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1rem;">
        <h1 style="font-size: 2rem;">🤖</h1>
        <h2>NEXA AUTO AI</h2>
        <p>Lead Management System</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    mode = st.radio("Access Mode", ["👤 Client Dashboard", "👑 Admin Dashboard"], label_visibility="collapsed")
    
    st.markdown("---")
    
    if mode == "👤 Client Dashboard":
        # Company selection for client
        companies = st.session_state.companies_db
        company_options = {c['name']: c for c in companies}
        selected_company = st.selectbox("Select Your Company", list(company_options.keys()))
        current_company = company_options[selected_company]
        
        st.markdown(f"""
        <div style="background: #f8f9fa; padding: 1rem; border-radius: 10px;">
            <b>🏢 {current_company['name']}</b><br>
            📊 Plan: {PLANS[current_company['plan']]['name']}<br>
            🎯 Leads Today: {current_company['leads_today']}/{current_company['leads_limit']}<br>
            📈 Total Leads: {current_company['leads_total']}<br>
            ✅ Status: {'🟢 Active' if current_company['active'] else '🔴 Inactive'}
        </div>
        """, unsafe_allow_html=True)
        
        # Upgrade option
        if current_company['plan'] == 'free':
            st.markdown("---")
            st.markdown("### 💰 Upgrade Plan")
            
            for plan_id, plan in PLANS.items():
                if plan_id != 'free':
                    if st.button(f"📊 {plan['name']} - ₹{plan['price']}/month", key=f"upgrade_{plan_id}"):
                        st.info(f"💳 Pay ₹{plan['price']} to UPI: {UPI_ID}")
                        st.success("After payment, contact support for activation")
        
    else:
        st.markdown("### 👑 Admin Controls")
        st.markdown(f"""
        <div style="background: #e8f4fd; padding: 1rem; border-radius: 10px;">
            <b>📧 Email:</b> {ADMIN_EMAIL}<br>
            <b>💳 UPI:</b> {UPI_ID}<br>
            <b>📞 Phone:</b> {PHONE}<br>
            <b>📊 Total Leads:</b> {len(st.session_state.all_leads)}
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
# CLIENT DASHBOARD
# ============================================

if mode == "👤 Client Dashboard":
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1.5rem; border-radius: 15px; margin-bottom: 1.5rem;">
        <h1 style="color: white;">🤖 Your Assigned Leads</h1>
        <p style="color: white;">Real-time leads assigned to you</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Get company leads
    company_leads = [l for l in st.session_state.all_leads if l.get('assigned_name') == current_company['name']]
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📊 Today's Leads", current_company['leads_today'])
    with col2:
        st.metric("🎯 Limit", current_company['leads_limit'])
    with col3:
        st.metric("⭐ Avg Score", f"{sum(l['score'] for l in company_leads[-10:]) // 10 if company_leads else 0}%")
    
    st.markdown("---")
    
    if not company_leads:
        st.info("No leads assigned yet. Leads will appear here automatically!")
    else:
        st.markdown(f"### 🎯 Your Leads ({len(company_leads)} total)")
        
        for lead in company_leads[-PLANS[current_company['plan']]['leads_per_day']:]:
            with st.container():
                col1, col2, col3, col4 = st.columns([2, 1.5, 1.5, 1])
                with col1:
                    st.markdown(f"**{lead['name']}**")
                    st.caption(f"📞 {lead['phone']}")
                with col2:
                    st.markdown(f"**{lead['loan_type']}**")
                    st.caption(f"₹{lead['amount']:,}")
                with col3:
                    score_color = "green" if lead['score'] >= 80 else "orange" if lead['score'] >= 60 else "red"
                    st.markdown(f"**Score:** <span style='color:{score_color};'>{lead['score']}%</span>", unsafe_allow_html=True)
                    st.caption(f"🔥 {lead['interest']} Interest")
                with col4:
                    st.markdown(f"📍 {lead['city']}")
                    st.caption(lead['time'])
                st.markdown("---")

# ============================================
# ADMIN DASHBOARD
# ============================================

else:
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); padding: 1.5rem; border-radius: 15px; margin-bottom: 1.5rem;">
        <h1 style="color: white;">👑 Admin Dashboard</h1>
        <p style="color: white;">Complete Control | Lead Management | Company Management</p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "🏢 Companies", "🎯 All Leads", "📈 Distribution Log"])
    
    with tab1:
        total_leads = len(st.session_state.all_leads)
        assigned_leads = len([l for l in st.session_state.all_leads if l.get('assigned_to')])
        unassigned = total_leads - assigned_leads
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📊 Total Leads", total_leads)
        with col2:
            st.metric("✅ Assigned", assigned_leads)
        with col3:
            st.metric("⏳ Unassigned", unassigned)
        with col4:
            st.metric("🏢 Companies", len(st.session_state.companies_db))
        
        st.markdown("---")
        
        # Company wise lead distribution
        st.markdown("### 🏢 Company Wise Lead Distribution")
        company_data = []
        for c in st.session_state.companies_db:
            company_leads = [l for l in st.session_state.all_leads if l.get('assigned_name') == c['name']]
            company_data.append({
                'Company': c['name'],
                'Plan': PLANS[c['plan']]['name'],
                'Today': c['leads_today'],
                'Limit': c['leads_limit'],
                'Total': c['leads_total'],
                'Status': '🟢 Active' if c['active'] else '🔴 Inactive'
            })
        st.dataframe(pd.DataFrame(company_data), use_container_width=True, hide_index=True)
        
        # Category wise leads
        st.markdown("### 📊 Loan Category Distribution")
        cat_data = {}
        for lead in st.session_state.all_leads:
            cat = lead['loan_category']
            cat_data[cat] = cat_data.get(cat, 0) + 1
        
        if cat_data:
            st.bar_chart(cat_data)
    
    with tab2:
        st.markdown("### 🏢 Manage Companies")
        
        # Add new company
        with st.expander("➕ Add New Company"):
            col1, col2 = st.columns(2)
            with col1:
                new_name = st.text_input("Company Name")
                new_email = st.text_input("Email")
            with col2:
                new_plan = st.selectbox("Plan", list(PLANS.keys()), format_func=lambda x: PLANS[x]['name'])
            
            if st.button("Add Company"):
                new_id = max([c['id'] for c in st.session_state.companies_db]) + 1 if st.session_state.companies_db else 1
                new_company = {
                    'id': new_id,
                    'name': new_name,
                    'email': new_email,
                    'plan': new_plan,
                    'leads_today': 0,
                    'leads_total': 0,
                    'active': True,
                    'created': str(datetime.date.today()),
                    'leads_limit': PLANS[new_plan]['leads_per_day']
                }
                st.session_state.companies_db.append(new_company)
                st.success(f"✅ {new_name} added!")
                st.rerun()
        
        # Company list with controls
        st.markdown("### Company List")
        
        for c in st.session_state.companies_db:
            with st.container():
                col1, col2, col3, col4, col5 = st.columns([2, 1.5, 1.5, 1, 1])
                with col1:
                    st.markdown(f"**{c['name']}**")
                    st.caption(c['email'])
                with col2:
                    st.markdown(f"Plan: {PLANS[c['plan']]['name']}")
                    st.caption(f"Limit: {c['leads_limit']}/day")
                with col3:
                    st.markdown(f"Today: {c['leads_today']}")
                    st.caption(f"Total: {c['leads_total']}")
                with col4:
                    if c['active']:
                        st.success("🟢 Active")
                    else:
                        st.error("🔴 Inactive")
                with col5:
                    if st.button(f"{'⏸️ Stop' if c['active'] else '▶️ Start'}", key=f"toggle_{c['id']}"):
                        c['active'] = not c['active']
                        st.rerun()
                
                # Update plan button
                if st.button(f"📊 Update Plan", key=f"plan_{c['id']}"):
                    with st.popover(f"Update {c['name']} Plan"):
                        new_plan = st.selectbox("Select Plan", list(PLANS.keys()), format_func=lambda x: PLANS[x]['name'], key=f"select_{c['id']}")
                        if st.button("Confirm Update"):
                            c['plan'] = new_plan
                            c['leads_limit'] = PLANS[new_plan]['leads_per_day']
                            st.success(f"Updated {c['name']} to {PLANS[new_plan]['name']}")
                            st.rerun()
                
                st.markdown("---")
    
    with tab3:
        st.markdown("### 🎯 All Leads")
        
        # Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            company_filter = st.selectbox("Filter by Company", ["All"] + [c['name'] for c in st.session_state.companies_db])
        with col2:
            cat_filter = st.selectbox("Filter by Loan Type", ["All"] + [LOAN_CATEGORIES[cat]['name'] for cat in LOAN_CATEGORIES.keys()])
        with col3:
            score_filter = st.selectbox("Filter by Score", ["All", "High (80+)", "Medium (60-79)", "Low (<60)"])
        
        filtered_leads = st.session_state.all_leads.copy()
        
        if company_filter != "All":
            filtered_leads = [l for l in filtered_leads if l.get('assigned_name') == company_filter]
        if cat_filter != "All":
            filtered_leads = [l for l in filtered_leads if l['loan_type'] == cat_filter]
        if score_filter == "High (80+)":
            filtered_leads = [l for l in filtered_leads if l['score'] >= 80]
        elif score_filter == "Medium (60-79)":
            filtered_leads = [l for l in filtered_leads if 60 <= l['score'] < 80]
        elif score_filter == "Low (<60)":
            filtered_leads = [l for l in filtered_leads if l['score'] < 60]
        
        if filtered_leads:
            df = pd.DataFrame(filtered_leads)
            st.dataframe(df[['name', 'phone', 'city', 'loan_type', 'amount', 'score', 'interest', 'assigned_name', 'time']], 
                        use_container_width=True, hide_index=True)
            
            if st.button("📥 Export All Leads to CSV"):
                csv = df.to_csv(index=False)
                st.download_button("Download CSV", csv, "all_leads.csv", "text/csv")
        else:
            st.info("No leads found")
    
    with tab4:
        st.markdown("### 📈 Lead Distribution Log")
        
        if st.session_state.distribution_log:
            df_log = pd.DataFrame(st.session_state.distribution_log[-100:])
            st.dataframe(df_log, use_container_width=True, hide_index=True)
            
            # Stats
            st.markdown("### Distribution Stats")
            company_stats = {}
            for log in st.session_state.distribution_log:
                company_stats[log['company']] = company_stats.get(log['company'], 0) + 1
            
            st.bar_chart(company_stats)
        else:
            st.info("No leads distributed yet")

# Update admin stats in sidebar
st.session_state.admin_total_leads = len(st.session_state.all_leads)
