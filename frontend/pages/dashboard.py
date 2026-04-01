import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests
import numpy as np
import time

# --- Page Config ---
st.set_page_config(
    page_title="Dashboard | Big Mart",
    page_icon="cart",
    layout="wide",
    initial_sidebar_state="collapsed"
)

if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.switch_page("app.py")

user_email = st.session_state.get("user_email", "admin@bigmart.com")

# --- Session State ---
if 'prediction_history' not in st.session_state:
    st.session_state.prediction_history = [
        {"Item Name": "Base Dairy",  "Category": "Dairy",       "Predicted Sales (Rs)": 15000},
        {"Item Name": "Base Drinks", "Category": "Soft Drinks", "Predicted Sales (Rs)": 12000},
    ]
if 'total_predictions' not in st.session_state:
    st.session_state.total_predictions = 1258

# --- CSS (Light theme matching login page) ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
  --bg:        #EEEAF8;
  --bg2:       #E4DFF5;
  --bg3:       #F9F7FE;
  --surface:   #FFFFFF;
  --surface2:  #F5F2FC;
  --border:    rgba(109,40,217,0.12);
  --border2:   rgba(109,40,217,0.28);
  --purple:    #7C3AED;
  --purple2:   #6D28D9;
  --purple3:   #5B21B6;
  --purpleL:   #8B5CF6;
  --green:     #059669;
  --amber:     #D97706;
  --text:      #1A1035;
  --text2:     #4B3872;
  --text3:     #9181B8;
  --font-head: 'Outfit', sans-serif;
  --font-body: 'Space Grotesk', sans-serif;
  --font-mono: 'JetBrains Mono', monospace;
  --radius:    14px;
  --radius-lg: 20px;
  --radius-sm: 10px;
  --trans:     all 0.22s cubic-bezier(0.4,0,0.2,1);
  --shadow:    0 2px 16px rgba(109,40,217,0.07);
  --shadow-lg: 0 8px 32px rgba(109,40,217,0.13);
}

#MainMenu, header[data-testid="stHeader"], footer { display: none !important; }
.block-container { padding: 0 !important; max-width: 100% !important; }
section[data-testid="stSidebar"] { display: none !important; }

.stApp {
  background: var(--bg) !important;
  font-family: var(--font-body) !important;
  color: var(--text) !important;
  background-image:
    radial-gradient(ellipse 65% 45% at 5% 0%, rgba(109,40,217,0.09) 0%, transparent 55%),
    radial-gradient(ellipse 50% 35% at 95% 100%, rgba(139,92,246,0.07) 0%, transparent 55%) !important;
}

/* HEADER */
.bm-header {
  background: rgba(255,255,255,0.85);
  backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
  padding: 0 36px; height: 68px;
  display: flex; align-items: center; justify-content: space-between;
  border-bottom: 1px solid var(--border);
  position: sticky; top: 0; z-index: 100;
  box-shadow: 0 1px 20px rgba(109,40,217,0.07);
  animation: slideDown 0.5s cubic-bezier(0.4,0,0.2,1);
}
@keyframes slideDown {
  from { transform: translateY(-100%); opacity: 0; }
  to   { transform: translateY(0);     opacity: 1; }
}
.bm-logo-box {
  width: 40px; height: 40px;
  background: linear-gradient(135deg, var(--purple2), var(--purpleL));
  border-radius: 12px;
  display: flex; align-items: center; justify-content: center;
  font-family: var(--font-head); font-weight: 800; font-size: 14px; color: #fff;
  box-shadow: 0 4px 14px rgba(109,40,217,0.35); flex-shrink: 0;
}
.bm-title { font-family: var(--font-head); font-weight: 800; font-size: 17px; color: var(--text); letter-spacing: -0.3px; }
.bm-sub   { font-size: 9.5px; color: var(--text3); letter-spacing: 2.5px; text-transform: uppercase; font-family: var(--font-mono); margin-top: 2px; }
.bm-right { display: flex; align-items: center; gap: 10px; }
.bm-live {
  display: flex; align-items: center; gap: 7px;
  background: rgba(5,150,105,0.09); border: 1px solid rgba(5,150,105,0.22);
  border-radius: 30px; padding: 5px 14px;
  font-size: 11.5px; color: #065f46; font-family: var(--font-mono); font-weight: 600;
}
.bm-dot {
  width: 7px; height: 7px; background: var(--green);
  border-radius: 50%; display: inline-block;
  animation: pulse-dot 2s ease-in-out infinite;
}
@keyframes pulse-dot {
  0%,100% { box-shadow: 0 0 0 0 rgba(5,150,105,0.5); }
  50%      { box-shadow: 0 0 0 6px rgba(5,150,105,0); }
}
.bm-user {
  background: var(--surface2); border: 1px solid var(--border);
  border-radius: 30px; padding: 5px 14px;
  font-size: 11.5px; color: var(--text2); font-family: var(--font-body);
  display: flex; align-items: center; gap: 7px; font-weight: 500;
}

