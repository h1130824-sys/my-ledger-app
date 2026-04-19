import streamlit as st
import pandas as pd
from datetime import datetime
import os

# 1. 網頁基本設定
st.set_page_config(page_title="雲端小管家", layout="centered")

DATA_FILE = "web_ledger.csv"

# 2. 初始化資料檔 (如果檔案不存在就建一個新的)
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=["日期", "項目", "金額", "類別"])
    df.to_csv(DATA_FILE, index=False)

def get_data():
    return pd.read_csv(DATA_FILE)

# --- 側邊欄：預算設定 ---
st.sidebar.header("⚙️ 預算管理")
budget = st.sidebar.number_input("本月總預算", value=10000)

# --- 主畫面 ---
st.title("💰 我的雲端記帳本")

# 3. 新增支出區塊
with st.expander("➕ 點我記錄新支出", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        item = st.text_input("項目", placeholder="例如：午餐")
        amount = st.number_input("金額", min_value=0.0, step=10.0)
    with col2:
        category = st.selectbox("類別", ["飲食", "交通", "娛樂", "居家", "其他"])
        date = st.date_input("日期", datetime.now())
    
    if st.button("確認提交"):
        if item:
            new_data = pd.DataFrame([[date, item, amount, category]], columns=["日期", "項目", "金額", "類別"])
            new_data.to_csv(DATA_FILE, mode='a', header=False, index=False)
            st.success(f"✅ 已記錄: {item} ${amount}")
            st.rerun()
        else:
            st.error("❌ 請輸入項目名稱！")

# 4. 數據讀取與計算
df = get_data()
total_spent = df["金額"].sum()
remaining = budget - total_spent
usage_rate = (total_spent / budget) if budget > 0 else 0

# 5. 視覺化面板
st.subheader("📊 財務概況")
c1, c2, c3 = st.columns(3)
c1.metric("總支出", f"${total_spent:,.0f}")
c2.metric("剩餘預算", f"${remaining:,.0f}")
c3.metric("使用率", f"{usage_rate*100:.1f}%")

# 預算進度條
if usage_rate >= 1.0:
    st.progress(1.0)
    st.error("🚨 預算已經爆了！別再買啦！")
elif usage_rate >= 0.8:
    st.progress(usage_rate)
    st.warning("⚠️ 預算快用完囉，注意荷包。")
else:
    st.progress(usage_rate)
    st.info("✅ 目前消費還在控制內。")

# 6. 圖表與表格
if not df.empty:
    st.subheader("📈 消費比例")
    category_df = df.groupby("類別")["金額"].sum()
    st.pie_chart(category_df)

    st.subheader("📋 最近消費記錄")
    st.dataframe(df.sort_values("日期", ascending=False), use_container_width=True)

# 7. 清空功能
if st.sidebar.button("🗑️ 清空所有數據"):
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)
        st.rerun()
