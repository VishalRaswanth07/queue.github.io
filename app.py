import streamlit as st
import pandas as pd
import random
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import os

# ──────────────────────────────────────────────
#  PAGE CONFIG
# ──────────────────────────────────────────────
st.set_page_config(
    page_title="Queue Randomness Explained",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ──────────────────────────────────────────────
#  GLOBAL CSS
# ──────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&display=swap');

/* ── Base & Background ── */
html, body, .stApp {
    font-family: 'Poppins', sans-serif !important;
    background: linear-gradient(135deg, #0a0a2e 0%, #1a0533 30%, #0d1b4b 60%, #1a0533 100%) !important;
    color: #f0f0f8;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: rgba(255,255,255,0.04); }
::-webkit-scrollbar-thumb { background: rgba(139,92,246,0.5); border-radius: 3px; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f0a1e 0%, #1a0f35 100%) !important;
    border-right: 1px solid rgba(139,92,246,0.2) !important;
}
[data-testid="stSidebar"] * { color: #d8d0f0 !important; }
[data-testid="stSidebar"] .stSlider .stMarkdown p { color: #c4b8e8 !important; }

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #db2777) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 14px !important;
    padding: 13px 30px !important;
    font-family: 'Poppins', sans-serif !important;
    font-size: 1rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.3px !important;
    box-shadow: 0 4px 20px rgba(124,58,237,0.4) !important;
    transition: all 0.25s ease !important;
    width: 100% !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(219,39,119,0.45) !important;
}

/* ── Tabs ── */
[data-baseweb="tab-list"] {
    background: rgba(255,255,255,0.04) !important;
    border-radius: 14px !important;
    padding: 6px 8px !important;
    gap: 6px !important;
    border: 1px solid rgba(139,92,246,0.15) !important;
}
[data-baseweb="tab"] {
    color: #a89bd0 !important;
    font-weight: 600 !important;
    border-radius: 10px !important;
    font-family: 'Poppins', sans-serif !important;
}
[data-baseweb="tab"][aria-selected="true"] {
    background: linear-gradient(135deg, rgba(124,58,237,0.45), rgba(219,39,119,0.3)) !important;
    color: #fff !important;
}

/* ── Sliders ── */
[data-testid="stSlider"] > div > div > div > div {
    background: linear-gradient(90deg, #7c3aed, #db2777) !important;
}

/* ── Number inputs ── */
[data-testid="stNumberInput"] input {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid rgba(139,92,246,0.3) !important;
    border-radius: 10px !important;
    color: #f0f0f8 !important;
}

/* ── Toggle ── */
[data-testid="stToggle"] { color: #c4b8e8 !important; }

/* ── Info / Warning / Success / Error boxes ── */
[data-testid="stAlert"] { border-radius: 14px !important; }

/* ── Remove Streamlit branding ── */
#MainMenu, footer, [data-testid="stHeader"] { visibility: hidden; }

/* ══════════════════════════════════════════════
   CUSTOM COMPONENTS
   ══════════════════════════════════════════════ */

/* Hero */
.hero-wrap {
    text-align: center;
    padding: 60px 20px 40px;
}
.hero-badge {
    display: inline-block;
    background: linear-gradient(135deg, rgba(124,58,237,0.3), rgba(219,39,119,0.3));
    border: 1px solid rgba(139,92,246,0.4);
    border-radius: 30px;
    padding: 6px 22px;
    font-size: 0.82rem;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #c4b8e8;
    margin-bottom: 20px;
}
.hero-title {
    font-size: clamp(2.2rem, 5vw, 3.8rem);
    font-weight: 900;
    line-height: 1.15;
    background: linear-gradient(90deg, #60a5fa, #a78bfa, #f472b6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 16px;
}
.hero-subtitle {
    font-size: 1.15rem;
    font-weight: 400;
    color: #9b8fc0;
    max-width: 560px;
    margin: 0 auto 36px;
    line-height: 1.7;
}
.hero-divider {
    width: 80px;
    height: 4px;
    background: linear-gradient(90deg, #7c3aed, #db2777);
    border-radius: 2px;
    margin: 0 auto;
}

/* Section label */
.sec-label {
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 2.5px;
    text-transform: uppercase;
    color: #7c3aed;
    margin-bottom: 8px;
}
.sec-title {
    font-size: 1.8rem;
    font-weight: 800;
    color: #e8e0ff;
    margin-bottom: 6px;
}
.sec-sub {
    font-size: 0.98rem;
    color: #8b82b0;
    margin-bottom: 28px;
    line-height: 1.6;
}

/* Story card */
.story-card {
    border-radius: 20px;
    padding: 28px 26px;
    height: 100%;
    border: 1px solid;
    position: relative;
    overflow: hidden;
}
.story-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    border-radius: 20px 20px 0 0;
}
.story-card-a {
    background: linear-gradient(145deg, rgba(16,185,129,0.12), rgba(6,95,70,0.08));
    border-color: rgba(16,185,129,0.25);
}
.story-card-a::before { background: linear-gradient(90deg, #10b981, #34d399); }
.story-card-b {
    background: linear-gradient(145deg, rgba(239,68,68,0.12), rgba(127,29,29,0.08));
    border-color: rgba(239,68,68,0.25);
}
.story-card-b::before { background: linear-gradient(90deg, #ef4444, #f97316); }

.story-icon { font-size: 2.4rem; margin-bottom: 10px; }
.story-title-a { font-size: 1.22rem; font-weight: 800; color: #34d399; margin-bottom: 14px; }
.story-title-b { font-size: 1.22rem; font-weight: 800; color: #f87171; margin-bottom: 14px; }
.story-item {
    display: flex;
    align-items: flex-start;
    gap: 10px;
    margin-bottom: 10px;
    font-size: 0.95rem;
    color: #ccc8e8;
    line-height: 1.5;
}
.story-item-icon { font-size: 1rem; margin-top: 1px; flex-shrink: 0; }
.story-result-a {
    margin-top: 18px;
    background: rgba(16,185,129,0.12);
    border-radius: 10px;
    padding: 10px 14px;
    font-size: 0.93rem;
    color: #6ee7b7;
    font-weight: 600;
}
.story-result-b {
    margin-top: 18px;
    background: rgba(239,68,68,0.12);
    border-radius: 10px;
    padding: 10px 14px;
    font-size: 0.93rem;
    color: #fca5a5;
    font-weight: 600;
}

/* Queue visual */
.queue-row {
    background: rgba(0,0,0,0.25);
    border-radius: 12px;
    padding: 14px 16px;
    font-size: 1.5rem;
    letter-spacing: 4px;
    margin: 14px 0 6px;
    min-height: 52px;
    word-break: break-all;
    line-height: 2;
}

/* Key idea card */
.key-idea-card {
    background: linear-gradient(135deg, rgba(124,58,237,0.2), rgba(219,39,119,0.15));
    border: 1px solid rgba(139,92,246,0.35);
    border-radius: 20px;
    padding: 32px 36px;
    text-align: center;
    margin: 28px 0;
}
.key-idea-icon { font-size: 2.8rem; margin-bottom: 14px; }
.key-idea-title { font-size: 1.35rem; font-weight: 800; color: #e2d9ff; margin-bottom: 12px; }
.key-idea-text  { font-size: 1.02rem; color: #b0a4d8; line-height: 1.75; max-width: 640px; margin: 0 auto; }

/* Why card */
.why-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: 18px;
    padding: 26px 24px;
    text-align: center;
    height: 100%;
    transition: transform 0.2s, border-color 0.2s;
}
.why-card:hover { transform: translateY(-4px); border-color: rgba(139,92,246,0.35); }
.why-card-icon  { font-size: 2.2rem; margin-bottom: 12px; }
.why-card-title { font-size: 1.05rem; font-weight: 700; color: #ddd6ff; margin-bottom: 8px; }
.why-card-text  { font-size: 0.9rem; color: #8880a8; line-height: 1.6; }

/* Metric card */
.metric-card {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: 18px;
    padding: 24px 20px;
    text-align: center;
    border-top: 4px solid;
}
.metric-val   { font-size: 2.3rem; font-weight: 900; margin: 6px 0 4px; }
.metric-lbl   { font-size: 0.78rem; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; color: #7c7498; }
.metric-note  { font-size: 0.82rem; color: #6b6488; margin-top: 5px; font-style: italic; }

/* Chart note */
.chart-note {
    background: rgba(124,58,237,0.1);
    border-left: 3px solid #7c3aed;
    border-radius: 0 12px 12px 0;
    padding: 12px 18px;
    font-size: 0.92rem;
    color: #b0a4d8;
    line-height: 1.6;
    margin-top: -4px;
    margin-bottom: 20px;
}

/* Comparison card */
.compare-card {
    border-radius: 18px;
    padding: 24px 20px;
    border: 1.5px solid;
}
.compare-card-a { background: rgba(16,185,129,0.07); border-color: rgba(16,185,129,0.3); }
.compare-card-b { background: rgba(239,68,68,0.07);  border-color: rgba(239,68,68,0.3); }

/* Learn card */
.learn-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.09);
    border-radius: 16px;
    padding: 22px 20px;
    display: flex;
    align-items: flex-start;
    gap: 16px;
    margin-bottom: 14px;
    transition: border-color 0.2s;
}
.learn-card:hover { border-color: rgba(139,92,246,0.4); }
.learn-num {
    background: linear-gradient(135deg, #7c3aed, #db2777);
    border-radius: 10px;
    width: 38px;
    height: 38px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.1rem;
    font-weight: 800;
    color: #fff;
    flex-shrink: 0;
}
.learn-title { font-size: 1rem; font-weight: 700; color: #ddd6ff; margin-bottom: 4px; }
.learn-desc  { font-size: 0.88rem; color: #7c7498; line-height: 1.55; }

/* Divider */
.fancy-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(139,92,246,0.4), rgba(219,39,119,0.3), transparent);
    margin: 50px 0;
}

/* Status badge */
.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    border-radius: 30px;
    padding: 8px 18px;
    font-size: 0.9rem;
    font-weight: 600;
    margin: 10px 0;
}
.status-ok      { background: rgba(16,185,129,0.15); border: 1px solid rgba(16,185,129,0.3); color: #6ee7b7; }
.status-warn    { background: rgba(245,158,11,0.15); border: 1px solid rgba(245,158,11,0.3); color: #fcd34d; }
.status-danger  { background: rgba(239,68,68,0.15);  border: 1px solid rgba(239,68,68,0.3);  color: #fca5a5; }

/* Insight box */
.insight-box {
    background: linear-gradient(135deg, rgba(245,158,11,0.12), rgba(239,68,68,0.08));
    border: 1px solid rgba(245,158,11,0.25);
    border-radius: 16px;
    padding: 18px 24px;
    font-size: 0.97rem;
    color: #fde68a;
    line-height: 1.7;
    margin: 18px 0;
}

h1,h2,h3,h4 { color: #e8e0ff !important; font-family: 'Poppins', sans-serif !important; }

/* ══ INPUT VISIBILITY — COMPREHENSIVE FIX ══ */

/* All generic inputs + textareas */
input, textarea {
    color: #1a1a2e !important;
    background-color: #f0eeff !important;
    caret-color: #7c3aed !important;
}

/* BaseWeb input wrapper — the actual styled box Streamlit uses */
[data-baseweb="input"] {
    background-color: #f0eeff !important;
    border: 1.5px solid #9d88e8 !important;
    border-radius: 10px !important;
}
[data-baseweb="input"]:focus-within {
    border-color: #7c3aed !important;
    box-shadow: 0 0 0 3px rgba(124,58,237,0.25) !important;
}
[data-baseweb="input"] input {
    color: #1a1a2e !important;
    background-color: transparent !important;
    font-weight: 600 !important;
    font-size: 0.97rem !important;
}

/* Number input container */
[data-testid="stNumberInput"] > div {
    background-color: #f0eeff !important;
    border: 1.5px solid #9d88e8 !important;
    border-radius: 10px !important;
}
[data-testid="stNumberInput"] input {
    color: #1a1a2e !important;
    background-color: transparent !important;
    font-weight: 600 !important;
}

/* Plus / Minus stepper buttons */
[data-testid="stNumberInput"] button {
    color: #7c3aed !important;
    background-color: rgba(124,58,237,0.12) !important;
    border: 1px solid rgba(124,58,237,0.3) !important;
    border-radius: 6px !important;
}
[data-testid="stNumberInput"] button:hover {
    background-color: rgba(124,58,237,0.28) !important;
    color: #fff !important;
}
[data-testid="stNumberInput"] button svg {
    fill: currentColor !important;
}

/* Placeholder text */
input::placeholder, textarea::placeholder {
    color: #7b6eaa !important;
    opacity: 1 !important;
}

/* Select boxes (dropdowns) */
[data-baseweb="select"] > div {
    background-color: #f0eeff !important;
    border: 1.5px solid #9d88e8 !important;
    border-radius: 10px !important;
    color: #1a1a2e !important;
}
[data-baseweb="select"] span {
    color: #1a1a2e !important;
    font-weight: 600 !important;
}

/* Story cards (native Streamlit container wrappers) */
.bank-box-a {
    background: linear-gradient(145deg, rgba(16,185,129,0.12), rgba(6,95,70,0.08));
    border: 1.5px solid rgba(16,185,129,0.3);
    border-radius: 18px;
    padding: 28px 26px;
}
.bank-box-b {
    background: linear-gradient(145deg, rgba(239,68,68,0.12), rgba(127,29,29,0.08));
    border: 1.5px solid rgba(239,68,68,0.3);
    border-radius: 18px;
    padding: 28px 26px;
}
.why-happen-box {
    background: linear-gradient(135deg, rgba(124,58,237,0.18), rgba(219,39,119,0.12));
    border: 1.5px solid rgba(139,92,246,0.35);
    border-radius: 18px;
    padding: 28px 32px;
    margin: 30px 0;
    text-align: center;
    font-size: 1.05rem;
    color: #ddd6ff;
    line-height: 1.85;
}
</style>
""", unsafe_allow_html=True)


# ──────────────────────────────────────────────
#  SIMULATION LOGIC  (unchanged)
# ──────────────────────────────────────────────
def simulate_queue(arrival_rate, service_rate, num_customers, constant_arrival=False):
    arrival_times, service_times = [], []
    for _ in range(num_customers):
        ia = 1.0 / arrival_rate if constant_arrival else random.expovariate(arrival_rate)
        sv = random.expovariate(service_rate)
        arrival_times.append(ia)
        service_times.append(sv)

    abs_arr, cur = [], 0.0
    for t in arrival_times:
        cur += t
        abs_arr.append(cur)

    dep_times, wait_times, events = [], [], []
    for i in range(num_customers):
        st_time = abs_arr[i] if i == 0 else max(abs_arr[i], dep_times[i - 1])
        dep = st_time + service_times[i]
        dep_times.append(dep)
        wait_times.append(st_time - abs_arr[i])
        events += [(abs_arr[i], 1), (st_time, -1)]

    events.sort(key=lambda x: x[0])
    q_timeline, cq = [], 0
    for t, d in events:
        cq += d
        q_timeline.append({"Time": t, "Queue Length": max(0, cq)})

    return wait_times, q_timeline


# ──────────────────────────────────────────────
#  CHART THEME
# ──────────────────────────────────────────────
PLOT = dict(
    plot_bgcolor="rgba(255,255,255,0.02)",
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(color="#b0a4d8", family="Poppins"),
    xaxis=dict(gridcolor="rgba(255,255,255,0.06)", zerolinecolor="rgba(255,255,255,0.06)"),
    yaxis=dict(gridcolor="rgba(255,255,255,0.06)", zerolinecolor="rgba(255,255,255,0.06)"),
    margin=dict(l=10, r=10, t=44, b=10),
    title_font=dict(size=14, color="#ddd6ff"),
)


# ──────────────────────────────────────────────
#  HELPER: metric card
# ──────────────────────────────────────────────
def metric_card(col, icon, label, value, note, border_color):
    col.markdown(f"""
    <div class="metric-card" style="border-top-color:{border_color};">
        <div class="metric-lbl">{icon} {label}</div>
        <div class="metric-val" style="color:{border_color};">{value}</div>
        <div class="metric-note">{note}</div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════
#  APP
# ══════════════════════════════════════════════
def main():

    # ─────────────────────────────────────────
    #  SECTION 1 — HERO
    # ─────────────────────────────────────────
    st.markdown("""
    <div class="hero-wrap">
        <div class="hero-badge">📊 Interactive Learning Tool</div>
        <div class="hero-title">Queue Randomness<br>Explained</div>
        <div class="hero-subtitle">
            Why waiting time increases even when averages look the same — explored through a simple, visual bank story.
        </div>
        <div class="hero-divider"></div>
    </div>
    """, unsafe_allow_html=True)


    # ─────────────────────────────────────────
    #  SECTION 2 — UNDERSTANDING THE CONCEPT
    # ─────────────────────────────────────────
    st.markdown("""
    <div class="sec-label">The Core Idea</div>
    <div class="sec-title">🏦 Imagine Two Banks</div>
    <div class="sec-sub">
        Same number of customers. Same serving speed. But one bank always has longer queues. Here's why.
    </div>
    """, unsafe_allow_html=True)

    # Story images
    img_smooth = os.path.join(os.path.dirname(__file__), "bank_smooth.png")
    img_crowd  = os.path.join(os.path.dirname(__file__), "bank_crowded.png")

    col_img_a, col_img_b = st.columns(2)
    if os.path.exists(img_smooth):
        with col_img_a:
            st.image(img_smooth, caption="🟢 Bank A — Calm & Organised", use_container_width=True)
    if os.path.exists(img_crowd):
        with col_img_b:
            st.image(img_crowd, caption="🔴 Bank B — Crowded & Chaotic", use_container_width=True)

    # ── Story cards: built with native Streamlit, no raw HTML divs/spans ──
    col_a, col_b = st.columns(2, gap="large")

    with col_a:
        st.markdown("""
        <div class="bank-box-a">
        """, unsafe_allow_html=True)
        st.markdown("### 🟢 Bank A — Smooth Flow")
        st.markdown("""
- 👤 Customers arrive **one by one**, evenly spaced
- ⚡ The teller finishes each customer **before the next arrives**
- 😊 No sudden rush — service flows **continuously**
        """)
        st.markdown("**Arrival pattern:**")
        st.markdown("""
> `👤` &nbsp;&nbsp;&nbsp; `👤` &nbsp;&nbsp;&nbsp; `👤` &nbsp;&nbsp;&nbsp; `👤` &nbsp;&nbsp;&nbsp; `👤` &nbsp;&nbsp;&nbsp; `👤`
        """)
        st.success("👉 Result: Very little waiting. Everyone is happy.")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_b:
        st.markdown("""
        <div class="bank-box-b">
        """, unsafe_allow_html=True)
        st.markdown("### 🔴 Bank B — Random Flow")
        st.markdown("""
- 😴 Sometimes **no customers** arrive for a long time
- 🚶 Then suddenly **many people come all at once!**
- ⚠️ The teller gets overwhelmed — a **queue builds fast**
        """)
        st.markdown("**Arrival pattern:**")
        st.markdown("""
> `👤` &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; `👤👤👤👤👤👤👤👤👤` &nbsp;&nbsp;&nbsp; `👤` &nbsp;&nbsp;&nbsp; `👤`
        """)
        st.error("👉 Result: Long queues and delays — even for late arrivals.")
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Why does this happen? ──
    st.markdown("""
    <div class="why-happen-box">
        <div style="font-size:2rem; margin-bottom:12px;">💡</div>
        <div style="font-size:1.25rem; font-weight:800; color:#e2d9ff; margin-bottom:14px;">Why does this happen?</div>
        <div style="color:#b0a4d8; max-width:620px; margin:0 auto;">
            Even though both banks have the <strong style="color:#ce93d8;">same average number of customers</strong>,
            Bank B experiences <strong style="color:#f87171;">sudden bursts of arrivals</strong> which overwhelm the teller.
            The queue grows faster than it can be cleared.
            <br><br>
            <span style="color:#fde68a; font-weight:700;">👉 Randomness causes waiting time — not just averages.</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)


    # ─────────────────────────────────────────
    #  SECTION 3 — WHY THIS APP
    # ─────────────────────────────────────────
    st.markdown("""
    <div class="sec-label">Purpose</div>
    <div class="sec-title">🚀 Why This App?</div>
    <div class="sec-sub">
        In real-world systems, we usually judge performance using averages. But that's not the full picture.
    </div>
    """, unsafe_allow_html=True)

    w1, w2, w3, w4 = st.columns(4, gap="medium")
    why_items = [
        ("🏦", "Real-world Systems", "Banks, hospitals, call centres, and traffic all face the same challenge — random arrivals."),
        ("📊", "Averages Lie", "Looking only at average arrival rate hides the danger of sudden bursts."),
        ("👁️", "Visual Understanding", "Seeing queues grow in real time builds intuition faster than any formula."),
        ("🛠️", "Design Better Systems", "Learning this helps engineers add the right buffer capacity to avoid overload."),
    ]
    for col, (icon, title, text) in zip([w1, w2, w3, w4], why_items):
        col.markdown(f"""
        <div class="why-card">
            <div class="why-card-icon">{icon}</div>
            <div class="why-card-title">{title}</div>
            <div class="why-card-text">{text}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)


    # ─────────────────────────────────────────
    #  SIDEBAR CONTROLS
    # ─────────────────────────────────────────
    st.sidebar.markdown("## ⚙️ Simulation Settings")
    st.sidebar.markdown("Adjust the parameters and click **Run Simulation** to explore.")
    st.sidebar.markdown("---")

    arrival_rate = st.sidebar.slider(
        "👥 Customers arriving per minute",
        1.0, 20.0, 10.0, 0.5,
        help="How many customers come to the bank each minute on average."
    )
    service_rate = st.sidebar.slider(
        "⚡ Customers served per minute",
        1.0, 25.0, 12.0, 0.5,
        help="How fast can the teller process each customer?"
    )
    num_customers = st.sidebar.number_input(
        "🔢 Total customers to simulate",
        50, 5000, 500, 50,
        help="How many customers to run through the simulation."
    )
    num_runs = st.sidebar.number_input(
        "🔁 Simulate this many days",
        1, 20, 10, 1,
        help="Each run = one day. See how results vary day-to-day."
    )
    compare_mode = st.sidebar.toggle(
        "⚖️ Compare Bank A vs Bank B",
        value=False,
        help="Side-by-side comparison: steady vs random arrivals."
    )

    st.sidebar.markdown("---")

    # Status indicator
    traffic = arrival_rate / service_rate
    if traffic >= 1.0:
        badge_cls = "status-danger"
        badge_icon = "🚨"
        badge_text = f"System Overloaded ({traffic*100:.0f}% busy)"
        sidebar_fn = st.sidebar.error
        card_color = "#ef4444"
        sidebar_msg = "Customers arrive faster than the teller can serve. Queue will grow forever!"
    elif traffic >= 0.8:
        badge_cls = "status-warn"
        badge_icon = "⚠️"
        badge_text = f"Getting Busy ({traffic*100:.0f}% busy)"
        sidebar_fn = st.sidebar.warning
        card_color = "#f59e0b"
        sidebar_msg = "System is under pressure. Random bursts will easily create long queues."
    else:
        badge_cls = "status-ok"
        badge_icon = "✅"
        badge_text = f"System Healthy ({traffic*100:.0f}% busy)"
        sidebar_fn = st.sidebar.success
        card_color = "#10b981"
        sidebar_msg = "Teller has enough capacity. Queues should stay short."

    st.sidebar.markdown(f"""
    <div class="status-badge {badge_cls}">{badge_icon} {badge_text}</div>
    """, unsafe_allow_html=True)
    sidebar_fn(sidebar_msg)

    st.sidebar.markdown("---")
    run_btn = st.sidebar.button("▶️ Run Simulation")


    # ─────────────────────────────────────────
    #  SECTION 4 — SIMULATION RESULTS
    # ─────────────────────────────────────────
    st.markdown("""
    <div class="sec-label">Interactive</div>
    <div class="sec-title">📊 Run the Simulation</div>
    <div class="sec-sub">Set parameters in the sidebar and click Run Simulation to explore the effects of randomness.</div>
    """, unsafe_allow_html=True)

    if not run_btn:
        st.markdown("""
        <div class="insight-box">
            👈 Adjust the sliders in the sidebar then click <b>▶️ Run Simulation</b> to see results.<br>
            💡 Tip: Turn on <b>Compare Bank A vs Bank B</b> for the most revealing comparison!
        </div>
        """, unsafe_allow_html=True)

    if run_btn:
        with st.spinner("Simulating your bank..."):

            # ── SINGLE MODE ──────────────────────────────────
            if not compare_mode:
                # Run multiple times for reliability
                multi_avgs = []
                for _ in range(num_runs):
                    w, _ = simulate_queue(arrival_rate, service_rate, num_customers)
                    multi_avgs.append(np.mean(w))

                waits, q_series = simulate_queue(arrival_rate, service_rate, num_customers)
                avg_w = np.mean(waits)
                max_w = np.max(waits)
                var_w = np.var(waits)

                # Metrics
                m1, m2, m3, m4 = st.columns(4, gap="medium")
                metric_card(m1, "🚦", "System Busy-ness",    f"{traffic*100:.0f}%",  "How hard the teller is working",           card_color)
                metric_card(m2, "⏱️", "Average Wait",         f"{avg_w:.1f} min",     "Typical time a customer waits",            card_color)
                metric_card(m3, "⏳", "Longest Wait",         f"{max_w:.1f} min",     "The unluckiest customer waited this long",  "#f59e0b")
                metric_card(m4, "📉", "Wait-Time Variability",f"{var_w:.1f}",         "High = very unpredictable wait times",      "#a78bfa")

                st.markdown("---")

                # Charts
                ch1, ch2 = st.columns(2, gap="large")

                with ch1:
                    fig1 = px.line(x=range(1, num_customers + 1), y=waits,
                                   title="⏱️ How Long Each Customer Waited")
                    fig1.update_traces(line_color="#60a5fa", line_width=2)
                    fig1.update_layout(**PLOT, xaxis_title="Customer Number", yaxis_title="Minutes Waited")
                    st.plotly_chart(fig1, use_container_width=True)
                    st.markdown("""
                    <div class="chart-note">
                        Each point = one customer. Big spikes show moments when a burst of arrivals hit.
                        The next few people had to wait much longer because the queue piled up suddenly.
                    </div>""", unsafe_allow_html=True)

                with ch2:
                    fig2 = px.histogram(x=waits, nbins=40,
                                        title="📊 Spread of Waiting Times")
                    fig2.update_traces(marker_color="#f472b6", opacity=0.85)
                    fig2.update_layout(**PLOT, xaxis_title="Minutes Waited", yaxis_title="Number of Customers")
                    st.plotly_chart(fig2, use_container_width=True)
                    st.markdown("""
                    <div class="chart-note">
                        Most customers wait a short time (bars on the left), but a long tail to the right
                        means some customers waited much longer — caused by random bursts.
                    </div>""", unsafe_allow_html=True)

                ch3, ch4 = st.columns(2, gap="large")

                with ch3:
                    df_q = pd.DataFrame(q_series)
                    fig3 = px.line(df_q, x="Time", y="Queue Length",
                                   title="🧍 Number of People Standing in Line Over Time",
                                   line_shape="hv")
                    fig3.update_traces(line_color="#a78bfa", line_width=2)
                    fig3.add_trace(go.Scatter(x=df_q["Time"], y=df_q["Queue Length"],
                                              fill="tozeroy", mode="none",
                                              fillcolor="rgba(167,139,250,0.1)", showlegend=False))
                    fig3.update_layout(**PLOT)
                    st.plotly_chart(fig3, use_container_width=True)
                    st.markdown("""
                    <div class="chart-note">
                        When a group arrives all at once, this line shoots up. After the rush it slowly
                        falls back — but the backlog takes time to clear even if arrivals slow down.
                    </div>""", unsafe_allow_html=True)

                with ch4:
                    df_runs = pd.DataFrame({"Day": range(1, num_runs+1), "Average Wait (min)": multi_avgs})
                    fig4 = px.bar(df_runs, x="Day", y="Average Wait (min)",
                                  title=f"📅 Average Wait Across {num_runs} Simulated Days",
                                  color="Average Wait (min)", color_continuous_scale="Purples")
                    fig4.update_layout(**PLOT)
                    st.plotly_chart(fig4, use_container_width=True)
                    st.markdown("""
                    <div class="chart-note">
                        Same settings, different days — yet results vary! This is randomness in action.
                        Some days the queue is short; other days it explodes unexpectedly.
                    </div>""", unsafe_allow_html=True)

                # Summary
                fix_msg = (
                    "➡️ Consider adding a second teller or reducing peak-hour arrivals."
                    if traffic >= 0.8 else
                    "➡️ The system is healthy, but random spikes can still cause temporary waits."
                )
                st.markdown(f"""
                <div class="insight-box">
                    🎯 <b>Plain-English Summary:</b><br>
                    Your teller is working at <b>{traffic*100:.0f}%</b> capacity.
                    On average, customers wait <b>{avg_w:.1f} minutes</b> —
                    but due to randomness the longest wait recorded was <b>{max_w:.1f} minutes</b>!<br>
                    {fix_msg}
                </div>
                """, unsafe_allow_html=True)

            # ── COMPARISON MODE ───────────────────────────────
            else:
                st.markdown("""
                <div class="insight-box">
                    ⚖️ Both banks have the <b>same arrival rate and same teller speed</b>.
                    The only difference is <b>how</b> customers arrive.
                    Watch the queue behave completely differently!
                </div>
                """, unsafe_allow_html=True)

                w_a, q_a = simulate_queue(arrival_rate, service_rate, num_customers, constant_arrival=True)
                w_b, q_b = simulate_queue(arrival_rate, service_rate, num_customers, constant_arrival=False)

                col_a, col_b = st.columns(2, gap="large")

                with col_a:
                    st.markdown("""
                    <div class="compare-card compare-card-a">
                        <h3 style="color:#34d399; margin-bottom:4px;">🟢 Bank A — Smooth Arrivals</h3>
                        <p style="color:#6b7280; font-size:0.9rem; margin-bottom:16px;">
                            Customers arrive at perfectly even intervals — no surprise bursts.
                        </p>
                    </div>
                    """, unsafe_allow_html=True)

                    m1, m2, m3 = st.columns(3)
                    metric_card(m1, "⏱️", "Avg Wait",     f"{np.mean(w_a):.2f}m", "typical wait",         "#10b981")
                    metric_card(m2, "⏳", "Max Wait",     f"{np.max(w_a):.2f}m",  "longest wait seen",    "#34d399")
                    metric_card(m3, "📉", "Variability",  f"{np.var(w_a):.2f}",   "how much times differ","#6ee7b7")

                    df_qa = pd.DataFrame(q_a)
                    fig_a = px.line(df_qa, x="Time", y="Queue Length",
                                    title="Queue Size — Bank A (Steady)", line_shape="hv")
                    fig_a.update_traces(line_color="#10b981", line_width=2.5)
                    fig_a.update_layout(**PLOT)
                    st.plotly_chart(fig_a, use_container_width=True)
                    st.markdown("""
                    <div class="chart-note" style="border-color:#10b981; color:#6ee7b7;">
                        Smooth arrivals keep the queue flat. The teller finishes each customer before the next one arrives.
                    </div>""", unsafe_allow_html=True)

                with col_b:
                    diff = np.mean(w_b) - np.mean(w_a)
                    st.markdown(f"""
                    <div class="compare-card compare-card-b">
                        <h3 style="color:#f87171; margin-bottom:4px;">🔴 Bank B — Random Arrivals</h3>
                        <p style="color:#6b7280; font-size:0.9rem; margin-bottom:16px;">
                            Same average rate, but customers arrive randomly in unpredictable bursts.
                        </p>
                    </div>
                    """, unsafe_allow_html=True)

                    m1, m2, m3 = st.columns(3)
                    metric_card(m1, "⏱️", "Avg Wait",     f"{np.mean(w_b):.2f}m", f"+{diff:.2f}m vs Bank A","#ef4444")
                    metric_card(m2, "⏳", "Max Wait",     f"{np.max(w_b):.2f}m",  "longest wait seen",        "#f87171")
                    metric_card(m3, "📉", "Variability",  f"{np.var(w_b):.2f}",   "how much times differ",    "#fca5a5")

                    df_qb = pd.DataFrame(q_b)
                    fig_b = px.line(df_qb, x="Time", y="Queue Length",
                                    title="Queue Size — Bank B (Random)", line_shape="hv")
                    fig_b.update_traces(line_color="#ef4444", line_width=2.5)
                    fig_b.update_layout(**PLOT)
                    st.plotly_chart(fig_b, use_container_width=True)
                    st.markdown("""
                    <div class="chart-note" style="border-color:#ef4444; color:#fca5a5;">
                        Random bursts send the queue spiking! After a rush, the backlog lingers even when
                        the next arrivals are slow.
                    </div>""", unsafe_allow_html=True)

                # Final comparison insight
                st.markdown(f"""
                <div class="key-idea-card">
                    <div class="key-idea-icon">🔍</div>
                    <div class="key-idea-title">Comparison Result</div>
                    <div class="key-idea-text">
                        ✅ <b>Bank A (steady)</b>: average wait was just <b>{np.mean(w_a):.2f} minutes</b>.<br>
                        🔴 <b>Bank B (random)</b>: average wait was <b>{np.mean(w_b):.2f} minutes</b>
                        — that's <b>{diff:.2f} minutes longer</b> for the exact same teller speed.<br><br>
                        <i>Same average. Same teller. Randomness made all the difference.</i>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)


    # ─────────────────────────────────────────
    #  SECTION 5 — WHAT YOU LEARN
    # ─────────────────────────────────────────
    st.markdown("""
    <div class="sec-label">Takeaways</div>
    <div class="sec-title">🎯 What You Learn from This App</div>
    <div class="sec-sub">
        By exploring this simulation, you build real intuition about queues and randomness.
    </div>
    """, unsafe_allow_html=True)

    learn_items = [
        ("Why queues suddenly become long",
         "Even when a server is fast 'on average', random bunches of customers can overwhelm it instantly — "
         "creating queues that take much longer to clear than they took to form."),
        ("Why averages can be misleading",
         "Saying 'our bank averages 10 customers per hour' hides the truth: sometimes 0 show up, "
         "sometimes 25 arrive at once. The average looks fine; the experience is miserable."),
        ("How randomness affects waiting time",
         "Randomness (variability) is the root cause of long waits — not just total volume. "
         "A predictable system with the same load is always faster and fairer."),
        ("How congestion builds in real systems",
         "Once a queue forms, it feeds on itself: people who arrived late still wait for the backlog to clear, "
         "even if the rush is already over. This is why traffic jams outlast the original incident."),
        ("How to design better systems",
         "Smart system designers add extra buffer capacity specifically to absorb random bursts — "
         "not just to handle the average. That's why hospitals overstaff and servers auto-scale."),
    ]

    col_l, col_r = st.columns(2, gap="large")
    for i, (title, desc) in enumerate(learn_items):
        target_col = col_l if i % 2 == 0 else col_r
        target_col.markdown(f"""
        <div class="learn-card">
            <div class="learn-num">{i+1}</div>
            <div>
                <div class="learn-title">{title}</div>
                <div class="learn-desc">{desc}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Footer
    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center; color:#4b4680; font-size:0.85rem; padding-bottom:40px;">
        🏦 Queue Randomness Explained &nbsp;·&nbsp; Built with Streamlit &nbsp;·&nbsp;
        An interactive tool to understand waiting time variability
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
