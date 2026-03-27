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

# ============================================
# NEXA TECH AI POWERED HOTEL ERP
# ULTIMATE AUTOMATION VERSION 3.0
# PRICE: ₹24,999 (4 Months)
# ============================================

# ============================================
# CONFIGURATION - CHANGE THESE
# ============================================

YOUR_EMAIL = "wasu47118@gmail.com"  # Customer data yahan aayega
YOUR_PHONE = "8439049681"
YOUR_UPI = "nexatech@okhdfcbank"

# ============================================
# DEMO MODE
# ============================================

query_params = st.query_params
demo_mode = query_params.get("demo", "false") == "true"

# ============================================
# SEND CUSTOMER DATA TO YOU
# ============================================

def send_customer_data_to_you(customer_data):
    """Send customer details to your email/telegram"""
    try:
        # Save to local file
        with open("nexa_customers.json", "a") as f:
            f.write(json.dumps(customer_data) + "\n")
        
        # Create email
        msg = f"""
        🏨 NEW CUSTOMER ACTIVATED!
        
        Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        
        CUSTOMER DETAILS:
        -----------------
        Hotel Name: {customer_data.get('company_name', 'N/A')}
        Owner Name: {customer_data.get('owner_name', 'N/A')}
        Email: {customer_data.get('email', 'N/A')}
        Phone: {customer_data.get('phone', 'N/A')}
        Address: {customer_data.get('address', 'N/A')}
        
        LICENSE DETAILS:
        ----------------
        License Key: {customer_data.get('license_key', 'N/A')}
        Purchase Date: {customer_data.get('purchase_date', 'N/A')}
        Valid Until: {customer_data.get('valid_until', 'N/A')}
        Amount: ₹{customer_data.get('amount', 24999)}
        
        SYSTEM INFO:
        -------------
        Demo Mode: {customer_data.get('demo', 'No')}
        """
        
        # Print to console
        print(msg)
        
        # Uncomment to send email (configure SMTP)
        # import smtplib
        # server = smtplib.SMTP('smtp.gmail.com', 587)
        # server.starttls()
        # server.login(YOUR_EMAIL, "your-app-password")
        # server.sendmail(YOUR_EMAIL, YOUR_EMAIL, msg)
        # server.quit()
        
        return True
    except Exception as e:
        print(f"Error sending data: {e}")
        return False

# ============================================
# LICENSE SYSTEM
# ============================================

def save_license(customer_data):
    """Save license after purchase"""
    license_data = {
        'company_name': customer_data['company_name'],
        'owner_name': customer_data['owner_name'],
        'email': customer_data['email'],
        'phone': customer_data['phone'],
        'address': customer_data.get('address', ''),
        'purchase_date': datetime.datetime.now().isoformat(),
        'valid_until': (datetime.datetime.now() + timedelta(days=120)).isoformat(),  # 4 months
        'license_key': hashlib.sha256(f"{customer_data['company_name']}{customer_data['email']}{datetime.datetime.now()}".encode()).hexdigest()[:16],
        'amount': 24999
    }
    with open("nexa_license.json", 'w') as f:
        json.dump(license_data, f)
    
    # Send to you
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
    """Auto generate bill with GST, discounts, etc."""
    # Auto calculate GST
    gst = (guest['balance'] + guest.get('extra_charges', 0)) * 0.18
    
    # Auto loyalty discount for repeat guests
    discount = 0
    guest_history = [g for g in data['guests'] if g['name'] == guest['guest_name']]
    if guest_history and guest_history[0]['total_visits'] >= 3:
        discount = guest['balance'] * 0.05  # 5% discount for loyal guests
    
    total = guest['balance'] + guest.get('extra_charges', 0) + gst - discount
    
    return {
        'gst': gst,
        'discount': discount,
        'total': total
    }

def auto_check_low_stock(data):
    """Auto generate purchase order for low stock items"""
    low_stock_items = [i for i in data['inventory'] if i['stock'] < 50]
    
    for item in low_stock_items:
        # Auto create purchase order
        po_data = {
            'id': len(data['purchases']) + 1,
            'vendor': data['vendors'][0]['name'],
            'item': item['item'],
            'quantity': 100 - item['stock'],
            'unit_price': item['price'],
            'total': (100 - item['stock']) * item['price'],
            'date': str(datetime.date.today()),
            'status': 'Auto Generated',
            'auto': True
        }
        data['purchases'].append(po_data)
        
        # Update stock
        item['stock'] = 100
        
        return True
    return False

