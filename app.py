import streamlit as st
import requests
import os
from dotenv import load_dotenv
from PIL import Image

# Load API keys
load_dotenv()
APP_ID = os.getenv("NUTRITIONIX_APP_ID")
API_KEY = os.getenv("NUTRITIONIX_API_KEY")

# --- Streamlit Page Setup ---
st.set_page_config(
    page_title="BiteWise | Nutrition & Calorie Predictor",
    page_icon="🥗",
    layout="centered"
)

# Load logo and display
logo = Image.open("Image/BiteWise white.png")
st.image(logo, use_container_width=False, width=220)

st.markdown(
    """
    <h1 style='text-align: center; color: #F4F4F4;'>BiteWise</h1>
    <h4 style='text-align: center; color: #AAAAAA;'>Your Nutrition and Calories Predictor</h4>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

# --- Functions ---

def get_nutrition_info(food_query):
    url = "https://trackapi.nutritionix.com/v2/natural/nutrients"
    headers = {
        "x-app-id": APP_ID,
        "x-app-key": API_KEY,
        "Content-Type": "application/json"
    }
    data = {"query": food_query, "timezone": "US/Eastern"}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.text}


def get_barcode_info(barcode):
    url = f"https://trackapi.nutritionix.com/v2/search/item?upc={barcode}"
    headers = {
        "x-app-id": APP_ID,
        "x-app-key": API_KEY
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.text}


def display_food_info(food):
    st.markdown(f"### 🍴 {food['food_name'].title()}")
    st.write(f"**Serving Size:** {food['serving_qty']} {food['serving_unit']}")
    st.write(f"**Calories:** {food['nf_calories']} kcal")
    st.write(f"**Protein:** {food['nf_protein']} g")
    st.write(f"**Carbohydrates:** {food['nf_total_carbohydrate']} g")
    st.write(f"**Fat:** {food['nf_total_fat']} g")

    tags = food.get("tags", {})
    if tags:
        tag_list = [v for v in tags.values() if v]
        if tag_list:
            st.markdown("**Wellness Tags:**")
            st.success(", ".join(str(tag) for tag in tag_list))

    st.markdown("---")


# --- Tabs UI ---
tab1, tab2 = st.tabs(["🔤 Text Input", "📦 Barcode Lookup"])

with tab1:
    food_input = st.text_input("🍽️ What did you eat?", placeholder="e.g. 2 boiled eggs and toast")

    if st.button("Analyze", key="analyze_text"):
        if not food_input.strip():
            st.warning("Please enter a food description.")
        else:
            result = get_nutrition_info(food_input)
            if "foods" in result:
                st.success("✅ Nutrition facts:")
                for food in result["foods"]:
                    display_food_info(food)
            else:
                st.error(f"❌ Error: {result.get('error', 'Unable to fetch data.')}")

with tab2:
    barcode_input = st.text_input("📦 Enter Barcode")

    if st.button("Lookup", key="analyze_barcode"):
        if not barcode_input.strip():
            st.warning("Please enter a barcode.")
        else:
            result = get_barcode_info(barcode_input)
            if "foods" in result and result["foods"]:
                st.success("✅ Product Found:")
                display_food_info(result["foods"][0])
            else:
                st.error(f"❌ Error: {result.get('error', 'No product found.')}")

# --- Footer ---
st.markdown("---")
st.markdown("<p style='text-align: center; font-size: 12px; color: gray;'>🔌 Powered by Nutritionix | Built with 💚 using Streamlit</p>", unsafe_allow_html=True)
