import streamlit as st
from google import genai
from PIL import Image
import os
from dotenv import load_dotenv

# 1. Page Configuration
st.set_page_config(
    page_title="MicrobiShield AI",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Key Loading
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY or "AapkiRealKey" in GEMINI_API_KEY:
    st.error("⚠️ Setup Error: Please make sure your .env file contains your real Gemini API key!")
    client = None
else:
    # New official way to initialize the client
    client = genai.Client(api_key=GEMINI_API_KEY)

# 3. Application Headings
st.title("🔬 MicrobiShield AI")
st.markdown("### Predictive Microbiology & Foodborne Illness Risk Assessment")
st.markdown("---")

# 4. Interface Columns
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.subheader("📥 Food Matrix Registration")
    
    food_name = st.text_input("What is the name of the food item? (e.g., Biryani)")
    ingredients = st.text_area("List the ingredients (separated by commas):")
    
    processing_method = st.selectbox(
        "How is this food processed/cooked?",
        ["Cooking", "Boiling", "Baking", "BBQ / Grilling", "Fermentation", "Raw / Uncooked"]
    )
    
    uploaded_image = st.file_uploader("Upload an image of the food (Optional):", type=["jpg", "jpeg", "png"])
    
    if uploaded_image:
        image = Image.open(uploaded_image)
        st.image(image, caption="Uploaded Sample Matrix", use_container_width=True)
    else:
        image = None

    submit_button = st.button("Analyze Food Safety Profile", type="primary")

with col2:
    st.subheader("📋 AI Microbiological Assessment")
    
    if submit_button:
        if not food_name or not ingredients:
            st.error("❌ Please fill out both the Food Name and Ingredients fields first.")
        elif client is None:
            st.error("❌ API client not initialized. Check your .env key setup.")
        else:
            with st.spinner("Analyzing nutrient matrix pathways and microbial profiles..."):
                
                prompt = f"""
                You are an expert AI system specializing in Predictive Microbiology, Food Safety, and Quality Assurance.
                Analyze the following food matrix and provide an exhaustive safety assessment.
                
                Food Item: {food_name}
                Ingredients List: {ingredients}
                Processing Method Used: {processing_method}
                
                Provide the analysis strictly under the following markdown headers:
                
                ### 🧫 1. Microbial Growth Susceptibility Matrix
                - List specific ingredients that support pathogen or spoilage growth (e.g., high water activity/protein supporting Campylobacter, Salmonella, Clostridium botulinum, or carbohydrates causing fungal/mould susceptibility).
                - Identify any antimicrobial ingredients present in the list (e.g., specific herbs, spices, acids) and explain if they will effectively scavenge or inhibit growth.
                
                ### 🤢 2. Foodborne Illness Risk & Clinical Symptoms
                - Detail the potential foodborne illnesses (e.g., Salmonellosis, Campylobacteriosis, Shigellosis, Bacillus cereus emetic/diarrheal syndromes) associated with this matrix if mishandled.
                - List the common signs and symptoms for each.
                
                ### ⏳ 3. Kinetic Spoilage Timeline (Room Temperature vs. Optimum Storage)
                - Maximum Safe Room Temperature Window (25°C - 35°C): State exact hours before rapid log-phase microbial multiplication rendering it unsafe.
                - Total Span to Visible Spoilage: Estimated time until organoleptic deterioration (odor, texture, slime, mold).
                
                ### ❄️ 4. Critical Control Points & Preservation Strategy
                - Optimum Storage Temperature & Humidity: Specify exact storage parameters (e.g., refrigeration <4°C or hot holding >60°C) to maximize shelf-life.
                - Super Ingredient Recommendations: Suggest natural preservatives or functional ingredients (e.g., specific organic acids, plant extracts, bacteriocins) that could be incorporated into this specific recipe to actively scavenge or retard targeted microbial pathways.
                """
                
                try:
                    # New direct generation endpoint format
                    if image:
                        response = client.models.generate_content(
                            model='gemini-2.5-flash',
                            contents=[prompt, image]
                        )
                    else:
                        response = client.models.generate_content(
                            model='gemini-2.5-flash',
                            contents=prompt
                        )
                        
                    st.markdown(response.text)
                    
                except Exception as e:
                    st.error(f"An execution error occurred: {e}")
    else:
        st.info("💡 Fill out the registration form details on the left, then click 'Analyze' to view your generated data sheet.")