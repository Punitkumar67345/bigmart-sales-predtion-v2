import streamlit as st

# ─── 1. Page Config (Must be first) ──────────────────────────────────────────
st.set_page_config(
    page_title="Big Mart | Login",
    page_icon="🛒",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ─── 2. Bulletproof Routing (Browser Native) ─────────────────────────────────
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# Naya Streamlit aur Purana Streamlit dono ko support karne ke liye try-except
try:
    params = st.query_params
except AttributeError:
    params = st.experimental_get_query_params()

# Agar form submit hua hai, toh URL me do_login=1 aayega
if "do_login" in params:
    st.session_state.logged_in = True
    
    # Email fetch karna
    em_val = params.get("em", "admin@bigmart.com")
    if isinstance(em_val, list):
        em_val = em_val[0] if len(em_val) > 0 else "admin@bigmart.com"
    st.session_state.user_email = em_val
    
    # URL ko clean karna taaki refresh par atke nahi
    try:
        st.query_params.clear()
    except AttributeError:
        st.experimental_set_query_params()

# Agar login true hai toh direct Dashboard fek do
if st.session_state.logged_in:
    try:
        st.switch_page("pages/dashboard.py")
    except Exception as e:
        st.error(f"🚨 Routing Failed! Ensure dashboard is at `pages/dashboard.py`\n{e}")
        st.stop()


# ─── 3. Full Page CSS & HTML (Exactly your premium design) ───────────────────
# Note: HTML string ke andar ZERO indentation hai taaki Code Block na bane!
html_content = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700;800;900&family=DM+Sans:wght@300;400;500&display=swap');

*, html, body, [class*="css"] { font-family: 'DM Sans', sans-serif !important; box-sizing: border-box; }
.stApp { background: linear-gradient(135deg, #EAECF5 0%, #DDE2F0 100%); min-height: 100vh; }
#MainMenu, footer, header, [data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"], [data-testid="stSidebarNav"] { display: none !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }
.page-wrapper { display: flex; justify-content: center; align-items: center; min-height: 100vh; padding: 20px; }
.login-card { display: flex; width: 860px; max-width: 96vw; min-height: 430px; border-radius: 30px; overflow: hidden; box-shadow: 0 40px 80px rgba(90, 60, 200, 0.18), 0 8px 30px rgba(0,0,0,0.1); background: #fff; animation: cardIn 0.7s cubic-bezier(0.16, 1, 0.3, 1) both; }
@keyframes cardIn { from { opacity: 0; transform: translateY(30px) scale(0.97); } to { opacity: 1; transform: translateY(0) scale(1); } }
.left-panel { flex: 1.3; padding: 50px 48px 40px 48px; background: #ffffff; display: flex; flex-direction: column; justify-content: center; position: relative; z-index: 2; }
.brand-logo { font-family: 'Nunito', sans-serif !important; font-size: 13px; font-weight: 800; color: #7C3AED !important; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 28px; display: flex; align-items: center; gap: 8px; }
.brand-logo span { background: linear-gradient(90deg,#7C3AED,#4F46E5); color: white !important; padding: 4px 10px; border-radius: 8px; font-size: 11px; }
.hello-title { font-family: 'Nunito', sans-serif !important; font-size: 34px; font-weight: 900; color: #1A1035 !important; margin: 0 0 5px 0; letter-spacing: -0.8px; line-height: 1.1; }
.signin-subtitle { font-size: 14px; color: #94A3B8 !important; margin: 0 0 32px 0; font-weight: 400; }
.input-wrap { position: relative; margin-bottom: 15px; }
.input-wrap .icon { position: absolute; left: 18px; top: 50%; transform: translateY(-50%); font-size: 16px; z-index: 2; pointer-events: none; line-height: 1; }
.input-wrap input { width: 100%; padding: 14px 44px 14px 46px; border: 1.5px solid #E8EDF8; border-radius: 50px; font-size: 13.5px; font-family: 'DM Sans', sans-serif !important; color: #1A1035 !important; background: #F7F9FF; outline: none; transition: all 0.25s; -webkit-appearance: none; }
.input-wrap input:focus { border-color: #7C3AED; background: #fff; box-shadow: 0 0 0 4px rgba(124,58,237,0.08); }
.input-wrap input::placeholder { color: #B8C1D8 !important; }
.eye-btn { position: absolute; right: 16px; top: 50%; transform: translateY(-50%); background: none; border: none; cursor: pointer; font-size: 15px; color: #B8C1D8; padding: 0; line-height: 1; transition: color 0.2s; }
.eye-btn:hover { color: #7C3AED; }
.extras-row { display: flex; align-items: center; justify-content: space-between; margin: 6px 0 26px 4px; }
.remember { display: flex; align-items: center; gap: 8px; font-size: 12.5px; color: #64748B !important; cursor: pointer; user-select: none; }
.remember input[type="checkbox"] { width: 15px; height: 15px; accent-color: #7C3AED; cursor: pointer; }
.forgot { font-size: 12.5px; color: #7C3AED !important; font-weight: 600; cursor: pointer; text-decoration: none; transition: opacity 0.2s; }
.forgot:hover { opacity: 0.75; }
.signin-btn { width: 100%; padding: 15px; background: linear-gradient(92deg, #7C3AED 0%, #4F46E5 100%); color: white !important; border: none; border-radius: 50px; font-size: 13px; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; cursor: pointer; font-family: 'DM Sans', sans-serif !important; box-shadow: 0 8px 24px rgba(124,58,237,0.38); transition: all 0.25s ease; position: relative; overflow: hidden; }
.signin-btn:hover { transform: translateY(-2px); box-shadow: 0 14px 32px rgba(124,58,237,0.5); }
.signin-btn:active { transform: translateY(0); }
.bottom-text { text-align: center; font-size: 12.5px; color: #94A3B8 !important; margin-top: 20px; }
.bottom-text a { color: #7C3AED !important; font-weight: 700; cursor: pointer; text-decoration: none; }
.right-panel { flex: 1; background: linear-gradient(150deg, #9333EA 0%, #6D28D9 45%, #3730A3 100%); position: relative; overflow: hidden; display: flex; align-items: center; justify-content: center; padding: 40px 36px 40px 60px; }
.right-panel::before { content: ''; position: absolute; left: -72px; top: -10%; width: 145px; height: 120%; background: white; border-radius: 0 60% 60% 0 / 0 50% 50% 0; z-index: 1; }
.right-panel::after { content: ''; position: absolute; left: -40px; top: 50%; transform: translateY(-50%); width: 100px; height: 100px; background: white; border-radius: 50%; z-index: 2; }
.right-inner { position: relative; z-index: 3; color: white; text-align: center; }
.right-inner h3 { font-family: 'Nunito', sans-serif !important; font-size: 26px; font-weight: 900; color: white !important; margin: 0 0 16px 0; }
.right-inner p { font-size: 13px; color: rgba(255,255,255,0.82) !important; line-height: 1.75; margin: 0 0 24px 0; }
.right-badge { display: inline-block; background: rgba(255,255,255,0.15); border: 1px solid rgba(255,255,255,0.25); color: white !important; font-size: 11px; font-weight: 600; padding: 6px 16px; border-radius: 50px; letter-spacing: 1px; text-transform: uppercase; }
.orb1 { position: absolute; width: 220px; height: 220px; border-radius: 50%; background: rgba(255,255,255,0.06); top: -70px; right: -60px; }
.orb2 { position: absolute; width: 150px; height: 150px; border-radius: 50%; background: rgba(255,255,255,0.06); bottom: -40px; right: 10px; }
.orb3 { position: absolute; width: 80px; height: 80px; border-radius: 50%; background: rgba(255,255,255,0.08); top: 50%; right: 60%; }
</style>

<div class="page-wrapper">
<div class="login-card">

<div class="left-panel">
<div class="brand-logo">🛒 Big Mart <span>INTEL</span></div>
<h1 class="hello-title">Hello!</h1>
<p class="signin-subtitle">Sign in to your account</p>

<form action="" target="_top" method="GET" style="margin:0; padding:0;">
<input type="hidden" name="do_login" value="1">

<div class="input-wrap">
<span class="icon">✉️</span>
<input type="email" name="em" placeholder="E-mail (e.g. admin@bigmart.com)" required />
</div>

<div class="input-wrap">
<span class="icon">🔒</span>
<input type="password" name="pwd" placeholder="Password" required />
<button type="button" class="eye-btn" onclick="const p=this.previousElementSibling; p.type=p.type==='password'?'text':'password'; this.textContent=p.type==='password'?'👁️':'🙈';">👁️</button>
</div>

<div class="extras-row">
<label class="remember">
<input type="checkbox" checked /> Remember me
</label>
<a class="forgot" href="javascript:void(0);" onclick="alert('Forgot Password feature coming soon!');">Forgot password?</a>
</div>

<button type="submit" class="signin-btn">SIGN IN</button>
</form>

<p class="bottom-text">Don't have an account? <a href="javascript:void(0);" onclick="alert('Account creation coming soon!');">Create</a></p>
</div>

<div class="right-panel">
<div class="orb1"></div>
<div class="orb2"></div>
<div class="orb3"></div>
<div class="right-inner">
<h3>Welcome Back!</h3>
<p>AI-powered sales forecasting,<br>shelf intelligence &amp; multi-objective<br>optimization — all in one place.</p>
<span class="right-badge">⚡ Enterprise Grade</span>
</div>
</div>

</div>
</div>
"""

# Render the HTML safely
st.markdown(html_content, unsafe_allow_html=True)