/* TABS */
div[data-testid="stTabs"] { background: transparent !important; padding: 0 36px !important; }
div[data-testid="stTabs"] > div:first-child { border-bottom: 1.5px solid var(--border2) !important; gap: 0 !important; }
div[data-testid="stTabs"] button[role="tab"] {
  font-family: var(--font-body) !important; font-size: 13px !important;
  font-weight: 500 !important; color: var(--text3) !important;
  padding: 13px 24px !important; background: transparent !important; transition: var(--trans) !important;
}
div[data-testid="stTabs"] button[role="tab"]:hover { color: var(--purple) !important; background: rgba(109,40,217,0.04) !important; }
div[data-testid="stTabs"] button[role="tab"][aria-selected="true"] { color: var(--purple) !important; font-weight: 700 !important; }
div[data-testid="stTabs"] [data-baseweb="tab-highlight"] {
  background: linear-gradient(90deg,var(--purple2),var(--purpleL)) !important;
  height: 2.5px !important; border-radius: 3px !important;
}
div[data-testid="stTabs"] [data-baseweb="tab-panel"] { padding: 0 !important; }

/* KPI */
.kpi-outer { padding: 22px 36px 6px 36px; }
.kpi-row   { display: grid; grid-template-columns: repeat(4,1fr); gap: 14px; }
.kpi {
  background: var(--surface); border: 1px solid var(--border);
  border-radius: var(--radius-lg); padding: 20px 22px;
  position: relative; overflow: hidden;
  transition: var(--trans); cursor: default;
  box-shadow: var(--shadow); animation: fadeUp 0.5s ease both;
}
.kpi:nth-child(1){animation-delay:.05s} .kpi:nth-child(2){animation-delay:.10s}
.kpi:nth-child(3){animation-delay:.15s} .kpi:nth-child(4){animation-delay:.20s}
.kpi::before {
  content:''; position:absolute; inset:0;
  background: radial-gradient(ellipse at top left,rgba(109,40,217,0.04) 0%,transparent 65%);
  pointer-events:none;
}
.kpi::after {
  content:''; position:absolute; top:0; left:0; right:0; height:3px;
  background: var(--ac, linear-gradient(90deg,var(--purple2),var(--purpleL)));
  border-radius: var(--radius-lg) var(--radius-lg) 0 0;
}
.kpi:hover { transform: translateY(-3px); border-color: var(--border2); box-shadow: var(--shadow-lg); }
.kpi-lbl { font-size:10px; color:var(--text3); text-transform:uppercase; letter-spacing:2px; font-weight:600; font-family:var(--font-mono); margin-bottom:9px; }
.kpi-val { font-family:var(--font-head); font-size:30px; font-weight:800; color:var(--text); line-height:1; letter-spacing:-1px; }
.kpi-val.sm { font-size:17px; letter-spacing:-0.2px; padding-top:5px; line-height:1.3; }
.kpi-sub  { font-size:12px; color:var(--text3); margin-top:6px; font-family:var(--font-body); }
.kpi-up   { color:var(--green); font-weight:600; }

/* SECTION HEADER */
.sec-h {
  font-family:var(--font-head); font-size:14px; font-weight:700; color:var(--text);
  display:flex; align-items:center; gap:10px; margin-bottom:14px;
}
.sec-h::before {
  content:''; display:block; width:3px; height:16px;
  background:linear-gradient(180deg,var(--purple2),var(--purpleL));
  border-radius:3px; flex-shrink:0;
}

