import streamlit as st

# 模擬 UW-Madison 周邊餐廳資料庫 (English version)
restaurant_db = {
    "energy": {"name": "Colectivo Coffee", "note": "Their cold brew and grain bowls will power you through afternoon classes!"},
    "spicy": {"name": "HaLong Bay", "note": "They don't hold back on the spice, especially their Thai curries."},
    "cheap": {"name": "Ian's Pizza", "note": "Campus classic. Fast, cheap, and a total lifesaver at the end of the month."},
    "sweet": {"name": "Memorial Union Terrace", "note": "Grab some Babcock Hall ice cream—it's the soul of Madison."}
}

st.set_page_config(page_title="UW-Madison Eatery Friend", page_icon="🍔")
st.title("What do you crave for today? 🍜")
st.write("---")

# 1. 自由輸入區
user_input = st.text_input("💡 Got a specific food or keyword in mind? Type it here (e.g., ramen, matcha, salad...):")

st.markdown("<p style='text-align: center; color: gray;'>— Or pick a vibe below —</p>", unsafe_allow_html=True)

# 2. 長方形大按鈕區
col1, col2 = st.columns(2)
selected_tag = None

with col1:
    if st.button("⚡ #energy Boost Energy", use_container_width=True):
        selected_tag = "energy"
    if st.button("🔥 #spicy Craving Spice", use_container_width=True):
        selected_tag = "spicy"

with col2:
    if st.button("💸 #cheap Budget Friendly", use_container_width=True):
        selected_tag = "cheap"
    if st.button("🍰 #sweet Sweet Treat", use_container_width=True):
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
    st.success(f"Got it! You're looking for: **{target}**")
    
    if target in restaurant_db:
        data = restaurant_db[target]
        name = data["name"]
        note = data["note"]
    else:
        name = "Popular spot around State Street"
        note = f"'{target}' is quite popular around UW-Madison. Take a walk down State Street and you'll find something amazing!"

    st.write(f"**Eatery Friend says:** {note}")
    
    tab1, tab2 = st.tabs(["🍴 Dine Out", "🍳 Cook at Home"])
    with tab1:
        st.write(f"📍 Recommended Spot: {name}")
        st.link_button("View on Google Maps", f"https://www.google.com/maps/search/{name}+near+UW+Madison", use_container_width=True)
    with tab2:
        st.write("Don't want to go out? Here is a quick DIY suggestion:")
        st.link_button("Search Quick Recipes", f"https://www.google.com/search?q={target}+quick+recipe+at+home", use_container_width=True)

st.write("---")
st.caption("A decision-making assistant built for UW-Madison students")
