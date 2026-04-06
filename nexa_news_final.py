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
import urllib.parse

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

# Telegram Bot Token (FREE - Get from @BotFather on Telegram)
# STEP 1: Open Telegram, search @BotFather
# STEP 2: Send /newbot
# STEP 3: Give name: Agra News Bot
# STEP 4: Give username: agra_news_bot
# STEP 5: Copy token and paste below
TELEGRAM_BOT_TOKEN = "8532416007:AAEzEjHNIJH97-Xmn7j75L8suuh_etbCkBk"  # CHANGE THIS AFTER GETTING TOKEN

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

if 'payment_pending' not in st.session_state:
    st.session_state.payment_pending = None

# ============================================
# TELEGRAM FUNCTIONS (FREE)
# ============================================
def send_telegram_message(chat_id, message):
    """Send message via Telegram Bot (FREE)"""
    if TELEGRAM_BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        return False
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        data = {
            "chat_id": chat_id,
            "text": message,
            "parse_mode": "HTML"
        }
        response = requests.post(url, json=data, timeout=10)
        return response.status_code == 200
    except:
        return False

def send_news_to_subscribers(news):
    """Send news to all Telegram subscribers"""
    message = f"""<b>📰 NEXA NEWS ALERT</b>

📍 <b>Agra News Update</b>
🏷️ Category: {CATEGORIES.get(news['category'], '📰 News')}

<b>{news['title']}</b>

{news['summary']}

🔗 <a href="{news['link']}">Read more</a>
⏰ Time: {news['time']}
📅 Date: {news['date']}
📡 Source: {news['source']}

---
⚡ Powered by NEXA NEWS AI
    """
    
    for sub in st.session_state.subscribers:
        if sub.get('active', True) and sub.get('telegram_id'):
            send_telegram_message(sub['telegram_id'], message)
    
    st.session_state.sent_news.add(news['title'])
    st.session_state.news_history.append({
        'title': news['title'],
        'sent_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'category': news['category']
    })

# ============================================
# AGRA NEWS FETCHER
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
    
    # Source 2: Times of India (Agra)
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

def check_new_news():
    """Background thread to check new news every 2 minutes"""
    while True:
        try:
            news_list = fetch_agra_news()
            for news in news_list:
                if news['title'] not in st.session_state.sent_news:
                    send_news_to_subscribers(news)
            time.sleep(120)
        except:
            time.sleep(60)

