import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import random
import json
import os

st.set_page_config(
    page_title="MegaQash Writers · Translation Platform",
    page_icon="✍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling
st.markdown("""
<style>
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
        max-width: 98% !important;
    }
    header[data-testid="stHeader"] {
        background-color: transparent !important;
    }
    .main-header {
        font-size: 1.8rem;
        font-weight: 800;
        color: #0b2d44;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 0.9rem;
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
        font-size: 1.6rem;
        font-weight: 700;
        color: #a8d8ea;
    }
    .metric-label {
        font-size: 0.78rem;
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

# Session State for User Auth database
if 'users_db' not in st.session_state:
    st.session_state['users_db'] = [
        {"name": "Emily Carter", "email": "client@nyu.edu", "role": "Client", "uni": "NYU", "country": "United States 🇺🇸"},
        {"name": "Freelance Writer", "email": "translator@megaqash.com", "role": "Freelance Writer", "uni": "Gold Tier", "country": "Kenya 🇰🇪"}
    ]

if 'logged_in_user' not in st.session_state:
    st.session_state['logged_in_user'] = None  # Start in logged out mode

# Sidebar Navigation
st.sidebar.title("MegaQash Writers")
st.sidebar.caption("Translation Task Platform")

view_mode = st.sidebar.radio(
    "Navigation View",
    [
        "🌐 Live Web Platform",
        "🔐 User Auth & Accounts",
        "📊 Dashboard & Metrics",
        "🎯 Task Explorer",
        "💳 Financials & M-Pesa",
        "✍️ AI Translator Assistant"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 👤 Current Session")
curr = st.session_state['logged_in_user']

if curr:
    st.sidebar.markdown(f"**Name:** {curr['name']}")
    st.sidebar.markdown(f"**Email:** {curr['email']}")
    st.sidebar.markdown(f"**Role:** `{curr['role']}`")
    if curr.get('uni'):
        st.sidebar.markdown(f"**University:** {curr['uni']}")
    
    if st.sidebar.button("🚪 Log Out", key="sidebar_logout_btn"):
        st.session_state['logged_in_user'] = None
        st.success("Logged out.")
        st.rerun()
else:
    st.sidebar.warning("Not Logged In")
    if st.sidebar.button("🔑 Log In / Sign Up", key="sidebar_login_btn"):
        st.session_state['logged_in_user'] = st.session_state['users_db'][0]
        st.rerun()

# --- VIEW 1: LIVE WEB PLATFORM ---
if view_mode == "🌐 Live Web Platform":
    html_content = get_html_content()
    components.html(html_content, height=920, scrolling=True)

# --- VIEW 2: USER AUTH & ACCOUNTS ---
elif view_mode == "🔐 User Auth & Accounts":
    st.markdown('<div class="main-header">Authentication & Account Management Service</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Register new Clients or Freelance Writers and manage active login sessions.</div>', unsafe_allow_html=True)

    auth_tab1, auth_tab2, auth_tab3 = st.tabs(["🔑 Log In", "📝 Create Account (Register)", "👥 Registered Accounts Database"])

    with auth_tab1:
        st.markdown("### User Login")
        with st.form("login_form"):
            login_email = st.text_input("Email Address", value="client@nyu.edu")
            login_password = st.text_input("Password", value="password123", type="password")
            submit_login = st.form_submit_button("⚡ Log In")

        if submit_login:
            found = next((u for u in st.session_state['users_db'] if u['email'].lower() == login_email.lower()), None)
            if found:
                st.session_state['logged_in_user'] = found
                st.success(f"✅ Successfully logged in as **{found['name']}** ({found['role']})!")
                st.rerun()
            else:
                st.error("❌ Invalid email or password. Please try again.")

        st.markdown("#### Quick 1-Click Demo Logins:")
        col_d1, col_d2 = st.columns(2)
        with col_d1:
            if st.button("🎓 Log in as Demo Client (Emily Carter)"):
                st.session_state['logged_in_user'] = st.session_state['users_db'][0]
                st.success("Logged in as Demo Client!")
                st.rerun()
        with col_d2:
            if st.button("✍️ Log in as Demo Writer"):
                st.session_state['logged_in_user'] = st.session_state['users_db'][1]
                st.success("Logged in as Demo Writer!")
                st.rerun()

    with auth_tab2:
        st.markdown("### Create New Account (Sign Up)")
        with st.form("register_form"):
            reg_name = st.text_input("Full Name", placeholder="e.g. Dr. Alex Vance")
            reg_email = st.text_input("Email Address", placeholder="e.g. alex@oxford.ac.uk")
            reg_password = st.text_input("Password", type="password", placeholder="Minimum 6 characters")
            reg_role = st.selectbox("Select Account Role", ["Client (Post Tasks & Hire)", "Freelance Writer (Translate Tasks)"])
            reg_uni = st.text_input("University / Organization Name", value="Oxford University")
            reg_country = st.text_input("Country", value="United Kingdom 🇬🇧")
            
            submit_reg = st.form_submit_button("🚀 Create Account & Sign In")

        if submit_reg:
            if not reg_name or not reg_email or not reg_password:
                st.error("Please fill in all required fields.")
            elif any(u['email'].lower() == reg_email.lower() for u in st.session_state['users_db']):
                st.warning("An account with this email address already exists!")
            else:
                new_user = {
                    "name": reg_name,
                    "email": reg_email,
                    "role": "Client" if "Client" in reg_role else "Freelance Writer",
                    "uni": reg_uni,
                    "country": reg_country
                }
                st.session_state['users_db'].append(new_user)
                st.session_state['logged_in_user'] = new_user
                st.balloons()
                st.success(f"🎉 Account created successfully! Welcome, **{reg_name}**.")
                st.rerun()

    with auth_tab3:
        st.markdown("### Registered Users Database")
        st.dataframe(pd.DataFrame(st.session_state['users_db']), use_container_width=True, hide_index=True)

# --- VIEW 3: DASHBOARD & METRICS ---
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

# --- VIEW 4: TASK EXPLORER ---
elif view_mode == "🎯 Task Explorer":
    st.markdown('<div class="main-header">Task Explorer</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Search and inspect available translation requests.</div>', unsafe_allow_html=True)
    
    CLIENTS = [
        {"name": "Emily Carter", "country": "United States", "flag": "🇺🇸", "uni": "NYU"},
        {"name": "Liam O'Sullivan", "country": "Ireland", "flag": "🇮🇪", "uni": "Trinity College"},
        {"name": "Sophie Müller", "country": "Germany", "flag": "🇩🇪", "uni": "Heidelberg"},
        {"name": "James Whitfield", "country": "United Kingdom", "flag": "🇬🇧", "uni": "Oxford"}
    ]
    LANGUAGES = ["Spanish", "French", "German", "Italian", "Japanese", "Swahili"]
    RATES = [0.20, 0.30, 0.40, 0.50, 0.75, 0.80, 1.00]

    random.seed(42)
    tasks_data = []
    for i in range(1, 31):
        client = random.choice(CLIENTS)
        lang = random.choice(LANGUAGES)
        rate = random.choice(RATES)
        tasks_data.append({
            "Task ID": f"TQ-{1000 + i}",
            "Client": f"{client['flag']} {client['name']} ({client['uni']})",
            "Target Language": lang,
            "Reward ($)": rate,
            "Status": "Available"
        })
    st.dataframe(pd.DataFrame(tasks_data), use_container_width=True, hide_index=True)

# --- VIEW 5: FINANCIALS & M-PESA ---
elif view_mode == "💳 Financials & M-Pesa":
    st.markdown('<div class="main-header">Financial Dashboard & Cashout</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Manage earnings and process M-Pesa payouts.</div>', unsafe_allow_html=True)
    
    col_a, col_b = st.columns(2)
    with col_a:
        st.metric("Available Balance", "$ 56.30", "+$ 12.40 today")
    with col_b:
        st.metric("Total Withdrawals", "$ 342.80", "M-Pesa Verified")

# --- VIEW 6: AI TRANSLATOR ASSISTANT ---
elif view_mode == "✍️ AI Translator Assistant":
    st.markdown('<div class="main-header">AI Translator Workspace</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Draft and refine your translations.</div>', unsafe_allow_html=True)
    
    source_text = st.text_area("Source Paragraph", "The rapid expansion of renewable energy technology has fundamentally reshaped global economic policies.", height=120)
    if st.button("✨ Draft Translation"):
        st.info("High-Accuracy Translation Draft generated.")
