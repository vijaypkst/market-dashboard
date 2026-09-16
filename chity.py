import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# Configure Layout
st.set_page_config(page_title="Institutional Pre-Market Alpha", layout="wide", page_icon="📊")

# Auto-refresh the dashboard every 30 seconds automatically
st_autorefresh(interval=30000, key="datarefresh")

st.title("📊 Institutional Pre-Market Alpha Dashboard")
st.caption(f"🔄 Auto-Refreshing | Last updated: {datetime.now().strftime('%I:%M:%S %p')} IST")
st.markdown("---")


# Data Fetching Logic
@st.cache_data(ttl=15)
def fetch_all_data():
    global_tickers = {
        "GIFT Nifty Futures": "SGXN1!",
        "Nifty 50 Spot": "^NSEI",
        "S&P 500 (US)": "^GSPC",
        "Nasdaq (US)": "^IXIC",
        "Nikkei 225 (Japan)": "^N225"
    }

    heavyweights = {
        "HDFC Bank": "HDB",
        "Reliance Ind.": "RELIANCE.NS",
        "ICICI Bank": "IBN",
        "Infosys": "INFY"
    }

    combined = {**global_tickers, **heavyweights}
    data = {}

    for name, ticker in combined.items():
        try:
            t = yf.Ticker(ticker)
            hist = t.history(period="2d")
            if len(hist) >= 1:
                curr = hist['Close'].iloc[-1]
                prev = hist['Close'].iloc[-2] if len(hist) > 1 else curr
                change = curr - prev
                pct = (change / prev) * 100
                data[name] = {"price": curr, "pct": pct}
        except:
            data[name] = {"price": 0.0, "pct": 0.0}
    return data


data_feed = fetch_all_data()

# ==========================================
# 📊 1. Implied Opening & Visual Message Alerts
# ==========================================
st.subheader("🔎 Implied Opening Calculator")
gift_nifty = data_feed.get("GIFT Nifty Futures", {"price": 0})["price"]
nifty_spot = data_feed.get("Nifty 50 Spot", {"price": 0})["price"]

if gift_nifty > 0 and nifty_spot > 0:
    gap = gift_nifty - nifty_spot
    gap_pct = (gap / nifty_spot) * 100

    # DYNAMIC VISUAL MESSAGES BASED ON VOLATILITY THRESHOLDS
    if gap <= -150:
        st.error(
            f"🚨 **CRITICAL BEARISH ALERT:** Severe Gap-Down expected ({gap:.2f} pts). Global markets are facing heavy selling pressure. Protect capital!")
    elif gap >= 150:
        st.success(
            f"🔥 **STRONG BULLISH ALERT:** Massive Gap-Up expected (+{gap:.2f} pts). Global markets are rallying hard. Watch for chase traps!")
    elif -50 <= gap <= 50:
        st.info(
            "😐 **NEUTRAL MARKET NOTICE:** The market is indicated to open flat. Volatility is low; wait for clear index trends.")

    c1, c2, c3 = st.columns(3)
    c1.metric("GIFT Nifty Futures", f"{gift_nifty:,.2f}")
    c2.metric("Nifty 50 Spot Close", f"{nifty_spot:,.2f}")

    if gap > 0:
        c3.metric("Implied Opening", f"+{gap:,.2f} pts", f"+{gap_pct:.2f}%")
        if gap < 150:
            st.success(f"🚀 **Mild Bullish Bias:** Expecting a Gap-Up opening of roughly {abs(gap):.2f} points.")
    else:
        c3.metric("Implied Opening", f"{gap:,.2f} pts", f"{gap_pct:.2f}%", delta_color="inverse")
        if gap > -150:
            st.error(f"⚠️ **Mild Bearish Bias:** Expecting a Gap-Down opening of roughly {abs(gap):.2f} points.")
else:
    st.warning("Awaiting live data streams...")

st.markdown("---")

# ==========================================
# 🌏 2. Global Sentiment Grid
# ==========================================
st.subheader("🌏 Global Sentiment Hub")
g1, g2, g3 = st.columns(3)


def render_box(col, title, key):
    asset = data_feed.get(key, {"price": 0, "pct": 0})
    col.metric(title, f"{asset['price']:,.2f}", f"{asset['pct']:.2f}%",
               delta_color="normal" if asset['pct'] >= 0 else "inverse")