# ============================================
# TELEGRAM SETUP GUIDE
# ============================================
def show_telegram_guide():
    st.markdown("""
    <div style="background: #ff6b6b; color: white; padding: 1.5rem; border-radius: 15px; text-align: center; margin-bottom: 1.5rem;">
        <h1>⚠️ IMPORTANT!</h1>
        <h2>TO GET NEWS ALERTS, YOU MUST HAVE TELEGRAM</h2>
        <p style="font-size: 1.2rem;">👇 Download Telegram App First 👇</p>
        <div style="display: flex; justify-content: center; gap: 1rem; margin-top: 0.5rem; flex-wrap: wrap;">
            <a href="https://telegram.org/android" target="_blank" style="background: white; color: #ff6b6b; padding: 0.5rem 1.5rem; border-radius: 8px; text-decoration: none; font-weight: bold;">📱 Android</a>
            <a href="https://telegram.org/ios" target="_blank" style="background: white; color: #ff6b6b; padding: 0.5rem 1.5rem; border-radius: 8px; text-decoration: none; font-weight: bold;">📱 iPhone</a>
            <a href="https://desktop.telegram.org" target="_blank" style="background: white; color: #ff6b6b; padding: 0.5rem 1.5rem; border-radius: 8px; text-decoration: none; font-weight: bold;">💻 Desktop</a>
        </div>
        <p style="margin-top: 1rem;">After downloading, search <b>@AgraNewsBot</b> and start the bot!</p>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# SUBSCRIPTION PAGE
# ============================================
def show_subscription_page():
    # Show Telegram banner first
    show_telegram_guide()
    
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); padding: 1.5rem; border-radius: 20px; text-align: center; margin-bottom: 1.5rem;">
        <h1 style="color: white;">📰 NEXA NEWS AI</h1>
        <p style="color: white;">Agra's Fastest News Alert System</p>
        <p style="color: #ffc107;">⚡ Only ₹100/month - Get instant news on Telegram!</p>
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
            <p>✅ <b>Multiple Sources</b> - Google News + Times of India</p>
            <p>✅ <b>Telegram Alerts</b> - Instant delivery</p>
            <p>✅ <b>24/7 Service</b> - Never miss news</p>
            <p>✅ <b>All Categories</b> - Crime, Business, Sports, Tech, etc.</p>
            
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
            phone = st.text_input("WhatsApp Number (Optional)")
            telegram_id = st.text_input("Telegram Username or ID *", placeholder="@username or 123456789")
            categories = st.multiselect("Select News Categories", list(CATEGORIES.values()), default=["📰 All News"])
            
            selected_keys = [k for k, v in CATEGORIES.items() if v in categories]
            
            agree = st.checkbox("I agree to receive news alerts on Telegram")
            
            if st.form_submit_button("💰 Subscribe - ₹100/month", use_container_width=True, type="primary"):
                if name and telegram_id and agree:
                    st.session_state.payment_pending = {
                        'name': name,
                        'phone': phone,
                        'telegram_id': telegram_id,
                        'categories': selected_keys,
                        'amount': 100
                    }
                    
                    st.info(f"💳 Pay ₹100 to UPI: {UPI_ID}")
                    
                    upi_link = f"upi://pay?pa={UPI_ID}&pn=NEXA%20NEWS&am=100&cu=INR"
                    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={urllib.parse.quote(upi_link)}"
                    
                    st.markdown(f"""
                    <div style="text-align: center;">
                        <h4>Scan to Pay ₹100</h4>
                        <img src="{qr_url}" width="200">
                        <p><b>UPI ID:</b> {UPI_ID}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("---")
                    st.markdown("### ✅ After Payment")
                    st.markdown("Click below button after successful payment")
                    
                    if st.button("✅ I have made the payment", use_container_width=True):
                        new_subscriber = {
                            'id': len(st.session_state.subscribers) + 1,
                            'name': name,
                            'phone': phone,
                            'telegram_id': telegram_id,
                            'categories': selected_keys,
                            'active': True,
                            'subscribed_date': datetime.now().strftime('%Y-%m-%d'),
                            'payment_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                            'payment_status': 'completed'
                        }
                        st.session_state.subscribers.append(new_subscriber)
                        
                        welcome_msg = f"""🎉 <b>Welcome to NEXA NEWS AI!</b>

Hello {name},

Your subscription has been activated successfully!

📅 Valid from: {datetime.now().strftime('%d-%m-%Y')}
💰 Plan: ₹100/month

You will receive Agra news alerts instantly on this Telegram account.

Thanks for subscribing!
📞 Support: {PHONE}

<i>Powered by NEXA TECH AI</i>"""
                        
                        send_telegram_message(telegram_id, welcome_msg)
                        
                        st.balloons()
                        st.success("✅ Payment confirmed! Your subscription is now ACTIVE!")
                        st.info("📱 Check your Telegram for welcome message")
                        st.session_state.payment_pending = None
                        st.rerun()
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
    total_revenue = total_subs * 100
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📱 Subscribers", total_subs)
    with col2:
        st.metric("💰 Total Revenue", f"₹{total_revenue}")
    with col3:
        st.metric("📰 News Sent", total_news)
    with col4:
        st.metric("🕐 Update", "2 minutes")
    
    st.markdown("---")
    
    tab1, tab2, tab3 = st.tabs(["📱 Subscribers", "📰 News History", "📤 Manual News"])
    
    with tab1:
        if st.session_state.subscribers:
            df = pd.DataFrame(st.session_state.subscribers)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No subscribers yet")
    
    with tab2:
        if st.session_state.news_history:
            df = pd.DataFrame(st.session_state.news_history[-50:])
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No news sent yet")
    
    with tab3:
        st.markdown("### 📤 Manual News Send")
        news_title = st.text_input("News Title")
        news_content = st.text_area("News Summary")
        news_link = st.text_input("News Link")
        
        if st.button("Send to All Subscribers"):
            for sub in st.session_state.subscribers:
                msg = f"""<b>📰 NEXA NEWS ALERT</b>

<b>{news_title}</b>

{news_content}

🔗 <a href="{news_link}">Read more</a>

---
⚡ Powered by NEXA NEWS AI"""
                send_telegram_message(sub['telegram_id'], msg)
            st.success("News sent to all subscribers!")

# ============================================
# LOGIN PAGE
# ============================================
def show_login():
    st.markdown("""
    <div style="background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); padding: 2rem; border-radius: 20px; text-align: center; margin-bottom: 2rem;">
        <h1 style="color: white;">📰 NEXA NEWS AI</h1>
        <p style="color: white;">Admin Login</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
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
        <b>📞 Support:</b><br>
        Phone: {PHONE}<br>
        UPI: {UPI_ID}
    </div>
    """, unsafe_allow_html=True)

if st.session_state.logged_in:
    show_admin_dashboard()
elif st.session_state.get('show_admin', False):
    show_login()
else:
    show_subscription_page()

# Start background news checker
if 'news_thread_started' not in st.session_state:
    st.session_state.news_thread_started = True
    thread = threading.Thread(target=check_new_news, daemon=True)
    thread.start()
