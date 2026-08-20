import streamlit as st
from google import genai

st.set_page_config(page_title="Smart Dining & Decision Engine", page_icon="🍽️", layout="wide")

st.title("🍽️ What do you crave for today?")
st.markdown("---")

api_key = st.secrets.get("GEMINI_API_KEY", "")

# 初始化 Session State
if "food_options" not in st.session_state:
    st.session_state.food_options = []
if "group_members" not in st.session_state:
    st.session_state.group_members = []

# ==========================================
# 側邊欄：全域摩擦力矩陣 (The Friction Matrix)
# ==========================================
st.sidebar.header("⚙️ Friction Matrix (Global Filters)")
user_location = st.sidebar.text_input("📍 Your Location / City", value="Livingston, NJ")
max_budget = st.sidebar.slider("💰 Max Budget (USD)", 5, 50, 20)
max_walk = st.sidebar.slider("🚶 Max Travel Time (mins)", 5, 30, 15)

st.sidebar.markdown("---")
st.sidebar.info("💡 **Pro-tip:** Set your budget and travel limits here to filter out unrealistic options instantly.")

# ==========================================
# 主畫面：分頁切換（單人模式 vs. 多人匿名模式）
# ==========================================
tab_solo, tab_group = st.tabs(["👤 Solo Decision Hub (單人模式)", "👥 Secret Group Consensus (多人匿名模式)"])

# ==========================================
# Tab 1: 單人模式 (Solo Mode)
# ==========================================
with tab_solo:
    st.subheader("👤 Solo Food & Decision Hub")
    st.markdown("Not sure what to eat? Let AI generate 6 tailored options based on your current vibe, then choose to go out or cook at home.")

    broad_craving = st.text_input("💡 What's your general mood or craving right now? (e.g., cozy, healthy, late-night comfort):", key="solo_input")
    
    if st.button("🎲 Generate 6 Custom Food Options", use_container_width=True, key="btn_solo"):
        if not api_key:
            st.warning("⚠️ Please configure your GEMINI_API_KEY in Streamlit Secrets.")
        else:
            with st.spinner("Brainstorming 6 options tailored to your constraints... 🍳"):
                try:
                    client = genai.Client(api_key=api_key)
                    prompt = (
                        f"Based on the vibe '{broad_craving}' near '{user_location}', "
                        f"considering a max budget of ${max_budget} and max travel time of {max_walk} mins, "
                        f"generate exactly 6 specific and diverse food or dish names. "
                        f"Return ONLY a valid Python list of 6 strings, for example: "
                        f"['Spicy Tonkotsu Ramen', 'Margherita Pizza', 'Avocado Toast', 'Crispy Chicken Tacos', 'Matcha Latte & Pastry', 'Greek Salad Bowl']. "
                        f"Do not include any numbering or extra text outside the list."
                    )
                    response = client.models.generate_content(model="gemini-3.6-flash", contents=prompt)
                    
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
                    st.session_state.food_options = ["Spicy Miso Ramen", "Truffle Cheeseburger", "Birria Tacos", "Classic Carbonara", "Salmon Poke Bowl", "Matcha Crepe Cake"]

    # 顯示 6 種選項並進行後續分流
    if st.session_state.food_options:
        st.markdown("---")
        st.write("### 👇 Pick one of the 6 options generated for you:")
        selected_food = st.selectbox("Choose your favorite:", st.session_state.food_options, key="solo_select")
        
        choice_type = st.radio("What would you like to do next?", ["🍴 I need a place (Find a restaurant)", "🍳 I need the food (Fridge-to-Table Waste Optimizer)"], key="solo_radio")

        fridge_items = ""
        if "I need the food" in choice_type:
            fridge_items = st.text_input("🧊 (Optional) What leftover ingredients do you have in your fridge? (e.g., eggs, cabbage, bacon):", key="solo_fridge")

        if st.button("✨ Get Final Decision", use_container_width=True, key="btn_solo_final"):
            with st.spinner(f"Analyzing details for '{selected_food}'..."):
                try:
                    client = genai.Client(api_key=api_key)
                    
                    if "I need a place" in choice_type:
                        detail_prompt = (
                            f"The user is at '{user_location}' with a max budget of ${max_budget} and max travel time of {max_walk} mins. "
                            f"They selected '{selected_food}'. "
                            f"Recommend 1 specific, real restaurant or cafe near '{user_location}' that satisfies these exact constraints. "
                            f"Include the restaurant name, why it fits their friction matrix, and their signature dish."
                        )
                    else:
                        detail_prompt = (
                            f"The user selected '{selected_food}' and wants to cook at home. "
                            f"Their available fridge items: '{fridge_items if fridge_items else 'None specified'}'. "
                            f"Provide a quick 3-step home recipe, estimate how much money they save compared to eating out (under ${max_budget}), "
                            f"and a quick sustainability/waste-reduction tip."
                        )
                    
                    res = client.models.generate_content(model="gemini-3.6-flash", contents=detail_prompt)
                    
                    st.markdown("---")
                    st.markdown("### 🎯 Your Custom Recommendation:")
                    st.markdown(res.text)
                    
                    st.markdown("---")
                    if "I need a place" in choice_type:
                        st.link_button("Search Places on Google Maps", f"https://www.google.com/maps/search/{selected_food}+near+{user_location}", use_container_width=True)
                    else:
                        st.link_button("Search Recipe Online", f"https://www.google.com/search?q={selected_food}+recipe", use_container_width=True)
                except Exception as e:
                    st.error(f"Oops! Something went wrong: {e}")

