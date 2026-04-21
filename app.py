import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os

# --- 1. 科技感 UI 配置 ---
st.set_page_config(page_title="NEURAL LEDGER v1.0", layout="wide", initial_sidebar_state="expanded")

# 自定義 CSS：注入深色科技感樣式
st.markdown("""
    <style>
    /* 全域背景與文字 */
    .stApp {
        background-color: #0E1117;
        color: #E0E0E0;
    }
    /* 卡片效果 */
    div[data-testid="stMetric"] {
        background-color: #161B22;
        border: 1px solid #30363D;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    /* 漸層標題 */
    .main-title {
        background: linear-gradient(90deg, #00F2FE 0%, #4FACFE 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 3rem;
    }
    /* 按鈕美化 */
    .stButton>button {
        width: 100%;
        background: linear-gradient(45deg, #2193b0, #6dd5ed);
        border: none;
        color: white;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

DATA_FILE = "web_ledger.csv"

if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=["日期", "項目", "金額", "類別"])
    df.to_csv(DATA_FILE, index=False)

def get_data():
    return pd.read_csv(DATA_FILE)

# --- 2. 側邊欄 (控制台風格) ---
with st.sidebar:
    st.markdown("### 🖥️ SYSTEM CONTROL")
    budget = st.number_input("CORE_BUDGET_SET", value=10000)
    st.divider()
    if st.button("🔴 RESET DATABASE"):
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)
            st.rerun()

# --- 3. 主畫面佈局 ---
st.markdown('<p class="main-title">FINANCIAL NEURAL LINK</p>', unsafe_allow_html=True)
st.caption("Status: Operational | Database: Local v1.02")

# 頂部指標
df = get_data()
total_spent = df["金額"].sum()
remaining = budget - total_spent
usage_rate = (total_spent / budget) if budget > 0 else 0

cols = st.columns(3)
with cols[0]:
    st.metric("TOTAL_OUTFLOW", f"$ {total_spent:,.0f}")
with cols[1]:
    st.metric("REMAINING_LIQUIDITY", f"$ {remaining:,.0f}")
with cols[2]:
    st.metric("RESOURCE_USAGE", f"{usage_rate*100:.1f}%")

# 進度條 (科技藍)
st.progress(min(usage_rate, 1.0))

# 4. 數據輸入 (橫向排列減少空間佔用)
with st.container():
    st.markdown("#### 📥 DATA_INPUT_MODULE")
    c1, c2, c3, c4 = st.columns([2, 1, 1, 1])
    with c1: item = st.text_input("ITEM_NAME", label_visibility="collapsed", placeholder="Item Name")
    with c2: amount = st.number_input("VALUE", label_visibility="collapsed", min_value=0.0)
    with c3: category = st.selectbox("TAG", ["飲食", "交通", "娛樂", "居家", "其他"], label_visibility="collapsed")
    with c4: 
        if st.button("EXECUTE"):
            if item:
                new_data = pd.DataFrame([[datetime.now().date(), item, amount, category]], columns=["日期", "項目", "金額", "類別"])
                new_data.to_csv(DATA_FILE, mode='a', header=False, index=False)
                st.rerun()

# 5. 視覺化面板 (互動式圖表)
st.divider()
row2_1, row2_2 = st.columns([1.2, 1])

with row2_1:
    st.markdown("#### 📜 TRANSACTION_LOG")
    st.dataframe(df.sort_values("日期", ascending=False), use_container_width=True, height=350)

with row2_2:
    st.markdown("#### 📉 ALLOCATION_ANALYSIS")
    if not df.empty:
        category_df = df.groupby("類別")["金額"].sum().reset_index()
        fig = px.pie(
            category_df, values='金額', names='類別', 
            hole=0.5, 
            color_discrete_sequence=px.colors.sequential.Cyan_r
        )
        fig.update_layout(
            margin=dict(t=0, b=0, l=0, r=0),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color="white",
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Waiting for data stream...")
