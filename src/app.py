import streamlit as st
import pandas as pd
import numpy as np
import joblib
from pathlib import Path

# 1. Page Configuration
st.set_page_config(page_title="Player Value Predictor", page_icon="⚽", layout="wide")

# 2. Load ML Artifacts
# @st.cache_resource ensures the models are only loaded once and cached in memory
@st.cache_resource
def load_models():
    project_root = Path(__file__).resolve().parents[1]
    preprocessor_path = project_root / "models" / "preprocessor.joblib"
    model_path = project_root / "models" / "xgboost_champion.joblib"

    preprocessor = joblib.load(preprocessor_path)
    model = joblib.load(model_path)
    return preprocessor, model

preprocessor, model = load_models()

# 3. Header
st.title("⚽ Professional Footballer Market Value Predictor")
st.markdown("""
This application uses an advanced **XGBoost Machine Learning model** ($R^2 = 0.8376$) 
to estimate a football player's market value based on their profile, club prestige, and performance statistics.
""")
st.divider()

# 4. User Inputs Section
st.header("Enter Player Data")

# We use columns to create a clean grid layout
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("👤 Player Profile")
    age = st.number_input("Age at Valuation", min_value=15.0, max_value=45.0, value=25.0, step=0.1)
    height = st.number_input("Height (cm)", min_value=150.0, max_value=210.0, value=180.0, step=1.0)
    position = st.selectbox("Position", ["Attack", "Midfield", "Defender", "Goalkeeper"])
    sub_position = st.selectbox("Sub-Position",["Centre-Forward", "Central Midfield", "Centre-Back", "Goalkeeper", "Left Winger", "Right Winger", "Attacking Midfield", "Defensive Midfield", "Right-Back", "Left-Back"])
    foot = st.selectbox("Foot",["right", "left", "both"])
    citizenship = st.text_input("Country of Citizenship", value="France")

with col2:
    st.subheader("🏟️ Club & League Context")
    valuation_year = st.number_input("Valuation Year", min_value=2000, max_value=2030, value=2026, step=1)
    club_id = st.number_input("Current Club ID (Transfermarkt)", min_value=1, value=583, step=1) # 583 is PSG
    country_name = st.text_input("League Country", value="France")
    is_major_league = st.selectbox("Is Major National League?", ["True", "False"])

with col3:
    st.subheader("📈 Recent Form (Last 365 Days)")
    rec_minutes = st.number_input("Minutes Played (365d)", min_value=0.0, value=2500.0, step=90.0)
    rec_goals = st.number_input("Goals (365d)", min_value=0.0, value=15.0, step=1.0)
    rec_assists = st.number_input("Assists (365d)", min_value=0.0, value=5.0, step=1.0)
    rec_yellow = st.number_input("Yellow Cards (365d)", min_value=0.0, value=3.0, step=1.0)
    rec_red = st.number_input("Red Cards (365d)", min_value=0.0, value=0.0, step=1.0)

st.subheader("🏆 Career Pedigree (Lifetime Stats)")
ccol1, ccol2, ccol3, ccol4, ccol5 = st.columns(5)
car_minutes = ccol1.number_input("Career Minutes", min_value=0.0, value=15000.0, step=90.0)
car_goals = ccol2.number_input("Career Goals", min_value=0.0, value=60.0, step=1.0)
car_assists = ccol3.number_input("Career Assists", min_value=0.0, value=25.0, step=1.0)
car_yellow = ccol4.number_input("Career Yellows", min_value=0.0, value=15.0, step=1.0)
car_red = ccol5.number_input("Career Reds", min_value=0.0, value=1.0, step=1.0)

st.divider()

# 5. Prediction Logic & Button
# We use a large, primary button to trigger the calculation
if st.button("🔮 Predict Market Value", use_container_width=True, type="primary"):
    
    # Pack the inputs into a dictionary matching the exact training column names
    input_data = {
        'current_club_id': club_id,
        'position': position,
        'sub_position': sub_position,
        'foot': foot,
        'height_in_cm': height,
        'country_of_citizenship': citizenship,
        'age_at_valuation': age,
        'country_name': country_name,
        'is_major_national_league': is_major_league, # String 'True'/'False' just like our training setup
        'career_minutes_played': car_minutes,
        'career_goals': car_goals,
        'career_assists': car_assists,
        'career_yellow_cards': car_yellow,
        'career_red_cards': car_red,
        'recent_365d_minutes_played': rec_minutes,
        'recent_365d_goals': rec_goals,
        'recent_365d_assists': rec_assists,
        'recent_365d_yellow_cards': rec_yellow,
        'recent_365d_red_cards': rec_red,
        'valuation_year': valuation_year
    }
    
    # Convert dictionary to a 1-row DataFrame
    input_df = pd.DataFrame([input_data])
    
    try:
        # Show a quick loading spinner for UX
        with st.spinner("Calculating valuation..."):
            
            # 1. Apply the Preprocessing Pipeline
            processed_data = preprocessor.transform(input_df)
            
            # 2. Make the Prediction (Returns Log Space)
            log_prediction = model.predict(processed_data)[0]
            
            # 3. Reverse the Log Transformation
            actual_prediction_eur = np.expm1(log_prediction)
        
        # Display the result beautifully!
        st.success("Analysis Complete!")
        
        # Use columns to center the big metric number
        _, center_col, _ = st.columns([1, 2, 1])
        with center_col:
            st.metric(
                label="Estimated Market Value", 
                value=f"€ {actual_prediction_eur:,.0f}"
            )
        
        # Add a quick disclaimer referencing your error analysis
        st.info(f"💡 **Model Insight:** Based on our Test Set, the model has an $R^2$ of 0.8376 with a Mean Absolute Error of ~€2.16M. Remember that real market values are also influenced by contract length, injuries, and marketing potential!")
        
    except Exception as e:
        st.error(f"An error occurred during calculation. Please check your inputs. Error details: {e}")