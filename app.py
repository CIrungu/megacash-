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
#  GLOBAL CSS
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }

.block-container {
    padding-top: 0rem !important;
    padding-bottom: 0rem !important;
    max-width: 100% !important;
}
header[data-testid="stHeader"] { background: transparent !important; }

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
#  DATA PERSISTENCE LAYER
# ─────────────────────────────────────────────
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
os.makedirs(DATA_DIR, exist_ok=True)
ADMINS_FILE = os.path.join(DATA_DIR, "admins.json")
PUBLISHED_FILE = os.path.join(DATA_DIR, "published_tasks.json")

def hash_password(password):
    """SHA-256 hash for password storage."""
    return hashlib.sha256(password.encode()).hexdigest()

def load_admins():
    """Load admin accounts from persistent JSON file."""
    if os.path.exists(ADMINS_FILE):
        with open(ADMINS_FILE, "r") as f:
            return json.load(f)
    return {}

def save_admins(admins):
    """Save admin accounts to persistent JSON file."""
    with open(ADMINS_FILE, "w") as f:
        json.dump(admins, f, indent=2)

def seed_admin():
    """Ensure a default super-admin account exists."""
    admins = load_admins()
    default_email = "admin@megaqash.com"
    if default_email not in admins:
        admins[default_email] = {
            "name": "Super Admin",
            "password_hash": hash_password("MegaQash2024!"),
            "role": "super_admin"
        }
        save_admins(admins)

DEFAULT_ADMIN_EMAIL = "admin@megaqash.com"
DEFAULT_ADMIN_PASS = "MegaQash2024!"

def verify_admin(email, password):
    """Verify admin credentials. Returns admin dict on success, None on failure."""
    if not email or not password:
        return None
    email_clean = email.strip().lower()
    # Built-in fallback so super admin always logs in successfully
    if email_clean == DEFAULT_ADMIN_EMAIL and password == DEFAULT_ADMIN_PASS:
        return {"name": "Super Admin", "email": DEFAULT_ADMIN_EMAIL, "role": "super_admin"}
    admins = load_admins()
    if email_clean in admins:
        if admins[email_clean].get("password_hash") == hash_password(password):
            return admins[email_clean]
    return None

def load_published_tasks():
    """Load published task IDs from persistent JSON file."""
    if os.path.exists(PUBLISHED_FILE):
        try:
            with open(PUBLISHED_FILE, "r") as f:
                return set(json.load(f))
        except (json.JSONDecodeError, TypeError):
            return set()
    return set()

def save_published_tasks(tasks):
    """Save published task IDs to persistent JSON file."""
    with open(PUBLISHED_FILE, "w") as f:
        json.dump(sorted(list(tasks)), f)

# ── Seed admin on startup ──
seed_admin()

# ─────────────────────────────────────────────
#  SESSION STATE INITIALIZATION
# ─────────────────────────────────────────────
if "published_tasks" not in st.session_state:
    st.session_state.published_tasks = load_published_tasks()
if "admin_authenticated" not in st.session_state:
    st.session_state.admin_authenticated = False
if "admin_email" not in st.session_state:
    st.session_state.admin_email = ""
if "admin_name" not in st.session_state:
    st.session_state.admin_name = ""
if "current_view" not in st.session_state:
    st.session_state.current_view = "🌐 Live Web Platform"