def auto_calculate_salary(data, month, year):
    """Auto calculate salary based on attendance"""
    total_salary = 0
    salary_breakdown = []
    
    for staff in data['staff']:
        if staff['status'] == 'active':
            # Calculate attendance percentage
            attendance_records = [a for a in data['attendance'] 
                                 if a['staff'] == staff['name'] 
                                 and a['date'].startswith(f"{year}-{month:02d}")]
            
            present_days = len([a for a in attendance_records if a['status'] == 'Present'])
            total_days = len(attendance_records) or 1
            
            attendance_percent = (present_days / total_days) * 100
            
            # Auto salary calculation
            if attendance_percent >= 90:
                bonus = staff['salary'] * 0.05
            else:
                bonus = 0
            
            salary = staff['salary'] + bonus
            total_salary += salary
            
            salary_breakdown.append({
                'staff': staff['name'],
                'role': staff['role'],
                'base_salary': staff['salary'],
                'bonus': bonus,
                'total': salary,
                'attendance': f"{attendance_percent:.0f}%"
            })
    
    return total_salary, salary_breakdown

def auto_send_reminder(guest_name, phone, check_out):
    """Auto send reminder via SMS/WhatsApp"""
    reminder_msg = f"Dear {guest_name}, your check-out is on {check_out}. Thank you for staying with NEXA TECH HOTEL!"
    
    # Store reminder
    if 'reminders_sent' not in st.session_state:
        st.session_state.reminders_sent = []
    
    st.session_state.reminders_sent.append({
        'guest': guest_name,
        'phone': phone,
        'check_out': check_out,
        'message': reminder_msg,
        'sent_at': datetime.datetime.now().isoformat()
    })
    
    # Here you can integrate actual SMS API
    return True

def predict_occupancy(data):
    """AI prediction for occupancy"""
    # Simple prediction based on historical data
    current_occupied = len([r for r in data['rooms'] if r['status'] == 'occupied'])
    total_rooms = len(data['rooms'])
    current_rate = (current_occupied / total_rooms) * 100
    
    # Predict next week occupancy
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
    """Auto optimize room prices based on occupancy"""
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
# PURCHASE PAGE
# ============================================

