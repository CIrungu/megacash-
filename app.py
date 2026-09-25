import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import random
import os
import json
import hashlib

# ─────────────────────────────────────────────
#  PAGE CONFIG  (must be first Streamlit call)
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="MegaQash Writers · Translation Platform",
    page_icon="✍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
#  USER STORAGE  (simple JSON file)
# ─────────────────────────────────────────────
USERS_FILE = os.path.join(os.path.dirname(__file__), "users.json")

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users: dict):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

def hash_pw(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

# ─────────────────────────────────────────────
#  SESSION STATE DEFAULTS
# ─────────────────────────────────────────────
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "user_name" not in st.session_state:
    st.session_state.user_name = ""
if "user_email" not in st.session_state:
    st.session_state.user_email = ""
if "auth_tab" not in st.session_state:
    st.session_state.auth_tab = "login"   # "login" | "register"

# ─────────────────────────────────────────────
#  GLOBAL CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }

/* Hide default Streamlit chrome on auth screen */
.block-container {
    padding-top: 0rem !important;
    padding-bottom: 0rem !important;
    max-width: 100% !important;
}
header[data-testid="stHeader"] { background: transparent !important; }

/* ── Auth page layout ── */
.auth-wrap {
    display: grid;
    grid-template-columns: 1fr 1fr;
    min-height: 100vh;
    font-family: 'Inter', sans-serif;
}
.hero-side {
    background: linear-gradient(135deg, #0d0d1a 0%, #13132a 55%, #1a1a35 100%);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    padding: 2.5rem 3rem;
    position: relative;
    overflow: hidden;
}
.hero-side::before {
    content:'';
    position:absolute;width:420px;height:420px;border-radius:50%;
    background:radial-gradient(circle,rgba(232,24,92,.18) 0%,transparent 70%);
    top:-80px;left:-80px;pointer-events:none;
}
.hero-logo { display:flex;align-items:center;gap:.7rem;z-index:2;position:relative; }
.hero-logo .li {
    width:38px;height:38px;border-radius:10px;
    background:#e8185c;display:flex;align-items:center;justify-content:center;
    font-weight:900;font-size:1.1rem;color:#fff;
    box-shadow:0 4px 18px rgba(232,24,92,.35);
}
.hero-logo span { font-size:1rem;font-weight:700;color:#e8eaf6;letter-spacing:-.01em; }
.hero-body { z-index:2;position:relative; }
.eyebrow {
    font-size:.72rem;font-weight:600;letter-spacing:.16em;
    text-transform:uppercase;color:#e8185c;margin-bottom:1.4rem;
}
.headline {
    font-size:clamp(2.2rem,4vw,3.2rem);font-weight:900;
    line-height:1.08;color:#e8eaf6;letter-spacing:-.03em;
}
.headline .acc { color:#00e5a0; }
.hero-sub {
    margin-top:1.4rem;font-size:.93rem;line-height:1.65;
    color:#8888aa;max-width:340px;
}
.stats-row { display:flex;gap:2rem;margin-top:2.5rem;z-index:2;position:relative; }
.stat { display:flex;flex-direction:column; }
.stat-v { font-size:1.4rem;font-weight:800;color:#e8eaf6;letter-spacing:-.03em; }
.stat-l { font-size:.7rem;font-weight:500;color:#8888aa;margin-top:2px; }
.hero-foot { font-size:.7rem;color:#333355;z-index:2;position:relative; }

/* ── Dashboard CSS ── */
.block-container-inner {
    padding-top: 1rem !important;
    max-width: 98% !important;
}
.main-header {
    font-size: 2rem; font-weight: 800;
    color: #0b2d44; margin-bottom: 0.2rem;
}
.sub-header {
    font-size: 0.95rem; color: #4a6572; margin-bottom: 1rem;
}
.metric-card {
    background: linear-gradient(135deg, #0b2d44, #1a4a6b);
    color: white; padding: 1rem; border-radius: 12px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08); text-align: center;
}
.metric-value { font-size: 1.7rem; font-weight: 700; color: #a8d8ea; }
.metric-label {
    font-size: 0.8rem; text-transform: uppercase;
    letter-spacing: 0.5px; opacity: 0.9;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  AUTH SCREEN
# ─────────────────────────────────────────────
def show_auth():
    tab = st.session_state.auth_tab

    # Split-screen hero HTML (left panel — pure display)
    st.markdown("""
    <div style="
        background:linear-gradient(135deg,#0d0d1a 0%,#13132a 55%,#1a1a35 100%);
        padding:2.5rem 3rem;
        border-radius:16px;
        margin-bottom:0;
        min-height:480px;
        position:relative;
        overflow:hidden;
    ">
      <div style="display:flex;align-items:center;gap:.7rem;margin-bottom:3rem;">
        <div style="width:38px;height:38px;border-radius:10px;background:#e8185c;
             display:flex;align-items:center;justify-content:center;
             font-weight:900;font-size:1.1rem;color:#fff;
             box-shadow:0 4px 18px rgba(232,24,92,.35);">M</div>
        <span style="font-size:1rem;font-weight:700;color:#e8eaf6;">MegaQash Technologies</span>
      </div>
      <p style="font-size:.72rem;font-weight:600;letter-spacing:.16em;
                text-transform:uppercase;color:#e8185c;margin-bottom:1.2rem;">Your Next Chapter</p>
      <h2 style="font-size:2.8rem;font-weight:900;line-height:1.08;
                 color:#e8eaf6;letter-spacing:-.03em;margin:0;">
        Build momentum<br>
        <span style="color:#00e5a0;">that<br>compounds.</span>
      </h2>
      <p style="margin-top:1.2rem;font-size:.93rem;line-height:1.65;
                color:#8888aa;max-width:340px;">
        One workspace for your membership, referrals,<br>
        and the work that moves your business forward.
      </p>
      <div style="display:flex;gap:2rem;margin-top:2rem;">
        <div><div style="font-size:1.4rem;font-weight:800;color:#e8eaf6;">12k+</div>
             <div style="font-size:.7rem;color:#8888aa;">Active Writers</div></div>
        <div><div style="font-size:1.4rem;font-weight:800;color:#e8eaf6;">$2.4M</div>
             <div style="font-size:.7rem;color:#8888aa;">Paid Out</div></div>
        <div><div style="font-size:1.4rem;font-weight:800;color:#e8eaf6;">98%</div>
             <div style="font-size:.7rem;color:#8888aa;">Satisfaction</div></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Tab switcher
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        if st.button("🔑  Sign In", use_container_width=True,
                     type="primary" if tab == "login" else "secondary"):
            st.session_state.auth_tab = "login"
            st.rerun()
    with col_t2:
        if st.button("✨  Create Account", use_container_width=True,
                     type="primary" if tab == "register" else "secondary"):
            st.session_state.auth_tab = "register"
            st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # ── LOGIN ──
    if tab == "login":
        st.markdown("#### Welcome Back · Enter your space")
        with st.form("login_form", clear_on_submit=False):
            email = st.text_input("Email", placeholder="you@example.com")
            password = st.text_input("Password", type="password", placeholder="••••••••")
            submitted = st.form_submit_button("Open dashboard  ↗", use_container_width=True, type="primary")

        if submitted:
            if not email or not password:
                st.error("Please fill in all fields.")
            else:
                users = load_users()
                key = email.strip().lower()
                if key not in users:
                    st.error("No account found with this email. Please register first.")
                elif users[key]["password"] != hash_pw(password):
                    st.error("Incorrect password. Please try again.")
                else:
                    st.session_state.authenticated = True
                    st.session_state.user_email = key
                    st.session_state.user_name = users[key]["name"]
                    st.success(f"Welcome back, {users[key]['name']}! Loading dashboard…")
                    st.rerun()

    # ── REGISTER ──
    else:
        st.markdown("#### Create Your Space · Join thousands of writers")
        with st.form("register_form", clear_on_submit=False):
            name     = st.text_input("Full Name", placeholder="Jane Doe")
            email    = st.text_input("Email", placeholder="you@example.com")
            password = st.text_input("Password (min 6 chars)", type="password", placeholder="••••••••")
            confirm  = st.text_input("Confirm Password", type="password", placeholder="••••••••")
            submitted = st.form_submit_button("Create account  ↗", use_container_width=True, type="primary")

        if submitted:
            if not name or not email or not password or not confirm:
                st.error("Please fill in all fields.")
            elif len(password) < 6:
                st.error("Password must be at least 6 characters.")
            elif password != confirm:
                st.error("Passwords do not match.")
            else:
                users = load_users()
                key = email.strip().lower()
                if key in users:
                    st.error("An account with this email already exists. Please sign in.")
                else:
                    users[key] = {"name": name.strip(), "password": hash_pw(password)}
                    save_users(users)
                    st.session_state.authenticated = True
                    st.session_state.user_email = key
                    st.session_state.user_name = name.strip()
                    st.success(f"Account created! Welcome, {name.strip()}! Loading dashboard…")
                    st.rerun()

# ─────────────────────────────────────────────
#  DASHBOARD  (shown only when authenticated)
# ─────────────────────────────────────────────
def get_html_content():
    html_path = os.path.join(os.path.dirname(__file__), "index.html")
    if os.path.exists(html_path):
        with open(html_path, "r", encoding="utf-8") as f:
            return f.read()
    return "<h3>Error: index.html not found.</h3>"

def show_dashboard():
    CLIENTS = [
        {"name": "Emily Carter",     "country": "United States", "flag": "🇺🇸", "uni": "NYU"},
        {"name": "Liam O'Sullivan",  "country": "Ireland",       "flag": "🇮🇪", "uni": "Trinity College"},
        {"name": "Sophie Müller",    "country": "Germany",       "flag": "🇩🇪", "uni": "Heidelberg"},
        {"name": "James Whitfield",  "country": "United Kingdom","flag": "🇬🇧", "uni": "Oxford"},
        {"name": "Chloé Dubois",     "country": "France",        "flag": "🇫🇷", "uni": "Sorbonne"},
        {"name": "Isabella Rossi",   "country": "Italy",         "flag": "🇮🇹", "uni": "Bocconi"},
        {"name": "Ava Thompson",     "country": "Canada",        "flag": "🇨🇦", "uni": "UofT"},
    ]
    LANGUAGES = ["Spanish","French","German","Italian","Portuguese","Japanese","Mandarin","Swahili"]
    RATES     = [0.20, 0.30, 0.40, 0.50, 0.75, 0.80, 1.00]

    # ── Sidebar ──
    initials = "".join(w[0] for w in st.session_state.user_name.split()).upper()[:2]
    st.sidebar.markdown(f"""
    <div style="display:flex;align-items:center;gap:.6rem;
                background:rgba(11,45,68,.08);border-radius:10px;padding:.6rem .9rem;margin-bottom:.5rem;">
      <div style="width:36px;height:36px;border-radius:50%;
                  background:linear-gradient(135deg,#4a9ec9,#1a6e8c);
                  display:flex;align-items:center;justify-content:center;
                  font-weight:700;color:#fff;font-size:.85rem;">{initials}</div>
      <div>
        <div style="font-weight:700;font-size:.9rem;color:#0b2d44;">{st.session_state.user_name}</div>
        <div style="font-size:.72rem;color:#6b8fa3;">{st.session_state.user_email}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.sidebar.title("MegaQash Writers")
    st.sidebar.caption("Translation Task Platform")

    view_mode = st.sidebar.radio(
        "Navigation View",
        ["🌐 Live Web Platform","📊 Dashboard & Metrics",
         "🎯 Task Explorer","💳 Financials & M-Pesa","✍️ AI Translator Assistant"]
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🏅 Translator Status")
    st.sidebar.markdown("**Tier:** Gold Tier Translator")
    st.sidebar.markdown("**Rating:** ⭐ 4.9 / 5.0")
    st.sidebar.markdown("**Completed Tasks:** 147")
    st.sidebar.markdown("**On-Time Delivery:** 98%")

    st.sidebar.markdown("---")
    # ── LOGOUT BUTTON ── lives in sidebar, fully Streamlit-native
    if st.sidebar.button("⏻  Logout", use_container_width=True, type="secondary"):
        st.session_state.authenticated = False
        st.session_state.user_name = ""
        st.session_state.user_email = ""
        st.session_state.auth_tab = "login"
        st.rerun()

    # ── Views ──
    if view_mode == "🌐 Live Web Platform":
        html_content = get_html_content()
        components.html(html_content, height=920, scrolling=True)

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
            - **University Client Demands**: Direct requests from NYU, Oxford, Sorbonne, Heidelberg.
            - **Session Timer Control**: Ensures high quality & rapid SLAs for clients.
            """)
        with c2:
            st.success("""
            - **Dynamic Pending Drawer**: Real-time review drawer with navbar badge notification.
            - **Instant M-Pesa Payouts**: Direct mobile money transfer with instant reference.
            - **Quality Rating System**: Translator stats and tier progression (Gold / Platinum).
            """)

    elif view_mode == "🎯 Task Explorer":
        st.markdown('<div class="main-header">Task Explorer</div>', unsafe_allow_html=True)
        st.markdown('<div class="sub-header">Search and inspect available translation requests.</div>', unsafe_allow_html=True)
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1: selected_rate = st.selectbox("Pay Rate ($)", ["All"] + RATES)
        with col_f2: selected_lang = st.selectbox("Target Language", ["All"] + LANGUAGES)
        with col_f3: search_query  = st.text_input("Search Client or Keyword", "")
        random.seed(42)
        tasks_data = []
        for i in range(1, 41):
            client = random.choice(CLIENTS)
            lang   = random.choice(LANGUAGES)
            rate   = random.choice(RATES)
            dur    = random.choice([1,2,3,4,6,8,12,24])
            tasks_data.append({
                "Task ID": f"TQ-{1000+i}",
                "Client": f"{client['flag']} {client['name']} ({client['uni']})",
                "Target Language": lang,
                "Reward ($)": rate,
                "Turnaround (hrs)": dur,
                "Status": "Available"
            })
        df = pd.DataFrame(tasks_data)
        if selected_rate != "All": df = df[df["Reward ($)"] == float(selected_rate)]
        if selected_lang != "All": df = df[df["Target Language"] == selected_lang]
        if search_query: df = df[df["Client"].str.contains(search_query, case=False)]
        st.dataframe(df, use_container_width=True, hide_index=True)

    elif view_mode == "💳 Financials & M-Pesa":
        st.markdown('<div class="main-header">Financial Dashboard & Cashout</div>', unsafe_allow_html=True)
        st.markdown('<div class="sub-header">Manage earnings and process M-Pesa payouts.</div>', unsafe_allow_html=True)
        col_a, col_b, col_c = st.columns(3)
        with col_a: st.metric("Available Balance",      "$ 56.30",  "+$ 12.40 today")
        with col_b: st.metric("Total Withdrawals",      "$ 342.80", "M-Pesa Verified")
        with col_c: st.metric("Average Payout per Task","$ 0.58",   "Top Tier")
        st.markdown("---")
        st.markdown("### 📱 Instant M-Pesa Cashout Simulator")
        with st.form("withdraw_form"):
            withdraw_amount = st.number_input("Withdrawal Amount ($)", min_value=1.0, max_value=56.30, value=10.0, step=0.5)
            phone_number    = st.text_input("M-Pesa Phone Number", value="+254 712 345 678")
            submit_withdraw = st.form_submit_button("⚡ Withdraw to M-Pesa")
        if submit_withdraw:
            ref_code = f"MPX-{random.randint(9000,9999)}-KE"
            st.balloons()
            st.success(f"✅ **${withdraw_amount:.2f}** transferred to **{phone_number}**. Reference: `{ref_code}`.")
        st.markdown("### 📋 Recent Withdrawal Logs")
        withdrawals = [
            {"Amount":"$ 5.00", "Method":"M-Pesa Instant","Reference":"MPX-8823-KE","Status":"✅ Success","Date":"2024-09-24"},
            {"Amount":"$ 8.50", "Method":"M-Pesa Instant","Reference":"MPX-8712-KE","Status":"✅ Success","Date":"2024-09-23"},
            {"Amount":"$ 3.20", "Method":"M-Pesa Instant","Reference":"MPX-8634-KE","Status":"✅ Success","Date":"2024-09-22"},
            {"Amount":"$ 7.00", "Method":"M-Pesa Instant","Reference":"MPX-8521-KE","Status":"✅ Success","Date":"2024-09-21"},
            {"Amount":"$12.40", "Method":"M-Pesa Instant","Reference":"MPX-8409-KE","Status":"✅ Success","Date":"2024-09-20"},
        ]
        st.table(pd.DataFrame(withdrawals))

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


# ─────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────
if st.session_state.authenticated:
    show_dashboard()
else:
    show_auth()
