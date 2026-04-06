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
    page_title="NEXA NEWS | Agra Fastest News",
    page_icon="⚡",
    layout="wide"
)

# Custom CSS for Professional Look
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    .stAppDeployButton {display: none;}
    
    /* Professional Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Flash News Banner */
    .flash-news {
        background: linear-gradient(90deg, #ff0000, #ff6b6b, #ff0000);
        background-size: 200% 100%;
        animation: flash 2s linear infinite;
        color: white;
        padding: 12px;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 20px;
        font-weight: bold;
        font-size: 1.2rem;
    }
    
    @keyframes flash {
        0% { background-position: 0% 0%; }
        100% { background-position: 200% 0%; }
    }
    
    /* Hero Section */
    .hero {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .hero h1 {
        color: white;
        font-size: 2.5rem;
        margin: 0;
    }
    
    .hero p {
        color: #ccc;
        font-size: 1.1rem;
    }
    
    /* Speed Badge */
    .speed-badge {
        background: #ffc107;
        color: #1e3c72;
        padding: 0.3rem 1rem;
        border-radius: 50px;
        font-weight: bold;
        display: inline-block;
        margin-top: 1rem;
    }
    
    /* Feature Card */
    .feature-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        transition: transform 0.3s;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
    }
    
    /* Price Card */
    .price-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 20px;
        padding: 1.5rem;
        text-align: center;
        color: white;
    }
    
    .price {
        font-size: 3rem;
        font-weight: bold;
    }
    
    /* News Card */
    .news-card {
        background: white;
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 3px 10px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
        transition: transform 0.3s;
    }
    
    .news-card:hover {
        transform: scale(1.02);
    }
    
    .news-image {
        width: 100%;
        height: 150px;
        object-fit: cover;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 3rem;
    }
    
    .news-content {
        padding: 1rem;
    }
    
    .news-title {
        font-size: 1.1rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    
    .news-category {
        display: inline-block;
        padding: 0.2rem 0.5rem;
        border-radius: 5px;
        font-size: 0.7rem;
        margin-bottom: 0.5rem;
    }
    
    /* Telegram Button */
    .telegram-btn {
        background: #0088cc;
        color: white;
        padding: 0.8rem 1.5rem;
        border-radius: 50px;
        text-decoration: none;
        font-weight: bold;
        display: inline-block;
        margin: 0.5rem;
    }
    
    .telegram-btn:hover {
        background: #006699;
        color: white;
    }
    
    /* Reminder Box */
    .reminder-box {
        background: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .footer {
        text-align: center;
        padding: 2rem;
        color: #666;
        font-size: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# CONFIGURATION
# ============================================
ADMIN_EMAIL = "wasu47118@gmail.com"
ADMIN_PASSWORD = "Wasu1234$"
UPI_ID = "8439049681@pthdfc"
PHONE = "8439049681"

# Telegram Bot Token
TELEGRAM_BOT_TOKEN = "8756226031:AAFpi0sBKKooqWrQhavpEFyN7peYJs0WfVw"  # CHANGE THIS!

# Categories with colors
CATEGORIES = {
    "all": {"name": "📰 All News", "color": "#667eea"},
    "crime": {"name": "🚨 Crime", "color": "#ff6b6b"},
    "cyber": {"name": "💻 Cyber Crime", "color": "#4ecdc4"},
    "business": {"name": "📊 Business", "color": "#45b7d1"},
    "technology": {"name": "📱 Technology", "color": "#96ceb4"},
    "sports": {"name": "⚽ Sports", "color": "#f4d03f"},
    "entertainment": {"name": "🎬 Entertainment", "color": "#dda0dd"},
    "politics": {"name": "🏛️ Politics", "color": "#ff9f43"},
    "health": {"name": "🏥 Health", "color": "#2ecc71"},
    "auto": {"name": "🚗 Auto", "color": "#e67e22"},
    "education": {"name": "📚 Education", "color": "#3498db"},
    "local": {"name": "🏘️ Local", "color": "#9b59b6"}
}

# Sample news images (for demo)
NEWS_IMAGES = {
    "crime": "🚨",
    "cyber": "💻",
    "business": "📊",
    "technology": "📱",
    "sports": "⚽",
    "entertainment": "🎬",
    "politics": "🏛️",
    "health": "🏥",
    "auto": "🚗",
    "education": "📚",
    "local": "🏘️",
    "default": "📰"
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

if 'payment_pending' not in st.session_state:
    st.session_state.payment_pending = None

# ============================================
# SUBSCRIPTION CHECK FUNCTION
# ============================================
def check_subscription(telegram_id):
    """Check if user has active subscription"""
    for sub in st.session_state.subscribers:
        if sub.get('telegram_id') == telegram_id and sub.get('active'):
            # Check expiry
            expiry_date = datetime.strptime(sub['expiry_date'], '%Y-%m-%d')
            if expiry_date > datetime.now():
                return True, sub
            else:
                sub['active'] = False
                return False, None
    return False, None

def send_expiry_reminders():
    """Send reminder to users whose subscription is expiring in 3 days"""
    today = datetime.now().date()
    for sub in st.session_state.subscribers:
        if sub.get('active'):
            expiry = datetime.strptime(sub['expiry_date'], '%Y-%m-%d').date()
            days_left = (expiry - today).days
            if days_left == 3:
                msg = f"""⚠️ <b>Subscription Expiry Reminder</b>

Hello {sub['name']},

Your NEXA NEWS subscription will expire in <b>3 days</b> ({sub['expiry_date']}).

💰 Please renew at ₹100/month
UPI: {UPI_ID}

Reply RENEW after payment to continue getting news.

Thanks!
📞 Support: {PHONE}"""
                send_telegram_message(sub['telegram_id'], msg)
            elif days_left == 1:
                msg = f"""🔴 <b>LAST DAY REMINDER!</b>

Hello {sub['name']},

Your subscription expires TOMORROW ({sub['expiry_date']}).

⚠️ Renew now to continue getting news alerts!

💰 ₹100/month
UPI: {UPI_ID}

Reply RENEW after payment."""
                send_telegram_message(sub['telegram_id'], msg)

# ============================================
# TELEGRAM FUNCTIONS
# ============================================
def send_telegram_message(chat_id, message):
    """Send message via Telegram Bot"""
    if TELEGRAM_BOT_TOKEN == "8756226031:AAFpi0sBKKooqWrQhavpEFyN7peYJs0WfVw":
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

def telegram_bot_handler():
    """Handle Telegram bot messages - check subscription first"""
    if TELEGRAM_BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        return
    
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            updates = response.json().get('result', [])
            for update in updates:
                chat_id = update.get('message', {}).get('chat', {}).get('id')
                text = update.get('message', {}).get('text', '')
                
                if text == '/start':
                    # Check subscription
                    has_sub, sub_data = check_subscription(str(chat_id))
                    if has_sub:
                        msg = f"""✅ <b>Welcome back {sub_data['name']}!</b>

Your subscription is ACTIVE until {sub_data['expiry_date']}.

📰 You will continue receiving Agra news alerts.

Need help? Contact: {PHONE}"""
                    else:
                        msg = f"""⚠️ <b>Subscription Required!</b>

Hello! To receive Agra news alerts, you need to subscribe.

💰 ₹100/month
UPI: {UPI_ID}

📱 Subscribe here: https://nexa-news-pro.streamlit.app

After payment, your account will be activated within 24 hours."""
                    
                    send_telegram_message(chat_id, msg)
                
                elif text.upper() == 'RENEW':
                    msg = f"""💰 <b>Renew Subscription</b>

Pay ₹100 to UPI: {UPI_ID}

After payment, reply with: PAID [Transaction ID]

Your service will be renewed immediately!"""
                    send_telegram_message(chat_id, msg)
                
                elif text.upper().startswith('PAID'):
                    # Admin will handle manually or auto-activate
                    msg = f"✅ Payment received! Your subscription will be renewed shortly."
                    send_telegram_message(chat_id, msg)
    except:
        pass

def send_news_to_subscribers(news):
    """Send news to all active Telegram subscribers"""
    image_emoji = NEWS_IMAGES.get(news['category'], NEWS_IMAGES['default'])
    
    message = f"""<b>⚡ FASTEST NEWS ALERT!</b>

{image_emoji} <b>{CATEGORIES[news['category']]['name']}</b>

<b>{news['title']}</b>

{news['summary']}

🔗 <a href="{news['link']}">Read full story →</a>

⏰ {news['time']} | 📅 {news['date']}
📡 Source: {news['source']}

---
⚡ <i>NEXA NEWS - Agra's Fastest</i>"""
    
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
    
    # Google News RSS (Agra)
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
    
    # Times of India (Agra)
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
    
    crime_keywords = ['crime', 'murder', 'theft', 'robbery', 'kidnap', 'rape', 'arrest', 'accused', 'police', 'case']
    cyber_keywords = ['cyber', 'hack', 'fraud', 'scam', 'online', 'digital', 'phishing', 'cyber crime']
    business_keywords = ['business', 'market', 'economy', 'company', 'startup', 'investment', 'stock', 'share']
    tech_keywords = ['tech', 'technology', 'app', 'software', 'ai', 'digital', 'smartphone', 'mobile']
    sports_keywords = ['sports', 'cricket', 'football', 'match', 'tournament', 'player', 'team', 'world cup']
    entertainment_keywords = ['film', 'movie', 'actor', 'actress', 'celebrity', 'bollywood', 'entertainment', 'song']
    politics_keywords = ['politics', 'election', 'minister', 'government', 'party', 'bjp', 'congress', 'modi']
    health_keywords = ['health', 'hospital', 'doctor', 'disease', 'covid', 'treatment', 'vaccine', 'medical']
    auto_keywords = ['car', 'auto', 'vehicle', 'bike', 'transport', 'road', 'traffic', 'automobile']
    education_keywords = ['school', 'college', 'education', 'student', 'exam', 'university', 'admission']
    
    if any(word in text_lower for word in crime_keywords):
        return "crime"
    elif any(word in text_lower for word in cyber_keywords):
        return "cyber"
    elif any(word in text_lower for word in business_keywords):
        return "business"
    elif any(word in text_lower for word in tech_keywords):
        return "technology"
    elif any(word in text_lower for word in sports_keywords):
        return "sports"
    elif any(word in text_lower for word in entertainment_keywords):
        return "entertainment"
    elif any(word in text_lower for word in politics_keywords):
        return "politics"
    elif any(word in text_lower for word in health_keywords):
        return "health"
    elif any(word in text_lower for word in auto_keywords):
        return "auto"
    elif any(word in text_lower for word in education_keywords):
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
            # Check expiry reminders daily
            send_expiry_reminders()
            # Handle Telegram bot messages
            telegram_bot_handler()
            time.sleep(120)
        except:
            time.sleep(60)

# ============================================
# SUBSCRIPTION PAGE
# ============================================
def show_subscription_page():
    # Flash News Banner
    st.markdown("""
    <div class="flash-news">
        ⚡⚡⚡ SABSE TEJ NEWS - AGRA KI PEHLE PEHLE ⚡⚡⚡
    </div>
    """, unsafe_allow_html=True)
    
    # Hero Section
    st.markdown("""
    <div class="hero">
        <h1>📰 NEXA NEWS</h1>
        <p>Agra Ka Number 1 Fastest News Alert System</p>
        <div class="speed-badge">
            ⚡ 2 minute mein news ⚡
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Telegram Banner
    st.markdown("""
    <div style="background: linear-gradient(135deg, #0088cc, #006699); padding: 1.5rem; border-radius: 15px; text-align: center; margin-bottom: 1.5rem;">
        <h2 style="color: white;">📱 Get News on Telegram!</h2>
        <p style="color: white;">Subscribe now and get instant news alerts</p>
        <div style="display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap;">
            <a href="https://telegram.org/android" target="_blank" class="telegram-btn">📱 Android</a>
            <a href="https://telegram.org/ios" target="_blank" class="telegram-btn">📱 iPhone</a>
            <a href="https://desktop.telegram.org" target="_blank" class="telegram-btn">💻 Desktop</a>
        </div>
        <p style="color: #ccc; margin-top: 1rem;">After downloading, search <b>@AgraFastestNewsBot</b> and start!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Features Section
    st.markdown("### 🎯 Why Choose NEXA NEWS?")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h1>⚡</h1>
            <h3>Fastest News</h3>
            <p>News delivered within 2-3 minutes</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h1>🎯</h1>
            <h3>Only Agra News</h3>
            <p>100% relevant local news</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h1>📚</h1>
            <h3>12+ Categories</h3>
            <p>Crime, Business, Sports, Tech, etc.</p>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown("""
        <div class="feature-card">
            <h1>🔗</h1>
            <h3>Multiple Sources</h3>
            <p>Google News + Times of India</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Subscription Form
    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.markdown("""
        <div class="price-card">
            <h2>📰 Subscription Plan</h2>
            <div class="price">₹100</div>
            <p>per month</p>
            <hr>
            <p>✅ Instant news alerts</p>
            <p>✅ 12+ categories</p>
            <p>✅ No spam</p>
            <p>✅ Cancel anytime</p>
            <p>✅ 24/7 support</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### 🔐 Subscribe Now")
        
        with st.form("subscribe_form"):
            name = st.text_input("Full Name *", placeholder="Enter your full name")
            telegram_id = st.text_input("Telegram ID *", placeholder="@username or 123456789")
            categories = st.multiselect("Select Categories", 
                                       [CATEGORIES[k]['name'] for k in CATEGORIES.keys()],
                                       default=["📰 All News"])
            
            selected_keys = [k for k, v in CATEGORIES.items() if v['name'] in categories]
            
            agree = st.checkbox("I agree to receive news alerts on Telegram")
            
            if st.form_submit_button("🚀 Subscribe Now - ₹100", use_container_width=True, type="primary"):
                if name and telegram_id and agree:
                    st.session_state.payment_pending = {
                        'name': name,
                        'telegram_id': telegram_id,
                        'categories': selected_keys,
                        'amount': 100
                    }
                    
                    st.info(f"💳 Pay ₹100 to UPI: **{UPI_ID}**")
                    
                    upi_link = f"upi://pay?pa={UPI_ID}&pn=NEXA%20NEWS&am=100&cu=INR"
                    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={urllib.parse.quote(upi_link)}"
                    
                    st.markdown(f"""
                    <div style="text-align: center;">
                        <h4>📱 Scan to Pay ₹100</h4>
                        <img src="{qr_url}" width="200">
                        <p><b>UPI ID:</b> {UPI_ID}</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown("---")
                    st.markdown("### ✅ After Payment")
                    st.markdown("Click below button after successful payment")
                    
                    if st.button("✅ I have made the payment", use_container_width=True):
                        expiry_date = (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
                        
                        new_subscriber = {
                            'id': len(st.session_state.subscribers) + 1,
                            'name': name,
                            'telegram_id': telegram_id,
                            'categories': selected_keys,
                            'active': True,
                            'subscribed_date': datetime.now().strftime('%Y-%m-%d'),
                            'expiry_date': expiry_date,
                            'payment_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                            'payment_status': 'completed'
                        }
                        st.session_state.subscribers.append(new_subscriber)
                        
                        welcome_msg = f"""🎉 <b>Welcome to NEXA NEWS!</b>

Hello {name},

✅ Your subscription is ACTIVE until {expiry_date}

💰 Plan: ₹100/month
📰 Categories: {', '.join([CATEGORIES[k]['name'] for k in selected_keys])}

You will receive Agra news alerts instantly on this Telegram account.

⚡ <b>Get ready for fastest news!</b>

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
    <div class="hero">
        <h1>👑 ADMIN DASHBOARD</h1>
        <p>Complete control of NEXA NEWS System</p>
    </div>
    """, unsafe_allow_html=True)
    
    total_subs = len(st.session_state.subscribers)
    total_news = len(st.session_state.sent_news)
    total_revenue = total_subs * 100
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📱 Subscribers", total_subs)
    with col2:
        st.metric("💰 Revenue", f"₹{total_revenue}")
    with col3:
        st.metric("📰 News Sent", total_news)
    with col4:
        st.metric("⚡ Speed", "2 minutes")
    
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
        news_category = st.selectbox("Category", list(CATEGORIES.keys()), format_func=lambda x: CATEGORIES[x]['name'])
        
        if st.button("Send to All Subscribers"):
            for sub in st.session_state.subscribers:
                emoji = NEWS_IMAGES.get(news_category, NEWS_IMAGES['default'])
                msg = f"""<b>⚡ FASTEST NEWS ALERT!</b>

{emoji} <b>{CATEGORIES[news_category]['name']}</b>

<b>{news_title}</b>

{news_content}

🔗 <a href="{news_link}">Read full story →</a>

---
⚡ <i>NEXA NEWS - Agra's Fastest</i>"""
                send_telegram_message(sub['telegram_id'], msg)
            st.success("News sent to all subscribers!")

# ============================================
# LOGIN PAGE
# ============================================
def show_login():
    st.markdown("""
    <div class="hero">
        <h1>🔐 Admin Login</h1>
        <p>Enter credentials to access dashboard</p>
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
                    st.success("✅ Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid credentials")

# ============================================
# MAIN
# ============================================

with st.sidebar:
    st.markdown("""
    <div style="text-align: center; padding: 1rem;">
        <h2>⚡ NEXA</h2>
        <h3>NEWS</h3>
        <p>Agra's Fastest</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    if st.session_state.logged_in:
        st.markdown("👑 Admin Mode")
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()
    else:
        mode = st.radio("", ["📰 Subscribe", "🔐 Admin"], label_visibility="collapsed")
        
        if mode == "🔐 Admin":
            st.session_state.show_admin = True
        else:
            st.session_state.show_admin = False
    
    st.markdown("---")
    st.markdown(f"""
    <div style="font-size: 0.8rem;">
        <b>📞 Support</b><br>
        📱 {PHONE}<br>
        💳 {UPI_ID}<br>
        ⚡ 24/7 Service
    </div>
    """, unsafe_allow_html=True)

if st.session_state.logged_in:
    show_admin_dashboard()
elif st.session_state.get('show_admin', False):
    show_login()
else:
    show_subscription_page()

# Start background thread
if 'news_thread_started' not in st.session_state:
    st.session_state.news_thread_started = True
    thread = threading.Thread(target=check_new_news, daemon=True)
    thread.start()