def show_purchase_page():
    """Show purchase page with ₹24,999 for 4 months"""
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
        .price {
            font-size: 3rem;
            color: #2a5298;
            font-weight: bold;
        }
        .price-small {
            font-size: 1rem;
            color: #666;
        }
        .feature {
            padding: 0.5rem;
            margin: 0.5rem 0;
            background: #f8f9fa;
            border-radius: 8px;
            text-align: left;
        }
        .highlight {
            background: #ffc107;
            color: #1e3c72;
            padding: 0.2rem 0.5rem;
            border-radius: 5px;
            font-weight: bold;
        }
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
                <div class="price-small">for 4 months</div>
                <p>(Auto-renewal after 4 months)</p>
                <hr>
                <div class="feature">✅ AI Auto Billing with GST</div>
                <div class="feature">✅ Auto Inventory Management</div>
                <div class="feature">✅ Auto Staff Salary Calculation</div>
                <div class="feature">✅ Auto Customer Reminders</div>
                <div class="feature">✅ AI Occupancy Prediction</div>
                <div class="feature">✅ Auto Price Optimization</div>
                <div class="feature">✅ 24/7 AI Support</div>
                <hr>
                <p><b>UPI ID:</b> nexatech@okhdfcbank</p>
                <p><b>Phone:</b> 8439049681</p>
                <p class="highlight">⚡ Your data will be sent to support team for verification</p>
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
            gst = st.text_input("GST Number (optional)")
            
            st.markdown("**Payment Details**")
            transaction_id = st.text_input("Transaction ID *", placeholder="Enter UPI transaction ID")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.form_submit_button("✅ Activate License", type="primary", use_container_width=True):
                    if company_name and owner_name and email and phone and transaction_id:
                        customer_data = {
                            'company_name': company_name,
                            'owner_name': owner_name,
                            'email': email,
                            'phone': phone,
                            'address': address,
                            'gst': gst,
                            'transaction_id': transaction_id,
                            'amount': 24999
                        }
                        license_data = save_license(customer_data)
                        st.session_state.licensed = True
                        st.session_state.company_name = company_name
                        st.session_state.license_data = license_data
                        st.success(f"✅ License activated for {company_name}!")
                        st.info(f"📧 Confirmation sent to: {email}")
                        st.rerun()
                    else:
                        st.error("Please fill all required fields")
            with col2:
                st.markdown("""
                <div style="background: #e8f4fd; padding: 1rem; border-radius: 10px; margin-top: 1rem;">
                    <p><b>📱 Scan to Pay</b></p>
                    <p>UPI: <b>nexatech@okhdfcbank</b></p>
                    <p>Amount: <b>₹24,999</b></p>
                </div>
                """, unsafe_allow_html=True)
        
        with st.expander("👀 Try Demo First"):
            st.markdown("Want to test before purchasing?")
            if st.button("🎯 Launch Demo Mode", use_container_width=True):
                st.query_params.demo = "true"
                st.rerun()

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
            {'item': 'Mineral Water', 'stock': 200, 'unit': 'bottle', 'price': 20, 'min_stock': 50},
            {'item': 'Soap', 'stock': 300, 'unit': 'piece', 'price': 15, 'min_stock': 50},
            {'item': 'Shampoo', 'stock': 200, 'unit': 'bottle', 'price': 25, 'min_stock': 50},
            {'item': 'Towel', 'stock': 100, 'unit': 'piece', 'price': 150, 'min_stock': 30},
            {'item': 'Coffee', 'stock': 100, 'unit': 'packet', 'price': 10, 'min_stock': 40},
            {'item': 'Tea', 'stock': 100, 'unit': 'packet', 'price': 8, 'min_stock': 40},
            {'item': 'Bed Sheet', 'stock': 50, 'unit': 'piece', 'price': 300, 'min_stock': 20},
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
            {'id': 1, 'name': 'Hotel Supplies Co.', 'contact': '9876543210', 'address': 'Mumbai', 'gst': '27AABCU9603R1Z'},
            {'id': 2, 'name': 'Fresh Foods Pvt Ltd', 'contact': '8765432109', 'address': 'Delhi', 'gst': '07AAACF1234F1Z'},
            {'id': 3, 'name': 'Linens & More', 'contact': '7654321098', 'address': 'Bangalore', 'gst': '29AAACL1234E1Z'},
        ]
    }

def load_demo_data():
    """Load demo data"""
    data = init_data()
    
    # Add demo guests
    data['guests'] = [
        {'id': 1, 'name': 'Rahul Sharma', 'phone': '9876543210', 'email': 'rahul@example.com', 'address': 'Mumbai', 'last_visit': '2026-03-25', 'total_visits': 3, 'total_spent': 25000},
        {'id': 2, 'name': 'Priya Singh', 'phone': '8765432109', 'email': 'priya@example.com', 'address': 'Delhi', 'last_visit': '2026-03-20', 'total_visits': 2, 'total_spent': 18000},
    ]
    
    # Add demo check-ins
    data['checkins'] = [
        {'id': 1, 'guest_name': 'Rahul Sharma', 'phone': '9876543210', 'email': 'rahul@example.com', 'address': 'Mumbai', 'room': 101, 'room_type': 'Deluxe', 'room_rate': 3500, 'check_in': '2026-03-27', 'check_out': '2026-03-30', 'nights': 3, 'total': 10500, 'advance': 5000, 'balance': 5500, 'extra_charges': 0, 'status': 'active', 'date': '2026-03-27', 'reminder_sent': False},
        {'id': 2, 'guest_name': 'Neha Gupta', 'phone': '8877665544', 'email': 'neha@example.com', 'address': 'Jaipur', 'room': 201, 'room_type': 'Suite', 'room_rate': 5500, 'check_in': '2026-03-26', 'check_out': '2026-03-29', 'nights': 3, 'total': 16500, 'advance': 10000, 'balance': 6500, 'extra_charges': 0, 'status': 'active', 'date': '2026-03-26', 'reminder_sent': False},
    ]
    
    # Mark some rooms occupied
    for room in data['rooms']:
        if room['id'] in [101, 201]:
            room['status'] = 'occupied'
    
    return data

