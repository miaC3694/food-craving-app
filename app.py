import streamlit as st
from google import genai

st.set_page_config(page_title="UW-Madison Eatery Friend", page_icon="🍔")
st.title("What do you crave for today? 🍜")
st.write("---")

# 從 Streamlit 的安全機制中讀取 API Key
api_key = st.secrets.get("GEMINI_API_KEY", "")

# 1. 自由輸入區
user_input = st.text_input("💡 Got a specific food or keyword in mind? Type it here (e.g., korean, boba, ramen...):")

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

# 3. 呼叫 AI 生成推薦
if target:
    st.write("---")
    st.success(f"Got it! You're looking for: **{target}**")
    
    if not api_key:
        st.warning("⚠️ Please configure your `GEMINI_API_KEY` in Streamlit Secrets to activate the AI brain.")
    else:
        with st.spinner("Your AI Eatery Friend is thinking... 🍳"):
            try:
                # 初始化 Gemini 客戶端
                client = genai.Client(api_key=api_key)
                
                # 設計給 AI 的 Prompt，限制在 UW-Madison 校園周邊
                prompt = f"""
                You are a friendly local foodie guide for an undergraduate student at UW-Madison. 
                The student is craving or looking for: '{target}'.
                Please recommend:
                1. One specific, real restaurant or cafe near the UW-Madison campus or State Street area that fits this.
                2. A short, friendly note on why it's great.
                3. A very brief, easy DIY home recipe or alternative if they don't want to go out.
                Keep the tone warm, modern, and concise.
                """
                
                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=prompt,
                )
                ai_output = response.text
            except Exception as e:
                ai_output = f"Oops! Something went wrong connecting to the AI: {e}"

        # 顯示 AI 的回答
        st.markdown(ai_output)
        
        # 4. 快速導航與搜尋按鈕
        st.write("---")
        tab1, tab2 = st.tabs(["🍴 Google Maps Search", "🍳 Quick Recipe Search"])
        with tab1:
            st.link_button("Search on Google Maps", f"https://www.google.com/maps/search/{target}+restaurant+near+UW+Madison", use_container_width=True)
        with tab2:
            st.link_button("Search DIY Recipes", f"https://www.google.com/search?q={target}+quick+recipe+at+home", use_container_width=True)

st.write("---")
st.caption("A smart decision-making assistant built for UW-Madison students, powered by Gemini")