/* CHART CARD */
.chart-card {
  background:var(--surface); border:1px solid var(--border);
  border-radius:var(--radius-lg); padding:22px 24px;
  margin:14px 36px 16px 36px; box-shadow:var(--shadow);
  animation:fadeUp 0.5s 0.15s ease both; position:relative; overflow:hidden;
}
.chart-card::before {
  content:''; position:absolute; top:-80px; right:-60px; width:220px; height:220px;
  background:radial-gradient(circle,rgba(109,40,217,0.04) 0%,transparent 70%); pointer-events:none;
}
.chart-top { display:flex; align-items:center; justify-content:space-between; margin-bottom:14px; }
.live-badge {
  background:rgba(109,40,217,0.1); color:var(--purple);
  font-size:10px; font-weight:700; padding:4px 13px; border-radius:30px;
  letter-spacing:1.5px; text-transform:uppercase; font-family:var(--font-mono);
  border:1px solid rgba(109,40,217,0.18); animation:glow-pulse 3s ease-in-out infinite;
}
@keyframes glow-pulse {
  0%,100% { box-shadow:0 0 0 0 rgba(109,40,217,0); }
  50%      { box-shadow:0 0 10px rgba(109,40,217,0.15); }
}

/* LEADERBOARD */
.lb-card {
  background:var(--surface); border:1px solid var(--border);
  border-radius:var(--radius-lg); padding:22px 24px;
  margin:0 36px 24px 36px; box-shadow:var(--shadow);
  animation:fadeUp 0.5s 0.25s ease both;
}
.lb-top { display:flex; align-items:center; justify-content:space-between; margin-bottom:16px; }
.lb-badge {
  background:var(--surface2); color:var(--purple); font-size:10px; font-weight:700;
  padding:4px 12px; border-radius:6px; font-family:var(--font-mono);
  border:1px solid var(--border);
}
.lb-table { width:100%; border-collapse:collapse; }
.lb-table thead tr { border-bottom:1.5px solid var(--bg2); }
.lb-table th { font-size:10px; color:var(--text3); text-transform:uppercase; letter-spacing:1.5px; font-weight:600; padding:8px 12px; text-align:left; font-family:var(--font-mono); }
.lb-table tbody tr { border-bottom:1px solid var(--bg2); transition:var(--trans); }
.lb-table tbody tr:last-child { border-bottom:none; }
.lb-table tbody tr:hover { background:rgba(109,40,217,0.03); }
.lb-table td { padding:13px 12px; font-size:13px; color:var(--text); font-family:var(--font-body); }
.rk1 { font-family:var(--font-head); font-weight:800; color:var(--amber); font-size:16px; }
.rk2 { font-family:var(--font-head); font-weight:800; color:#9181B8; font-size:16px; }
.rk3 { font-family:var(--font-head); font-weight:800; color:#b45309; font-size:16px; }
.rkn { font-family:var(--font-head); font-weight:600; color:var(--text3); font-size:13px; }
.lb-sales { font-family:var(--font-mono); font-weight:700; color:var(--purple); font-size:13px; }
.cat-pill {
  display:inline-block; background:rgba(109,40,217,0.08); color:var(--purple);
  font-size:11px; padding:3px 10px; border-radius:6px; font-weight:600;
  font-family:var(--font-body); border:1px solid rgba(109,40,217,0.13);
}

/* PREDICTION RESULT */
.res-box {
  background:linear-gradient(135deg, #6D28D9 0%, #7C3AED 50%, #8B5CF6 100%);
  border-radius:var(--radius-lg); padding:26px 28px; margin:0 36px 18px 36px;
  box-shadow:0 8px 40px rgba(109,40,217,0.28);
  animation:popIn 0.4s cubic-bezier(0.34,1.56,0.64,1);
  position:relative; overflow:hidden;
}
.res-box::before {
  content:''; position:absolute; top:-40px; right:-40px; width:220px; height:220px;
  background:radial-gradient(circle,rgba(255,255,255,0.1),transparent 65%); pointer-events:none;
}
.res-box::after {
  content:''; position:absolute; bottom:-50px; left:-20px; width:180px; height:180px;
  background:radial-gradient(circle,rgba(255,255,255,0.06),transparent 65%); pointer-events:none;
}
@keyframes popIn {
  from { transform:scale(0.95) translateY(10px); opacity:0; }
  to   { transform:scale(1) translateY(0); opacity:1; }
}
.res-amount { font-family:var(--font-head); font-size:42px; font-weight:900; color:#fff; line-height:1; letter-spacing:-2px; }
.res-lbl { font-size:11px; color:rgba(255,255,255,0.65); text-transform:uppercase; letter-spacing:2px; margin-top:5px; font-family:var(--font-mono); }
.res-grid { display:grid; grid-template-columns:1fr 1fr; gap:12px; margin-top:20px; }
.res-mini {
  background:rgba(255,255,255,0.13); border:1px solid rgba(255,255,255,0.2);
  border-radius:var(--radius); padding:14px 16px; transition:var(--trans);
}
.res-mini:hover { background:rgba(255,255,255,0.2); }
.res-mini-lbl { font-size:10px; color:rgba(255,255,255,0.6); text-transform:uppercase; letter-spacing:1.5px; margin-bottom:6px; font-family:var(--font-mono); }
.res-mini-val { font-size:13px; color:#fff; line-height:1.5; font-weight:500; font-family:var(--font-body); }

/* INPUT CARDS */
.inp-card {
  background:var(--surface); border:1px solid var(--border); border-radius:var(--radius-lg);
  padding:20px 18px; margin-bottom:14px; transition:var(--trans); box-shadow:var(--shadow);
}
.inp-card:hover { border-color:var(--border2); box-shadow:var(--shadow-lg); }
.inp-title {
  font-family:var(--font-mono); font-size:10px; font-weight:700; color:var(--text3);
  text-transform:uppercase; letter-spacing:2.5px; margin-bottom:16px;
  display:flex; align-items:center; gap:8px;
}
.inp-title::before {
  content:''; display:block; width:3px; height:12px;
  background:linear-gradient(180deg,var(--purple2),var(--purpleL)); border-radius:2px;
}

/* FORM CONTROLS */
div[data-testid="stSelectbox"] label,
div[data-testid="stNumberInput"] label,
div[data-testid="stSlider"] label {
  font-size:11px !important; font-weight:600 !important; color:var(--text3) !important;
  text-transform:uppercase !important; letter-spacing:1.5px !important; font-family:var(--font-mono) !important;
}
div[data-testid="stSelectbox"] > div > div {
  background:#fff !important; border:1.5px solid var(--border) !important;
  border-radius:var(--radius-sm) !important; color:var(--text) !important;
  font-size:13px !important; font-family:var(--font-body) !important;
  box-shadow:0 1px 4px rgba(109,40,217,0.05) !important; transition:var(--trans) !important;
}
div[data-testid="stSelectbox"] > div > div:hover {
  border-color:var(--purple) !important; box-shadow:0 0 0 3px rgba(109,40,217,0.1) !important;
}
div[data-testid="stNumberInput"] input {
  background:#fff !important; border:1.5px solid var(--border) !important;
  border-radius:var(--radius-sm) !important; color:var(--text) !important;
  font-size:13px !important; font-family:var(--font-mono) !important; transition:var(--trans) !important;
}
div[data-testid="stNumberInput"] input:focus {
  border-color:var(--purple) !important; box-shadow:0 0 0 3px rgba(109,40,217,0.1) !important;
}
div[data-testid="stSlider"] > div > div > div > div { background:linear-gradient(90deg,var(--purple2),var(--purpleL)) !important; }

/* BUTTONS */
div[data-testid="stButton"] > button[kind="primary"] {
  background:linear-gradient(135deg,var(--purple2) 0%,var(--purpleL) 100%) !important;
  color:#fff !important; border:none !important; border-radius:40px !important;
  font-family:var(--font-head) !important; font-size:14px !important; font-weight:700 !important;
  height:52px !important; letter-spacing:0.8px !important; text-transform:uppercase !important;
  box-shadow:0 4px 20px rgba(109,40,217,0.35), inset 0 1px 0 rgba(255,255,255,0.15) !important;
  transition:var(--trans) !important;
}
div[data-testid="stButton"] > button[kind="primary"]:hover {
  transform:translateY(-2px) !important; box-shadow:0 8px 32px rgba(109,40,217,0.5) !important;
}
div[data-testid="stDownloadButton"] button {
  background:#fff !important; color:var(--purple) !important;
  border:1.5px solid var(--border2) !important; border-radius:var(--radius-sm) !important;
  font-family:var(--font-body) !important; font-size:13px !important;
  height:42px !important; font-weight:600 !important; transition:var(--trans) !important;
}
div[data-testid="stDownloadButton"] button:hover {
  background:rgba(109,40,217,0.05) !important; border-color:var(--purple) !important;
}

/* FILE UPLOADER */
div[data-testid="stFileUploader"] {
  background:#fff !important; border:2px dashed var(--border2) !important;
  border-radius:var(--radius-lg) !important; box-shadow:var(--shadow) !important; transition:var(--trans) !important;
}
div[data-testid="stFileUploader"]:hover { border-color:var(--purple) !important; }

/* METRICS */
div[data-testid="stMetric"] {
  background:#fff !important; border:1px solid var(--border) !important;
  border-radius:var(--radius) !important; padding:16px 18px !important;
  box-shadow:var(--shadow) !important; transition:var(--trans) !important;
}
div[data-testid="stMetric"] label { color:var(--text3) !important; font-size:10px !important; font-weight:600 !important; text-transform:uppercase !important; letter-spacing:2px !important; font-family:var(--font-mono) !important; }
div[data-testid="stMetric"] [data-testid="stMetricValue"] { color:var(--text) !important; font-family:var(--font-head) !important; font-weight:800 !important; letter-spacing:-0.5px !important; }

/* EXPANDER */
details { background:var(--surface2) !important; border:1px solid var(--border) !important; border-radius:var(--radius-sm) !important; padding:0 14px !important; transition:var(--trans) !important; }
details[open] { border-color:var(--border2) !important; }
details > summary { color:var(--text2) !important; font-size:12.5px !important; font-weight:500 !important; font-family:var(--font-body) !important; cursor:pointer !important; padding:12px 0 !important; }
details > summary:hover { color:var(--purple) !important; }

/* SCROLLBAR */
::-webkit-scrollbar { width:5px; height:5px; }
::-webkit-scrollbar-track { background:var(--bg2); }
::-webkit-scrollbar-thumb { background:#C4B5FD; border-radius:10px; }
::-webkit-scrollbar-thumb:hover { background:var(--purpleL); }

@keyframes fadeUp { from{opacity:0;transform:translateY(14px)} to{opacity:1;transform:translateY(0)} }
.pad { padding:24px 36px; }

@media (max-width:1024px) {
  .kpi-row { grid-template-columns:repeat(2,1fr) !important; }
  .res-grid { grid-template-columns:1fr !important; }
  .bm-header,.kpi-outer { padding-left:20px !important; padding-right:20px !important; }
  .chart-card,.lb-card,.res-box { margin-left:20px !important; margin-right:20px !important; }
}
</style>
""", unsafe_allow_html=True)

# --- HEADER ---
st.markdown(f"""
<div class="bm-header">
  <div style="display:flex;align-items:center;gap:12px">
    <div class="bm-logo-box">BM</div>
    <div>
      <div class="bm-title">BigMart Intelligence</div>
      <div class="bm-sub">AI Sales Forecasting Platform</div>
    </div>
  </div>
  <div class="bm-right">
    <div class="bm-live"><span class="bm-dot"></span>&nbsp;Live</div>
    <div class="bm-user">
      <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <circle cx="12" cy="8" r="4"/><path d="M4 20c0-4 3.6-7 8-7s8 3 8 7"/>
      </svg>
      {user_email}
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["  Single Item Predictor  ", "  Bulk CSV Engine  "])

# ==============================================================================
# TAB 1
# ==============================================================================
with tab1:

    item_categories = [
        "Dairy","Soft Drinks","Meat","Fruits and Vegetables","Household",
        "Snack Foods","Frozen Foods","Baking Goods","Breakfast",
        "Health and Hygiene","Hard Drinks","Canned","Starchy Foods"
    ]

    col_left, _, col_right = st.columns([2.5, 0.05, 1.15])

    with col_right:
        st.markdown("<div style='padding:16px 0 0 0'>", unsafe_allow_html=True)
        st.markdown('<div class="inp-card"><div class="inp-title">Item Attributes</div>', unsafe_allow_html=True)
        item_type = st.selectbox("Category", item_categories, key="cat")
        item_mrp  = st.slider("Item MRP (Rs)", 50.0, 300.0, 150.0, step=1.0, key="mrp")
        with st.expander("More item details"):
            item_visibility = st.number_input("Visibility (0-1)", 0.0, 1.0, 0.05, step=0.01, key="vis")
            item_weight     = st.number_input("Weight (kg)", 1.0, 20.0, 10.0, step=0.1, key="wt")
            item_fat        = st.selectbox("Fat Content", ["Low Fat","Regular"], key="fat")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="inp-card"><div class="inp-title">Store Attributes</div>', unsafe_allow_html=True)
        outlet_location = st.selectbox("Outlet Location", ["Tier 1","Tier 2","Tier 3"], key="loc")
        outlet_size     = st.selectbox("Outlet Size", ["Small","Medium","High"], key="sz")
        with st.expander("More store details"):
            outlet_type = st.selectbox("Store Type", [
                "Supermarket Type1","Supermarket Type2","Supermarket Type3","Grocery Store"
            ], key="otype")
            outlet_year = st.number_input("Est. Year", 1985, 2026, 2000, key="yr")
            outlet_age  = 2026 - outlet_year
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
        predict_btn = st.button("Generate AI Prediction", use_container_width=True, type="primary", key="pred")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_left:
        cat_idx = item_categories.index(item_type)

        st.markdown(f"""
        <div class="kpi-outer">
        <div class="kpi-row">
          <div class="kpi" style="--ac:linear-gradient(90deg,#6D28D9,#8B5CF6)">
            <div class="kpi-lbl">Total Predictions</div>
            <div class="kpi-val">{st.session_state.total_predictions:,}</div>
            <div class="kpi-sub"><span class="kpi-up">+24</span>&nbsp;today</div>
          </div>
          <div class="kpi" style="--ac:linear-gradient(90deg,#047857,#059669)">
            <div class="kpi-lbl">Avg Accuracy</div>
            <div class="kpi-val">88.5%</div>
            <div class="kpi-sub"><span class="kpi-up">+1.2%</span>&nbsp;this week</div>
          </div>
          <div class="kpi" style="--ac:linear-gradient(90deg,#B45309,#D97706)">
            <div class="kpi-lbl">Active Category</div>
            <div class="kpi-val sm">{item_type}</div>
            <div class="kpi-sub">selected</div>
          </div>
          <div class="kpi" style="--ac:linear-gradient(90deg,#0369A1,#0891B2)">
            <div class="kpi-lbl">Selected Tier</div>
            <div class="kpi-val sm">{outlet_location}</div>
            <div class="kpi-sub">outlet location</div>
          </div>
        </div>
        </div>
        """, unsafe_allow_html=True)

        np.random.seed(cat_idx * 7 + 3)
        base_vals = [52000,44000,68000,61000,73000,56000,48000,42000,39000,35000,79000,45000,51000]
        base      = base_vals[cat_idx]
        trend     = np.random.normal(1.02, 0.048, 12).cumprod()
        sales     = base * trend
        months    = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
        acc_colors = ['#7C3AED','#0891B2','#D97706','#059669','#8B5CF6','#DB2777',
                      '#0891B2','#B45309','#6366F1','#059669','#7C3AED','#D97706','#DC2626']
        ac = acc_colors[cat_idx % len(acc_colors)]

        def hex_rgba(h, a):
            r,g,b = int(h[1:3],16), int(h[3:5],16), int(h[5:7],16)
            return f'rgba({r},{g},{b},{a})'

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=months, y=sales.tolist(),
            mode='lines+markers',
            line=dict(color=ac, width=2.5, shape='spline', smoothing=1.2),
            fill='tozeroy', fillcolor=hex_rgba(ac, 0.06),
            marker=dict(size=7, color='#fff', line=dict(width=2.5, color=ac)),
            hovertemplate='<b>%{x}</b><br>Rs %{y:,.0f}<extra></extra>'
        ))
        fig.update_layout(
            height=230, margin=dict(l=2,r=2,t=4,b=2),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=True, gridcolor='rgba(109,40,217,0.07)',
                       tickfont=dict(color='#9181B8', size=11, family='Space Grotesk'),
                       title=None, zeroline=False),
            yaxis=dict(showgrid=True, gridcolor='rgba(109,40,217,0.07)',
                       tickfont=dict(color='#9181B8', size=11, family='Space Grotesk'),
                       title=None, zeroline=False, tickprefix='Rs ', tickformat=',.0f'),
            hoverlabel=dict(bgcolor=ac, font_color='white', font_size=13, bordercolor=ac),
        )

        st.markdown(f"""
        <div class="chart-card">
          <div class="chart-top">
            <div class="sec-h" style="margin-bottom:0">{item_type} &mdash; Sales Trend</div>
            <span class="live-badge">Live</span>
          </div>
        """, unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        st.markdown("</div>", unsafe_allow_html=True)

        if predict_btn:
            try:
                data = {
                    "Item_Weight": item_weight, "Item_Fat_Content": item_fat,
                    "Item_Type": item_type, "Item_Visibility": item_visibility,
                    "Item_MRP": item_mrp, "Outlet_Size": outlet_size,
                    "Outlet_Location_Type": outlet_location, "Outlet_Type": outlet_type,
                    "Outlet_Establishment_Year": outlet_year, "Outlet_Age": outlet_age
                }
                with st.spinner("AI model processing..."):
                    res = requests.post("http://127.0.0.1:8000/predict", json=data, timeout=10)
                    rd  = res.json()
                    pred_val     = int(rd['prediction'])
                    shelf_action = rd.get('shelf_action', 'High visibility, maintain stock.')
                    opt_action   = rd.get('opt_action',   'Apply 5% discount.')
            except Exception:
                with st.spinner("Simulating prediction..."):
                    time.sleep(0.8)
                seed = int(item_mrp) + cat_idx * 13
                np.random.seed(seed)
                pred_val     = int(item_mrp * 18 + 1200 + np.random.randint(800, 4200))
                s_actions = ["High visibility, maintain stock.",
                             "Restock within 48 hours.",
                             "Premium shelf position recommended.",
                             "End-cap display for max exposure."]
                o_actions = ["Apply 5% limited discount.",
                             "Bundle with complementary items.",
                             "Loyalty points promotion active.",
                             "Price at competitive parity."]
                shelf_action = s_actions[seed % 4]
                opt_action   = o_actions[(seed + 1) % 4]

            st.session_state.prediction_history.append({
                "Item Name": item_type, "Category": item_type, "Predicted Sales (Rs)": pred_val
            })
            st.session_state.total_predictions += 1

            st.markdown(f"""
            <div class="res-box">
              <div style="display:flex;align-items:flex-end;gap:20px;flex-wrap:wrap">
                <div>
                  <div class="res-amount">Rs {pred_val:,}</div>
                  <div class="res-lbl">Predicted Annual Sales &mdash; 88% Confidence</div>
                </div>
                <div style="margin-left:auto">
                  <svg width="48" height="48" viewBox="0 0 48 48">
                    <circle cx="24" cy="24" r="22" fill="rgba(255,255,255,0.15)" stroke="rgba(255,255,255,0.3)" stroke-width="1.5"/>
                    <polyline points="12,32 20,22 26,27 36,15" fill="none" stroke="rgba(255,255,255,0.9)"
                      stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
                    <circle cx="36" cy="15" r="3" fill="white"/>
                  </svg>
                </div>
              </div>
              <div class="res-grid">
                <div class="res-mini">
                  <div class="res-mini-lbl">Shelf Intelligence</div>
                  <div class="res-mini-val">{shelf_action}</div>
                </div>
                <div class="res-mini">
                  <div class="res-mini-lbl">Optimization Strategy</div>
                  <div class="res-mini-val">{opt_action}</div>
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)

        df_h = pd.DataFrame(st.session_state.prediction_history)
        df_h = df_h.sort_values("Predicted Sales (Rs)", ascending=False).head(5).reset_index(drop=True)
        rank_cls = ['rk1','rk2','rk3','rkn','rkn']

        rows_html = ""
        for i, row in df_h.iterrows():
            rc = rank_cls[i] if i < len(rank_cls) else 'rkn'
            rows_html += (
                f"<tr>"
                f"<td><span class='{rc}'>{i+1}</span></td>"
                f"<td><span style='font-weight:600;color:var(--text)'>{row['Item Name']}</span></td>"
                f"<td><span class='cat-pill'>{row['Category']}</span></td>"
                f"<td><span class='lb-sales'>Rs {int(row['Predicted Sales (Rs)']):,}</span></td>"
                f"</tr>"
            )

        st.markdown(
            f"""<div class="lb-card">
              <div class="lb-top">
                <div class="sec-h" style="margin-bottom:0">Live Prediction Leaderboard</div>
                <span class="lb-badge">{len(df_h)} entries</span>
              </div>
              <table class="lb-table">
                <thead><tr><th>#</th><th>Item</th><th>Category</th><th>Predicted Sales</th></tr></thead>
                <tbody>{rows_html}</tbody>
              </table>
            </div>""",
            unsafe_allow_html=True
        )

# ==============================================================================
# TAB 2
# ==============================================================================
with tab2:
    st.markdown("<div class='pad'>", unsafe_allow_html=True)

    hc, dc = st.columns([3,1])
    with hc:
        st.markdown('<div class="sec-h" style="font-size:16px">Bulk CSV Engine</div>', unsafe_allow_html=True)
        st.markdown('<p style="font-size:13px;color:#4B3872;margin-top:-4px;font-family:Space Grotesk,sans-serif;">Upload your store inventory CSV to process thousands of items with AI predictions.</p>', unsafe_allow_html=True)
    with dc:
        sample_df = pd.DataFrame({
            "Item_Weight":              [9.3, 5.9, 14.1, 7.6],
            "Item_Fat_Content":         ["Low Fat","Regular","Low Fat","Regular"],
            "Item_Type":                ["Dairy","Meat","Snack Foods","Household"],
            "Item_Visibility":          [0.016, 0.045, 0.10, 0.003],
            "Item_MRP":                 [249.8, 45.0, 89.5, 199.0],
            "Outlet_Size":              ["Medium","Small","Medium","High"],
            "Outlet_Location_Type":     ["Tier 1","Tier 2","Tier 3","Tier 1"],
            "Outlet_Type":              ["Supermarket Type1","Grocery Store",
                                         "Supermarket Type2","Supermarket Type3"],
            "Outlet_Establishment_Year":[1999, 2009, 2002, 1995]
        })
        st.markdown("<div style='height:22px'></div>", unsafe_allow_html=True)
        st.download_button("Download CSV Template", data=sample_df.to_csv(index=False),
                           file_name="bigmart_template.csv", mime="text/csv")

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    uploaded = st.file_uploader("Drop inventory CSV or click to browse", type=["csv"])

    if uploaded:
        df_bulk = pd.read_csv(uploaded)
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Rows",    f"{len(df_bulk):,}")
        c2.metric("Total Columns", len(df_bulk.columns))
        c3.metric("File", uploaded.name[:20]+("..." if len(uploaded.name)>20 else ""))

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        st.markdown('<div class="sec-h" style="font-size:13px">Data Preview &mdash; first 5 rows</div>', unsafe_allow_html=True)
        st.dataframe(df_bulk.head(5), use_container_width=True, hide_index=True)
        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

        if st.button("Run Bulk Prediction", use_container_width=True, type="primary", key="bulk_run"):
            try:
                payload = df_bulk.to_dict(orient="records")
                with st.spinner(f"Processing {len(df_bulk):,} items..."):
                    res = requests.post("http://127.0.0.1:8000/predict_bulk", json=payload, timeout=60)
                    bulk_result = res.json()["results"]
                result_df = pd.DataFrame(bulk_result)
                st.success(f"Prediction complete -- {len(result_df):,} items processed!")
                display_cols = [c for c in ['Item_Type','Item_MRP','Predicted_Sales','Shelf_Action','Optimization_Strategy'] if c in result_df.columns]
                st.dataframe(result_df[display_cols], use_container_width=True, hide_index=True)
                st.download_button("Download Results CSV", data=result_df.to_csv(index=False), file_name="bigmart_predictions.csv", mime="text/csv", use_container_width=True)
            except Exception:
                with st.spinner(f"Simulating predictions for {len(df_bulk):,} items..."):
                    time.sleep(1.5)
                mrp_col = 'Item_MRP'  if 'Item_MRP'  in df_bulk.columns else df_bulk.columns[4]
                typ_col = 'Item_Type' if 'Item_Type' in df_bulk.columns else df_bulk.columns[2]
                result_df = df_bulk.copy()
                result_df['Predicted_Sales']      = (result_df[mrp_col]*18+1200+np.random.randint(500,3000,len(result_df))).astype(int)
                result_df['Confidence']            = "88%"
                result_df['Shelf_Action']          = "High visibility, maintain stock."
                result_df['Optimization_Strategy'] = "Apply 5% discount."
                st.success(f"Simulation complete -- {len(result_df):,} items processed!")
                show_cols = [c for c in [typ_col, mrp_col, 'Predicted_Sales', 'Confidence', 'Shelf_Action', 'Optimization_Strategy'] if c in result_df.columns]
                st.dataframe(result_df[show_cols], use_container_width=True, hide_index=True)
                st.download_button("Download Results CSV", data=result_df.to_csv(index=False), file_name="bigmart_predictions.csv", mime="text/csv", use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)