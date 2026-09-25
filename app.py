import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import random
import os

st.set_page_config(
    page_title="MegaQash Writers · Translation Platform",
    page_icon="✍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium Custom CSS for full-screen web platform view
st.markdown("""
<style>
    /* Remove default Streamlit top padding */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
        max-width: 98% !important;
    }
    header[data-testid="stHeader"] {
        background-color: transparent !important;
    }
    .main-header {
        font-size: 2rem;
        font-weight: 800;
        color: #0b2d44;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 0.95rem;
        color: #4a6572;
        margin-bottom: 1rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #0b2d44, #1a4a6b);
        color: white;
        padding: 1rem;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        text-align: center;
    }
    .metric-value {
        font-size: 1.7rem;
        font-weight: 700;
        color: #a8d8ea;
    }
    .metric-label {
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        opacity: 0.9;
    }
</style>
""", unsafe_allow_html=True)

def get_html_content():
    html_path = os.path.join(os.path.dirname(__file__), "index.html")
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            return f.read()
    return "<h3>Error: index.html file not found.</h3>"

# Sidebar Navigation
st.sidebar.title("MegaQash Writers")
st.sidebar.caption("Translation Task Platform")

view_mode = st.sidebar.radio(
    "Navigation View",
    [
        "🌐 Live Web Platform",
        "📊 Dashboard & Metrics",
        "🎯 Task Explorer",
        "💳 Financials & M-Pesa",
        "✍️ AI Translator Assistant"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🏅 Translator Status")
st.sidebar.markdown("**Tier:** Gold Tier Translator")
st.sidebar.markdown("**Rating:** ⭐ 4.9 / 5.0")
st.sidebar.markdown("**Completed Tasks:** 147")
st.sidebar.markdown("**On-Time Delivery:** 98%")

CLIENTS = [
    {"name": "Emily Carter", "country": "United States", "flag": "🇺🇸", "uni": "NYU"},
    {"name": "Liam O'Sullivan", "country": "Ireland", "flag": "🇮🇪", "uni": "Trinity College"},
    {"name": "Sophie Müller", "country": "Germany", "flag": "🇩🇪", "uni": "Heidelberg"},
    {"name": "James Whitfield", "country": "United Kingdom", "flag": "🇬🇧", "uni": "Oxford"},
    {"name": "Chloé Dubois", "country": "France", "flag": "🇫🇷", "uni": "Sorbonne"},
    {"name": "Isabella Rossi", "country": "Italy", "flag": "🇮🇹", "uni": "Bocconi"},
    {"name": "Ava Thompson", "country": "Canada", "flag": "🇨🇦", "uni": "UofT"}
]

LANGUAGES = ["Spanish", "French", "German", "Italian", "Portuguese", "Japanese", "Mandarin", "Swahili"]
RATES = [0.20, 0.30, 0.40, 0.50, 0.75, 0.80, 1.00]

# --- VIEW 1: LIVE WEB PLATFORM ---
if view_mode == "🌐 Live Web Platform":
    html_content = get_html_content()
    components.html(html_content, height=920, scrolling=True)

# --- VIEW 2: DASHBOARD & METRICS ---
elif view_mode == "📊 Dashboard & Metrics":
    st.markdown('<div class="main-header">Platform Performance & Metrics</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Live analytics and overview for MegaQash Writers.</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="metric-card"><div class="metric-value">200</div><div class="metric-label">Live Tasks Available</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card"><div class="metric-value">20</div><div class="metric-label">Languages</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card"><div class="metric-value">12 Min</div><div class="metric-label">Avg. Completion Time</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="metric-card"><div class="metric-value">1,247</div><div class="metric-label">Completed Tasks</div></div>', unsafe_allow_html=True)

    st.markdown("### 🌟 Platform Key Strengths")
    c1, c2 = st.columns(2)
    with c1:
        st.info("""
        - **Real-Time Task Grid**: Instant filtering across pay tiers ($0.20 - $1.00).
        - **University Client Demands**: Direct requests from researchers at NYU, Oxford, Sorbonne, Heidelberg.
        - **Session Timer Control**: Ensures high quality & rapid SLAs for clients.
        """)
    with c2:
        st.success("""
        - **Dynamic Pending Drawer**: Real-time review drawer with navbar badge notification.
        - **Instant M-Pesa Payouts**: Direct mobile money transfer with instant reference verification.
        - **Quality Rating System**: Translator stats and tier progression (Gold / Platinum).
        """)

# --- VIEW 3: TASK EXPLORER ---
elif view_mode == "🎯 Task Explorer":
    st.markdown('<div class="main-header">Task Explorer</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Search and inspect available translation requests.</div>', unsafe_allow_html=True)
    
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        selected_rate = st.selectbox("Pay Rate ($)", ["All"] + RATES)
    with col_f2:
        selected_lang = st.selectbox("Target Language", ["All"] + LANGUAGES)
    with col_f3:
        search_query = st.text_input("Search Client or Keyword", "")

    random.seed(42)
    tasks_data = []
    for i in range(1, 41):
        client = random.choice(CLIENTS)
        lang = random.choice(LANGUAGES)
        rate = random.choice(RATES)
        duration = random.choice([1, 2, 3, 4, 6, 8, 12, 24])
        tasks_data.append({
            "Task ID": f"TQ-{1000 + i}",
            "Client": f"{client['flag']} {client['name']} ({client['uni']})",
            "Target Language": lang,
            "Reward ($)": rate,
            "Turnaround (hrs)": duration,
            "Status": "Available"
        })
    df_tasks = pd.DataFrame(tasks_data)

    if selected_rate != "All":
        df_tasks = df_tasks[df_tasks["Reward ($)"] == float(selected_rate)]
    if selected_lang != "All":
        df_tasks = df_tasks[df_tasks["Target Language"] == selected_lang]
    if search_query:
        df_tasks = df_tasks[df_tasks["Client"].str.contains(search_query, case=False)]

    st.dataframe(df_tasks, use_container_width=True, hide_index=True)

# --- VIEW 4: FINANCIALS & M-PESA ---
elif view_mode == "💳 Financials & M-Pesa":
    st.markdown('<div class="main-header">Financial Dashboard & Cashout</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Manage earnings and process M-Pesa payouts.</div>', unsafe_allow_html=True)
    
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.metric("Available Balance", "$ 56.30", "+$ 12.40 today")
    with col_b:
        st.metric("Total Withdrawals", "$ 342.80", "M-Pesa Verified")
    with col_c:
        st.metric("Average Payout per Task", "$ 0.58", "Top Tier")

    st.markdown("---")
    st.markdown("### 📱 Instant M-Pesa Cashout Simulator")
    
    with st.form("withdraw_form"):
        withdraw_amount = st.number_input("Withdrawal Amount ($)", min_value=1.0, max_value=56.30, value=10.0, step=0.5)
        phone_number = st.text_input("M-Pesa Phone Number", value="+254 712 345 678")
        submit_withdraw = st.form_submit_button("⚡ Withdraw to M-Pesa")

    if submit_withdraw:
        ref_code = f"MPX-{random.randint(9000, 9999)}-KE"
        st.balloons()
        st.success(f"✅ Success! **${withdraw_amount:.2f}** transferred to **{phone_number}**. Reference ID: `{ref_code}`.")

    st.markdown("### 📋 Recent Withdrawal Logs")
    withdrawals = [
        {"Amount": "$ 5.00", "Method": "M-Pesa Instant", "Reference": "MPX-8823-KE", "Status": "✅ Success", "Date": "2024-09-24"},
        {"Amount": "$ 8.50", "Method": "M-Pesa Instant", "Reference": "MPX-8712-KE", "Status": "✅ Success", "Date": "2024-09-23"},
        {"Amount": "$ 3.20", "Method": "M-Pesa Instant", "Reference": "MPX-8634-KE", "Status": "✅ Success", "Date": "2024-09-22"},
        {"Amount": "$ 7.00", "Method": "M-Pesa Instant", "Reference": "MPX-8521-KE", "Status": "✅ Success", "Date": "2024-09-21"},
        {"Amount": "$ 12.40", "Method": "M-Pesa Instant", "Reference": "MPX-8409-KE", "Status": "✅ Success", "Date": "2024-09-20"},
    ]
    st.table(pd.DataFrame(withdrawals))

# --- VIEW 5: AI TRANSLATOR ASSISTANT ---
elif view_mode == "✍️ AI Translator Assistant":
    st.markdown('<div class="main-header">AI Translator Workspace</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Draft and refine your translations.</div>', unsafe_allow_html=True)
    
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        source_text = st.text_area(
            "Source Paragraph",
            "The rapid expansion of renewable energy technology has fundamentally reshaped global economic policies over the past decade.",
            height=150
        )
        target_lang = st.selectbox("Target Language", LANGUAGES)
        
    with col_t2:
        st.markdown("**Suggested Translation Draft:**")
        if st.button("✨ Draft Translation"):
            st.info(f"**[{target_lang} Draft]:**\n\n*(High-Accuracy Translation Draft)*")
            st.text_area("Final Edited Version", f"[Translated text in {target_lang} goes here]", height=120)
