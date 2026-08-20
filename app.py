import streamlit as st
from google import genai
import urllib.parse

st.set_page_config(page_title="Smart Dining & Decision Engine", page_icon="🍽️", layout="wide")

# 修正文法：What do you crave for today?
st.title("What do you crave for today? 🍽️")
st.markdown("Your smart local foodie guide and decision engine.")
st.write("---")

api_key = st.secrets.get("GEMINI_API_KEY", "")

# 初始化 Session State
if "group_members" not in st.session_state:
    st.session_state.group_members = []

# ==========================================
# 0. 網頁最上方：全域地址與摩擦力矩陣 (Global Settings & Filters)
# ==========================================
st.subheader("📍 Where are you located & what are your limits?")
col_addr, col_bud, col_walk = st.columns([2, 1, 1])

with col_addr:
    global_address = st.text_input("Your Address, City, or Location:", value="Livingston, NJ")
with col_bud:
    global_budget = st.slider("Max Budget ($)", 5, 50, 20)
with col_walk:
    global_walk = st.slider("Max Travel (mins)", 5, 30, 15)

st.markdown("---")

# ==========================================
# 主畫面：分頁切換（單人模式 vs. 多人匿名模式）
# ==========================================
tab_solo, tab_group = st.tabs(["👤 Solo Decision Hub", "👥 Secret Group Consensus"])

