import streamlit as st
import requests
import feedparser
import json
import time
import threading
import hashlib
import re
from datetime import datetime, timedelta
import pandas as pd
import random

# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(
    page_title="NEXA NEWS AI | Agra News Alert",
    page_icon="📰",
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
# CONFIGURATION
# ============================================
ADMIN_EMAIL = "wasu47118@gmail.com"
ADMIN_PASSWORD = "Wasu1234$"
UPI_ID = "8439049681@pthdfc"
PHONE = "8439049681"

# Categories
CATEGORIES = {
    "all": "📰 All News",
    "crime": "🚨 Crime",
    "cyber": "💻 Cyber Crime",
    "business": "📊 Business",
    "technology": "📱 Technology",
    "sports": "⚽ Sports",
    "entertainment": "🎬 Entertainment",
    "politics": "🏛️ Politics",
    "health": "🏥 Health",
    "auto": "🚗 Auto",
    "education": "📚 Education",
    "local": "🏘️ Local Agra"
}

# ============================================
# DATABASE
# ============================================
if 'subscribers' not in st.session_state:
    st.session_state.subscribers = []

if 'news_history' not in st.session_state:
    st.session_state.news_history = []

if 'sent_news' not in st.session_state:
    st.session_state.sent_news = set()

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_type = None
    st.session_state.user_data = None

# ============================================
# AGRA NEWS FETCHER (MULTIPLE SOURCES)
# ============================================
def fetch_agra_news():
    """Fetch news from multiple sources - only AGRA"""
    all_news = []
    seen_titles = set()
    
    # Source 1: Google News RSS (Agra)
    try:
        url = "https://news.google.com/rss/search?q=Agra+India&hl=en-IN&gl=IN&ceid=IN:en"
        feed = feedparser.parse(url)
        for entry in feed.entries[:10]:
            title = entry.title
            if "agra" in title.lower() or "agra" in entry.get('summary', '').lower():
                if title not in seen_titles:
                    seen_titles.add(title)
                    all_news.append({
                        'title': title,
                        'summary': entry.get('summary', '')[:200],
                        'link': entry.link,
                        'source': 'Google News',
                        'time': datetime.now().strftime('%H:%M:%S'),
                        'date': datetime.now().strftime('%Y-%m-%d')
                    })
    except:
        pass
    
    # Source 2: NewsAPI (Agra)
    try:
        # Free API - limited requests
        api_key = "YOUR_NEWSAPI_KEY"  # Get free from newsapi.org
        url = f"https://newsapi.org/v2/everything?q=Agra&language=en&sortBy=publishedAt&apiKey={api_key}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            for article in data.get('articles', [])[:10]:
                title = article.get('title', '')
                if title and title not in seen_titles:
                    seen_titles.add(title)
                    all_news.append({
                        'title': title,
                        'summary': article.get('description', '')[:200],
                        'link': article.get('url', ''),
                        'source': 'NewsAPI',
                        'time': datetime.now().strftime('%H:%M:%S'),
                        'date': article.get('publishedAt', '')[:10]
                    })
    except:
        pass
    
    # Source 3: Times of India (Agra)
    try:
        url = "https://timesofindia.indiatimes.com/rssfeeds/-2128936835.cms"
        feed = feedparser.parse(url)
        for entry in feed.entries[:10]:
            title = entry.title
            if "agra" in title.lower():
                if title not in seen_titles:
                    seen_titles.add(title)
                    all_news.append({
                        'title': title,
                        'summary': entry.get('summary', '')[:200],
                        'link': entry.link,
                        'source': 'Times of India',
                        'time': datetime.now().strftime('%H:%M:%S'),
                        'date': datetime.now().strftime('%Y-%m-%d')
                    })
    except:
        pass
    
    # Source 4: Amar Ujala (Agra in Hindi)
    try:
        url = "https://www.amarujala.com/rss/agra.xml"
        feed = feedparser.parse(url)
        for entry in feed.entries[:10]:
            title = entry.title
            if title not in seen_titles:
                seen_titles.add(title)
                all_news.append({
                    'title': title,
                    'summary': entry.get('summary', '')[:200],
                    'link': entry.link,
                    'source': 'Amar Ujala',
                    'time': datetime.now().strftime('%H:%M:%S'),
                    'date': datetime.now().strftime('%Y-%m-%d')
                })
    except:
        pass
    
    # Source 5: Hindustan (Agra)
    try:
        url = "https://www.livehindustan.com/rss/agra/feed.rss"
        feed = feedparser.parse(url)
        for entry in feed.entries[:10]:
            title = entry.title
            if title not in seen_titles:
                seen_titles.add(title)
                    all_news.append({
                        'title': title,
                        'summary': entry.get('summary', '')[:200],
                        'link': entry.link,
                        'source': 'Hindustan',
                        'time': datetime.now().strftime('%H:%M:%S'),
                        'date': datetime.now().strftime('%Y-%m-%d')
                    })
    except:
        pass
    
    # Categorize news
    for news in all_news:
        news['category'] = categorize_news(news['title'] + ' ' + news['summary'])
    
    return all_news

