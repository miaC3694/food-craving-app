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
                # 更新後的 AI Prompt，更強調精細化的推薦
                prompt = f"""
                You are a local foodie guide for an undergraduate student at UW-Madison.
                The student is looking for: '{target}'.
                
                Please provide:
                1. One specific restaurant or cafe near the UW-Madison campus (State Street or nearby).
                2. One specific dish name that perfectly matches their request (e.g., if they ask for 'warm but not too spicy', suggest something like Chicken Pho or Miso Ramen).
                3. A short, friendly note explaining why this specific dish fits their current mood.
                4. A simple 'Cook at Home' version or quick tip if they prefer to stay in.
                
                Keep the tone warm, modern, and empathetic to a student's budget and schedule.
                """
                
                response = client.models.generate_content(
                    model="gemini-3.6-flash",
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