# ─────────────────────────────────────────────
#  DASHBOARD  (loads directly — no auth required)
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

    # ── Check query parameters for direct admin access (?view=admin or ?admin=true) ──
    query_view = str(st.query_params.get("view", "")).lower()
    is_admin_query = ("admin" in st.query_params) or (query_view == "admin")

    NAV_OPTIONS = [
        "🌐 Live Web Platform",
        "📊 Dashboard & Metrics",
        "🎯 Task Explorer",
        "💳 Financials & M-Pesa",
        "✍️ AI Translator Assistant",
        "🛡️ Admin Dashboard"
    ]

    if is_admin_query:
        st.session_state.current_view = "🛡️ Admin Dashboard"
    elif "current_view" not in st.session_state or st.session_state.current_view not in NAV_OPTIONS:
        st.session_state.current_view = "🌐 Live Web Platform"

    # ── Top Bar Switcher (Always visible on mobile & desktop) ──
    col_t_brand, col_t_btn = st.columns([3, 1])
    with col_t_brand:
        st.markdown("""
        <div style="display:flex;align-items:center;gap:0.6rem;padding:0.3rem 0;margin-bottom:0.4rem;">
          <span style="font-size:1.3rem;">✍️</span>
          <span style="font-weight:800;font-size:1.15rem;color:#0b2d44;letter-spacing:-0.2px;">MegaQash Writers</span>
          <span style="background:#e8f2fa;color:#0b4b6b;font-size:0.72rem;font-weight:700;padding:0.18rem 0.6rem;border-radius:12px;">Open Platform</span>
        </div>
        """, unsafe_allow_html=True)
    with col_t_btn:
        if st.session_state.current_view == "🛡️ Admin Dashboard":
            if st.button("🌐 Client Platform", key="top_to_client", use_container_width=True, type="secondary"):
                st.session_state.current_view = "🌐 Live Web Platform"
                if "admin" in st.query_params: del st.query_params["admin"]
                if "view" in st.query_params: del st.query_params["view"]
                st.rerun()
        else:
            if st.button("🛡️ Admin Portal", key="top_to_admin", use_container_width=True, type="primary"):
                st.session_state.current_view = "🛡️ Admin Dashboard"
                st.query_params["view"] = "admin"
                st.rerun()

    # ── Sidebar ──
    st.sidebar.markdown(f"""
    <div style="display:flex;align-items:center;gap:.6rem;
                background:rgba(11,45,68,.08);border-radius:10px;padding:.6rem .9rem;margin-bottom:.5rem;">
      <div style="width:36px;height:36px;border-radius:50%;
                  background:linear-gradient(135deg,#4a9ec9,#1a6e8c);
                  display:flex;align-items:center;justify-content:center;
                  font-weight:700;color:#fff;font-size:.85rem;">MW</div>
      <div>
        <div style="font-weight:700;font-size:.9rem;color:#0b2d44;">MegaQash Writer</div>
        <div style="font-size:.72rem;color:#6b8fa3;">writer@megaqash.com</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    col_sb1, col_sb2 = st.sidebar.columns(2)
    with col_sb1:
        if st.sidebar.button("🌐 Client View", key="sb_client_btn", use_container_width=True,
                             type="primary" if st.session_state.current_view != "🛡️ Admin Dashboard" else "secondary"):
            st.session_state.current_view = "🌐 Live Web Platform"
            if "admin" in st.query_params: del st.query_params["admin"]
            if "view" in st.query_params: del st.query_params["view"]
            st.rerun()
    with col_sb2:
        if st.sidebar.button("🛡️ Admin Portal", key="sb_admin_btn", use_container_width=True,
                             type="primary" if st.session_state.current_view == "🛡️ Admin Dashboard" else "secondary"):
            st.session_state.current_view = "🛡️ Admin Dashboard"
            st.query_params["view"] = "admin"
            st.rerun()

    st.sidebar.title("MegaQash Writers")
    st.sidebar.caption("Translation Task Platform")

    cur_idx = NAV_OPTIONS.index(st.session_state.current_view)
    selected_view = st.sidebar.radio(
        "Navigation View",
        NAV_OPTIONS,
        index=cur_idx,
        key="nav_radio"
    )
    if selected_view != st.session_state.current_view:
        st.session_state.current_view = selected_view
        if selected_view == "🛡️ Admin Dashboard":
            st.query_params["view"] = "admin"
        else:
            if "admin" in st.query_params: del st.query_params["admin"]
            if "view" in st.query_params: del st.query_params["view"]
        st.rerun()

    view_mode = st.session_state.current_view

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🏅 Translator Status")
    st.sidebar.markdown("**Tier:** Gold Tier Translator")
    st.sidebar.markdown("**Rating:** ⭐ 4.9 / 5.0")
    st.sidebar.markdown("**Completed Tasks:** 147")
    st.sidebar.markdown("**On-Time Delivery:** 98%")

    # ── Views ──
    if view_mode == "🌐 Live Web Platform":
        html_content = get_html_content()
        # Inject published task IDs into the HTML so the client JS knows which tasks are available
        published_ids = list(st.session_state.published_tasks)
        injection_script = f'<script>window.__ADMIN_PUBLISHED_TASKS__ = {json.dumps(published_ids)};</script>'
        html_content = html_content.replace('</head>', injection_script + '</head>')
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

    elif view_mode == "🛡️ Admin Dashboard":
        show_admin_dashboard(CLIENTS, LANGUAGES, RATES)


# ─────────────────────────────────────────────
#  ADMIN LOGIN PORTAL
# ─────────────────────────────────────────────
def show_admin_login():
    """Render admin sign-in portal with seeded credentials hint."""
    st.markdown("")

    col_left, col_center, col_right = st.columns([1, 2, 1])
    with col_center:
        st.markdown("""
        <div style="background:linear-gradient(135deg,#1a1a2e,#16213e,#0f3460);
                    border-radius:20px;padding:2.5rem 2rem;margin-top:2rem;
                    box-shadow:0 12px 40px rgba(0,0,0,0.3);text-align:center;">
          <div style="font-size:3rem;margin-bottom:0.8rem;">🛡️</div>
          <div style="font-size:1.5rem;font-weight:800;color:#e8e8e8;letter-spacing:-0.3px;margin-bottom:0.3rem;">
            Admin Portal
          </div>
          <div style="font-size:0.85rem;color:#8fa8c8;">
            Sign in to manage and publish translation tasks.
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height:1.5rem;'></div>", unsafe_allow_html=True)

        with st.form("admin_login_form"):
            email = st.text_input("📧 Admin Email", value="admin@megaqash.com", placeholder="admin@megaqash.com")
            password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
            submitted = st.form_submit_button("🔐 Sign In", type="primary", use_container_width=True)

        if submitted:
            if not email or not password:
                st.error("❌ Please fill in both email and password.")
            else:
                admin = verify_admin(email, password)
                if admin:
                    st.session_state.admin_authenticated = True
                    st.session_state.admin_email = email.strip().lower()
                    st.session_state.admin_name = admin["name"]
                    st.success("✅ Logged in successfully!")
                    st.rerun()
                else:
                    st.error("❌ Invalid email or password. Please try again.")

        st.markdown("""
        <div style="background:#f0f4fa;border-radius:12px;padding:1rem;margin-top:1rem;
                    border:1px solid #d0d8e8;text-align:center;">
          <div style="font-size:0.78rem;color:#6b7c93;margin-bottom:0.3rem;font-weight:600;">
            🔑 Default Admin Credentials
          </div>
          <div style="font-size:0.82rem;color:#0b2d44;">
            <b>Email:</b> admin@megaqash.com<br>
            <b>Password:</b> MegaQash2024!
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)
        if st.button("🌐 Return to Client Platform (No Auth Required)", use_container_width=True):
            st.session_state.current_view = "🌐 Live Web Platform"
            if "admin" in st.query_params: del st.query_params["admin"]
            if "view" in st.query_params: del st.query_params["view"]
            st.rerun()


# ─────────────────────────────────────────────
#  ADMIN DASHBOARD FUNCTION
# ─────────────────────────────────────────────
def show_admin_dashboard(CLIENTS, LANGUAGES, RATES):
    """Admin control panel: view all translation tasks and publish them to make them available to clients."""

    # ── Auth Gate ──
    if not st.session_state.admin_authenticated:
        show_admin_login()
        return

    # ── Signed-in bar + Navigation + Logout ──
    col_user, col_client, col_logout = st.columns([4, 2, 1])
    with col_user:
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:0.6rem;margin-bottom:0.5rem;">
          <div style="width:32px;height:32px;border-radius:50%;
                      background:linear-gradient(135deg,#27ae60,#2ecc71);
                      display:flex;align-items:center;justify-content:center;
                      font-weight:700;color:#fff;font-size:0.8rem;">
            {st.session_state.admin_name[0].upper()}
          </div>
          <div>
            <span style="font-weight:700;font-size:0.88rem;color:#0b2d44;">
              {st.session_state.admin_name}
            </span>
            <span style="font-size:0.75rem;color:#6b8fa3;margin-left:0.3rem;">
              {st.session_state.admin_email}
            </span>
          </div>
        </div>
        """, unsafe_allow_html=True)
    with col_client:
        if st.button("🌐 Switch to Client View", use_container_width=True):
            st.session_state.current_view = "🌐 Live Web Platform"
            if "admin" in st.query_params: del st.query_params["admin"]
            if "view" in st.query_params: del st.query_params["view"]
            st.rerun()
    with col_logout:
        if st.button("🚪 Sign Out", use_container_width=True):
            st.session_state.admin_authenticated = False
            st.session_state.admin_email = ""
            st.session_state.admin_name = ""
            st.rerun()

    # ── Admin Header ──
    st.markdown("""
    <div style="background:linear-gradient(135deg,#1a1a2e,#16213e,#0f3460);
                border-radius:18px;padding:1.8rem 2rem;margin-bottom:1.5rem;
                box-shadow:0 8px 32px rgba(0,0,0,0.2);">
      <div style="display:flex;align-items:center;gap:0.8rem;margin-bottom:0.6rem;">
        <span style="font-size:1.8rem;">🛡️</span>
        <span style="font-size:1.6rem;font-weight:800;color:#e8e8e8;letter-spacing:-0.3px;">Admin Control Center</span>
      </div>
      <div style="font-size:0.88rem;color:#8fa8c8;line-height:1.5;">
        Manage and publish translation tasks. Tasks remain <b style="color:#f39c12;">"Already Taken"</b> on the
        client side until you press <b style="color:#27ae60;">Submit</b> to make them available.
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Admin Stats Row ──
    total_tasks = 200
    published_count = len(st.session_state.published_tasks)
    pending_count = total_tasks - published_count

    col_s1, col_s2, col_s3, col_s4 = st.columns(4)
    with col_s1:
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#0f3460,#1a4a6b);color:white;padding:1rem;
                    border-radius:14px;text-align:center;box-shadow:0 4px 12px rgba(0,0,0,0.15);">
          <div style="font-size:1.8rem;font-weight:800;color:#a8d8ea;">{total_tasks}</div>
          <div style="font-size:0.75rem;text-transform:uppercase;letter-spacing:0.5px;opacity:0.9;">Total Tasks</div>
        </div>
        """, unsafe_allow_html=True)
    with col_s2:
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#1b5e20,#2e7d32);color:white;padding:1rem;
                    border-radius:14px;text-align:center;box-shadow:0 4px 12px rgba(0,0,0,0.15);">
          <div style="font-size:1.8rem;font-weight:800;color:#a5d6a7;">{published_count}</div>
          <div style="font-size:0.75rem;text-transform:uppercase;letter-spacing:0.5px;opacity:0.9;">Published</div>
        </div>
        """, unsafe_allow_html=True)
    with col_s3:
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#e65100,#f57c00);color:white;padding:1rem;
                    border-radius:14px;text-align:center;box-shadow:0 4px 12px rgba(0,0,0,0.15);">
          <div style="font-size:1.8rem;font-weight:800;color:#ffe0b2;">{pending_count}</div>
          <div style="font-size:0.75rem;text-transform:uppercase;letter-spacing:0.5px;opacity:0.9;">Unpublished</div>
        </div>
        """, unsafe_allow_html=True)
    with col_s4:
        pct = int((published_count / total_tasks) * 100) if total_tasks > 0 else 0
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#4a148c,#6a1b9a);color:white;padding:1rem;
                    border-radius:14px;text-align:center;box-shadow:0 4px 12px rgba(0,0,0,0.15);">
          <div style="font-size:1.8rem;font-weight:800;color:#ce93d8;">{pct}%</div>
          <div style="font-size:0.75rem;text-transform:uppercase;letter-spacing:0.5px;opacity:0.9;">Published Rate</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)

    # ── Bulk Actions ──
    col_bulk1, col_bulk2, col_bulk3 = st.columns([1, 1, 2])
    with col_bulk1:
        if st.button("✅ Publish All Tasks", use_container_width=True, type="primary"):
            st.session_state.published_tasks = set(range(1, total_tasks + 1))
            save_published_tasks(st.session_state.published_tasks)
            st.rerun()
    with col_bulk2:
        if st.button("🔄 Unpublish All Tasks", use_container_width=True):
            st.session_state.published_tasks = set()
            save_published_tasks(st.session_state.published_tasks)
            st.rerun()

    st.markdown("---")

    # ── Filters ──
    st.markdown("### 📋 Translation Task Control Panel")
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        status_filter = st.selectbox("Filter by Status", ["All", "Published", "Unpublished"])
    with col_f2:
        lang_filter = st.selectbox("Filter by Language", ["All"] + LANGUAGES, key="admin_lang")
    with col_f3:
        rate_filter = st.selectbox("Filter by Rate ($)", ["All"] + RATES, key="admin_rate")

    # ── Generate task data (same seed as client side) ──
    language_pairs = [
        {"code": "es", "name": "Spanish"},  {"code": "fr", "name": "French"},
        {"code": "de", "name": "German"},   {"code": "it", "name": "Italian"},
        {"code": "pt", "name": "Portuguese"},{"code": "ja", "name": "Japanese"},
        {"code": "zh", "name": "Mandarin"}, {"code": "ko", "name": "Korean"},
        {"code": "ru", "name": "Russian"},  {"code": "ar", "name": "Arabic"},
        {"code": "hi", "name": "Hindi"},    {"code": "nl", "name": "Dutch"},
        {"code": "sv", "name": "Swedish"},  {"code": "tr", "name": "Turkish"},
        {"code": "pl", "name": "Polish"},   {"code": "vi", "name": "Vietnamese"},
        {"code": "th", "name": "Thai"},     {"code": "id", "name": "Indonesian"},
        {"code": "el", "name": "Greek"},    {"code": "he", "name": "Hebrew"},
    ]
    paragraph_templates = [
        "Hi, how are you today?",
        "Thank you so much!",
        "See you tomorrow morning.",
        "The meeting starts at nine.",
        "Please send me the file.",
        "I love this weather.",
        "Where is the bathroom?",
        "Have a great weekend!",
        "Good morning, I hope you are having a wonderful day. The weather today is perfect for a walk in the park.",
        "Thank you very much for your help yesterday. I really appreciated your advice about the project.",
        "Excuse me, could you please tell me where the nearest train station is? I need to catch a train.",
    ]
    price_tiers = [0.20, 0.30, 0.40, 0.50, 0.75, 0.80, 1.00]
    all_clients = [
        {"name": "Emily Carter",     "country": "United States", "flag": "🇺🇸", "uni": "NYU"},
        {"name": "Liam O'Sullivan",  "country": "Ireland",       "flag": "🇮🇪", "uni": "Trinity College"},
        {"name": "Sophie Müller",    "country": "Germany",       "flag": "🇩🇪", "uni": "Heidelberg"},
        {"name": "James Whitfield",  "country": "United Kingdom","flag": "🇬🇧", "uni": "Oxford"},
        {"name": "Chloé Dubois",     "country": "France",        "flag": "🇫🇷", "uni": "Sorbonne"},
        {"name": "Isabella Rossi",   "country": "Italy",         "flag": "🇮🇹", "uni": "Bocconi"},
        {"name": "Ava Thompson",     "country": "Canada",        "flag": "🇨🇦", "uni": "UofT"},
        {"name": "Lucas van der Berg","country": "Netherlands",  "flag": "🇳🇱", "uni": "Utrecht"},
        {"name": "Oliver Hansen",    "country": "Denmark",       "flag": "🇩🇰", "uni": "Copenhagen"},
        {"name": "Mia Andersson",    "country": "Sweden",        "flag": "🇸🇪", "uni": "Lund"},
    ]

    tasks_data = []
    for i in range(total_tasks):
        task_id = i + 1
        lang = language_pairs[i % len(language_pairs)]
        paragraph = paragraph_templates[i % len(paragraph_templates)]
        client = all_clients[i % len(all_clients)]
        price = price_tiers[i % len(price_tiers)]
        deadline = [2, 4, 6, 8, 12, 24][i % 6]
        is_published = task_id in st.session_state.published_tasks

        tasks_data.append({
            "Task ID": task_id,
            "Ref": f"#MQ-2024-{str(task_id).zfill(4)}",
            "Client": f"{client['flag']} {client['name']}",
            "University": client['uni'],
            "Language": f"English → {lang['name']}",
            "Rate ($)": price,
            "Deadline (hrs)": deadline,
            "Description": f"Translate: '{paragraph[:60]}...'",
            "Status": "✅ Published" if is_published else "⏳ Unpublished",
            "_id": task_id,
            "_lang_name": lang['name'],
        })

    # ── Apply filters ──
    filtered_data = tasks_data
    if status_filter == "Published":
        filtered_data = [t for t in filtered_data if t["_id"] in st.session_state.published_tasks]
    elif status_filter == "Unpublished":
        filtered_data = [t for t in filtered_data if t["_id"] not in st.session_state.published_tasks]
    if lang_filter != "All":
        filtered_data = [t for t in filtered_data if lang_filter in t["_lang_name"]]
    if rate_filter != "All":
        filtered_data = [t for t in filtered_data if abs(t["Rate ($)"] - float(rate_filter)) < 0.001]

    st.markdown(f"**Showing {len(filtered_data)} tasks**")

    # ── Display tasks as interactive cards with submit buttons ──
    for task in filtered_data:
        task_id = task["_id"]
        is_pub = task_id in st.session_state.published_tasks

        # Card styling based on status
        if is_pub:
            border_color = "#27ae60"
            bg_color = "#f0faf4"
            status_badge = '<span style="background:#27ae60;color:white;padding:0.2rem 0.7rem;border-radius:30px;font-size:0.72rem;font-weight:700;">✅ Published</span>'
        else:
            border_color = "#f39c12"
            bg_color = "#fffdf5"
            status_badge = '<span style="background:#f39c12;color:white;padding:0.2rem 0.7rem;border-radius:30px;font-size:0.72rem;font-weight:700;">⏳ Unpublished</span>'

        st.markdown(f"""
        <div style="background:{bg_color};border:2px solid {border_color};border-radius:14px;
                    padding:1rem 1.2rem;margin-bottom:0.5rem;
                    box-shadow:0 2px 8px rgba(0,0,0,0.05);">
          <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:0.5rem;">
            <div style="display:flex;align-items:center;gap:0.6rem;">
              <span style="font-family:monospace;font-size:0.72rem;color:#7a9fb5;font-weight:600;">{task['Ref']}</span>
              <span style="font-weight:700;color:#0b2d44;font-size:0.88rem;">{task['Client']}</span>
              <span style="font-size:0.72rem;color:#6b93aa;">🎓 {task['University']}</span>
            </div>
            <div style="display:flex;align-items:center;gap:0.6rem;">
              <span style="font-weight:800;color:#106a4b;background:#e2f0e9;padding:0.15rem 0.6rem;border-radius:30px;font-size:0.85rem;">${task['Rate ($)']:.2f}</span>
              <span style="background:#e8f2fa;color:#0b4b6b;padding:0.15rem 0.6rem;border-radius:30px;font-size:0.72rem;font-weight:600;">{task['Language']}</span>
              <span style="font-size:0.72rem;color:#8a6d1a;">⏰ {task['Deadline (hrs)']}h</span>
              {status_badge}
            </div>
          </div>
        </div>
        """, unsafe_allow_html=True)

        # Submit / Unpublish button
        col_a1, col_a2, col_a3 = st.columns([4, 1, 1])
        with col_a2:
            if not is_pub:
                if st.button("📤 Submit", key=f"pub_{task_id}", use_container_width=True, type="primary"):
                    st.session_state.published_tasks.add(task_id)
                    save_published_tasks(st.session_state.published_tasks)
                    st.rerun()
        with col_a3:
            if is_pub:
                if st.button("↩️ Revoke", key=f"unpub_{task_id}", use_container_width=True):
                    st.session_state.published_tasks.discard(task_id)
                    save_published_tasks(st.session_state.published_tasks)
                    st.rerun()


# ─────────────────────────────────────────────
#  ENTRY POINT — dashboard loads directly
# ─────────────────────────────────────────────
show_dashboard()
