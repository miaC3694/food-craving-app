import streamlit as st

# 模擬 UW-Madison 周邊餐廳資料庫
restaurant_db = {
    "#energy": {"name": "Colectivo Coffee", "note": "他們的冷萃咖啡與燕麥碗能讓你撐過下午的課！"},
    "#spicy": {"name": "HaLong Bay", "note": "這家店的辣度很有誠意，特別是他們的泰式咖哩。"},
    "#cheap": {"name": "Ian's Pizza", "note": "校園經典，Slice 便宜又管飽，月底救星。"},
    "#sweet": {"name": "Memorial Union Terrace", "note": "來份 Babcock Hall 的冰淇淋，這是 Madison 的靈魂。"}
}

st.set_page_config(page_title="UW-Madison Eatery Friend", page_icon="🍔")
st.title("What do you crave for today? 🍜")
st.write("---")

choice = st.radio("今天是什麼心情？", ["#energy", "#spicy", "#cheap", "#sweet"])

if st.button("告訴我該吃什麼"):
    data = restaurant_db[choice]
    st.success(f"收到！看來你現在需要 {choice}")
    st.write(f"**美食朋友說：** {data['note']}")
    
    tab1, tab2 = st.tabs(["🍴 出門吃這家", "🍳 在家自己弄"])
    with tab1:
        st.write(f"📍 建議：{data['name']}")
        st.link_button("在 Google Maps 上查看", f"https://www.google.com/maps/search/{data['name']}+near+UW+Madison")
    with tab2:
        st.write("不想出門？那來看看怎麼在家 DIY：")
        st.link_button("查看簡易食譜教學", f"https://www.google.com/search?q={choice.replace('#', '')}+quick+recipe+at+home")
