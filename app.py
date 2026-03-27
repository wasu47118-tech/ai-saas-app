import streamlit as st
import pandas as pd
import datetime
import random
import hashlib
import json
import os
from datetime import timedelta

# ============================================
# HOTEL ERP - COMPLETE MANAGEMENT SYSTEM
# ENTERPRISE GRADE AI AUTOMATION
# ============================================

# Page config
st.set_page_config(
    page_title="Hotel ERP System",
    page_icon="🏨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .stApp {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    }
    
    .main-container {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        margin: 0.5rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .dashboard-header {
        background: linear-gradient(135deg, #1e3c72, #2a5298);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .dashboard-header h1 {
        font-size: 2rem;
        margin: 0;
    }
    
    .stat-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 15px;
        padding: 1rem;
        text-align: center;
        margin: 0.5rem 0;
    }
    
    .stat-number {
        font-size: 2rem;
        font-weight: bold;
    }
    
    .card {
        background: #f8f9fa;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 4px solid #2a5298;
    }
    
    .alert {
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
    
    /* Table styling */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background: #1e3c72;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# DATABASE INITIALIZATION
# ============================================

if 'hotel_data' not in st.session_state:
    st.session_state.hotel_data = {
        'guests': [],
        'rooms': [
            {'id': 101, 'type': 'Deluxe', 'price': 3500, 'status': 'available'},
            {'id': 102, 'type': 'Deluxe', 'price': 3500, 'status': 'available'},
            {'id': 103, 'type': 'Deluxe', 'price': 3500, 'status': 'available'},
            {'id': 201, 'type': 'Suite', 'price': 5500, 'status': 'available'},
            {'id': 202, 'type': 'Suite', 'price': 5500, 'status': 'available'},
            {'id': 203, 'type': 'Presidential', 'price': 9500, 'status': 'available'},
        ],
        'checkins': [],
        'checkouts': [],
        'bills': [],
        'inventory': [
            {'item': 'Mineral Water', 'stock': 100, 'unit': 'bottle', 'price': 20},
            {'item': 'Soap', 'stock': 200, 'unit': 'piece', 'price': 15},
            {'item': 'Shampoo', 'stock': 150, 'unit': 'bottle', 'price': 25},
            {'item': 'Towel', 'stock': 80, 'unit': 'piece', 'price': 150},
            {'item': 'Coffee', 'stock': 50, 'unit': 'packet', 'price': 10},
        ],
        'purchases': [],
        'staff': [
            {'id': 1, 'name': 'Rajesh Kumar', 'role': 'Manager', 'salary': 35000, 'joining': '2024-01-15', 'status': 'active'},
            {'id': 2, 'name': 'Priya Singh', 'role': 'Front Desk', 'salary': 18000, 'joining': '2024-03-10', 'status': 'active'},
            {'id': 3, 'name': 'Amit Sharma', 'role': 'Housekeeping', 'salary': 15000, 'joining': '2024-02-01', 'status': 'active'},
            {'id': 4, 'name': 'Sunil Verma', 'role': 'Chef', 'salary': 25000, 'joining': '2024-01-20', 'status': 'active'},
        ],
        'attendance': [],
        'salaries_paid': [],
        'vendors': [
            {'id': 1, 'name': 'Hotel Supplies Co.', 'contact': '9876543210', 'address': 'Mumbai'},
            {'id': 2, 'name': 'Fresh Foods Pvt Ltd', 'contact': '8765432109', 'address': 'Delhi'},
        ],
        'expenses': []
    }

# ============================================
# SIDEBAR - MAIN MENU
# ============================================

with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1rem;">
        <h2>🏨 HOTEL ERP</h2>
        <p style="color: #aaa;">Enterprise Resource Planning</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    menu = st.radio(
        "MAIN MENU",
        [
            "🏠 Dashboard",
            "📝 Check-in",
            "🧾 Check-out & Billing",
            "👥 Guest Records",
            "🛍️ Inventory",
            "📦 Purchases",
            "👔 Staff Management",
            "💰 Salary & Attendance",
            "📊 Reports & Analytics"
        ]
    )
    
    st.markdown("---")
    st.markdown(f"""
    <div style="font-size: 0.8rem; text-align: center;">
        <b>AI Hotel ERP</b><br>
        © 2026 Enterprise Edition<br>
        UPI: 8439049681@pthdfc
    </div>
    """, unsafe_allow_html=True)

# ============================================
# DASHBOARD
# ============================================
if menu == "🏠 Dashboard":
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="dashboard-header">
        <h1>🏨 HOTEL ERP DASHBOARD</h1>
        <p>Real-time hotel management system | Powered by AI</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats
    col1, col2, col3, col4 = st.columns(4)
    
    active_guests = len([c for c in st.session_state.hotel_data['checkins'] if c.get('status') == 'active'])
    today_checkins = len([c for c in st.session_state.hotel_data['checkins'] if c.get('date') == str(datetime.date.today())])
    today_revenue = sum(b.get('total', 0) for b in st.session_state.hotel_data['bills'] if b.get('date') == str(datetime.date.today()))
    occupancy = len([r for r in st.session_state.hotel_data['rooms'] if r['status'] == 'occupied']) / len(st.session_state.hotel_data['rooms']) * 100
    
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{active_guests}</div>
            <div>Active Guests</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{today_checkins}</div>
            <div>Today's Check-ins</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">₹{today_revenue:,}</div>
            <div>Today's Revenue</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-number">{occupancy:.0f}%</div>
            <div>Occupancy Rate</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Recent Activity
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🧾 Recent Check-ins")
        recent_checkins = st.session_state.hotel_data['checkins'][-5:]
        if recent_checkins:
            df = pd.DataFrame(recent_checkins)
            st.dataframe(df[['guest_name', 'room', 'check_in', 'nights', 'total']], use_container_width=True, hide_index=True)
        else:
            st.info("No recent check-ins")
    
    with col2:
        st.markdown("### 📋 Today's Bills")
        today_bills = [b for b in st.session_state.hotel_data['bills'] if b.get('date') == str(datetime.date.today())]
        if today_bills:
            df = pd.DataFrame(today_bills)
            st.dataframe(df[['guest_name', 'room', 'total']], use_container_width=True, hide_index=True)
        else:
            st.info("No bills today")
    
    # Room Status
    st.markdown("### 🛏️ Room Status")
    room_df = pd.DataFrame(st.session_state.hotel_data['rooms'])
    st.dataframe(room_df, use_container_width=True, hide_index=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# CHECK-IN
# ============================================
elif menu == "📝 Check-in":
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    st.markdown("## 📝 New Guest Check-in")
    
    col1, col2 = st.columns(2)
    
    with col1:
        guest_name = st.text_input("Guest Name *", placeholder="Full name")
        phone = st.text_input("Phone Number *", placeholder="10 digit number")
        email = st.text_input("Email", placeholder="Optional")
        address = st.text_area("Address", placeholder="Guest address")
        
    with col2:
        # Available rooms
        available_rooms = [r for r in st.session_state.hotel_data['rooms'] if r['status'] == 'available']
        room_options = {f"{r['id']} - {r['type']} (₹{r['price']}/night)": r for r in available_rooms}
        
        if room_options:
            selected_room = st.selectbox("Select Room", list(room_options.keys()))
            room = room_options[selected_room]
            
            nights = st.number_input("Number of Nights", min_value=1, max_value=30, value=1)
            check_in = st.date_input("Check-in Date", datetime.date.today())
            advance = st.number_input("Advance Payment (₹)", min_value=0, value=0)
            
            total_amount = room['price'] * nights
            balance = total_amount - advance
            
            st.info(f"""
            **Room Charges:** ₹{room['price']} x {nights} nights = ₹{total_amount:,}
            **Advance Paid:** ₹{advance:,}
            **Balance:** ₹{balance:,}
            """)
        else:
            st.error("No rooms available!")
            room = None
    
    special_requests = st.text_area("Special Requests", placeholder="Any special requests?")
    
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
                'nights': nights,
                'check_out': str(check_in + timedelta(days=nights)),
                'total': total_amount,
                'advance': advance,
                'balance': balance,
                'special_requests': special_requests,
                'status': 'active',
                'date': str(datetime.date.today())
            }
            st.session_state.hotel_data['checkins'].append(checkin_data)
            
            # Update room status
            for r in st.session_state.hotel_data['rooms']:
                if r['id'] == room['id']:
                    r['status'] = 'occupied'
            
            # Add to guests database
            guest_data = {
                'id': len(st.session_state.hotel_data['guests']) + 1,
                'name': guest_name,
                'phone': phone,
                'email': email,
                'address': address,
                'last_visit': str(check_in),
                'total_visits': 1,
                'total_spent': total_amount
            }
            st.session_state.hotel_data['guests'].append(guest_data)
            
            st.success(f"✅ {guest_name} checked in successfully!")
            st.balloons()
        else:
            st.error("Please fill all required fields")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# CHECK-OUT & BILLING
# ============================================
elif menu == "🧾 Check-out & Billing":
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
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
            <b>Check-out:</b> {guest['check_out']}<br>
            <b>Room Charges:</b> ₹{guest['room_rate']} x {guest['nights']} = ₹{guest['total']:,}<br>
            <b>Advance Paid:</b> ₹{guest['advance']:,}<br>
            <b>Balance:</b> ₹{guest['balance']:,}
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 💰 Additional Charges")
        
        col1, col2 = st.columns(2)
        with col1:
            food_charges = st.number_input("Food & Beverage", min_value=0, value=0)
            laundry = st.number_input("Laundry", min_value=0, value=0)
            minibar = st.number_input("Mini Bar", min_value=0, value=0)
        with col2:
            spa = st.number_input("Spa Services", min_value=0, value=0)
            misc = st.number_input("Miscellaneous", min_value=0, value=0)
            discount = st.number_input("Discount", min_value=0, value=0)
        
        gst = (guest['balance'] + food_charges + laundry + minibar + spa + misc) * 0.18
        total = guest['balance'] + food_charges + laundry + minibar + spa + misc + gst - discount
        
        st.info(f"""
        **GST (18%):** ₹{gst:,.0f}
        **Total Amount:** ₹{total:,.0f}
        """)
        
        if st.button("💰 Generate Final Bill", type="primary", use_container_width=True):
            bill_data = {
                'id': len(st.session_state.hotel_data['bills']) + 1,
                'guest_name': guest['guest_name'],
                'room': guest['room'],
                'room_type': guest['room_type'],
                'check_in': guest['check_in'],
                'check_out': str(datetime.date.today()),
                'room_charges': guest['balance'],
                'food_charges': food_charges,
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
            
            # Update guest status
            for c in st.session_state.hotel_data['checkins']:
                if c['id'] == guest['id']:
                    c['status'] = 'checked_out'
                    c['actual_checkout'] = str(datetime.date.today())
            
            # Update room status
            for r in st.session_state.hotel_data['rooms']:
                if r['id'] == guest['room']:
                    r['status'] = 'available'
            
            st.success(f"✅ Bill generated for {guest['guest_name']}")
            
            # Print bill
            st.markdown(f"""
            <div style="background: #e8f4fd; padding: 1.5rem; border-radius: 12px; margin-top: 1rem;">
                <h2 style="text-align: center;">🏨 HOTEL INVOICE</h2>
                <hr>
                <p><b>Guest:</b> {guest['guest_name']}</p>
                <p><b>Room:</b> {guest['room']} ({guest['room_type']})</p>
                <p><b>Check-in:</b> {guest['check_in']} | <b>Check-out:</b> {datetime.date.today()}</p>
                <hr>
                <p><b>Room Charges:</b> ₹{guest['balance']:,.0f}</p>
                <p><b>Food & Beverage:</b> ₹{food_charges:,}</p>
                <p><b>Laundry:</b> ₹{laundry:,}</p>
                <p><b>Mini Bar:</b> ₹{minibar:,}</p>
                <p><b>Spa:</b> ₹{spa:,}</p>
                <p><b>Misc:</b> ₹{misc:,}</p>
                <p><b>GST (18%):</b> ₹{gst:,.0f}</p>
                <p><b>Discount:</b> -₹{discount:,}</p>
                <hr>
                <h3 style="text-align: right;">Total: ₹{total:,.0f}</h3>
                <p style="text-align: center; font-size: 0.8rem;">Thank you for staying with us!</p>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No active guests")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# GUEST RECORDS
# ============================================
elif menu == "👥 Guest Records":
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
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
                
                # Guest history
                selected_guest = results[0]['name']
                guest_visits = [c for c in st.session_state.hotel_data['checkins'] 
                               if c.get('guest_name') == selected_guest]
                if guest_visits:
                    st.markdown("### 📋 Visit History")
                    st.dataframe(pd.DataFrame(guest_visits), use_container_width=True, hide_index=True)
    else:
        st.info("No guest records yet")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# INVENTORY
# ============================================
elif menu == "🛍️ Inventory":
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    st.markdown("## 🛍️ Inventory Management")
    
    tab1, tab2 = st.tabs(["📦 Current Stock", "📝 Update Stock"])
    
    with tab1:
        df = pd.DataFrame(st.session_state.hotel_data['inventory'])
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Low stock alert
        low_stock = [i for i in st.session_state.hotel_data['inventory'] if i['stock'] < 50]
        if low_stock:
            st.warning(f"⚠️ {len(low_stock)} items are running low on stock!")
            st.dataframe(pd.DataFrame(low_stock), use_container_width=True, hide_index=True)
    
    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            item = st.selectbox("Select Item", [i['item'] for i in st.session_state.hotel_data['inventory']])
        with col2:
            quantity = st.number_input("Quantity to Add", min_value=1, value=10)
        
        if st.button("Update Stock"):
            for i in st.session_state.hotel_data['inventory']:
                if i['item'] == item:
                    i['stock'] += quantity
                    st.success(f"✅ Added {quantity} {i['unit']}(s) to {item}")
                    break
    
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# PURCHASES
# ============================================
elif menu == "📦 Purchases":
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    st.markdown("## 📦 Purchase Orders")
    
    tab1, tab2 = st.tabs(["➕ New Purchase", "📋 Purchase History"])
    
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
            purchase_data = {
                'id': len(st.session_state.hotel_data['purchases']) + 1,
                'vendor': vendor,
                'item': item,
                'quantity': quantity,
                'unit_price': unit_price,
                'total': total,
                'date': str(datetime.date.today())
            }
            st.session_state.hotel_data['purchases'].append(purchase_data)
            st.success(f"✅ Purchase order created for {quantity} {item}")
    
    with tab2:
        if st.session_state.hotel_data['purchases']:
            df = pd.DataFrame(st.session_state.hotel_data['purchases'])
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No purchase history")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# STAFF MANAGEMENT
# ============================================
elif menu == "👔 Staff Management":
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    st.markdown("## 👔 Staff Management")
    
    tab1, tab2 = st.tabs(["👥 Staff List", "➕ Add Staff"])
    
    with tab1:
        df = pd.DataFrame(st.session_state.hotel_data['staff'])
        st.dataframe(df, use_container_width=True, hide_index=True)
    
    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Staff Name")
            role = st.selectbox("Role", ["Manager", "Front Desk", "Housekeeping", "Chef", "Security", "Maintenance"])
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
    
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# SALARY & ATTENDANCE
# ============================================
elif menu == "💰 Salary & Attendance":
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    st.markdown("## 💰 Salary & Attendance")
    
    tab1, tab2 = st.tabs(["📋 Attendance", "💰 Process Salary"])
    
    with tab1:
        st.markdown("### Mark Attendance")
        staff_names = [s['name'] for s in st.session_state.hotel_data['staff'] if s['status'] == 'active']
        
        if staff_names:
            selected_staff = st.multiselect("Select Staff", staff_names)
            status = st.selectbox("Status", ["Present", "Absent", "Leave", "Half Day"])
            
            if st.button("✅ Mark Attendance"):
                for staff in selected_staff:
                    attendance_data = {
                        'staff': staff,
                        'date': str(datetime.date.today()),
                        'status': status
                    }
                    st.session_state.hotel_data['attendance'].append(attendance_data)
                st.success(f"✅ Attendance marked for {len(selected_staff)} staff")
        else:
            st.info("No active staff")
    
    with tab2:
        st.markdown("### Process Monthly Salary")
        month = st.selectbox("Select Month", ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])
        year = st.number_input("Year", value=2026)
        
        if st.button("💰 Process Salary"):
            total_salary = 0
            for staff in st.session_state.hotel_data['staff']:
                if staff['status'] == 'active':
                    total_salary += staff['salary']
            
            salary_data = {
                'month': month,
                'year': year,
                'total_salary': total_salary,
                'date': str(datetime.date.today())
            }
            st.session_state.hotel_data['salaries_paid'].append(salary_data)
            
            st.success(f"✅ Salary processed for {month} {year}: ₹{total_salary:,}")
            
            # Show breakdown
            st.markdown("### Salary Breakdown")
            salary_df = pd.DataFrame([{'Staff': s['name'], 'Role': s['role'], 'Salary': s['salary']} 
                                     for s in st.session_state.hotel_data['staff'] if s['status'] == 'active'])
            st.dataframe(salary_df, use_container_width=True, hide_index=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# ============================================
# REPORTS & ANALYTICS
# ============================================
elif menu == "📊 Reports & Analytics":
    st.markdown('<div class="main-container">', unsafe_allow_html=True)
    
    st.markdown("## 📊 Reports & Analytics")
    
    report_type = st.selectbox("Select Report", ["Daily Revenue", "Monthly Revenue", "Occupancy Report", "Staff Report", "Inventory Report"])
    
    if report_type == "Daily Revenue":
        st.markdown("### Daily Revenue Report")
        
        # Get today's date
        today = str(datetime.date.today())
        
        # Today's bills
        today_bills = [b for b in st.session_state.hotel_data['bills'] if b.get('date') == today]
        
        if today_bills:
            df = pd.DataFrame(today_bills)
            st.dataframe(df, use_container_width=True, hide_index=True)
            total_revenue = sum(b['total'] for b in today_bills)
            st.metric("Total Revenue Today", f"₹{total_revenue:,}")
        else:
            st.info("No bills for today")
        
        # Today's check-ins
        today_checkins = [c for c in st.session_state.hotel_data['checkins'] if c.get('date') == today]
        if today_checkins:
            st.markdown("### Today's Check-ins")
            st.dataframe(pd.DataFrame(today_checkins), use_container_width=True, hide_index=True)
    
    elif report_type == "Monthly Revenue":
        st.markdown("### Monthly Revenue Report")
        
        month = st.selectbox("Select Month", ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"])
        
        # Filter bills by month (simplified)
        monthly_bills = [b for b in st.session_state.hotel_data['bills'] if b.get('date', '').startswith(f"2026-{str(month).zfill(2)}")]
        
        if monthly_bills:
            df = pd.DataFrame(monthly_bills)
            st.dataframe(df, use_container_width=True, hide_index=True)
            total = sum(b['total'] for b in monthly_bills)
            st.metric(f"Total Revenue - {month}", f"₹{total:,}")
        else:
            st.info(f"No bills for {month}")
    
    elif report_type == "Occupancy Report":
        st.markdown("### Occupancy Report")
        
        total_rooms = len(st.session_state.hotel_data['rooms'])
        occupied = len([r for r in st.session_state.hotel_data['rooms'] if r['status'] == 'occupied'])
        available = total_rooms - occupied
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Rooms", total_rooms)
        with col2:
            st.metric("Occupied", occupied)
        with col3:
            st.metric("Available", available)
        
        # Room type breakdown
        st.markdown("### Room Type Breakdown")
        room_types = {}
        for r in st.session_state.hotel_data['rooms']:
            if r['type'] not in room_types:
                room_types[r['type']] = {'total': 0, 'occupied': 0}
            room_types[r['type']]['total'] += 1
            if r['status'] == 'occupied':
                room_types[r['type']]['occupied'] += 1
        
        for room_type, stats in room_types.items():
            st.markdown(f"**{room_type}:** {stats['occupied']}/{stats['total']} occupied")
    
    elif report_type == "Staff Report":
        st.markdown("### Staff Report")
        
        st.dataframe(pd.DataFrame(st.session_state.hotel_data['staff']), use_container_width=True, hide_index=True)
        
        total_salary = sum(s['salary'] for s in st.session_state.hotel_data['staff'] if s['status'] == 'active')
        st.metric("Monthly Salary Cost", f"₹{total_salary:,}")
    
    elif report_type == "Inventory Report":
        st.markdown("### Inventory Report")
        
        st.dataframe(pd.DataFrame(st.session_state.hotel_data['inventory']), use_container_width=True, hide_index=True)
        
        low_stock = [i for i in st.session_state.hotel_data['inventory'] if i['stock'] < 50]
        if low_stock:
            st.warning(f"⚠️ Low stock items: {len(low_stock)}")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<style>
    .footer {
        text-align: center;
        padding: 1rem;
        color: #666;
        font-size: 0.8rem;
        margin-top: 2rem;
    }
</style>
<div class="footer">
    <b>🏨 HOTEL ERP SYSTEM</b> | AI-Powered Hotel Management<br>
    © 2026 Enterprise Edition | Support: 8439049681 | UPI: 8439049681@pthdfc
</div>
""", unsafe_allow_html=True)
