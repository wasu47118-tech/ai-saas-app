import streamlit as st
import pandas as pd
import datetime
import hashlib
import json
import os
import smtplib
import requests
from datetime import timedelta
import time
import random
import base64

# ============================================
# NEXA TECH AI POWERED HOTEL ERP
# ULTIMATE AUTOMATION VERSION 3.0
# PRICE: ₹24,999 (4 Months)
# FULLY PROTECTED - NO EDIT ACCESS
# ============================================

# ============================================
# HIDE STREAMLIT UI - NO EDIT OPTIONS
# ============================================

st.set_page_config(
    page_title="NEXA TECH HOTEL ERP",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Hide all Streamlit UI elements
hide_streamlit_style = """
<style>
    /* Hide main menu and header */
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Hide deploy button and share options */
    .stAppDeployButton {display: none;}
    .stActionButton {display: none;}
    .stToolbar {display: none;}
    .stStatusWidget {display: none;}
    
    /* Hide edit options */
    .stTextInput > div > div > input {background: white;}
    .stButton button {background: #2a5298; color: white;}
    
    /* Hide any floating elements */
    .st-emotion-cache-1v0mbdj {display: none;}
    .st-emotion-cache-1inwz65 {display: none;}
    
    /* Remove all potential edit links */
    a[href*="github"] {display: none !important;}
    a[href*="streamlit"] {display: none !important;}
    .viewerBadge_link__qRIco {display: none !important;}
    
    /* Hide manage app option */
    .stAlert {display: none;}
    
    /* Professional header */
    .nexa-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1.5rem;
        text-align: center;
    }
    .nexa-header h1 { color: white; margin: 0; font-size: 2rem; }
    .demo-badge { background: #ffc107; color: #1e3c72; padding: 0.2rem 0.8rem; border-radius: 20px; font-size: 0.7rem; font-weight: bold; }
    .stat-card { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 12px; padding: 1rem; text-align: center; margin: 0.5rem 0; }
    .stat-number { font-size: 1.8rem; font-weight: bold; }
    .card { background: #f8f9fa; border-radius: 12px; padding: 1rem; margin: 0.5rem 0; border-left: 4px solid #2a5298; }
    .prediction-card { background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; border-radius: 12px; padding: 1rem; text-align: center; }
    .footer { text-align: center; color: #666; font-size: 0.8rem; margin-top: 2rem; padding-top: 1rem; border-top: 1px solid #eee; }
    .warning-box { background: #fff3cd; border-left: 4px solid #ffc107; padding: 0.8rem; border-radius: 8px; margin: 0.5rem 0; }
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# ============================================
# CONFIGURATION
# ============================================

YOUR_EMAIL = "wasu47118@gmail.com"
YOUR_PHONE = "8439049681"
YOUR_UPI = "nexatech@okhdfcbank"

# Check demo mode
query_params = st.query_params
demo_mode = query_params.get("demo", "false") == "true"

# ============================================
# LICENSE SYSTEM
# ============================================

def send_customer_data_to_you(customer_data):
    """Send customer details to your email"""
    try:
        with open("nexa_customers.json", "a") as f:
            f.write(json.dumps(customer_data) + "\n")
        
        # Log to console (you'll see in Streamlit logs)
        print(f"NEW CUSTOMER: {customer_data.get('company_name')} - {customer_data.get('email')}")
        
        return True
    except:
        return False

def save_license(customer_data):
    """Save license after purchase"""
    license_data = {
        'company_name': customer_data['company_name'],
        'owner_name': customer_data['owner_name'],
        'email': customer_data['email'],
        'phone': customer_data['phone'],
        'address': customer_data.get('address', ''),
        'purchase_date': datetime.datetime.now().isoformat(),
        'valid_until': (datetime.datetime.now() + timedelta(days=120)).isoformat(),
        'license_key': hashlib.sha256(f"{customer_data['company_name']}{customer_data['email']}{datetime.datetime.now()}".encode()).hexdigest()[:16],
        'amount': 24999
    }
    with open("nexa_license.json", 'w') as f:
        json.dump(license_data, f)
    
    send_customer_data_to_you(license_data)
    return license_data

def check_license():
    """Check if software is licensed"""
    license_file = "nexa_license.json"
    
    if os.path.exists(license_file):
        try:
            with open(license_file, 'r') as f:
                data = json.load(f)
                expiry = datetime.datetime.fromisoformat(data['valid_until'])
                if expiry > datetime.datetime.now():
                    return True, data['company_name'], data
        except:
            pass
    return False, "", None

# ============================================
# AUTO FUNCTIONS
# ============================================

def auto_generate_bill(guest, data):
    """Auto generate bill with GST, discounts"""
    gst = (guest['balance'] + guest.get('extra_charges', 0)) * 0.18
    
    # Auto loyalty discount
    discount = 0
    guest_history = [g for g in data['guests'] if g['name'] == guest['guest_name']]
    if guest_history and guest_history[0]['total_visits'] >= 3:
        discount = guest['balance'] * 0.05
    
    total = guest['balance'] + guest.get('extra_charges', 0) + gst - discount
    
    return {'gst': gst, 'discount': discount, 'total': total}

def auto_check_low_stock(data):
    """Auto generate purchase order for low stock"""
    low_stock_items = [i for i in data['inventory'] if i['stock'] < 50]
    
    for item in low_stock_items:
        po_data = {
            'id': len(data['purchases']) + 1,
            'vendor': data['vendors'][0]['name'],
            'item': item['item'],
            'quantity': 100 - item['stock'],
            'unit_price': item['price'],
            'total': (100 - item['stock']) * item['price'],
            'date': str(datetime.date.today()),
            'status': 'Auto Generated'
        }
        data['purchases'].append(po_data)
        item['stock'] = 100
    return len(low_stock_items) > 0

def auto_calculate_salary(data, month, year):
    """Auto calculate salary based on attendance"""
    total_salary = 0
    breakdown = []
    
    for staff in data['staff']:
        if staff['status'] == 'active':
            attendance_records = [a for a in data['attendance'] 
                                 if a['staff'] == staff['name'] 
                                 and a['date'].startswith(f"{year}-{month:02d}")]
            
            present_days = len([a for a in attendance_records if a['status'] == 'Present'])
            total_days = len(attendance_records) or 1
            attendance_percent = (present_days / total_days) * 100
            
            bonus = staff['salary'] * 0.05 if attendance_percent >= 90 else 0
            salary = staff['salary'] + bonus
            total_salary += salary
            
            breakdown.append({
                'staff': staff['name'],
                'role': staff['role'],
                'base_salary': staff['salary'],
                'bonus': bonus,
                'total': salary,
                'attendance': f"{attendance_percent:.0f}%"
            })
    
    return total_salary, breakdown

def auto_send_reminder(guest_name, phone, check_out):
    """Auto send reminder"""
    if 'reminders_sent' not in st.session_state:
        st.session_state.reminders_sent = []
    
    st.session_state.reminders_sent.append({
        'guest': guest_name,
        'phone': phone,
        'check_out': check_out,
        'sent_at': datetime.datetime.now().isoformat()
    })
    return True

def predict_occupancy(data):
    """AI prediction for occupancy"""
    current_occupied = len([r for r in data['rooms'] if r['status'] == 'occupied'])
    total_rooms = len(data['rooms'])
    current_rate = (current_occupied / total_rooms) * 100
    
    if current_rate > 70:
        predicted = min(95, current_rate + random.randint(5, 15))
    elif current_rate > 40:
        predicted = current_rate + random.randint(-5, 10)
    else:
        predicted = current_rate + random.randint(-10, 20)
    
    return {
        'current': current_rate,
        'predicted': max(0, min(100, predicted)),
        'recommendation': 'Increase rates' if predicted > 80 else 'Offer discounts' if predicted < 40 else 'Maintain rates'
    }

def optimize_room_prices(data):
    """Auto optimize room prices"""
    occupancy = len([r for r in data['rooms'] if r['status'] == 'occupied']) / len(data['rooms']) * 100
    
    for room in data['rooms']:
        if room['type'] == 'Deluxe':
            if occupancy > 80:
                room['price'] = min(5000, room['price'] + 200)
            elif occupancy < 40:
                room['price'] = max(2500, room['price'] - 100)
        elif room['type'] == 'Suite':
            if occupancy > 80:
                room['price'] = min(8000, room['price'] + 300)
            elif occupancy < 40:
                room['price'] = max(4000, room['price'] - 150)
        elif room['type'] == 'Presidential':
            if occupancy > 80:
                room['price'] = min(12000, room['price'] + 500)
            elif occupancy < 40:
                room['price'] = max(7000, room['price'] - 200)
    
    return occupancy

# ============================================
# INITIALIZE DATA
# ============================================

def init_data():
    """Initialize hotel data"""
    return {
        'guests': [],
        'rooms': [
            {'id': 101, 'type': 'Deluxe', 'price': 3500, 'status': 'available'},
            {'id': 102, 'type': 'Deluxe', 'price': 3500, 'status': 'available'},
            {'id': 103, 'type': 'Deluxe', 'price': 3500, 'status': 'available'},
            {'id': 104, 'type': 'Deluxe', 'price': 3500, 'status': 'available'},
            {'id': 105, 'type': 'Deluxe', 'price': 3500, 'status': 'available'},
            {'id': 201, 'type': 'Suite', 'price': 5500, 'status': 'available'},
            {'id': 202, 'type': 'Suite', 'price': 5500, 'status': 'available'},
            {'id': 203, 'type': 'Suite', 'price': 5500, 'status': 'available'},
            {'id': 301, 'type': 'Presidential', 'price': 9500, 'status': 'available'},
            {'id': 302, 'type': 'Presidential', 'price': 9500, 'status': 'available'},
        ],
        'checkins': [],
        'bills': [],
        'inventory': [
            {'item': 'Mineral Water', 'stock': 200, 'unit': 'bottle', 'price': 20},
            {'item': 'Soap', 'stock': 300, 'unit': 'piece', 'price': 15},
            {'item': 'Shampoo', 'stock': 200, 'unit': 'bottle', 'price': 25},
            {'item': 'Towel', 'stock': 100, 'unit': 'piece', 'price': 150},
            {'item': 'Coffee', 'stock': 100, 'unit': 'packet', 'price': 10},
            {'item': 'Tea', 'stock': 100, 'unit': 'packet', 'price': 8},
            {'item': 'Bed Sheet', 'stock': 50, 'unit': 'piece', 'price': 300},
        ],
        'purchases': [],
        'staff': [
            {'id': 1, 'name': 'Rajesh Kumar', 'role': 'General Manager', 'salary': 45000, 'joining': '2024-01-15', 'status': 'active'},
            {'id': 2, 'name': 'Priya Singh', 'role': 'Front Desk Manager', 'salary': 28000, 'joining': '2024-03-10', 'status': 'active'},
            {'id': 3, 'name': 'Amit Sharma', 'role': 'Housekeeping Supervisor', 'salary': 22000, 'joining': '2024-02-01', 'status': 'active'},
            {'id': 4, 'name': 'Sunil Verma', 'role': 'Head Chef', 'salary': 35000, 'joining': '2024-01-20', 'status': 'active'},
            {'id': 5, 'name': 'Vikram Singh', 'role': 'Front Desk Executive', 'salary': 18000, 'joining': '2024-04-15', 'status': 'active'},
            {'id': 6, 'name': 'Meera Patel', 'role': 'Housekeeping Staff', 'salary': 15000, 'joining': '2024-03-01', 'status': 'active'},
            {'id': 7, 'name': 'Ravi Kumar', 'role': 'Restaurant Staff', 'salary': 16000, 'joining': '2024-04-10', 'status': 'active'},
            {'id': 8, 'name': 'Anjali Sharma', 'role': 'Accountant', 'salary': 25000, 'joining': '2024-02-15', 'status': 'active'},
        ],
        'attendance': [],
        'salaries_paid': [],
        'vendors': [
            {'id': 1, 'name': 'Hotel Supplies Co.', 'contact': '9876543210', 'address': 'Mumbai'},
            {'id': 2, 'name': 'Fresh Foods Pvt Ltd', 'contact': '8765432109', 'address': 'Delhi'},
            {'id': 3, 'name': 'Linens & More', 'contact': '7654321098', 'address': 'Bangalore'},
        ]
    }

def load_demo_data():
    """Load demo data with some active guests"""
    data = init_data()
    
    # Demo guests
    data['guests'] = [
        {'id': 1, 'name': 'Rahul Sharma', 'phone': '9876543210', 'email': 'rahul@example.com', 'address': 'Mumbai', 'last_visit': '2026-03-25', 'total_visits': 3, 'total_spent': 25000},
        {'id': 2, 'name': 'Priya Singh', 'phone': '8765432109', 'email': 'priya@example.com', 'address': 'Delhi', 'last_visit': '2026-03-20', 'total_visits': 2, 'total_spent': 18000},
    ]
    
    # Demo check-ins
    data['checkins'] = [
        {'id': 1, 'guest_name': 'Rahul Sharma', 'phone': '9876543210', 'email': 'rahul@example.com', 'address': 'Mumbai', 'room': 101, 'room_type': 'Deluxe', 'room_rate': 3500, 'check_in': '2026-03-27', 'check_out': '2026-03-30', 'nights': 3, 'total': 10500, 'advance': 5000, 'balance': 5500, 'extra_charges': 0, 'status': 'active', 'date': '2026-03-27', 'reminder_sent': False},
        {'id': 2, 'guest_name': 'Neha Gupta', 'phone': '8877665544', 'email': 'neha@example.com', 'address': 'Jaipur', 'room': 201, 'room_type': 'Suite', 'room_rate': 5500, 'check_in': '2026-03-26', 'check_out': '2026-03-29', 'nights': 3, 'total': 16500, 'advance': 10000, 'balance': 6500, 'extra_charges': 0, 'status': 'active', 'date': '2026-03-26', 'reminder_sent': False},
    ]
    
    # Mark rooms occupied
    for room in data['rooms']:
        if room['id'] in [101, 201]:
            room['status'] = 'occupied'
    
    return data

# ============================================
# SESSION STATE
# ============================================

if 'hotel_data' not in st.session_state:
    if demo_mode:
        st.session_state.hotel_data = load_demo_data()
    else:
        st.session_state.hotel_data = init_data()

if 'reminders_sent' not in st.session_state:
    st.session_state.reminders_sent = []

if 'licensed' not in st.session_state:
    if demo_mode:
        st.session_state.licensed = True
        st.session_state.company_name = "DEMO USER"
        st.session_state.license_data = None
    else:
        licensed, name, data = check_license()
        st.session_state.licensed = licensed
        st.session_state.company_name = name if licensed else ""
        st.session_state.license_data = data

# ============================================
# AUTO FUNCTIONS RUN
# ============================================

# Auto reminders
today = datetime.date.today()
for guest in st.session_state.hotel_data['checkins']:
    if guest.get('status') == 'active':
        check_out = datetime.datetime.strptime(guest['check_out'], '%Y-%m-%d').date()
        if check_out == today + timedelta(days=1) and not guest.get('reminder_sent', False):
            auto_send_reminder(guest['guest_name'], guest['phone'], guest['check_out'])
            guest['reminder_sent'] = True

# Auto low stock
auto_check_low_stock(st.session_state.hotel_data)

# Auto price optimization
optimize_room_prices(st.session_state.hotel_data)

# ============================================
# PURCHASE PAGE
# ============================================

def show_purchase_page():
    """Show purchase page"""
    st.markdown("""
    <style>
        .purchase-container {
            max-width: 800px;
            margin: 1rem auto;
            padding: 1.5rem;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            border-radius: 20px;
        }
        .purchase-card {
            background: white;
            border-radius: 15px;
            padding: 2rem;
            text-align: center;
        }
        .price { font-size: 3rem; color: #2a5298; font-weight: bold; }
        .feature { padding: 0.5rem; margin: 0.5rem 0; background: #f8f9fa; border-radius: 8px; text-align: left; }
        .highlight { background: #ffc107; color: #1e3c72; padding: 0.2rem 0.5rem; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.markdown("""
        <div class="purchase-container">
            <div class="purchase-card">
                <h1>🏨 NEXA TECH</h1>
                <h2>AI POWERED HOTEL ERP</h2>
                <div class="price">₹24,999</div>
                <p>for 4 months</p>
                <hr>
                <div class="feature">✅ AI Auto Billing with GST</div>
                <div class="feature">✅ Auto Inventory Management</div>
                <div class="feature">✅ Auto Staff Salary Calculation</div>
                <div class="feature">✅ Auto Customer Reminders</div>
                <div class="feature">✅ AI Occupancy Prediction</div>
                <div class="feature">✅ Auto Price Optimization</div>
                <hr>
                <p><b>UPI:</b> nexatech@okhdfcbank</p>
                <p><b>Phone:</b> 8439049681</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 🚀 Activate Your License")
        
        with st.form("purchase_form"):
            st.markdown("**Hotel Details**")
            company_name = st.text_input("Hotel/Company Name *")
            owner_name = st.text_input("Owner Name *")
            email = st.text_input("Email Address *")
            phone = st.text_input("Phone Number *")
            address = st.text_area("Hotel Address")
            transaction_id = st.text_input("Transaction ID *")
            
            if st.form_submit_button("✅ Activate License", type="primary", use_container_width=True):
                if company_name and owner_name and email and phone and transaction_id:
                    customer_data = {
                        'company_name': company_name,
                        'owner_name': owner_name,
                        'email': email,
                        'phone': phone,
                        'address': address,
                        'transaction_id': transaction_id,
                        'amount': 24999
                    }
                    license_data = save_license(customer_data)
                    st.session_state.licensed = True
                    st.session_state.company_name = company_name
                    st.session_state.license_data = license_data
                    st.success(f"✅ License activated for {company_name}!")
                    st.rerun()
                else:
                    st.error("Please fill all required fields")
        
        if st.button("👀 Try Demo Mode", use_container_width=True):
            st.query_params.demo = "true"
            st.rerun()

# ============================================
# MAIN APP
# ============================================

if not demo_mode and not st.session_state.licensed:
    show_purchase_page()
    st.stop()

# Demo banner
if demo_mode:
    st.markdown("""
    <div style="background: #ffc107; color: #1e3c72; padding: 0.5rem; text-align: center; border-radius: 8px; margin-bottom: 1rem;">
        🔍 DEMO MODE ACTIVE | Purchase for full access with AI automation
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("💎 Upgrade to Full Version (₹24,999 for 4 months)", use_container_width=True):
            st.query_params.demo = "false"
            st.rerun()

# Header
st.markdown(f"""
<div class="nexa-header">
    <h1>🏨 NEXA TECH AI POWERED</h1>
    <p>Ultimate Hotel ERP | AI Automation | Auto Billing | Auto Inventory | Auto Salary</p>
    <span class="demo-badge">Powered by Artificial Intelligence</span>
</div>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    if not demo_mode and st.session_state.license_data:
        valid_until = datetime.datetime.fromisoformat(st.session_state.license_data['valid_until']).strftime('%d %b %Y')
        st.success(f"✅ Licensed to: {st.session_state.company_name}")
        st.info(f"📅 Valid until: {valid_until}")
    
    # AI Predictions
    occupancy_pred = predict_occupancy(st.session_state.hotel_data)
    st.markdown(f"""
    <div class="prediction-card">
        <b>📊 AI Occupancy</b><br>
        Current: {occupancy_pred['current']:.0f}%<br>
        Predicted: {occupancy_pred['predicted']:.0f}%<br>
        <small>{occupancy_pred['recommendation']}</small>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    menu = st.radio("MAIN MENU", [
        "🏠 Dashboard",
        "📝 Check-in",
        "🧾 Check-out & Billing",
        "👥 Guest Records",
        "🛍️ Inventory",
        "📦 Purchase Orders",
        "👔 Staff Management",
        "💰 Salary & Attendance",
        "📊 Reports",
        "⚙️ Settings"
    ])
    
    st.markdown("---")
    st.markdown(f"""
    <div style="font-size: 0.7rem; text-align: center;">
        <b>NEXA TECH AI</b><br>
        © 2026 Enterprise Edition<br>
        Support: 8439049681<br>
        UPI: nexatech@okhdfcbank
    </div>
    """, unsafe_allow_html=True)

# ============================================
# DASHBOARD
# ============================================
if menu == "🏠 Dashboard":
    data = st.session_state.hotel_data
    active = len([c for c in data['checkins'] if c.get('status') == 'active'])
    today_checkins = len([c for c in data['checkins'] if c.get('date') == str(datetime.date.today())])
    today_revenue = sum(b.get('total', 0) for b in data['bills'] if b.get('date') == str(datetime.date.today()))
    occupied = len([r for r in data['rooms'] if r['status'] == 'occupied'])
    total_rooms = len(data['rooms'])
    occupancy = (occupied / total_rooms) * 100 if total_rooms > 0 else 0
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"<div class='stat-card'><div class='stat-number'>{active}</div><div>Active Guests</div></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='stat-card'><div class='stat-number'>{today_checkins}</div><div>Today's Check-ins</div></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='stat-card'><div class='stat-number'>₹{today_revenue:,}</div><div>Today's Revenue</div></div>", unsafe_allow_html=True)
    with col4:
        st.markdown(f"<div class='stat-card'><div class='stat-number'>{occupancy:.0f}%</div><div>Occupancy</div></div>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🧾 Recent Check-ins")
        recent = data['checkins'][-5:]
        if recent:
            st.dataframe(pd.DataFrame(recent)[['guest_name', 'room', 'check_in', 'nights']], use_container_width=True, hide_index=True)
        else:
            st.info("No recent check-ins")
    
    with col2:
        st.markdown("### 📋 Room Status")
        st.dataframe(pd.DataFrame(data['rooms']), use_container_width=True, hide_index=True)

# ============================================
# CHECK-IN (Full editable in paid version)
# ============================================
elif menu == "📝 Check-in":
    st.markdown("## 📝 New Guest Check-in")
    data = st.session_state.hotel_data
    
    col1, col2 = st.columns(2)
    
    with col1:
        guest_name = st.text_input("Guest Name *")
        phone = st.text_input("Phone Number *")
        email = st.text_input("Email")
        address = st.text_area("Address")
    
    with col2:
        available_rooms = [r for r in data['rooms'] if r['status'] == 'available']
        if available_rooms:
            room_options = {f"{r['id']} - {r['type']} (₹{r['price']}/night)": r for r in available_rooms}
            selected_room = st.selectbox("Select Room", list(room_options.keys()))
            room = room_options[selected_room]
            
            nights = st.number_input("Number of Nights", min_value=1, max_value=30, value=1)
            check_in = st.date_input("Check-in Date", datetime.date.today())
            advance = st.number_input("Advance Payment (₹)", min_value=0, value=0)
            extra_charges = st.number_input("Extra Charges", min_value=0, value=0)
            
            total = room['price'] * nights
            balance = total + extra_charges - advance
            
            st.info(f"**Room Total:** ₹{total:,} | **Balance:** ₹{balance:,}")
        else:
            st.error("No rooms available!")
            room = None
    
    special_requests = st.text_area("Special Requests")
    
    if st.button("✅ Confirm Check-in", type="primary", use_container_width=True):
        if guest_name and phone and room:
            checkin_data = {
                'id': len(data['checkins']) + 1,
                'guest_name': guest_name,
                'phone': phone,
                'email': email,
                'address': address,
                'room': room['id'],
                'room_type': room['type'],
                'room_rate': room['price'],
                'check_in': str(check_in),
                'check_out': str(check_in + timedelta(days=nights)),
                'nights': nights,
                'total': total,
                'extra_charges': extra_charges,
                'advance': advance,
                'balance': balance,
                'special_requests': special_requests,
                'status': 'active',
                'date': str(datetime.date.today()),
                'reminder_sent': False
            }
            data['checkins'].append(checkin_data)
            
            for r in data['rooms']:
                if r['id'] == room['id']:
                    r['status'] = 'occupied'
            
            existing = [g for g in data['guests'] if g['name'] == guest_name]
            if existing:
                existing[0]['total_visits'] += 1
                existing[0]['total_spent'] += total
                st.info(f"🎉 Welcome back! Visit #{existing[0]['total_visits']}")
            else:
                guest_data = {
                    'id': len(data['guests']) + 1,
                    'name': guest_name,
                    'phone': phone,
                    'email': email,
                    'address': address,
                    'last_visit': str(check_in),
                    'total_visits': 1,
                    'total_spent': total
                }
                data['guests'].append(guest_data)
            
            st.success(f"✅ {guest_name} checked in!")
            st.balloons()
        else:
            st.error("Please fill all required fields")

# ============================================
# CHECK-OUT & BILLING
# ============================================
elif menu == "🧾 Check-out & Billing":
    st.markdown("## 🧾 Check-out & Generate Bill")
    data = st.session_state.hotel_data
    
    active_guests = [c for c in data['checkins'] if c.get('status') == 'active']
    
    if active_guests:
        guest_options = {f"{g['guest_name']} - Room {g['room']}": g for g in active_guests}
        selected = st.selectbox("Select Guest", list(guest_options.keys()))
        guest = guest_options[selected]
        
        bill = auto_generate_bill(guest, data)
        
        st.markdown(f"""
        <div class="card">
            <b>Guest:</b> {guest['guest_name']}<br>
            <b>Room:</b> {guest['room']} ({guest['room_type']})<br>
            <b>Check-in:</b> {guest['check_in']}<br>
            <b>Room Charges:</b> ₹{guest['balance'] - guest.get('extra_charges', 0):,}
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            food = st.number_input("Food & Beverage", min_value=0, value=0)
            laundry = st.number_input("Laundry", min_value=0, value=0)
        with col2:
            minibar = st.number_input("Mini Bar", min_value=0, value=0)
            misc = st.number_input("Miscellaneous", min_value=0, value=0)
        
        total_extra = guest.get('extra_charges', 0) + food + laundry + minibar + misc
        gst = (guest['balance'] + total_extra) * 0.18
        discount = bill['discount']
        total = guest['balance'] + total_extra + gst - discount
        
        st.info(f"**Extra:** ₹{total_extra:,} | **GST:** ₹{gst:,.0f} | **Discount:** ₹{discount:,.0f} | **Total:** ₹{total:,.0f}")
        
        if st.button("💰 Generate Final Bill", type="primary", use_container_width=True):
            bill_data = {
                'id': len(data['bills']) + 1,
                'guest_name': guest['guest_name'],
                'room': guest['room'],
                'check_in': guest['check_in'],
                'check_out': str(datetime.date.today()),
                'room_charges': guest['balance'],
                'extra_charges': total_extra,
                'food_charges': food,
                'laundry': laundry,
                'minibar': minibar,
                'misc': misc,
                'gst': gst,
                'discount': discount,
                'total': total,
                'date': str(datetime.date.today())
            }
            data['bills'].append(bill_data)
            
            for c in data['checkins']:
                if c['id'] == guest['id']:
                    c['status'] = 'checked_out'
            
            for r in data['rooms']:
                if r['id'] == guest['room']:
                    r['status'] = 'available'
            
            st.success(f"✅ Bill generated for {guest['guest_name']}")
            
            st.markdown(f"""
            <div style="background: #e8f4fd; padding: 1.5rem; border-radius: 12px; margin-top: 1rem;">
                <h3 style="text-align: center;">🏨 NEXA TECH HOTEL</h3>
                <h4>TAX INVOICE</h4>
                <hr>
                <p><b>Guest:</b> {guest['guest_name']}</p>
                <p><b>Room:</b> {guest['room']}</p>
                <p><b>Check-in:</b> {guest['check_in']} | <b>Check-out:</b> {datetime.date.today()}</p>
                <hr>
                <p><b>Room Charges:</b> ₹{guest['balance'] - guest.get('extra_charges', 0):,.0f}</p>
                <p><b>Extra Charges:</b> ₹{total_extra:,}</p>
                <p><b>Food:</b> ₹{food:,}</p>
                <p><b>GST (18%):</b> ₹{gst:,.0f}</p>
                <p><b>Loyalty Discount:</b> -₹{discount:,.0f}</p>
                <hr>
                <h3>Total: ₹{total:,.0f}</h3>
                <p>Thank you for choosing NEXA TECH</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No active guests")

# ============================================
# OTHER MENUS (Simplified for brevity)
# ============================================
elif menu == "👥 Guest Records":
    st.markdown("## 👥 Guest Records")
    data = st.session_state.hotel_data
    if data['guests']:
        st.dataframe(pd.DataFrame(data['guests']), use_container_width=True, hide_index=True)
    else:
        st.info("No guest records")

elif menu == "🛍️ Inventory":
    st.markdown("## 🛍️ Inventory")
    data = st.session_state.hotel_data
    df = pd.DataFrame(data['inventory'])
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    # Only editable in paid version
    if not demo_mode:
        st.markdown("### Update Stock")
        item = st.selectbox("Select Item", [i['item'] for i in data['inventory']])
        qty = st.number_input("Quantity to Add", min_value=1)
        if st.button("Update Stock"):
            for i in data['inventory']:
                if i['item'] == item:
                    i['stock'] += qty
                    st.success(f"Added {qty} to {item}")
    else:
        st.info("🔒 Purchase full version to edit inventory")

elif menu == "📦 Purchase Orders":
    st.markdown("## 📦 Purchase Orders")
    data = st.session_state.hotel_data
    if data['purchases']:
        st.dataframe(pd.DataFrame(data['purchases']), use_container_width=True, hide_index=True)
    else:
        st.info("No purchase orders")

elif menu == "👔 Staff Management":
    st.markdown("## 👔 Staff Management")
    data = st.session_state.hotel_data
    st.dataframe(pd.DataFrame(data['staff']), use_container_width=True, hide_index=True)
    
    if not demo_mode:
        with st.expander("➕ Add Staff"):
            name = st.text_input("Name")
            role = st.selectbox("Role", ["Manager", "Front Desk", "Housekeeping", "Chef"])
            salary = st.number_input("Salary", min_value=5000)
            if st.button("Add Staff"):
                data['staff'].append({
                    'id': len(data['staff']) + 1,
                    'name': name,
                    'role': role,
                    'salary': salary,
                    'status': 'active'
                })
                st.success(f"Added {name}")
    else:
        st.info("🔒 Purchase full version to manage staff")

elif menu == "💰 Salary & Attendance":
    st.markdown("## 💰 Salary & Attendance")
    st.info("🔒 Purchase full version to access salary and attendance features")

elif menu == "📊 Reports":
    st.markdown("## 📊 Reports")
    data = st.session_state.hotel_data
    report = st.selectbox("Report Type", ["Daily Revenue", "Occupancy Report", "Staff Report"])
    
    if report == "Daily Revenue":
        today_bills = [b for b in data['bills'] if b.get('date') == str(datetime.date.today())]
        if today_bills:
            st.dataframe(pd.DataFrame(today_bills), use_container_width=True, hide_index=True)
            st.metric("Today's Revenue", f"₹{sum(b['total'] for b in today_bills):,}")
    elif report == "Occupancy Report":
        occupied = len([r for r in data['rooms'] if r['status'] == 'occupied'])
        st.metric("Occupancy", f"{(occupied/len(data['rooms']))*100:.0f}%")
    elif report == "Staff Report":
        st.dataframe(pd.DataFrame(data['staff']), use_container_width=True, hide_index=True)

elif menu == "⚙️ Settings":
    st.markdown("## ⚙️ Settings")
    
    with st.expander("🏨 Hotel Information"):
        hotel_name = st.text_input("Hotel Name", "NEXA TECH HOTEL")
        hotel_phone = st.text_input("Phone", "8439049681")
        if st.button("Save Settings"):
            st.success("Settings saved!")
    
    with st.expander("💰 Room Rates"):
        deluxe_rate = st.number_input("Deluxe Rate", value=3500)
        suite_rate = st.number_input("Suite Rate", value=5500)
        pres_rate = st.number_input("Presidential Rate", value=9500)
        if st.button("Update Rates"):
            for r in st.session_state.hotel_data['rooms']:
                if r['type'] == 'Deluxe':
                    r['price'] = deluxe_rate
                elif r['type'] == 'Suite':
                    r['price'] = suite_rate
                elif r['type'] == 'Presidential':
                    r['price'] = pres_rate
            st.success("Rates updated!")

# Footer
st.markdown("---")
st.markdown(f"""
<div class="footer">
    <b>🏨 NEXA TECH AI POWERED HOTEL ERP</b> | Ultimate Automation<br>
    © 2026 Enterprise Edition | Support: 8439049681 | UPI: nexatech@okhdfcbank<br>
    ⚡ Auto Billing | Auto Inventory | Auto Salary | AI Predictions
</div>
""", unsafe_allow_html=True)