def categorize_news(text):
    """Auto categorize news based on keywords"""
    text_lower = text.lower()
    
    if any(word in text_lower for word in ['crime', 'murder', 'theft', 'robbery', 'kidnap', 'rape', 'arrest', 'accused']):
        return "crime"
    elif any(word in text_lower for word in ['cyber', 'hack', 'fraud', 'scam', 'online', 'digital', 'phishing']):
        return "cyber"
    elif any(word in text_lower for word in ['business', 'market', 'economy', 'company', 'startup', 'investment', 'stock']):
        return "business"
    elif any(word in text_lower for word in ['tech', 'technology', 'app', 'software', 'ai', 'digital', 'smartphone']):
        return "technology"
    elif any(word in text_lower for word in ['sports', 'cricket', 'football', 'match', 'tournament', 'player', 'team']):
        return "sports"
    elif any(word in text_lower for word in ['film', 'movie', 'actor', 'actress', 'celebrity', 'bollywood', 'entertainment']):
        return "entertainment"
    elif any(word in text_lower for word in ['politics', 'election', 'minister', 'government', 'party', 'bjp', 'congress']):
        return "politics"
    elif any(word in text_lower for word in ['health', 'hospital', 'doctor', 'disease', 'covid', 'treatment', 'vaccine']):
        return "health"
    elif any(word in text_lower for word in ['car', 'auto', 'vehicle', 'bike', 'transport', 'road', 'traffic']):
        return "auto"
    elif any(word in text_lower for word in ['school', 'college', 'education', 'student', 'exam', 'university']):
        return "education"
    else:
        return "local"

def send_whatsapp_message(phone, message):
    """Send WhatsApp message (using pywhatkit or similar)"""
    try:
        # Method 1: PyWhatKit (requires web.whatsapp.com open)
        import pywhatkit as kit
        # Send instantly
        kit.sendwhatmsg_instantly(phone, message, wait_time=15)
        return True
    except:
        try:
            # Method 2: Using requests (if you have WhatsApp API)
            # api_url = "https://api.whatsapp.com/send?phone=" + phone + "&text=" + message
            # webbrowser.open(api_url)
            return False
        except:
            return False

def send_news_to_subscribers(news):
    """Send news to all subscribers"""
    message = f"""📰 *NEXA NEWS ALERT*
    
📍 *Agra News Update*
🏷️ Category: {CATEGORIES.get(news['category'], '📰 News')}

*{news['title']}*

{news['summary']}

🔗 Read more: {news['link']}
⏰ Time: {news['time']}
📅 Date: {news['date']}
📡 Source: {news['source']}

---
⚡ Powered by NEXA NEWS AI
💬 Reply STOP to unsubscribe
    """
    
    for sub in st.session_state.subscribers:
        if sub.get('active', True):
            send_whatsapp_message(sub['phone'], message)
    
    # Add to sent history
    st.session_state.sent_news.add(news['title'])
    st.session_state.news_history.append({
        'title': news['title'],
        'sent_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'category': news['category']
    })