render_box(g1, "S&P 500 (USA)", "S&P 500 (US)")
render_box(g2, "Nasdaq (USA)", "Nasdaq (US)")
render_box(g3, "Nikkei 225 (Japan)", "Nikkei 225 (Japan)")

st.markdown("---")

# ==========================================
# 🏛️ 3. Heavyweights Monitor
# ==========================================
st.subheader("🏛️ Institutional Heavyweight Pulse Check")
st.caption("Monitoring structural trendsetters that drive the Nifty 50 index direction.")
h1, h2, h3, h4 = st.columns(4)

render_box(h1, "HDFC Bank (Anchor)", "HDFC Bank")
render_box(h2, "Reliance Industries", "Reliance Ind.")
render_box(h3, "ICICI Bank", "ICICI Bank")
render_box(h4, "Infosys (IT Driver)", "Infosys")

st.markdown("---")

# ==========================================
# 📖 NEW ADDITION: ON-SCREEN MORNING EXECUTION MANUAL
# ==========================================
st.subheader("🧠 Professional Live Trading Playbook")
expander = st.expander("📖 Click to expand your Step-by-Step Morning Routine Guide", expanded=True)
with expander:
    col_play1, col_play2 = st.columns(2)

    with col_play1:
        st.markdown("""
        ### ⏱️ The 4-Step Morning Timeline
        1. **08:30 AM (Global Check):** Look at the top color banner. Green = Bullish day, Red = Dangerous Macro selling, Blue = Rangebound/Flat.
        2. **08:45 AM (Find the Driver):** Check the *Global Sentiment Hub*. Is the gap coming from the US markets overnight, or is Asia (Nikkei) leading the momentum?
        3. **09:00 AM (Heavyweight Pulse):** Look at *HDFC Bank* and *Reliance*. If the calculator says Gap-Up but these heavyweights are red, **the gap is weak** and likely to fail.
        4. **09:15 AM (Execution Lock):** Do not place market orders in the first 15 mins. Let retail panic clear out. Trade setups after **09:30 AM**.
        """)

    with col_play2:
        st.markdown("""
        ### 🚨 The 09:08 AM "Gap Trap" Verification Rule
        Never buy a gap blindly before cross-referencing domestic order flow.
        * At **09:08 AM IST**, open the official **NSE India Pre-Open Page**.
        * Compare NSE's calculated *Equilibrium Price* against this dashboard's *Implied Opening*.
        * **The Trap:** If this dashboard indicates a +100 point gap up, but the official NSE system shows a flat or negative opening, big institutions are dumping shares. **Stand aside.**
        """)

st.markdown("---")

# ==========================================
# 🗓️ SIDEBAR LAYOUT
# ==========================================
st.sidebar.header("🗓️ Corporate Action Calendar")
st.sidebar.caption("High-impact events driving stock-specific pre-open volume.")

events_data = {
    "Symbol": ["EMAMILTD", "FEDERALBNK", "ORISSAMINE", "RESPONIND", "SKYWAYS", "YATHARTH"],
    "Company Name": ["Emami Limited", "Federal Bank", "Orissa Minerals", "Responsive Ind.", "Skyways Air",
                     "Yatharth Hospital"],
    "Action/Purpose": ["Buyback Plan", "Fund Raising", "Financial Results", "Buyback Plan", "Dividend & Q1",
                       "Fund Raising"],
    "Date": ["17-Sep-2026", "17-Sep-2026", "17-Sep-2026", "17-Sep-2026", "17-Sep-2026", "17-Sep-2026"]
}
df_events = pd.DataFrame(events_data)
st.sidebar.dataframe(df_events, use_container_width=True, hide_index=True)

st.sidebar.markdown("---")
st.sidebar.header("📊 Quick Trading Cheat Sheet")
st.sidebar.markdown("""
* **Gap (+) AND Heavyweights Green:** Bullish. Look to buy market dips.
* **Gap (+) BUT Heavyweights Red:** Trap Warning. Expect a spike and immediate crash.
* **Gap (-) AND Global Hub Red:** Bearish. Do not catch a falling knife.
""")
