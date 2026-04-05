import streamlit as st
import requests
import time

# ─── 1. Page Config (Must be first) ──────────────────────────────────────────
st.set_page_config(
    page_title="Big Mart | Register",
    page_icon="🛒",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ─── 2. Bulletproof Routing & Auth ───────────────────────────────────────────
try:
    params = st.query_params
except AttributeError:
    params = st.experimental_get_query_params()

if "action" in params:
    action = params.get("action")
    if isinstance(action, list): action = action[0]

    # --- ROUTE TO LOGIN PAGE ---
    if action == "go_login":
        st.switch_page("app.py")

    # --- REGISTER LOGIC ---
    elif action == "register":
        em_val = params.get("em")
        if isinstance(em_val, list): em_val = em_val[0]
        pwd_val = params.get("pwd")
        if isinstance(pwd_val, list): pwd_val = pwd_val[0]
        
        try:
            res = requests.post("http://127.0.0.1:8000/register", json={"email": em_val, "password": pwd_val})
            if res.status_code == 200:
                st.success("✅ Account created successfully! Redirecting to Login...")
                time.sleep(2) # 2 sec ruk kar wapas login par bhej do
                st.switch_page("app.py")
            else:
                st.error(f"🚨 {res.json().get('detail')}")
        except Exception:
            st.error("🚨 Backend server is down!")
    
    try:
        st.query_params.clear()
    except AttributeError:
        st.experimental_set_query_params()


# ─── 3. Full Page CSS & HTML ─────────────────────────────────────────────────
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
.pwd-input { -webkit-text-security: disc; }
.pwd-toggle:checked ~ .pwd-input { -webkit-text-security: none; }
.eye-label { position: absolute; right: 18px; top: 50%; transform: translateY(-50%); font-size: 16px; cursor: pointer; z-index: 10; user-select: none; transition: color 0.2s; color: #B8C1D8; line-height: 1; }
.eye-label:hover { color: #7C3AED; }
.pwd-toggle:checked ~ .eye-label .eye-open { display: inline; }
.pwd-toggle:checked ~ .eye-label .eye-closed { display: none; }
.pwd-toggle:not(:checked) ~ .eye-label .eye-open { display: none; }
.pwd-toggle:not(:checked) ~ .eye-label .eye-closed { display: inline; }
.signin-btn { width: 100%; padding: 15px; background: linear-gradient(92deg, #7C3AED 0%, #4F46E5 100%); color: white !important; border: none; border-radius: 50px; font-size: 13px; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; cursor: pointer; font-family: 'DM Sans', sans-serif !important; box-shadow: 0 8px 24px rgba(124,58,237,0.38); transition: all 0.25s ease; margin-top: 10px; position: relative; overflow: hidden; }
.signin-btn:hover { transform: translateY(-2px); box-shadow: 0 14px 32px rgba(124,58,237,0.5); }
.signin-btn:active { transform: translateY(0); }
.bottom-text { text-align: center; font-size: 12.5px; color: #94A3B8 !important; margin-top: 20px; display: flex; justify-content: center; align-items: center; gap: 6px; }
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
<div class="brand-logo">🛒 Big Mart <span>intelligence</span></div>
<h1 class="hello-title">Create Account</h1>
<p class="signin-subtitle">Join the AI forecasting platform</p>

<form action="" target="_top" method="GET" style="margin:0; padding:0;">
  
  <div class="input-wrap">
    <span class="icon">✉️</span>
    <input type="email" name="em" placeholder="E-mail (e.g. newuser@bigmart.com)" required />
  </div>

  <div class="input-wrap">
    <span class="icon">🔒</span>
    <input type="checkbox" id="show-pass" class="pwd-toggle" style="display: none !important; width: 0 !important; height: 0 !important; padding: 0 !important; margin: 0 !important; border: none !important; position: absolute; visibility: hidden;">
    <input type="text" name="pwd" class="pwd-input" placeholder="Create a Password" required />
    <label for="show-pass" class="eye-label">
      <span class="eye-open">🙈</span>
      <span class="eye-closed">👁️</span>
    </label>
  </div>

  <button type="submit" name="action" value="register" class="signin-btn">SIGN UP</button>
  
  <p class="bottom-text">
    Already have an account? 
    <button type="submit" name="action" value="go_login" formnovalidate style="background:none; border:none; color:#7C3AED; font-weight:700; cursor:pointer; font-size:12.5px; padding:0; font-family:inherit;">
      Sign In
    </button>
  </p>
</form>

</div>

<div class="right-panel">
<div class="orb1"></div>
<div class="orb2"></div>
<div class="orb3"></div>
<div class="right-inner">
<h3>Empower Your Sales</h3>
<p>Create an account to access<br>enterprise-grade AI tools and<br>maximize your profits.</p>
<span class="right-badge">⚡ Setup is Free</span>
</div>
</div>

</div>
</div>
"""

st.markdown(html_content, unsafe_allow_html=True)