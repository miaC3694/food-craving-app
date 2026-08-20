import streamlit as st
from google import genai

st.set_page_config(page_title="Whar are you craving for today?", page_icon="🍽️")
st.title("What are you craving for today? 🍽️")
st.write("---")

api_key = st.secrets.get("GEMINI_API_KEY", "")

# 初始化 Session State（用來記住生成的 6 個選項）
if "food_options" not in st.session_state:
    st.session_state.food_options = []

# 1. 輸入地點與大方向心情
user_location = st.text_input("📍 Enter your location or city:", value="Livingston, NJ")
broad_craving = st.text_input("💡 What's your general mood or craving? (e.g., cozy, late night, healthy, comforting):")

# 2. 點擊按鈕讓 AI 生成 6 種食物
if st.button("🎲 Generate 6 Food Options", use_container_width=True):
    if not api_key:
        st.warning("⚠️ Please configure your GEMINI_API_KEY in Streamlit Secrets.")
    else:
        with st.spinner("Brainstorming 6 delicious ideas for you... 🍳"):
            try:
                client = genai.Client(api_key=api_key)
                prompt = (
                    f"Based on the vibe '{broad_craving}' near '{user_location}', "
                    f"generate exactly 6 specific and diverse food or dish names. "
                    f"Return ONLY a valid Python list of 6 strings, for example: "
                    f"['Spicy Tonkotsu Ramen', 'Margherita Pizza', 'Avocado Toast', 'Crispy Chicken Tacos', 'Matcha Latte & Pastry', 'Greek Salad Bowl']. "
                    f"Do not include any numbering or extra text outside the list."
                )
                response = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=prompt,
                )
                
                # 清理並解析 AI 回傳的清單
                text = response.text.strip()
                if "```" in text:
                    text = text.split("```")[1]
                    if text.startswith("python"):
                        text = text[6:]
                text = text.strip()
                
                options = eval(text)
                if isinstance(options, list) and len(options) > 0:
                    st.session_state.food_options = options
                else:
                    st.session_state.food_options = ["Spicy Miso Ramen", "Truffle Cheeseburger", "Birria Tacos", "Classic Carbonara", "Salmon Poke Bowl", "Matcha Crepe Cake"]
            except Exception as e:
                # 預設備用選項，避免報錯
                st.session_state.food_options = [
                    "Spicy Miso Ramen", 
                    "Truffle Cheeseburger", 
                    "Birria Tacos", 
                    "Classic Carbonara", 
                    "Salmon Poke Bowl", 
                    "Matcha Crepe Cake"
                ]

# 3. 如果已經有 6 個選項，展示出來讓使用者挑選
if st.session_state.food_options:
    st.write("---")
    st.write("### 👇 Pick one of the 6 options generated for you:")
    
    # 讓使用者從 6 個選項中勾選或選擇一個
    selected_food = st.selectbox("Choose your favorite:", st.session_state.food_options)
    
    # 讓使用者決定意圖：找餐廳 (I need a place) 還是找食譜 (I need the food)
    choice_type = st.radio("What would you like to do next?", ["🍴 I need a place (Find a restaurant)", "🍳 I need the food (Get a recipe & cook at home)"])

    if st.button("✨ Get Final Recommendation", use_container_width=True):
        with st.spinner(f"Analyzing details for '{selected_food}'..."):
            try:
                client = genai.Client(api_key=api_key)
                
                if "I need a place" in choice_type:
                    detail_prompt = (
                        f"The user is at '{user_location}' and selected '{selected_food}'. "
                        f"Recommend 1 specific, real restaurant or cafe near '{user_location}' that serves this. "
                        f"Include the restaurant name, why it's great, and what makes their version special."
                    )
                else:
                    detail_prompt = (
                        f"The user selected '{selected_food}' and wants to make it at home. "
                        f"Provide a quick, easy 3-step home recipe or preparation guide for '{selected_food}'."
                    )
                
                res = client.models.generate_content(
                    model="gemini-3.6-flash",
                    contents=detail_prompt,
                )
                
                st.write("---")
                st.markdown("### 🎯 Your Custom Recommendation:")
                st.markdown(res.text)
                
                # 4. 快速跳轉按鈕
                st.write("---")
                if "I need a place" in choice_type:
                    st.link_button("Search Places on Google Maps", f"https://www.google.com/maps/search/{selected_food}+near+{user_location}", use_container_width=True)
                else:
                    st.link_button("Search Recipe Online", f"https://www.google.com/search?q={selected_food}+recipe", use_container_width=True)
            except Exception as e:
                st.error(f"Oops! Something went wrong: {e}")

st.write("---")
st.caption("A two-stage intelligent food discovery assistant, powered by Gemini 3.6 Flash")
