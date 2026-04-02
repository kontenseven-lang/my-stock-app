import streamlit as st
import yfinance as yf

# 設定網頁標題與風格
st.set_page_config(page_title="台股投資助手", layout="wide")

st.title("📈 台股全方位投資助手")

# 建立分頁
tab1, tab2 = st.tabs(["本益比查詢", "損益與保本計算器"])

# --- 分頁 1：本益比查詢 ---
with tab1:
    st.header("即時本益比計算")
    col_input1, col_input2 = st.columns(2)
    with col_input1:
        stock_id = st.text_input("請輸入股票代碼", "2330", key="pe_stock")
    with col_input2:
        eps = st.number_input("請輸入預估 EPS", value=30.0, step=0.1, key="pe_eps")
    
    if st.button("🚀 查詢報價並計算", use_container_width=True):
        ticker = yf.Ticker(f"{stock_id}.TW")
        price = ticker.fast_info['last_price']
        if not price:
            ticker = yf.Ticker(f"{stock_id}.TWO")
            price = ticker.fast_info['last_price']
            
        if price:
            pe = price / eps
            st.metric("最新股價", f"${price:.2f}", delta_color="normal")
            st.metric("計算本益比", f"{pe:.2f} 倍")
            if pe < 12: st.success("评价偏低")
            elif pe <= 20: st.info("评价合理")
            else: st.warning("评价偏高")
        else:
            st.error("找不到該股票資料")

# --- 分頁 2：買賣損益與保本計算器 ---
with tab2:
    st.header("買賣損益與保本價分析")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        buy_price = st.number_input("買入股價", value=100.0, step=0.1)
    with col2:
        shares = st.number_input("購買股數", value=1000, step=100)
    with col3:
        discount_percent = st.slider("手續費折扣 (如 6 折請選 60)", 10, 100, 60)
    
    # 計算買入成本
    brokerage_rate = 0.001425
    tax_rate = 0.003
    discount = discount_percent / 100
    
    buy_fee = int(buy_price * shares * brokerage_rate * discount)
    if buy_fee < 20: buy_fee = 20  # 低消通常為 20 元
    total_cost = (buy_price * shares) + buy_fee
    
    # 計算保本價公式：
    # 賣出淨額 = 賣出總價 - 賣出手續費 - 交易稅
    # 需滿足：賣出淨額 >= 買入總成本
    # 簡化公式：保本價 ≈ 買入價 * (1 + 買手續費率) / (1 - 賣手續費率 - 交易稅率)
    breakeven_price = total_cost / (shares * (1 - (brokerage_rate * discount) - tax_rate))
    
    st.divider()
    
    # 顯示保本價資訊
    st.subheader(f"🚩 保本股價： {breakeven_price:.2f} 元")
    st.caption(f"股價需高於此數值才開始獲利 (已含 0.3% 交易稅與 {discount_percent} 折手續費)")

    # 模擬賣出計算
    st.write("---")
    sell_price = st.number_input("模擬賣出股價", value=round(breakeven_price * 1.05, 2), step=0.1)
    
    sell_fee = int(sell_price * shares * brokerage_rate * discount)
    if sell_fee < 20: sell_fee = 20
    sell_tax = int(sell_price * shares * tax_rate)
    sell_net = (sell_price * shares) - sell_fee - sell_tax
    
    profit = int(sell_net - total_cost)
    profit_rate = (profit / total_cost) * 100
    
    # 呈現損益結果
    res_col1, res_col2 = st.columns(2)
    with res_col1:
        st.metric("預估損益金額", f"{profit:,} 元", delta=f"{profit_rate:.2f}%")
    with res_col2:
        st.write(f"總成本：{total_cost:,} 元")
        st.write(f"賣出淨額：{sell_net:,} 元")
