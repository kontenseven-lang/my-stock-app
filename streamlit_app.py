import streamlit as st
import yfinance as yf

# 網頁基本設定
st.set_page_config(page_title="台股本益比助手", layout="centered")

st.title("📈 台股本益比即時計算器")
st.info("輸入股號與 EPS，自動抓取 Yahoo Finance 最新報價。")

# 側邊欄或主畫面輸入
with st.container():
    stock_id = st.text_input("請輸入股票代碼 (例如: 2330)", "2330")
    eps = st.number_input("請輸入預估 EPS (例如: 32.34)", value=10.0, step=0.1)
    submit = st.button("🚀 開始計算", use_container_width=True)

if submit:
    try:
        # 自動嘗試上市 (.TW) 或上櫃 (.TWO)
        ticker_id = f"{stock_id}.TW"
        stock = yf.Ticker(ticker_id)
        price = stock.fast_info['last_price']
        
        if price is None or price == 0:
            ticker_id = f"{stock_id}.TWO"
            stock = yf.Ticker(ticker_id)
            price = stock.fast_info['last_price']

        if price and price > 0:
            pe_ratio = price / eps
            
            # 漂亮的結果展示
            st.divider()
            st.subheader(f"查詢結果：{stock_id}")
            
            c1, c2 = st.columns(2)
            c1.metric("最新股價", f"${price:.2f} TWD")
            c2.metric("計算本益比", f"{pe_ratio:.2f} 倍")

            # 投資評價提示
            if pe_ratio < 12:
                st.success("✨ 評價提示：目前本益比偏低，具備價值投資潛力。")
            elif 12 <= pe_ratio <= 20:
                st.info("⚖️ 評價提示：目前評價處於合理範圍。")
            else:
                st.warning("⚠️ 評價提示：目前本益比偏高，請留意回檔風險。")
        else:
            st.error(f"❌ 找不到股號 {stock_id} 的即時行情，請確認代碼是否正確。")
            
    except Exception as e:
        st.error(f"發生非預期錯誤：{e}")
