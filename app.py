import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os

# --- 1. 科技感 UI 配置 ---
st.set_page_config(page_title="NEURAL LEDGER v1.0", layout="wide", initial_sidebar_state="expanded")

# 自定義 CSS：打造深色科技感介面
st.markdown("""
    <style>
    .stApp {
        background-color: #0E1117;
        color: #E0E0E0;
    }
    /* 指標卡片樣式 */
    div[data-testid="stMetric"] {
        background-color: #161B22;
        border: 1px solid #30363D;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.4);
    }
    /* 漸層標題 */
    .main-title {
        background: linear-gradient(90deg, #00F2FE 0%, #4FACFE 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 3rem;
        margin-bottom: 0px;
    }
    /* 執行按鈕樣式 */
    .stButton>button {
        width: 100%;
        background: linear-gradient(45deg, #2193b0, #6dd5ed);
        border: none;
        color: white;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 0 15px rgba(79, 172, 254, 0.5);
    }
    </style>
    """, unsafe_allow_html=True)

DATA_FILE = "web_ledger.csv"

# 初始化資料庫
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=["日期", "項目", "金額", "類別"])
    df.to_csv(DATA_FILE, index=False)

def get_data():
    return pd.read_csv(DATA_FILE)

# --- 2. 側邊欄控制台 ---
with st.sidebar:
    st.markdown("### 🖥️ SYSTEM CONTROL")
    budget = st.number_input("CORE_BUDGET_SET", value=10000)
    st.divider()
    st.caption("Database Operations")
    if st.button("🔴 RESET DATABASE"):
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)
            st.rerun()

# --- 3. 數據運算中心 ---
df = get_data()
total_spent = df["金額"].sum()
remaining = budget - total_spent
usage_rate = (total_spent / budget) if budget > 0 else 0

# --- 4. 主畫面抬頭 ---
st.markdown('<p class="main-title">FINANCIAL NEURAL LINK</p>', unsafe_allow_html=True)
st.caption(f"Status: Operational | Last Sync: {datetime.now().strftime('%H:%M:%S')}")

# 頂部指標卡片
cols = st.columns(3)
with cols[0]:
    st.metric("TOTAL_OUTFLOW", f"$ {total_spent:,.0f}")
with cols[1]:
    st.metric("REMAINING_LIQUIDITY", f"$ {remaining:,.0f}")
with cols[2]:
    st.metric("RESOURCE_USAGE", f"{usage_rate*100:.1f}%")

# --- 5. 強化版預算警示系統 ---
st.progress(min(usage_rate, 1.0))

if usage_rate >= 1.0:
    st.error(f"🚨 警告：預算已破表！超支金額: ${ (total_spent - budget):,.0f}")
    st.toast("FATAL ERROR: Budget Exceeded!", icon="🚨")
elif usage_rate >= 0.8:
    st.warning(f"🟡 提醒：資源使用率達 {usage_rate*100:.1f}%，請注意支出。")
    st.toast("WARNING: Low Budget Reservoir", icon="⚠️")
else:
    st.success(f"✨ 系統狀態良好：剩餘流動資金 ${remaining:,.0f}")

# --- 6. 數據輸入模組 ---
st.divider()
with st.container():
    st.markdown("#### 📥 DATA_INPUT_MODULE")
    c1, c2, c3, c4 = st.columns([2, 1, 1, 1])
    with c1: 
        item = st.text_input("ITEM_NAME", placeholder="輸入支出項目...", label_visibility="collapsed")
    with c2: 
        amount = st.number_input("VALUE", min_value=0.0, step=10.0, label_visibility="collapsed")
    with c3: 
        category = st.selectbox("TAG", ["飲食", "交通", "娛樂", "居家", "其他"], label_visibility="collapsed")
    with c4: 
        if st.button("EXECUTE"):
            if item:
                new_entry = pd.DataFrame([[datetime.now().date(), item, amount, category]], columns=["日期", "項目", "金額", "類別"])
                new_entry.to_csv(DATA_FILE, mode='a', header=False, index=False)
                st.toast("Data Encrypted & Saved", icon="🔒")
                st.rerun()
            else:
                st.error("Missing Input")

# --- 7. 視覺化面板 ---
row2_1, row2_2 = st.columns([1.2, 1])

with row2_1:
    st.markdown("#### 📜 TRANSACTION_LOG")
    st.dataframe(df.sort_values("日期", ascending=False), use_container_width=True, height=400)

with row2_2:
    st.markdown("#### 📉 ALLOCATION_ANALYSIS")
    if not df.empty:
        category_df = df.groupby("類別")["金額"].sum().reset_index()
        # 採用科技感配色
        tech_colors = ['#00F2FE', '#4FACFE', '#2193b0', '#6dd5ed', '#30363D']
        fig = px.pie(
            category_df, values='金額', names='類別', 
            hole=0.5, 
            color_discrete_sequence=tech_colors
        )
        fig.update_layout(
            margin=dict(t=30, b=0, l=0, r=0),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color="white",
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Waiting for data input to generate analysis...")