def check_new_news():
    """Background thread to check new news every 2 minutes"""
    while True:
        try:
            news_list = fetch_agra_news()
            for news in news_list:
                if news['title'] not in st.session_state.sent_news:
                    send_news_to_subscribers(news)
            time.sleep(120)  # Check every 2 minutes
        except:
            time.sleep(60)

# ============================================
# SUBSCRIPTION PAGE
# ============================================
def show_subscription_page():
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); padding: 2rem; border-radius: 20px; text-align: center; margin-bottom: 2rem;">
        <h1 style="color: white;">📰 NEXA NEWS AI</h1>
        <p style="color: white;">Agra's Fastest News Alert System</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1.5])
    
    with col1:
        st.markdown("""
        <div style="background: white; padding: 1.5rem; border-radius: 15px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
            <h2 style="color: #1e3c72;">🎯 Features</h2>
            <p>✅ <b>Only Agra News</b> - 100% relevant</p>
            <p>✅ <b>Real-time Alerts</b> - Every 2-3 minutes</p>
            <p>✅ <b>No Duplicates</b> - One news, once</p>
            <p>✅ <b>Multiple Sources</b> - 5+ news sources</p>
            <p>✅ <b>Category Wise</b> - Choose your interest</p>
            <p>✅ <b>24/7 Service</b> - Never miss news</p>
            
            <div style="background: #e8f4fd; padding: 1rem; border-radius: 10px; margin-top: 1rem;">
                <h3>💰 ₹100/month</h3>
                <p>Cancel anytime • No hidden charges</p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 🔐 Subscribe Now")
        
        with st.form("subscribe_form"):
            name = st.text_input("Full Name *")
            phone = st.text_input("WhatsApp Number *", placeholder="+91XXXXXXXXXX")
            categories = st.multiselect("Select News Categories", list(CATEGORIES.values()), default=["📰 All News"])
            
            # Convert selected categories to keys
            selected_keys = [k for k, v in CATEGORIES.items() if v in categories]
            
            agree = st.checkbox("I agree to receive news alerts on WhatsApp")
            
            if st.form_submit_button("💰 Subscribe - ₹100/month", use_container_width=True, type="primary"):
                if name and phone and agree:
                    # Store subscriber
                    subscriber = {
                        'id': len(st.session_state.subscribers) + 1,
                        'name': name,
                        'phone': phone,
                        'categories': selected_keys,
                        'active': True,
                        'subscribed_date': datetime.now().strftime('%Y-%m-%d'),
                        'payment_status': 'pending'
                    }
                    st.session_state.subscribers.append(subscriber)
                    
                    # Show payment QR
                    st.info(f"💳 Pay ₹100 to UPI: {UPI_ID}")
                    st.success("✅ After payment, service will be activated!")
                    
                    # Show QR code (optional)
                    st.markdown("""
                    <div style="text-align: center;">
                        <p>Scan to Pay</p>
                        <img src="https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=upi://pay?pa=8439049681@pthdfc&pn=NEXA%20NEWS&am=100&cu=INR" width="200">
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.error("Please fill all required fields")

# ============================================
# ADMIN DASHBOARD
# ============================================
def show_admin_dashboard():
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); padding: 1rem; border-radius: 15px; margin-bottom: 1rem;">
        <h2 style="color: white;">👑 ADMIN DASHBOARD</h2>
        <p style="color: white;">News Alerts | Subscribers | Analytics</p>
    </div>
    """, unsafe_allow_html=True)
    
    total_subs = len(st.session_state.subscribers)
    total_news = len(st.session_state.sent_news)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📱 Subscribers", total_subs)
    with col2:
        st.metric("📰 News Sent", total_news)
    with col3:
        st.metric("🕐 Update Frequency", "2 minutes")
    with col4:
        st.metric("📡 Sources Active", "5")
    
    st.markdown("---")
    
    tab1, tab2, tab3 = st.tabs(["📱 Subscribers", "📰 News History", "⚙️ Settings"])
    
    with tab1:
        if st.session_state.subscribers:
            df = pd.DataFrame(st.session_state.subscribers)
            st.dataframe(df, use_container_width=True, hide_index=True)
            
            # Manual send option
            st.markdown("### 📤 Manual News Send")
            news_title = st.text_input("News Title")
            news_content = st.text_area("News Content")
            if st.button("Send to All Subscribers"):
                for sub in st.session_state.subscribers:
                    msg = f"📰 *NEXA NEWS ALERT*\n\n{news_title}\n\n{news_content}"
                    send_whatsapp_message(sub['phone'], msg)
                st.success("News sent to all subscribers!")
        else:
            st.info("No subscribers yet")
    
    with tab2:
        if st.session_state.news_history:
            df = pd.DataFrame(st.session_state.news_history[-50:])
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No news sent yet")
    
    with tab3:
        st.markdown("### ⚙️ System Settings")
        
        # Test WhatsApp
        st.markdown("#### 📱 Test WhatsApp")
        test_phone = st.text_input("Test Phone Number")
        test_msg = st.text_area("Test Message", "This is a test message from NEXA NEWS AI")
        if st.button("Send Test"):
            send_whatsapp_message(test_phone, test_msg)
            st.success("Test message sent!")
        
        st.markdown("---")
        st.markdown("#### 📊 Stats")
        st.json({
            'total_subscribers': len(st.session_state.subscribers),
            'total_news_sent': len(st.session_state.sent_news),
            'active_sources': 5,
            'update_frequency': '2 minutes'
        })

# ============================================
# LOGIN PAGE
# ============================================
def show_login():
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); padding: 2rem; border-radius: 20px; text-align: center; margin-bottom: 2rem;">
        <h1 style="color: white;">📰 NEXA NEWS AI</h1>
        <p style="color: white;">Agra's Fastest News Alert System</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### 🔐 Admin Login")
        with st.form("admin_login"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            
            if st.form_submit_button("Login", use_container_width=True):
                if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
                    st.session_state.logged_in = True
                    st.session_state.user_type = "admin"
                    st.success("✅ Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid credentials")

# ============================================
# MAIN
# ============================================

# Sidebar
with st.sidebar:
    st.markdown("### 📰 NEXA NEWS AI")
    st.markdown("Agra News Alert System")
    st.markdown("---")
    
    if st.session_state.logged_in:
        st.markdown(f"👑 Logged in as Admin")
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()
    else:
        mode = st.radio("Mode", ["📱 Subscribe to News", "🔐 Admin Login"], label_visibility="collapsed")
        
        if mode == "🔐 Admin Login":
            st.session_state.show_admin = True
        else:
            st.session_state.show_admin = False
    
    st.markdown("---")
    st.markdown(f"""
    <div style="font-size: 0.8rem;">
        <b>Features:</b><br>
        • Only Agra News<br>
        • Real-time alerts<br>
        • No duplicates<br>
        • 5+ news sources<br>
        • ₹100/month
    </div>
    """, unsafe_allow_html=True)

# Page routing
if st.session_state.logged_in:
    show_admin_dashboard()
elif st.session_state.get('show_admin', False):
    show_login()
else:
    show_subscription_page()

# ============================================
# BACKGROUND NEWS CHECKER (Starts only once)
# ============================================
if 'news_thread_started' not in st.session_state:
    st.session_state.news_thread_started = True
    thread = threading.Thread(target=check_new_news, daemon=True)
    thread.start()