# ==========================================
# Tab 1: 單人模式 (Solo Mode)
# ==========================================
with tab_solo:
    st.subheader("👤 Solo Food & Decision Hub")
    st.markdown("Choose whether you want to go out to a restaurant or cook at home with tailored AI guidance.")

    solo_intent = st.radio("What's your plan?", ["🍴 I want to go out (Find Restaurants)", "🍳 I want to cook at home (Recipe & Shopping Optimizer)"], key="solo_intent_choice")

    st.markdown("---")

    # ------------------------------------------
    # 模式 A：單人出去吃 (Find 3+ Restaurants with Direct Maps Links)
    # ------------------------------------------
    if "go out" in solo_intent:
        st.markdown("### 🍴 Restaurant Finder")
        st.markdown(f"Searching near: **{global_address}** (Max Budget: **${global_budget}**, Max Travel: **{global_walk} mins**)")
        
        solo_craving = st.text_input("💡 What kind of food or vibe are you craving? (e.g., warm soup, tacos, sushi):", key="solo_out_craving")
        
        if st.button("🔍 Find Top Restaurant Options", use_container_width=True, key="btn_find_restaurants"):
            if not api_key:
                st.warning("⚠️ Please configure your GEMINI_API_KEY in Streamlit Secrets.")
            else:
                with st.spinner("Scanning local spots matching your friction matrix... 🍳"):
                    try:
                        client = genai.Client(api_key=api_key)
                        prompt = (
                            f"You are a local foodie guide. The user is at '{global_address}'. "
                            f"Their constraints: max budget ${global_budget}, max travel time {global_walk} mins. "
                            f"They are craving: '{solo_craving}'. "
                            f"Please provide AT LEAST 3 to 5 specific, real restaurants or cafes near '{global_address}' that fit these constraints. "
                            f"For each restaurant, strictly include: "
                            f"1. Exact Restaurant Name. "
                            f"2. Address or Area. "
                            f"3. Their signature dish that matches the craving. "
                            f"4. Why it fits their budget and travel limit. "
                            f"Keep the tone warm, modern, and structured."
                        )
                        response = client.models.generate_content(model="gemini-3.6-flash", contents=prompt)
                        st.markdown("---")
                        st.markdown("### 🌟 Recommended Restaurants for You:")
                        st.markdown(response.text)
                        
                        st.markdown("---")
                        st.write("### 🗺️ Quick Map Navigation:")
                        encoded_query = urllib.parse.quote(f"{solo_craving} restaurant near {global_address}")
                        st.link_button("📍 Open All Options on Google Maps", f"https://www.google.com/maps/search/{encoded_query}", use_container_width=True)
                    except Exception as e:
                        st.error(f"⚠️ AI service is busy right now (503 / High Demand). Please wait a few seconds and try again! Details: {e}")

    # ------------------------------------------
    # 模式 B：單人自煮 (Cook at Home - Two Sub-Modes)
    # ------------------------------------------
    else:
        st.markdown("### 🍳 Cook at Home Optimizer")
        cook_mode = st.radio("Choose your cooking approach:", [
            "🧊 Mode 1: Based on ingredients I already have in my fridge", 
            "🎯 Mode 2: Pick a specific dish I want to make + Get Shopping List & Nearby Markets"
        ], key="cook_mode_choice")
        
        st.markdown("---")

        if "Mode 1" in cook_mode:
            fridge_contents = st.text_input("🧊 What ingredients do you currently have in your fridge? (e.g., eggs, cabbage, bacon, rice):", key="mode1_fridge")
            desired_style = st.text_input("💡 Any specific style or flavor you want to make out of them? (Optional, e.g., Asian style, quick soup):", key="mode1_style")
            
            if st.button("✨ Generate Recipe from My Fridge", use_container_width=True, key="btn_mode1"):
                if not api_key:
                    st.warning("⚠️ Please configure your GEMINI_API_KEY in Streamlit Secrets.")
                else:
                    with st.spinner("Crafting a recipe from your fridge items... 🍳"):
                        try:
                            client = genai.Client(api_key=api_key)
                            prompt = (
                                f"The user is at '{global_address}' and wants to cook at home using what's in their fridge. "
                                f"Fridge ingredients available: '{fridge_contents}'. "
                                f"Desired style/craving: '{desired_style if desired_style else 'Any delicious recipe'}'. "
                                f"Please provide: "
                                f"1. A delicious, quick recipe utilizing these ingredients. "
                                f"2. Useful cooking tips & culinary tricks. "
                                f"3. Estimated money saved compared to eating out (keeping budget under ${global_budget}) and a sustainability/waste-reduction note."
                            )
                            response = client.models.generate_content(model="gemini-3.6-flash", contents=prompt)
                            st.markdown("---")
                            st.markdown("### 🎯 Your Fridge-to-Table Recipe:")
                            st.markdown(response.text)
                            
                            st.markdown("---")
                            st.link_button("Search Recipe Online", f"https://www.google.com/search?q={desired_style}+recipe", use_container_width=True)
                        except Exception as e:
                            st.error(f"⚠️ AI service is busy right now. Please try again in a moment! Details: {e}")

        else:
            target_dish = st.text_input("💡 What specific dish do you want to make? (e.g., Pad Thai, Creamy Carbonara, Beef Stew):", key="mode2_dish")
            my_fridge_inventory = st.text_input("🧊 (Optional) What ingredients do you ALREADY have at home so we can exclude them from the shopping list?:", key="mode2_inventory")
            
            if st.button("🛒 Generate Recipe, Shopping List & Nearby Markets", use_container_width=True, key="btn_mode2"):
                if not api_key:
                    st.warning("⚠️ Please configure your GEMINI_API_KEY in Streamlit Secrets.")
                else:
                    with st.spinner("Generating recipe, customized shopping list, and local markets... 🍳"):
                        try:
                            client = genai.Client(api_key=api_key)
                            prompt = (
                                f"The user is at '{global_address}' and wants to cook '{target_dish}' at home. "
                                f"They ALREADY have these ingredients at home: '{my_fridge_inventory if my_fridge_inventory else 'None'}'. "
                                f"Please provide: "
                                f"1. A clear, easy-to-follow recipe for '{target_dish}'. "
                                f"2. A customized 'Shopping List' containing ONLY the missing ingredients they still need to buy. "
                                f"3. 2-3 specific, real grocery stores or supermarkets near '{global_address}' where they can buy these ingredients. "
                                f"4. Useful cooking tips and estimated money saved compared to dining out (under ${global_budget})."
                            )
                            response = client.models.generate_content(model="gemini-3.6-flash", contents=prompt)
                            st.markdown("---")
                            st.markdown("### 🎯 Recipe, Shopping List & Local Markets:")
                            st.markdown(response.text)
                            
                            st.markdown("---")
                            col_m1, col_m2 = st.columns(2)
                            with col_m1:
                                encoded_grocery = urllib.parse.quote(f"grocery store near {global_address}")
                                st.link_button("Search Grocery Stores on Maps", f"https://www.google.com/maps/search/{encoded_grocery}", use_container_width=True)
                            with col_m2:
                                st.link_button("Search Recipe Online", f"https://www.google.com/search?q={target_dish}+recipe", use_container_width=True)
                        except Exception as e:
                            st.error(f"⚠️ AI service is busy right now. Please try again in a moment! Details: {e}")

