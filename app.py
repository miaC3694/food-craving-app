import streamlit as st
from google import genai

st.set_page_config(page_title="Smart Eatery Friend", page_icon="🍔")
st.title("What do you crave for today? 🍜")
st.write("---")

# 從 Streamlit 的安全機制中讀取 API Key
api_key = st.secrets.get("GEMINI_API_KEY", "")

# 1. 地點與關鍵字輸入區
col_loc, col_food = st.columns(2)
with col_loc:
    user_location = st.text_input("📍 Enter your location, city, or address:", value="UW-Madison, State Street")
with col_food:
    user_input = st.text_input("💡 What are you craving? (e.g., warm soup, tacos):")

st.markdown("<p style='text-align: center; color: gray;'>— Or pick a vibe below —</p>", unsafe_allow_html=True)

# 2. 長方形大按鈕區
col1, col2 = st.columns(2)
selected_tag = None

with col1:
    if st.button("⚡ #energy Boost Energy", use_container_width=True):
        selected_tag = "energy boost snack"
    if st.button("🔥 #spicy Craving Spice", use_container_width=True):
        selected_tag = "spicy food"

with col2:
    if st.button("💸 #cheap Budget Friendly", use_container_width=True):
        selected_tag = "cheap eats under 15 dollars"
    if st.button("🍰 #sweet Sweet Treat", use_container_width=True):
        selected_tag = "sweet treat dessert"

# 判斷輸入來源
target = user_input if user_input else selected_tag

# 3. 呼叫 AI 生成動態區域推薦
if target:
    st.write("---")
    st.success(f"Searching near **{user_location}** for: **{target}**")
    
    if not api_key:
        st.warning("⚠️ Please configure your `GEMINI_API_KEY` in Streamlit Secrets to activate the AI brain.")
    else:
        with st.spinner("Your AI Eatery Friend is scanning the area... 🍳"):
            try:
                # 初始化 Gemini 客戶端
                client = genai.Client(api_key=api_key)
                
                # 結合使用者輸入的地點與需求
                prompt = (
                    f"You are a local foodie guide. "
                    f"The user is located at or near: '{user_location}'. "
                    f"They are looking for: '{target}'. "
                    f"Please provide: "
                    f"1. One specific, real restaurant or cafe close to '{user_location}'. "
                    f"2. One specific dish name that matches their exact request. "
                    f"3. A short, friendly note explaining why this fits their mood. "
                    f"4. A simple 'Cook at Home' version or quick tip. "
                    f"Keep the tone warm, modern, and concise."
                )
                
                response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=prompt,
                )
                ai_output = response.text
            except Exception as e:
                ai_output = f"Oops! Something went wrong connecting to the AI: {e}"

        # 顯示 AI 的回答
        st.markdown(ai_output)
        
        # 4. 動態 Google Maps 與食譜搜尋按鈕
        st.write("---")
        tab1, tab2 = st.tabs(["🍴 Google Maps Search", "🍳 Quick Recipe Search"])
        with tab1:
            st.link_button("Search on Google Maps", f"https://www.google.com/maps/search/{target}+restaurant+near+{user_location}", use_container_width=True)
        with tab2:
            st.link_button("Search DIY Recipes", f"https://www.google.com/search?q={target}+quick+recipe+at+home", use_container_width=True)

st.log = "---"
st.caption("A smart location-aware decision assistant, powered by Gemini")
