import streamlit as st
from google import genai

st.set_page_config(page_title="Smart Eatery & Recipe Finder", page_icon="🍽️")
st.title("What are we exploring today? 🍽️")
st.write("---")

# 從 Streamlit Secrets 讀取 API Key
api_key = st.secrets.get("GEMINI_API_KEY", "")

# 1. 地點設定區（不限校園，全球通用）
user_location = st.text_input("📍 Enter your location, city, or address:", value="Livingston, NJ")

st.write("### ✨ Pick a craving vibe:")

# 2. 六個長方形網格按鈕區（3欄 x 2排）
col1, col2, col3 = st.columns(3)
selected_tag = None

with col1:
    if st.button("🍜 Warm Soup", use_container_width=True):
        selected_tag = "warm and comforting soup"
    if st.button("🍔 Burgers & Fries", use_container_width=True):
        selected_tag = "juicy burgers and fries"

with col2:
    if st.button("🌮 Tacos & Mexican", use_container_width=True):
        selected_tag = "tacos and Mexican food"
    if st.button("🍰 Sweet Dessert", use_container_width=True):
        selected_tag = "sweet treat and dessert"

with col3:
    if st.button("🥗 Fresh Bowls", use_container_width=True):
        selected_tag = "fresh and healthy bowls"
    if st.button("☕ Cozy Café", use_container_width=True):
        selected_tag = "cozy coffee and pastry"

st.write("---")

# 3. 自由輸入區（支援 "I need a place" 或 "I need the food" 等情境關鍵字）
user_input = st.text_input("💡 Or type freely (e.g., 'I need a place for a date night' or 'I need the food recipe for pad thai'):")

# 判斷最終目標（優先採用文字輸入，否則採用按鈕點擊）
target = user_input if user_input else selected_tag

# 4. 呼叫 AI 進行智慧解析與推薦
if target:
    st.write("---")
    st.success(f"Target near **{user_location}**: **{target}**")
    
    if not api_key:
        st.warning("⚠️ Please configure your `GEMINI_API_KEY` in Streamlit Secrets to activate the AI brain.")
    else:
        with st.spinner("AI Foodie is analyzing your request... 🍳"):
            try:
                client = genai.Client(api_key=api_key)
                
                # 智慧 Prompt：讓 AI 自動判斷使用者是要找餐廳還是找食譜
                prompt = (
                    f"You are an intelligent food guide and local expert. "
                    f"The user is located at: '{user_location}'. "
                    f"Their request or selected vibe is: '{target}'. "
                    f"Please analyze their intent: "
                    f"- If they want a place ('I need a place'), recommend 1 specific real restaurant near '{user_location}' and their signature dish. "
                    f"- If they want the food/recipe ('I need the food'), provide a quick, delicious recipe or preparation breakdown. "
                    f"- If it's a category button, provide both a great local spot and a quick home alternative. "
                    f"Keep the tone warm, modern, and concise."
                )
                
                response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=prompt,
                )
                ai_output = response.text
            except Exception as e:
                ai_output = f"Oops! Something went wrong connecting to the AI: {e}"

        # 顯示 AI 回應
        st.markdown(ai_output)
        
        # 5. 快速導航與食譜搜尋按鈕
        st.write("---")
        tab1, tab2 = st.tabs(["🍴 Search Places on Google Maps", "🍳 Search Recipes Online"])
        with tab1:
            st.link_button("Search Places Nearby", f"https://www.google.com/maps/search/{target}+near+{user_location}", use_container_width=True)
        with tab2:
            st.link_button("Search Recipes", f"https://www.google.com/search?q={target}+recipe", use_container_width=True)

st.write("---")
st.caption("A smart multi-intent food assistant, powered by Gemini 3.6 Flash")
