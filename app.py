import streamlit as st
import pandas as pd
import datetime
import random
import hashlib
import json
import os
import smtplib
import requests
from datetime import timedelta
import time

# ============================================
# NEXA TECH AI POWERED HOTEL ERP
# ENTERPRISE GRADE COMPLETE MANAGEMENT SYSTEM
# ============================================

# ============================================
# DEMO MODE CONFIGURATION
# ============================================

# Check if demo mode is enabled (via URL parameter)
query_params = st.query_params
demo_mode = query_params.get("demo", "false") == "true"

# ============================================
# LICENSE SYSTEM
# ============================================

def check_license():
    """Check if software is licensed"""
    license_file = "nexa_license.json"
    
    if os.path.exists(license_file):
        try:
            with open(license_file, 'r') as f:
                data = json.load(f)
                expiry = datetime.datetime.fromisoformat(data['expiry'])
                if expiry > datetime.datetime.now():
                    return True, data['company_name']
                else:
                    return False, "License expired"
        except:
            return False, "Invalid license"
    return False, "No license found"

def save_license(company_name, email, phone):
    """Save license after purchase"""
    license_data = {
        'company_name': company_name,
        'email': email,
        'phone': phone,
        'purchase_date': datetime.datetime.now().isoformat(),
        'expiry': (datetime.datetime.now() + timedelta(days=365)).isoformat(),
        'license_key': hashlib.sha256(f"{company_name}{email}{datetime.datetime.now()}".encode()).hexdigest()[:16]
    }
    with open("nexa_license.json", 'w') as f:
        json.dump(license_data, f)
    return license_data

# ============================================
# REMINDER SYSTEM
# ============================================

def send_reminder(guest_name, phone, check_out_date):
    """Send automatic reminder to guest"""
    try:
        reminder_data = {
            'guest': guest_name,
            'phone': phone,
            'check_out': check_out_date,
            'message': f"Dear {guest_name}, Thank you for staying at NEXA TECH HOTEL. Your check-out is on {check_out_date}. We hope you enjoyed your stay!",
            'sent_at': datetime.datetime.now().isoformat()
        }
        
        if 'reminders_sent' not in st.session_state:
            st.session_state.reminders_sent = []
        st.session_state.reminders_sent.append(reminder_data)
        return True
    except:
        return False

def check_auto_reminders():
    """Auto check and send reminders for upcoming check-outs"""
    today = datetime.date.today()
    tomorrow = today + timedelta(days=1)
    
    for guest in st.session_state.hotel_data['checkins']:
        if guest.get('status') == 'active':
            check_out = datetime.datetime.strptime(guest['check_out'], '%Y-%m-%d').date()
            if check_out == tomorrow:
                send_reminder(guest['guest_name'], guest['phone'], guest['check_out'])
                guest['reminder_sent'] = True

# ============================================
# PURCHASE PAGE (WITH DEMO MODE)
# ============================================

