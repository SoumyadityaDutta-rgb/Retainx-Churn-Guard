import streamlit as st
import pandas as pd
import joblib
from google import genai   
import os
import datetime

# ===============================
# CONFIG
# ===============================
st.set_page_config(page_title="RETAINX", page_icon="📊", layout="wide")

# ===============================
# CUSTOM CSS INJECTION
# ===============================
st.markdown(""" 
<style>
... (YOUR CSS BLOCK REMAINS EXACTLY SAME — NOT MODIFIED)
</style>
""", unsafe_allow_html=True)

# ===============================
# HEADER
# ===============================
# (UNCHANGED HEADER CODE)

# ---------- GEMINI ----------
try:
    # Access API key from secrets
    if "general" in st.secrets and "GEMINI_API_KEY" in st.secrets["general"]:
        api_key = st.secrets["general"]["GEMINI_API_KEY"]
    elif "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
    else:
        st.error("GEMINI_API_KEY not found in secrets. Please check .streamlit/secrets.toml")
        st.stop()

    # ✅ UPDATED CLIENT INITIALIZATION
    client = genai.Client(api_key=api_key)

except Exception as e:
    st.error(f"Error configuring Gemini API: {e}")
    st.stop()

# ---------- LOAD ML ARTIFACTS ----------
# (UNCHANGED)

# ---------- FEATURE DEFINITIONS ----------
# (UNCHANGED)

# ===============================
# MAIN LAYOUT
# ===============================
# (UNCHANGED FULL UI CODE)

# ===============================
# PREDICT + EXPLAIN
# ===============================
if st.button("🔮 Predict Churn & Get Insights"):

    user_df = user_df[ALL_FEATURES]

    try:
        X_processed = preprocessor.transform(user_df)

        churn_prob = model.predict_proba(X_processed)[0][1]
        churn_pred = "Yes" if churn_prob >= 0.5 else "No"

        st.markdown("### 📊 Prediction")
        st.write(f"**Churn Prediction:** {churn_pred}")
        st.write(f"**Churn Probability:** {churn_prob*100:.2f}%")

        prompt = f"""
        A machine learning churn model has made the following prediction:

        - Churn: {churn_pred}
        - Probability: {churn_prob*100:.2f}%

        Customer details:
        {user_data}

        Your task:
        1. Explain why the model likely predicted this outcome
        2. Identify the most influential factors
        3. Suggest 3 actionable business strategies to reduce churn

        Do NOT re-predict churn.
        Do NOT contradict the model.
        Focus on explanation and recommendations.
        """

        with st.spinner("Generating business insights..."):
            # ✅ UPDATED GENERATE CALL
            response = client.models.generate_content(
                model="gemini-2.5-pro",
                contents=prompt,
            )

        st.markdown("### 🧠Explanation & Recommendations")
        st.write(response.text)

    except Exception as e:
        st.error(f"An error occurred during prediction: {e}")
