import streamlit as st

# 模擬 UW-Madison 周邊餐廳資料庫
restaurant_db = {
    "energy": {"name": "Colectivo Coffee", "note": "他們的冷萃咖啡與燕麥碗能讓你撐過下午的課！"},
    "spicy": {"name": "HaLong Bay", "note": "這家店的辣度很有誠意，特別是他們的泰式咖哩。"},
    "cheap": {"name": "Ian's Pizza", "note": "校園經典，Slice 便宜又管飽，月底救星。"},
    "sweet": {"name": "Memorial Union Terrace", "note": "來份 Babcock Hall 的冰淇淋，這是 Madison 的靈魂。"}
}

st.set_page_config(page_title="UW-Madison Eatery Friend", page_icon="🍔")
st.title("What do you crave for today? 🍜")
st.write("---")

# 1. 自由輸入區
user_input = st.text_input("💡 有特定的食物或關鍵字嗎？直接打出來（例如：ramen, 抹茶, 沙拉...）：")

st.markdown("<p style='text-align: center; color: gray;'>— 或者從下方選一個感覺 —</p>", unsafe_allow_html=True)

# 2. 長方形大按鈕區 (使用 use_container_width=True 讓按鈕變成滿版長方形)
col1, col2 = st.columns(2)
selected_tag = None

with col1:
    if st.button("⚡ #energy 補充體力", use_container_width=True):
        selected_tag = "energy"
    if st.button("🔥 #spicy 想吃辣的", use_container_width=True):
        selected_tag = "spicy"

with col2:
    if st.button("💸 #cheap 月底救星", use_container_width=True):
        selected_tag = "cheap"
    if st.button("🍰 #sweet 甜點療癒", use_container_width=True):
        selected_tag = "sweet"

# 判斷使用者是用「打字的」還是「按按鈕的」
target = None
if user_input:
    target = user_input
elif selected_tag:
    target = selected_tag

# 3. 顯示結果互動區
if target:
    st.write("---")
    st.success(f"收到！你鎖定了：**{target}**")
    
    # 如果有在資料庫內就抓資料，沒有就動態生成通用的回答
    if target in restaurant_db:
        data = restaurant_db[target]
        name = data["name"]
        note = data["note"]
    else:
        name = f"State Street 附近的精選好店"
        note = f"關於「{target}」，這在 UW-Madison 附近討論度很高，去 State Street 找找準沒錯！"

    st.write(f"**美食朋友說：** {note}")
    
    tab1, tab2 = st.tabs(["🍴 出門吃這家", "🍳 在家自己弄"])
    with tab1:
        st.write(f"📍 推薦店家：{name}")
        st.link_button("在 Google Maps 上查看", f"https://www.google.com/maps/search/{name}+near+UW+Madison", use_container_width=True)
    with tab2:
        st.write("不想出門？那來看看怎麼在家快速 DIY：")
        st.link_button("查看簡易食譜教學", f"https://www.google.com/search?q={target}+quick+recipe+at+home", use_container_width=True)

st.write("---")
st.caption("專為 UW-Madison 學生設計的決策輔助工具")