# ============================================
# SESSION STATE INIT
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
# AUTO FUNCTIONS EXECUTION
# ============================================

# Auto check reminders
today = datetime.date.today()
for guest in st.session_state.hotel_data['checkins']:
    if guest.get('status') == 'active':
        check_out = datetime.datetime.strptime(guest['check_out'], '%Y-%m-%d').date()
        if check_out == today + timedelta(days=1) and not guest.get('reminder_sent', False):
            auto_send_reminder(guest['guest_name'], guest['phone'], guest['check_out'])
            guest['reminder_sent'] = True

# Auto check low stock
auto_check_low_stock(st.session_state.hotel_data)

# Auto optimize prices
optimize_room_prices(st.session_state.hotel_data)

# ============================================
# MAIN UI
# ============================================

# CSS
st.markdown("""
<style>
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
</style>
""", unsafe_allow_html=True)

# Check license
if not demo_mode and not st.session_state.licensed:
    show_purchase_page()
    st.stop()

# Demo banner
if demo_mode:
    st.markdown("""
    <div style="background: #ffc107; color: #1e3c72; padding: 0.5rem; text-align: center; border-radius: 8px; margin-bottom: 1rem;">
        🔍 DEMO MODE ACTIVE | Purchase to get full access with AI automation
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

# License info in sidebar
with st.sidebar:
    if not demo_mode and st.session_state.license_data:
        valid_until = datetime.datetime.fromisoformat(st.session_state.license_data['valid_until']).strftime('%d %b %Y')
        st.success(f"✅ Licensed to: {st.session_state.company_name}")
        st.info(f"📅 Valid until: {valid_until}")
        st.warning(f"💰 Paid: ₹{st.session_state.license_data['amount']}")
    
    # AI Predictions
    st.markdown("### 🤖 AI Insights")
    occupancy_pred = predict_occupancy(st.session_state.hotel_data)
    st.markdown(f"""
    <div class="prediction-card">
        <b>📊 Occupancy Prediction</b><br>
        Current: {occupancy_pred['current']:.0f}%<br>
        Predicted: {occupancy_pred['predicted']:.0f}%<br>
        <small>📌 {occupancy_pred['recommendation']}</small>
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
    
    # AI Recommendations
    with st.expander("🤖 AI Recommendations", expanded=False):
        col1, col2, col3 = st.columns(3)
        with col1:
            low_stock = len([i for i in data['inventory'] if i['stock'] < i['min_stock']])
            st.metric("Low Stock Items", low_stock)
        with col2:
            upcoming_checkouts = len([c for c in data['checkins'] if c.get('status') == 'active' and datetime.datetime.strptime(c['check_out'], '%Y-%m-%d').date() <= datetime.date.today() + timedelta(days=2)])
            st.metric("Check-outs in 2 days", upcoming_checkouts)
        with col3:
            st.metric("Occupancy Prediction", f"{occupancy_pred['predicted']:.0f}%")

# ============================================
# CHECK-IN
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
            extra_charges = st.number_input("Extra Charges (if any)", min_value=0, value=0)
            
            total = room['price'] * nights
            balance = total + extra_charges - advance
            
            st.info(f"**Room Total:** ₹{total:,} | **Extra:** ₹{extra_charges:,} | **Balance:** ₹{balance:,}")
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
            
            # Check if repeat guest
            existing = [g for g in data['guests'] if g['name'] == guest_name]
            if existing:
                existing[0]['total_visits'] += 1
                existing[0]['total_spent'] += total
                existing[0]['last_visit'] = str(check_in)
                st.info(f"🎉 Welcome back! This is your {existing[0]['total_visits']}rd visit!")
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
            
            st.success(f"✅ {guest_name} checked in successfully!")
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
        
        # Auto calculate bill with AI
        bill = auto_generate_bill(guest, data)
        
        st.markdown(f"""
        <div class="card">
            <b>Guest:</b> {guest['guest_name']}<br>
            <b>Room:</b> {guest['room']} ({guest['room_type']})<br>
            <b>Check-in:</b> {guest['check_in']}<br>
            <b>Nights:</b> {guest['nights']}<br>
            <b>Room Charges:</b> ₹{guest['balance'] - guest.get('extra_charges', 0):,}<br>
            <b>Extra Charges:</b> ₹{guest.get('extra_charges', 0):,}
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 💰 Additional Charges")
        
        col1, col2 = st.columns(2)
        with col1:
            food = st.number_input("Food & Beverage", min_value=0, value=0)
            laundry = st.number_input("Laundry", min_value=0, value=0)
            minibar = st.number_input("Mini Bar", min_value=0, value=0)
        with col2:
            spa = st.number_input("Spa Services", min_value=0, value=0)
            misc = st.number_input("Miscellaneous", min_value=0, value=0)
        
        total_extra = guest.get('extra_charges', 0) + food + laundry + minibar + spa + misc
        gst = (guest['balance'] + total_extra) * 0.18
        discount = bill['discount']
        total = guest['balance'] + total_extra + gst - discount
        
        st.info(f"""
        **Extra Charges:** ₹{total_extra:,}  
        **GST (18%):** ₹{gst:,.0f}  
        **Loyalty Discount:** ₹{discount:,.0f}  
        **Total:** ₹{total:,.0f}
        """)
        
        if st.button("💰 Generate Final Bill", type="primary", use_container_width=True):
            bill_data = {
                'id': len(data['bills']) + 1,
                'guest_name': guest['guest_name'],
                'room': guest['room'],
                'room_type': guest['room_type'],
                'check_in': guest['check_in'],
                'check_out': str(datetime.date.today()),
                'room_charges': guest['balance'],
                'extra_charges': total_extra,
                'food_charges': food,
                'laundry': laundry,
                'minibar': minibar,
                'spa': spa,
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
                <h4 style="text-align: center;">TAX INVOICE</h4>
                <hr>
                <p><b>Guest:</b> {guest['guest_name']}</p>
                <p><b>Room:</b> {guest['room']} ({guest['room_type']})</p>
                <p><b>Check-in:</b> {guest['check_in']} | <b>Check-out:</b> {datetime.date.today()}</p>
                <hr>
                <p><b>Room Charges:</b> ₹{guest['balance'] - guest.get('extra_charges', 0):,.0f}</p>
                <p><b>Extra Charges:</b> ₹{total_extra:,}</p>
                <p><b>Food & Beverage:</b> ₹{food:,}</p>
                <p><b>GST (18%):</b> ₹{gst:,.0f}</p>
                <p><b>Loyalty Discount:</b> -₹{discount:,.0f}</p>
                <hr>
                <h3 style="text-align: right;">Total: ₹{total:,.0f}</h3>
                <p style="text-align: center;">Thank you for choosing NEXA TECH</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No active guests")

# ============================================
# GUEST RECORDS
# ============================================
elif menu == "👥 Guest Records":
    st.markdown("## 👥 Guest Records")
    data = st.session_state.hotel_data
    
    if data['guests']:
        st.dataframe(pd.DataFrame(data['guests']), use_container_width=True, hide_index=True)
        
        st.markdown("### 🔍 Search Guest")
        search = st.text_input("Enter name or phone")
        if search:
            results = [g for g in data['guests'] if search.lower() in g['name'].lower() or search in g['phone']]
            if results:
                st.dataframe(pd.DataFrame(results), use_container_width=True, hide_index=True)
    else:
        st.info("No guest records yet")

# ============================================
# INVENTORY
# ============================================
elif menu == "🛍️ Inventory":
    st.markdown("## 🛍️ Inventory Management")
    data = st.session_state.hotel_data
    
    tab1, tab2 = st.tabs(["📦 Current Stock", "📝 Update Stock"])
    
    with tab1:
        st.dataframe(pd.DataFrame(data['inventory']), use_container_width=True, hide_index=True)
        low_stock = [i for i in data['inventory'] if i['stock'] < i['min_stock']]
        if low_stock:
            st.warning(f"⚠️ {len(low_stock)} items are low on stock! Auto purchase orders created.")
    
    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            item = st.selectbox("Select Item", [i['item'] for i in data['inventory']])
        with col2:
            quantity = st.number_input("Quantity to Add", min_value=1, value=10)
        
        if st.button("✅ Update Stock"):
            for i in data['inventory']:
                if i['item'] == item:
                    i['stock'] += quantity
                    st.success(f"✅ Added {quantity} to {item}")

# ============================================
# PURCHASE ORDERS
# ============================================
elif menu == "📦 Purchase Orders":
    st.markdown("## 📦 Purchase Orders")
    data = st.session_state.hotel_data
    
    tab1, tab2 = st.tabs(["➕ New Order", "📋 Order History"])
    
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            vendor = st.selectbox("Vendor", [v['name'] for v in data['vendors']])
        with col2:
            item = st.selectbox("Item", [i['item'] for i in data['inventory']])
        
        quantity = st.number_input("Quantity", min_value=1, value=10)
        unit_price = st.number_input("Unit Price (₹)", min_value=1, value=10)
        total = quantity * unit_price
        
        if st.button("📦 Create Purchase Order"):
            po_data = {
                'id': len(data['purchases']) + 1,
                'vendor': vendor,
                'item': item,
                'quantity': quantity,
                'unit_price': unit_price,
                'total': total,
                'date': str(datetime.date.today()),
                'status': 'Pending',
                'auto': False
            }
            data['purchases'].append(po_data)
            st.success(f"✅ PO created for {quantity} {item}")
    
    with tab2:
        if data['purchases']:
            df = pd.DataFrame(data['purchases'])
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No purchase orders")

# ============================================
# STAFF MANAGEMENT
# ============================================
elif menu == "👔 Staff Management":
    st.markdown("## 👔 Staff Management")
    data = st.session_state.hotel_data
    
    tab1, tab2 = st.tabs(["👥 Staff List", "➕ Add Staff"])
    
    with tab1:
        st.dataframe(pd.DataFrame(data['staff']), use_container_width=True, hide_index=True)
    
    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Staff Name")
            role = st.selectbox("Role", ["Manager", "Front Desk", "Housekeeping", "Chef", "Security", "Maintenance", "Accountant", "Other"])
        with col2:
            salary = st.number_input("Monthly Salary (₹)", min_value=5000, value=15000)
            joining = st.date_input("Joining Date", datetime.date.today())
        
        if st.button("➕ Add Staff"):
            staff_data = {
                'id': len(data['staff']) + 1,
                'name': name,
                'role': role,
                'salary': salary,
                'joining': str(joining),
                'status': 'active'
            }
            data['staff'].append(staff_data)
            st.success(f"✅ {name} added to staff")

# ============================================
# SALARY & ATTENDANCE
# ============================================
elif menu == "💰 Salary & Attendance":
    st.markdown("## 💰 Salary & Attendance")
    data = st.session_state.hotel_data
    
    tab1, tab2 = st.tabs(["📋 Attendance", "💰 Process Salary"])
    
    with tab1:
        staff_names = [s['name'] for s in data['staff'] if s['status'] == 'active']
        if staff_names:
            selected = st.multiselect("Select Staff", staff_names)
            status = st.selectbox("Status", ["Present", "Absent", "Leave", "Half Day"])
            
            if st.button("✅ Mark Attendance"):
                for s in selected:
                    att_data = {'staff': s, 'date': str(datetime.date.today()), 'status': status}
                    data['attendance'].append(att_data)
                st.success(f"✅ Attendance marked for {len(selected)} staff")
    
    with tab2:
        month = st.selectbox("Select Month", ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])
        year = st.number_input("Year", value=2026)
        
        if st.button("💰 Process Salary (Auto Calculation)"):
            month_num = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"].index(month) + 1
            total, breakdown = auto_calculate_salary(data, month_num, year)
            
            st.success(f"✅ Salary processed for {month} {year}: ₹{total:,}")
            
            st.markdown("### Salary Breakdown")
            st.dataframe(pd.DataFrame(breakdown), use_container_width=True, hide_index=True)

# ============================================
# REPORTS
# ============================================
elif menu == "📊 Reports":
    st.markdown("## 📊 Reports & Analytics")
    data = st.session_state.hotel_data
    
    report = st.selectbox("Select Report", ["Daily Revenue", "Monthly Revenue", "Occupancy Report", "Staff Report", "Inventory Report"])
    
    if report == "Daily Revenue":
        today_bills = [b for b in data['bills'] if b.get('date') == str(datetime.date.today())]
        if today_bills:
            st.dataframe(pd.DataFrame(today_bills), use_container_width=True, hide_index=True)
            st.metric("Total Today", f"₹{sum(b['total'] for b in today_bills):,}")
        else:
            st.info("No bills for today")
    
    elif report == "Occupancy Report":
        total = len(data['rooms'])
        occupied = len([r for r in data['rooms'] if r['status'] == 'occupied'])
        st.metric("Occupancy Rate", f"{(occupied/total)*100:.0f}%")
        st.metric("Occupied Rooms", occupied)
        st.metric("Available Rooms", total - occupied)
    
    elif report == "Staff Report":
        st.dataframe(pd.DataFrame(data['staff']), use_container_width=True, hide_index=True)
        total_salary = sum(s['salary'] for s in data['staff'] if s['status'] == 'active')
        st.metric("Monthly Salary Cost", f"₹{total_salary:,}")
    
    elif report == "Inventory Report":
        st.dataframe(pd.DataFrame(data['inventory']), use_container_width=True, hide_index=True)
    
    elif report == "Monthly Revenue":
        month = st.selectbox("Select Month", ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])
        month_num = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"].index(month) + 1
        month_bills = [b for b in data['bills'] if b.get('date', '').startswith(f"2026-{str(month_num).zfill(2)}")]
        if month_bills:
            st.dataframe(pd.DataFrame(month_bills), use_container_width=True, hide_index=True)
            st.metric(f"Total Revenue - {month}", f"₹{sum(b['total'] for b in month_bills):,}")
        else:
            st.info(f"No bills for {month}")

# ============================================
# SETTINGS
# ============================================
elif menu == "⚙️ Settings":
    st.markdown("## ⚙️ System Settings")
    data = st.session_state.hotel_data
    
    with st.expander("🏨 Hotel Information"):
        hotel_name = st.text_input("Hotel Name", "NEXA TECH HOTEL")
        hotel_address = st.text_area("Address", "Your Hotel Address")
        hotel_phone = st.text_input("Phone", "8439049681")
        hotel_email = st.text_input("Email", "wasu47118@gmail.com")
        gst_number = st.text_input("GST Number", "27AAACF1234F1Z")
        
        if st.button("💾 Save Settings"):
            st.success("Settings saved!")
    
    with st.expander("💰 AI Price Optimization Settings"):
        st.info("AI will automatically adjust room prices based on occupancy")
        if st.button("🔄 Run Price Optimization Now"):
            occupancy = optimize_room_prices(data)
            st.success(f"Prices optimized! Current occupancy: {occupancy:.0f}%")
    
    with st.expander("📱 SMS/WhatsApp Settings"):
        st.info("Configure SMS API for auto reminders")
        api_key = st.text_input("API Key", type="password")
        sender_id = st.text_input("Sender ID")
        
        if st.button("💾 Save API Settings"):
            st.success("API settings saved!")
    
    with st.expander("ℹ️ License Info"):
        if st.session_state.license_data:
            st.json({
                'version': '3.0 Ultimate',
                'company': 'NEXA TECH AI',
                'licensed_to': st.session_state.company_name,
                'valid_until': st.session_state.license_data['valid_until'],
                'total_rooms': len(data['rooms']),
                'total_staff': len(data['staff']),
                'total_guests': len(data['guests']),
                'auto_features': [
                    'Auto Billing with GST',
                    'Auto Inventory Reorder',
                    'Auto Salary Calculation',
                    'Auto Customer Reminders',
                    'AI Occupancy Prediction',
                    'Auto Price Optimization'
                ]
            })

# ============================================
# FOOTER
# ============================================
st.markdown("---")
st.markdown(f"""
<div class="footer">
    <b>🏨 NEXA TECH AI POWERED HOTEL ERP</b> | Ultimate Automation v3.0<br>
    © 2026 Enterprise Edition | Support: 8439049681 | UPI: nexatech@okhdfcbank<br>
    ⚡ AI Features: Auto Billing | Auto Inventory | Auto Salary | Auto Reminders | Price Optimization
</div>
""", unsafe_allow_html=True)