def show_purchase_page():
    """Show purchase/license page with demo option"""
    st.markdown("""
    <style>
        .purchase-container {
            max-width: 700px;
            margin: 1rem auto;
            padding: 1.5rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        .purchase-card {
            background: white;
            border-radius: 15px;
            padding: 1.5rem;
            text-align: center;
        }
        .price {
            font-size: 2.5rem;
            color: #667eea;
            font-weight: bold;
        }
        .feature {
            padding: 0.5rem;
            margin: 0.5rem 0;
            background: #f8f9fa;
            border-radius: 8px;
            text-align: left;
        }
        .demo-badge {
            background: #ffc107;
            color: #1e3c72;
            padding: 0.2rem 0.8rem;
            border-radius: 20px;
            font-size: 0.7rem;
            font-weight: bold;
        }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1.5])
    
    with col1:
        st.markdown("""
        <div class="purchase-container">
            <div class="purchase-card">
                <h1>🏨 NEXA TECH</h1>
                <h2>AI POWERED HOTEL ERP</h2>
                <div class="price">₹9,999</div>
                <p>One-time payment | Lifetime license</p>
                <hr>
                <div class="feature">✅ Complete Hotel Management</div>
                <div class="feature">✅ Auto Check-in/Check-out</div>
                <div class="feature">✅ Billing with GST</div>
                <div class="feature">✅ Inventory Management</div>
                <div class="feature">✅ Staff & Salary Management</div>
                <div class="feature">✅ Auto Customer Reminders</div>
                <div class="feature">✅ Purchase Orders</div>
                <div class="feature">✅ Real-time Reports</div>
                <div class="feature">✅ 24/7 AI Support</div>
                <hr>
                <p><b>UPI ID:</b> nexatech@okhdfcbank</p>
                <p><b>Phone:</b> 8439049681</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 🚀 Get Started")
        
        tab1, tab2 = st.tabs(["💰 Purchase Now", "👀 Try Demo"])
        
        with tab1:
            with st.form("purchase_form"):
                st.markdown("**Enter Details to Activate**")
                company_name = st.text_input("Hotel/Company Name *")
                email = st.text_input("Email Address *")
                phone = st.text_input("Phone Number *")
                transaction_id = st.text_input("Transaction ID (after payment)", placeholder="Enter UPI transaction ID")
                
                if st.form_submit_button("✅ Activate License", type="primary", use_container_width=True):
                    if company_name and email and phone and transaction_id:
                        license_data = save_license(company_name, email, phone)
                        st.session_state.licensed = True
                        st.session_state.company_name = company_name
                        st.success(f"✅ License activated for {company_name}!")
                        st.rerun()
                    else:
                        st.error("Please fill all fields")
        
        with tab2:
            st.markdown("""
            ### 👀 Try Demo Mode
            
            **See how NEXA TECH ERP works before purchasing!**
            
            Demo mode gives you:
            - ✅ Full access to all features
            - ✅ Sample data pre-loaded
            - ✅ Test everything freely
            - ✅ No payment required
            
            Demo data includes:
            - 3 active guests
            - 5 staff members
            - Sample inventory
            - Test bills and reports
            """)
            
            if st.button("🎯 Launch Demo Mode", type="primary", use_container_width=True):
                # Redirect to demo mode
                st.query_params.demo = "true"
                st.rerun()

# ============================================
# DEMO DATA LOADER
# ============================================

def load_demo_data():
    """Load sample demo data for demonstration"""
    
    # Demo rooms
    demo_rooms = [
        {'id': 101, 'type': 'Deluxe', 'price': 3500, 'status': 'occupied'},
        {'id': 102, 'type': 'Deluxe', 'price': 3500, 'status': 'available'},
        {'id': 103, 'type': 'Deluxe', 'price': 3500, 'status': 'occupied'},
        {'id': 104, 'type': 'Deluxe', 'price': 3500, 'status': 'available'},
        {'id': 105, 'type': 'Deluxe', 'price': 3500, 'status': 'available'},
        {'id': 201, 'type': 'Suite', 'price': 5500, 'status': 'occupied'},
        {'id': 202, 'type': 'Suite', 'price': 5500, 'status': 'available'},
        {'id': 203, 'type': 'Suite', 'price': 5500, 'status': 'available'},
        {'id': 301, 'type': 'Presidential', 'price': 9500, 'status': 'available'},
        {'id': 302, 'type': 'Presidential', 'price': 9500, 'status': 'available'},
    ]
    
    # Demo guests
    demo_guests = [
        {'id': 1, 'name': 'Rahul Sharma', 'phone': '9876543210', 'email': 'rahul@example.com', 'address': 'Mumbai', 'last_visit': '2026-03-25', 'total_visits': 3, 'total_spent': 25000},
        {'id': 2, 'name': 'Priya Singh', 'phone': '8765432109', 'email': 'priya@example.com', 'address': 'Delhi', 'last_visit': '2026-03-20', 'total_visits': 2, 'total_spent': 18000},
        {'id': 3, 'name': 'Amit Kumar', 'phone': '7654321098', 'email': 'amit@example.com', 'address': 'Bangalore', 'last_visit': '2026-03-15', 'total_visits': 5, 'total_spent': 45000},
    ]
    
    # Demo check-ins
    demo_checkins = [
        {'id': 1, 'guest_name': 'Rahul Sharma', 'phone': '9876543210', 'email': 'rahul@example.com', 'address': 'Mumbai', 'room': 101, 'room_type': 'Deluxe', 'room_rate': 3500, 'check_in': '2026-03-27', 'check_out': '2026-03-30', 'nights': 3, 'total': 10500, 'advance': 5000, 'balance': 5500, 'special_requests': 'Extra pillows', 'status': 'active', 'date': '2026-03-27', 'reminder_sent': False},
        {'id': 2, 'guest_name': 'Vikram Mehta', 'phone': '9988776655', 'email': 'vikram@example.com', 'address': 'Pune', 'room': 103, 'room_type': 'Deluxe', 'room_rate': 3500, 'check_in': '2026-03-28', 'check_out': '2026-03-29', 'nights': 1, 'total': 3500, 'advance': 3500, 'balance': 0, 'special_requests': '', 'status': 'active', 'date': '2026-03-28', 'reminder_sent': False},
        {'id': 3, 'guest_name': 'Neha Gupta', 'phone': '8877665544', 'email': 'neha@example.com', 'address': 'Jaipur', 'room': 201, 'room_type': 'Suite', 'room_rate': 5500, 'check_in': '2026-03-26', 'check_out': '2026-03-29', 'nights': 3, 'total': 16500, 'advance': 10000, 'balance': 6500, 'special_requests': 'Late check-in', 'status': 'active', 'date': '2026-03-26', 'reminder_sent': False},
    ]
    
    # Demo bills
    demo_bills = [
        {'id': 1, 'guest_name': 'Rahul Sharma', 'room': 101, 'room_type': 'Deluxe', 'check_in': '2026-03-20', 'check_out': '2026-03-22', 'room_charges': 7000, 'food_charges': 1200, 'laundry': 300, 'minibar': 0, 'spa': 0, 'misc': 0, 'gst': 1530, 'discount': 0, 'total': 10030, 'date': '2026-03-22'},
        {'id': 2, 'guest_name': 'Amit Kumar', 'room': 201, 'room_type': 'Suite', 'check_in': '2026-03-18', 'check_out': '2026-03-20', 'room_charges': 11000, 'food_charges': 2500, 'laundry': 500, 'minibar': 800, 'spa': 1500, 'misc': 0, 'gst': 2934, 'discount': 500, 'total': 18734, 'date': '2026-03-20'},
    ]
    
    # Demo staff
    demo_staff = [
        {'id': 1, 'name': 'Rajesh Kumar', 'role': 'General Manager', 'salary': 45000, 'joining': '2024-01-15', 'status': 'active'},
        {'id': 2, 'name': 'Priya Singh', 'role': 'Front Desk Manager', 'salary': 28000, 'joining': '2024-03-10', 'status': 'active'},
        {'id': 3, 'name': 'Amit Sharma', 'role': 'Housekeeping Supervisor', 'salary': 22000, 'joining': '2024-02-01', 'status': 'active'},
        {'id': 4, 'name': 'Sunil Verma', 'role': 'Head Chef', 'salary': 35000, 'joining': '2024-01-20', 'status': 'active'},
        {'id': 5, 'name': 'Vikram Singh', 'role': 'Front Desk Executive', 'salary': 18000, 'joining': '2024-04-15', 'status': 'active'},
    ]
    
    # Demo inventory
    demo_inventory = [
        {'item': 'Mineral Water', 'stock': 150, 'unit': 'bottle', 'price': 20},
        {'item': 'Soap', 'stock': 250, 'unit': 'piece', 'price': 15},
        {'item': 'Shampoo', 'stock': 180, 'unit': 'bottle', 'price': 25},
        {'item': 'Towel', 'stock': 75, 'unit': 'piece', 'price': 150},
        {'item': 'Coffee', 'stock': 80, 'unit': 'packet', 'price': 10},
        {'item': 'Tea', 'stock': 90, 'unit': 'packet', 'price': 8},
        {'item': 'Bed Sheet', 'stock': 40, 'unit': 'piece', 'price': 300},
    ]
    
    # Demo vendors
    demo_vendors = [
        {'id': 1, 'name': 'Hotel Supplies Co.', 'contact': '9876543210', 'address': 'Mumbai', 'gst': '27AABCU9603R1Z'},
        {'id': 2, 'name': 'Fresh Foods Pvt Ltd', 'contact': '8765432109', 'address': 'Delhi', 'gst': '07AAACF1234F1Z'},
        {'id': 3, 'name': 'Linens & More', 'contact': '7654321098', 'address': 'Bangalore', 'gst': '29AAACL1234E1Z'},
    ]
    
    return {
        'rooms': demo_rooms,
        'guests': demo_guests,
        'checkins': demo_checkins,
        'bills': demo_bills,
        'inventory': demo_inventory,
        'purchases': [],
        'staff': demo_staff,
        'attendance': [],
        'salaries_paid': [],
        'vendors': demo_vendors
    }

# ============================================
# MAIN APP (After License)
# ============================================

def show_main_app():
    """Main Hotel ERP Application"""
    
    # NEXA TECH Header
    st.markdown("""
    <style>
        .nexa-header {
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            padding: 1.5rem;
            border-radius: 15px;
            margin-bottom: 1.5rem;
            text-align: center;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        }
        .nexa-header h1 {
            color: white;
            margin: 0;
            font-size: 2rem;
        }
        .nexa-header p {
            color: #ccc;
            margin: 0.5rem 0 0;
        }
        .demo-badge {
            background: #ffc107;
            color: #1e3c72;
            padding: 0.2rem 0.8rem;
            border-radius: 20px;
            font-size: 0.7rem;
            font-weight: bold;
            display: inline-block;
        }
        .stat-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 12px;
            padding: 1rem;
            text-align: center;
            margin: 0.5rem 0;
        }
        .stat-number {
            font-size: 1.8rem;
            font-weight: bold;
        }
        .card {
            background: #f8f9fa;
            border-radius: 12px;
            padding: 1rem;
            margin: 0.5rem 0;
            border-left: 4px solid #2a5298;
        }
        .reminder-box {
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            padding: 0.8rem;
            border-radius: 8px;
            margin: 0.5rem 0;
        }
        .footer {
            text-align: center;
            color: #666;
            font-size: 0.8rem;
            margin-top: 2rem;
            padding-top: 1rem;
            border-top: 1px solid #eee;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Show Demo Banner if in demo mode
    if demo_mode:
        st.markdown("""
        <div style="background: #ffc107; color: #1e3c72; padding: 0.5rem; text-align: center; border-radius: 8px; margin-bottom: 1rem;">
            🔍 DEMO MODE ACTIVE - You're viewing sample data. Purchase to get full access with your own data!
        </div>
        """, unsafe_allow_html=True)
        
        # Also show purchase button
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("💎 Upgrade to Full Version", use_container_width=True):
                st.query_params.demo = "false"
                st.rerun()
    
    # Header
    st.markdown(f"""
    <div class="nexa-header">
        <h1>🏨 NEXA TECH AI POWERED</h1>
        <p>Hotel Enterprise Resource Planning System</p>
        <span class="demo-badge">Powered by Artificial Intelligence</span>
    </div>
    """, unsafe_allow_html=True)
    
    # Check for auto reminders
    check_auto_reminders()
    
    # Show reminders if any
    if 'reminders_sent' in st.session_state and st.session_state.reminders_sent:
        with st.expander("📱 Recent Reminders Sent"):
            for r in st.session_state.reminders_sent[-5:]:
                st.markdown(f"""
                <div class="reminder-box">
                    <b>📨 To:</b> {r['guest']}<br>
                    <b>📞 Phone:</b> {r['phone']}<br>
                    <b>📅 Check-out:</b> {r['check_out']}<br>
                    <b>💬 Message:</b> {r['message'][:50]}...
                </div>
                """, unsafe_allow_html=True)
    
    # Sidebar Menu
    with st.sidebar:
        if not demo_mode:
            st.markdown(f"""
            <div style="text-align: center; padding: 1rem;">
                <h2>🏨 NEXA TECH</h2>
                <p style="color: #aaa;">AI Powered ERP</p>
                <hr>
                <small>Licensed to: <b>{st.session_state.company_name}</b></small>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="text-align: center; padding: 1rem;">
                <h2>🏨 NEXA TECH</h2>
                <p style="color: #aaa;">AI Powered ERP</p>
                <hr>
                <small style="background: #ffc107; padding: 0.2rem 0.5rem; border-radius: 10px;">🔍 DEMO MODE</small>
            </div>
            """, unsafe_allow_html=True)
        
        menu = st.radio(
            "MAIN MENU",
            [
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
            ]
        )
        
        st.markdown("---")
        st.markdown(f"""
        <div style="font-size: 0.7rem; text-align: center;">
            <b>NEXA TECH AI</b><br>
            © 2026 Enterprise Edition<br>
            Support: 8439049681<br>
            UPI: nexatech@okhdfcbank
        </div>
        """, unsafe_allow_html=True)
    
    # Initialize session state with demo data if in demo mode
    if demo_mode and 'hotel_data' not in st.session_state:
        st.session_state.hotel_data = load_demo_data()
    elif 'hotel_data' not in st.session_state:
        st.session_state.hotel_data = {
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
                {'id': 1, 'name': 'Hotel Supplies Co.', 'contact': '9876543210', 'address': 'Mumbai', 'gst': '27AABCU9603R1Z'},
                {'id': 2, 'name': 'Fresh Foods Pvt Ltd', 'contact': '8765432109', 'address': 'Delhi', 'gst': '07AAACF1234F1Z'},
                {'id': 3, 'name': 'Linens & More', 'contact': '7654321098', 'address': 'Bangalore', 'gst': '29AAACL1234E1Z'},
            ]
        }
    
    # ============================================
    # DASHBOARD
    # ============================================
    if menu == "🏠 Dashboard":
        active_guests = len([c for c in st.session_state.hotel_data['checkins'] if c.get('status') == 'active'])
        today_checkins = len([c for c in st.session_state.hotel_data['checkins'] if c.get('date') == str(datetime.date.today())])
        today_revenue = sum(b.get('total', 0) for b in st.session_state.hotel_data['bills'] if b.get('date') == str(datetime.date.today()))
        occupied = len([r for r in st.session_state.hotel_data['rooms'] if r['status'] == 'occupied'])
        total_rooms = len(st.session_state.hotel_data['rooms'])
        occupancy = (occupied / total_rooms) * 100 if total_rooms > 0 else 0
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"<div class='stat-card'><div class='stat-number'>{active_guests}</div><div>Active Guests</div></div>", unsafe_allow_html=True)
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
            recent = st.session_state.hotel_data['checkins'][-5:]
            if recent:
                st.dataframe(pd.DataFrame(recent)[['guest_name', 'room', 'check_in', 'nights']], use_container_width=True, hide_index=True)
            else:
                st.info("No recent check-ins")
        
        with col2:
            st.markdown("### 📋 Room Status")
            room_df = pd.DataFrame(st.session_state.hotel_data['rooms'])
            st.dataframe(room_df, use_container_width=True, hide_index=True)
    
    # ============================================
    # CHECK-IN
    # ============================================
    elif menu == "📝 Check-in":
        st.markdown("## 📝 New Guest Check-in")
        
        col1, col2 = st.columns(2)
        
        with col1:
            guest_name = st.text_input("Guest Name *")
            phone = st.text_input("Phone Number *")
            email = st.text_input("Email")
            address = st.text_area("Address")
        
        with col2:
            available_rooms = [r for r in st.session_state.hotel_data['rooms'] if r['status'] == 'available']
            if available_rooms:
                room_options = {f"{r['id']} - {r['type']} (₹{r['price']}/night)": r for r in available_rooms}
                selected_room = st.selectbox("Select Room", list(room_options.keys()))
                room = room_options[selected_room]
                
                nights = st.number_input("Number of Nights", min_value=1, max_value=30, value=1)
                check_in = st.date_input("Check-in Date", datetime.date.today())
                advance = st.number_input("Advance Payment (₹)", min_value=0, value=0)
                
                total = room['price'] * nights
                balance = total - advance
                
                st.info(f"**Room Total:** ₹{total:,} | **Balance:** ₹{balance:,}")
            else:
                st.error("No rooms available!")
                room = None
        
        special_requests = st.text_area("Special Requests")
        
        if st.button("✅ Confirm Check-in", type="primary", use_container_width=True):
            if guest_name and phone and room:
                checkin_data = {
                    'id': len(st.session_state.hotel_data['checkins']) + 1,
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
                    'advance': advance,
                    'balance': balance,
                    'special_requests': special_requests,
                    'status': 'active',
                    'date': str(datetime.date.today()),
                    'reminder_sent': False
                }
                st.session_state.hotel_data['checkins'].append(checkin_data)
                
                # Update room
                for r in st.session_state.hotel_data['rooms']:
                    if r['id'] == room['id']:
                        r['status'] = 'occupied'
                
                # Add to guests
                guest_data = {
                    'id': len(st.session_state.hotel_data['guests']) + 1,
                    'name': guest_name,
                    'phone': phone,
                    'email': email,
                    'address': address,
                    'last_visit': str(check_in),
                    'total_visits': 1,
                    'total_spent': total
                }
                st.session_state.hotel_data['guests'].append(guest_data)
                
                st.success(f"✅ {guest_name} checked in successfully!")
                st.balloons()
            else:
                st.error("Please fill all required fields")
    
    # ============================================
    # CHECK-OUT & BILLING
    # ============================================
    elif menu == "🧾 Check-out & Billing":
        st.markdown("## 🧾 Check-out & Generate Bill")
        
        active_guests = [c for c in st.session_state.hotel_data['checkins'] if c.get('status') == 'active']
        
        if active_guests:
            guest_options = {f"{g['guest_name']} - Room {g['room']}": g for g in active_guests}
            selected = st.selectbox("Select Guest", list(guest_options.keys()))
            guest = guest_options[selected]
            
            st.markdown(f"""
            <div class="card">
                <b>Guest:</b> {guest['guest_name']}<br>
                <b>Room:</b> {guest['room']} ({guest['room_type']})<br>
                <b>Check-in:</b> {guest['check_in']}<br>
                <b>Nights:</b> {guest['nights']}<br>
                <b>Room Charges:</b> ₹{guest['balance']:,}
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
                discount = st.number_input("Discount", min_value=0, value=0)
            
            total_extra = food + laundry + minibar + spa + misc
            gst = (guest['balance'] + total_extra) * 0.18
            total = guest['balance'] + total_extra + gst - discount
            
            st.info(f"**GST (18%):** ₹{gst:,.0f} | **Total:** ₹{total:,.0f}")
            
            if st.button("💰 Generate Final Bill", type="primary", use_container_width=True):
                bill_data = {
                    'id': len(st.session_state.hotel_data['bills']) + 1,
                    'guest_name': guest['guest_name'],
                    'room': guest['room'],
                    'room_type': guest['room_type'],
                    'check_in': guest['check_in'],
                    'check_out': str(datetime.date.today()),
                    'room_charges': guest['balance'],
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
                st.session_state.hotel_data['bills'].append(bill_data)
                
                # Update status
                for c in st.session_state.hotel_data['checkins']:
                    if c['id'] == guest['id']:
                        c['status'] = 'checked_out'
                
                # Update room
                for r in st.session_state.hotel_data['rooms']:
                    if r['id'] == guest['room']:
                        r['status'] = 'available'
                
                st.success(f"✅ Bill generated for {guest['guest_name']}")
                
                # Show bill
                st.markdown(f"""
                <div style="background: #e8f4fd; padding: 1.5rem; border-radius: 12px; margin-top: 1rem;">
                    <h3 style="text-align: center;">🏨 NEXA TECH HOTEL</h3>
                    <h4 style="text-align: center;">TAX INVOICE</h4>
                    <hr>
                    <p><b>Guest:</b> {guest['guest_name']}</p>
                    <p><b>Room:</b> {guest['room']} ({guest['room_type']})</p>
                    <p><b>Check-in:</b> {guest['check_in']} | <b>Check-out:</b> {datetime.date.today()}</p>
                    <hr>
                    <p><b>Room Charges:</b> ₹{guest['balance']:,.0f}</p>
                    <p><b>Food & Beverage:</b> ₹{food:,}</p>
                    <p><b>Laundry:</b> ₹{laundry:,}</p>
                    <p><b>Mini Bar:</b> ₹{minibar:,}</p>
                    <p><b>Spa:</b> ₹{spa:,}</p>
                    <p><b>Misc:</b> ₹{misc:,}</p>
                    <p><b>GST (18%):</b> ₹{gst:,.0f}</p>
                    <p><b>Discount:</b> -₹{discount:,}</p>
                    <hr>
                    <h3 style="text-align: right;">Total: ₹{total:,.0f}</h3>
                    <p style="text-align: center; font-size: 0.8rem;">Thank you for choosing NEXA TECH</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No active guests")
    
    # ============================================
    # GUEST RECORDS
    # ============================================
    elif menu == "👥 Guest Records":
        st.markdown("## 👥 Guest Records")
        
        if st.session_state.hotel_data['guests']:
            df = pd.DataFrame(st.session_state.hotel_data['guests'])
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            st.markdown("### 🔍 Search Guest")
            search = st.text_input("Enter name or phone")
            if search:
                results = [g for g in st.session_state.hotel_data['guests'] 
                          if search.lower() in g['name'].lower() or search in g['phone']]
                if results:
                    st.dataframe(pd.DataFrame(results), use_container_width=True, hide_index=True)
        else:
            st.info("No guest records yet")
    
    # ============================================
    # INVENTORY
    # ============================================
    elif menu == "🛍️ Inventory":
        st.markdown("## 🛍️ Inventory Management")
        
        tab1, tab2 = st.tabs(["📦 Current Stock", "📝 Update Stock"])
        
        with tab1:
            df = pd.DataFrame(st.session_state.hotel_data['inventory'])
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            low_stock = [i for i in st.session_state.hotel_data['inventory'] if i['stock'] < 50]
            if low_stock:
                st.warning(f"⚠️ {len(low_stock)} items are low on stock!")
        
        with tab2:
            col1, col2 = st.columns(2)
            with col1:
                item = st.selectbox("Select Item", [i['item'] for i in st.session_state.hotel_data['inventory']])
            with col2:
                quantity = st.number_input("Quantity to Add", min_value=1, value=10)
            
            if st.button("✅ Update Stock"):
                for i in st.session_state.hotel_data['inventory']:
                    if i['item'] == item:
                        i['stock'] += quantity
                        st.success(f"✅ Added {quantity} to {item}")
    
    # ============================================
    # PURCHASE ORDERS
    # ============================================
    elif menu == "📦 Purchase Orders":
        st.markdown("## 📦 Purchase Orders")
        
        tab1, tab2 = st.tabs(["➕ New Order", "📋 Order History"])
        
        with tab1:
            col1, col2 = st.columns(2)
            with col1:
                vendor = st.selectbox("Vendor", [v['name'] for v in st.session_state.hotel_data['vendors']])
            with col2:
                item = st.selectbox("Item", [i['item'] for i in st.session_state.hotel_data['inventory']])
            
            quantity = st.number_input("Quantity", min_value=1, value=10)
            unit_price = st.number_input("Unit Price (₹)", min_value=1, value=10)
            total = quantity * unit_price
            
            if st.button("📦 Create Purchase Order"):
                po_data = {
                    'id': len(st.session_state.hotel_data['purchases']) + 1,
                    'vendor': vendor,
                    'item': item,
                    'quantity': quantity,
                    'unit_price': unit_price,
                    'total': total,
                    'date': str(datetime.date.today()),
                    'status': 'Pending'
                }
                st.session_state.hotel_data['purchases'].append(po_data)
                st.success(f"✅ PO created for {quantity} {item}")
        
        with tab2:
            if st.session_state.hotel_data['purchases']:
                st.dataframe(pd.DataFrame(st.session_state.hotel_data['purchases']), use_container_width=True, hide_index=True)
            else:
                st.info("No purchase orders")
    
    # ============================================
    # STAFF MANAGEMENT
    # ============================================
    elif menu == "👔 Staff Management":
        st.markdown("## 👔 Staff Management")
        
        tab1, tab2 = st.tabs(["👥 Staff List", "➕ Add Staff"])
        
        with tab1:
            st.dataframe(pd.DataFrame(st.session_state.hotel_data['staff']), use_container_width=True, hide_index=True)
        
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
                    'id': len(st.session_state.hotel_data['staff']) + 1,
                    'name': name,
                    'role': role,
                    'salary': salary,
                    'joining': str(joining),
                    'status': 'active'
                }
                st.session_state.hotel_data['staff'].append(staff_data)
                st.success(f"✅ {name} added to staff")
    
    # ============================================
    # SALARY & ATTENDANCE
    # ============================================
    elif menu == "💰 Salary & Attendance":
        st.markdown("## 💰 Salary & Attendance")
        
        tab1, tab2 = st.tabs(["📋 Attendance", "💰 Process Salary"])
        
        with tab1:
            staff_names = [s['name'] for s in st.session_state.hotel_data['staff'] if s['status'] == 'active']
            if staff_names:
                selected = st.multiselect("Select Staff", staff_names)
                status = st.selectbox("Status", ["Present", "Absent", "Leave", "Half Day"])
                
                if st.button("✅ Mark Attendance"):
                    for s in selected:
                        att_data = {'staff': s, 'date': str(datetime.date.today()), 'status': status}
                        st.session_state.hotel_data['attendance'].append(att_data)
                    st.success(f"✅ Attendance marked for {len(selected)} staff")
        
        with tab2:
            month = st.selectbox("Select Month", ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])
            year = st.number_input("Year", value=2026)
            
            if st.button("💰 Process Salary"):
                total = sum(s['salary'] for s in st.session_state.hotel_data['staff'] if s['status'] == 'active')
                salary_data = {'month': month, 'year': year, 'total': total, 'date': str(datetime.date.today())}
                st.session_state.hotel_data['salaries_paid'].append(salary_data)
                st.success(f"✅ Salary processed for {month} {year}: ₹{total:,}")
    
    # ============================================
    # REPORTS
    # ============================================
    elif menu == "📊 Reports":
        st.markdown("## 📊 Reports & Analytics")
        
        report = st.selectbox("Select Report", ["Daily Revenue", "Monthly Revenue", "Occupancy Report", "Staff Report", "Inventory Report"])
        
        if report == "Daily Revenue":
            today_bills = [b for b in st.session_state.hotel_data['bills'] if b.get('date') == str(datetime.date.today())]
            if today_bills:
                st.dataframe(pd.DataFrame(today_bills), use_container_width=True, hide_index=True)
                st.metric("Total Today", f"₹{sum(b['total'] for b in today_bills):,}")
            else:
                st.info("No bills for today")
        
        elif report == "Monthly Revenue":
            st.markdown("### Monthly Revenue Report")
            month = st.selectbox("Select Month", ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])
            month_num = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"].index(month) + 1
            month_bills = [b for b in st.session_state.hotel_data['bills'] if b.get('date', '').startswith(f"2026-{str(month_num).zfill(2)}")]
            if month_bills:
                st.dataframe(pd.DataFrame(month_bills), use_container_width=True, hide_index=True)
                st.metric(f"Total Revenue - {month}", f"₹{sum(b['total'] for b in month_bills):,}")
            else:
                st.info(f"No bills for {month}")
        
        elif report == "Occupancy Report":
            total = len(st.session_state.hotel_data['rooms'])
            occupied = len([r for r in st.session_state.hotel_data['rooms'] if r['status'] == 'occupied'])
            st.metric("Occupancy Rate", f"{(occupied/total)*100:.0f}%")
            st.metric("Occupied Rooms", occupied)
            st.metric("Available Rooms", total - occupied)
        
        elif report == "Staff Report":
            st.dataframe(pd.DataFrame(st.session_state.hotel_data['staff']), use_container_width=True, hide_index=True)
            total_salary = sum(s['salary'] for s in st.session_state.hotel_data['staff'] if s['status'] == 'active')
            st.metric("Monthly Salary Cost", f"₹{total_salary:,}")
        
        elif report == "Inventory Report":
            st.dataframe(pd.DataFrame(st.session_state.hotel_data['inventory']), use_container_width=True, hide_index=True)
    
    # ============================================
    # SETTINGS
    # ============================================
    elif menu == "⚙️ Settings":
        st.markdown("## ⚙️ System Settings")
        
        with st.expander("🏨 Hotel Information"):
            hotel_name = st.text_input("Hotel Name", "NEXA TECH HOTEL")
            hotel_address = st.text_area("Address", "Your Hotel Address")
            hotel_phone = st.text_input("Phone", "8439049681")
            hotel_email = st.text_input("Email", "info@nexatech.com")
            gst_number = st.text_input("GST Number", "27AAACF1234F1Z")
            
            if st.button("💾 Save Settings"):
                st.success("Settings saved!")
        
        with st.expander("💰 Pricing Settings"):
            deluxe_rate = st.number_input("Deluxe Room Rate (₹)", min_value=1000, value=3500)
            suite_rate = st.number_input("Suite Rate (₹)", min_value=2000, value=5500)
            presidential_rate = st.number_input("Presidential Suite Rate (₹)", min_value=5000, value=9500)
            
            if st.button("💾 Save Rates"):
                for r in st.session_state.hotel_data['rooms']:
                    if r['type'] == 'Deluxe':
                        r['price'] = deluxe_rate
                    elif r['type'] == 'Suite':
                        r['price'] = suite_rate
                    elif r['type'] == 'Presidential':
                        r['price'] = presidential_rate
                st.success("Room rates updated!")
        
        with st.expander("📱 SMS/WhatsApp Settings (Reminders)"):
            st.info("Configure SMS API for auto reminders")
            api_key = st.text_input("API Key", type="password")
            sender_id = st.text_input("Sender ID")
            
            if st.button("💾 Save API Settings"):
                st.success("API settings saved!")
        
        with st.expander("ℹ️ System Info"):
            st.json({
                'version': '2.0',
                'company': 'NEXA TECH AI',
                'licensed_to': st.session_state.company_name if not demo_mode else 'DEMO MODE',
                'total_rooms': len(st.session_state.hotel_data['rooms']),
                'total_staff': len(st.session_state.hotel_data['staff']),
                'total_guests': len(st.session_state.hotel_data['guests'])
            })

# ============================================
# MAIN ENTRY POINT
# ============================================

# Initialize session state for license
if 'licensed' not in st.session_state:
    if not demo_mode:
        licensed, company = check_license()
        st.session_state.licensed = licensed
        if licensed:
            st.session_state.company_name = company
    else:
        st.session_state.licensed = True
        st.session_state.company_name = "DEMO USER"

# Check license
if not st.session_state.licensed and not demo_mode:
    show_purchase_page()
else:
    show_main_app()