# ==========================================
# Tab 2: 多人匿名模式 (Secret Group Consensus)
# ==========================================
with tab_group:
    st.subheader("👥 Secret Group Consensus (Anonymous Mode)")
    st.markdown(f"📍 Current Group Location Context: **{global_address}**")
    st.markdown("🔒 *Your individual inputs are 100% private. The AI will compute a safe mutual intersection without revealing what anyone specifically wanted or wanted to spend.*")
    
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        member_name = st.text_input("Your Nickname (for session tracking only):", value="Friend 1", key="grp_name")
        my_secret_craving = st.text_input("What do you secretly want to eat?", key="grp_craving")
        my_max_spending = st.slider("Your Personal Budget Limit ($):", 5, 50, global_budget, key="grp_budget")
    with col_g2:
        diet_option = st.selectbox("Dietary Note / Restrictions:", ["None", "Vegetarian", "Vegan", "Gluten-Free", "Halal", "Dairy-Free", "Custom (Type below)"], key="grp_diet_select")
        if "Custom" in diet_option:
            my_dietary_restriction = st.text_input("Type your custom dietary note (e.g., nut allergy, no seafood):", key="grp_custom_diet")
        else:
            my_dietary_restriction = diet_option
            
        my_travel_limit = st.slider("Your Max Travel Limit (mins):", 5, 30, global_walk, key="grp_travel")

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
                            f"Location: '{global_address}'. "
                            f"Here are the anonymous/secret preferences of group members: {group_data_str}. "
                            f"Please calculate the strict mutual intersection (take the lowest budget constraint among them to ensure nobody overspends, "
                            f"respect all dietary restrictions including custom notes, and find a common craving ground). "
                            f"Do NOT expose individual choices or secrets. "
                            f"Provide: "
                            f"1. The computed 'Safe Zone' profile (mutual budget limit and shared style). "
                            f"2. ONE specific, real restaurant near '{global_address}' that satisfies everyone safely. "
                            f"3. A polite, warm message to seal the group consensus."
                        )
                        
                        res = client.models.generate_content(model="gemini-3.6-flash", contents=consensus_prompt)
                        
                        st.markdown("---")
                        st.markdown("### 🎯 Mutual Group Recommendation (No Social Friction):")
                        st.markdown(res.text)
                        
                        st.markdown("---")
                        encoded_consensus = urllib.parse.quote(f"restaurant near {global_address}")
                        st.link_button("Search Consensus Spot on Google Maps", f"https://www.google.com/maps/search/{encoded_consensus}", use_container_width=True)
                    except Exception as e:
                        st.error(f"⚠️ AI service is busy right now (503 / High Demand). Please wait a few seconds and try clicking 'Compute Mutual Safe Zone' again! Details: {e}")

st.markdown("---")
st.caption("Powered by Gemini 3.6 Flash | Built for smart, friction-free dining decisions.")
