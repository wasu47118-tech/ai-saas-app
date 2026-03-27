import streamlit as st

st.set_page_config(page_title="AI SaaS", page_icon="🤖", layout="wide")

st.title("🤖 AI ENTERPRISE SAAS")
st.markdown("---")

st.markdown("""
### 🚀 AI Data Entry & Customer Reminder System

**For companies of ALL sizes**

- ✅ Auto monthly subscription
- ✅ AI document processing  
- ✅ Customer reminder system
- ✅ 24/7 operation
- ✅ Enterprise security
""")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### 💰 Startup Plan")
    st.markdown("**₹999/month**")
    st.markdown("- 500 documents\n- 5 employees\n- Basic reminders")

with col2:
    st.markdown("### 📈 Business Plan")  
    st.markdown("**₹2499/month**")
    st.markdown("- 2000 documents\n- 20 employees\n- SMS reminders")

with col3:
    st.markdown("### 🏢 Enterprise Plan")
    st.markdown("**₹9999/month**")
    st.markdown("- Unlimited\n- Custom AI\n- 24/7 support")

st.markdown("---")
st.markdown("### 📱 Contact for Demo")
st.markdown("**UPI:** 8439049681@pthdfc")
st.markdown("**Phone:** 8439049681")