# ==========================================
# Tab 2: 多人匿名模式 (Secret Group Consensus)
# ==========================================
with tab_group:
    st.subheader("👥 Secret Group Consensus (Anonymous Mode)")
    st.markdown("🔒 *Your individual inputs are 100% private. The AI will compute a safe mutual intersection without revealing what anyone specifically wanted or wanted to spend.*")
    
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        member_name = st.text_input("Your Nickname (for session tracking only):", value="Friend 1", key="grp_name")
        my_secret_craving = st.text_input("What do you secretly want to eat?", key="grp_craving")
        my_max_spending = st.slider("Your Personal Budget Limit ($):", 5, 50, max_budget, key="grp_budget")
    with col_g2:
        my_dietary_restriction = st.selectbox("Dietary Note / Restrictions:", ["None", "Vegetarian", "Vegan", "Gluten-Free", "Halal", "Dairy-Free"], key="grp_diet")
        my_travel_limit = st.slider("Your Max Travel Limit (mins):", 5, 30, max_walk, key="grp_travel")

    if st.button("📥 Submit My Secret Preference", use_container_width=True, key="btn_grp_submit"):
        existing = [m for m in st.session_state.group_members if m["name"] == member_name]
        if existing:
            st.session_state.group_members.remove(existing[0])
        
        st.session_state.group_members.append({
            "name": member_name,
            "craving": my_secret_craving,
            "budget": my_max_spending,
            "diet": my_dietary_restriction,
            "travel": my_travel_limit
        })
        st.success(f"✅ {member_name}'s preferences securely locked in! ({len(st.session_state.group_members)} member(s) submitted)")

    if st.session_state.group_members:
        st.write("---")
        st.write(f"📊 **Current Group Status:** {len(st.session_state.group_members)} participant(s) ready.")
        
        if st.button("🚀 Compute Mutual Safe Zone (Run AI Consensus)", use_container_width=True, key="btn_grp_compute"):
            if not api_key:
                st.warning("⚠️ Please configure your GEMINI_API_KEY in Streamlit Secrets.")
            else:
                with st.spinner("Computing safest intersection without exposing individual secrets... 🧠"):
                    try:
                        client = genai.Client(api_key=api_key)
                        group_data_str = str(st.session_state.group_members)
                        consensus_prompt = (
                            f"You are a neutral, highly intelligent group dining mediator. "
                            f"Location: '{user_location}'. "
                            f"Here are the anonymous/secret preferences of group members: {group_data_str}. "
                            f"Please calculate the strict mutual intersection (take the lowest budget constraint among them to ensure nobody overspends, "
                            f"respect all dietary restrictions, and find a common craving ground). "
                            f"Do NOT expose individual choices or secrets. "
                            f"Provide: "
                            f"1. The computed 'Safe Zone' profile (mutual budget limit and shared style). "
                            f"2. ONE specific, real restaurant near '{user_location}' that satisfies everyone safely. "
                            f"3. A polite, warm message to seal the group consensus."
                        )
                        
                        res = client.models.generate_content(model="gemini-3.6-flash", contents=consensus_prompt)
                        
                        st.markdown("---")
                        st.markdown("### 🎯 Mutual Group Recommendation (No Social Friction):")
                        st.markdown(res.text)
                    except Exception as e:
                        st.error(f"Group consensus error: {e}")

st.markdown("---")
st.caption("Powered by Gemini 3.6 Flash | Built for smart, friction-free dining decisions.")
