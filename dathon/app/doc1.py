import streamlit as st
import pandas as pd
import joblib
import google.generativeai as genai
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
    /* -------------------------------------------------------------------------
     * PREMIUM DARK GLASSMORPHISM THEME
     * ------------------------------------------------------------------------- */
    
    /* IMPORT FONTS */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    /* GLOBAL THEME */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* App Background - Deep Night Theme */
    .stApp {
        background: linear-gradient(to bottom right, #0F172A, #1E293B);
        color: #E2E8F0;
    }
    
    /* HEADINGS */
    h1, h2, h3 {
        color: #F8FAFC !important;
        font-weight: 700 !important;
    }
    
    /* H1 Gradient Effect */
    h1 {
        background: linear-gradient(to right, #06b6d4, #8b5cf6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
        padding-bottom: 0.5rem;
    }
    
    /* SIDEBAR */
    [data-testid="stSidebar"] {
        background-color: #020617 !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: #E2E8F0 !important;
    }

    /* GLASS CARDS (Generic Containers) */
    /* Note: Since we cannot wrap elements in divs, we style the main block container 
       or specific widget groups if possible. Here we add a subtle glass effect to 
       the main content area to make it pop against the dark background. */
    .block-container {
        background: rgba(30, 41, 59, 0.4);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.05);
        padding: 3rem 2rem !important;
        margin-top: 2rem;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
    }

    /* INPUTS & SELECTBOXES */
    /* Target the inner input elements */
    /* TEXT + SELECT + NUMBER INPUTS */
    .stTextInput input,
    .stNumberInput input,
    .stSelectbox div[data-baseweb="select"] > div {
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: #F8FAFC !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 8px !important;
    }

/* Fix the full number input container (including +/- buttons area) */
    div[data-testid="stNumberInput"] > div {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border-radius: 8px !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }

/* Fix +/- buttons background */
    div[data-testid="stNumberInput"] button {
        background-color: transparent !important;
        color: #F8FAFC !important;
    }
    div[data-testid="stNumberInput"] input {
        background-color: rgba(255, 255, 255, 0.05) !important;
        color: #F8FAFC !important;
    }

    div[data-testid="stNumberInput"] div[data-baseweb="input"] {
        background-color: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 8px !important;
    }

    div[data-testid="stNumberInput"] div {
        background-color: rgba(255, 255, 255, 0.05) !important;
    }

    
    /* Focus States */
    .stTextInput input:focus, 
    .stSelectbox div[data-baseweb="select"] > div:focus-within, 
    .stNumberInput input:focus {
        border-color: #38bdf8 !important;
        box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.2) !important;
    }
    
    /* Dropdown Menu Items */
    ul[data-baseweb="menu"] {
        background-color: #1E293B !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
    }
    
    li[data-baseweb="option"] {
        color: #E2E8F0 !important;
    }
    
    li[data-baseweb="option"]:hover {
        background-color: rgba(255, 255, 255, 0.1) !important;
    }
    
    /* BUTTONS */
    .stButton > button {
        background: linear-gradient(to right, #0ea5e9, #6366f1) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .stButton > button:hover {
        box-shadow: 0 0 15px rgba(99, 102, 241, 0.6);
        transform: translateY(-2px);
    }
    
    .stButton > button:active {
        transform: translateY(0px);
    }
    
    /* TEXT & LABELS */
    .stMarkdown, .stText, p, label {
        color: #E2E8F0 !important;
    }
    
    label {
        font-weight: 600 !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* METRICS & OTHER WIDGETS */
    [data-testid="stMetricValue"] {
        color: #38bdf8 !important;
    }
    
    /* REMOVE DEFAULT STREAMLIT DECORATION */
    header[data-testid="stHeader"] {
        background: transparent !important;
    }
    
    footer {
        visibility: hidden;
    }
    
</style>
""", unsafe_allow_html=True)
# ===============================
# HEADER
# ===============================
st.markdown("""
    <div style="display: flex; justify-content: center; align-items: center; margin-bottom: 2rem;">
        <div style="font-size: 3rem; margin-right: 15px;">🤖</div>
        <h1 style="text-align: center; margin: 0; padding: 0;">RETAINX: ML-based Churn Predictor & Advisor</h1>
    </div>
""", unsafe_allow_html=True)

# Dynamic Greeting
hour = datetime.datetime.now().hour
if 5 <= hour < 12:
    greeting = "Good Morning"
elif 12 <= hour < 18:
    greeting = "Good Afternoon"
else:
    greeting = "Good Evening"

st.markdown(f"""
    <h3 style='text-align: center; color: #94a3b8; font-weight: 400; margin-top: -20px; margin-bottom: 40px; font-style: italic;'>
        {greeting}! Ready to predict customer retention?
    </h3>
""", unsafe_allow_html=True)

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
        
    genai.configure(api_key=api_key)
    llm = genai.GenerativeModel("gemini-2.0-flash-001")
except Exception as e:
    st.error(f"Error configuring Gemini API: {e}")
    st.stop()

# ---------- LOAD ML ARTIFACTS ----------
@st.cache_resource
def load_artifacts():
    try:
        # Construct absolute paths relative to this script
        # app/doc1.py -> parent is app/ -> parent is project root
        base_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(base_dir)
        
        model_path = os.path.join(project_root, "models", "churn_model.pkl")
        preprocessor_path = os.path.join(project_root, "models", "preprocessor.pkl")
        
        if not os.path.exists(model_path):
            st.error(f"Model file not found at: {model_path}")
            return None, None
            
        if not os.path.exists(preprocessor_path):
            st.error(f"Preprocessor file not found at: {preprocessor_path}")
            return None, None

        model = joblib.load(model_path)
        preprocessor = joblib.load(preprocessor_path)
        return model, preprocessor
    except Exception as e:
        st.error(f"Error loading model files: {e}")
        return None, None

model, preprocessor = load_artifacts()

if model is None or preprocessor is None:
    st.stop()

# ---------- FEATURE DEFINITIONS (MUST MATCH TRAINING) ----------
NUMERICAL_FEATURES = ['SeniorCitizen', 'tenure', 'MonthlyCharges', 'TotalCharges']

CATEGORICAL_FEATURES = [
    'gender', 'Partner', 'Dependents',
    'PhoneService', 'MultipleLines', 'InternetService',
    'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport',
    'StreamingTV', 'StreamingMovies', 'Contract',
    'PaperlessBilling', 'PaymentMethod'
]

ALL_FEATURES = NUMERICAL_FEATURES + CATEGORICAL_FEATURES

# ===============================
# MAIN LAYOUT (Split View)
# ===============================
col_left, col_right = st.columns([2, 1], gap="large")

with col_left:
    # ===============================
    # USER INPUT
    # ===============================
    st.markdown("### Customer Details")

    # --- 1. Demographics ---
    st.markdown("#### 👤 Demographics")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        gender = st.selectbox("Gender", ["Male", "Female"])
    with c2:
        senior_citizen = st.selectbox("Senior Citizen", ["No", "Yes"])
    with c3:
        partner = st.selectbox("Partner", ["Yes", "No"])
    with c4:
        dependents = st.selectbox("Dependents", ["Yes", "No"])

    # --- 2. Services ---
    st.markdown("#### 📡 Services")
    c1, c2, c3 = st.columns(3)
    with c1:
        phone_service = st.selectbox("Phone Service", ["Yes", "No"])
    with c2:
        multiple_lines = st.selectbox("Multiple Lines", ["Yes", "No", "No phone service"])
    with c3:
        internet_service = st.selectbox("Internet Service", ["DSL", "Fiber optic", "No"])

    # --- 3. Security & Support ---
    st.markdown("#### 🛡️ Security & Support")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        online_security = st.selectbox("Online Security", ["Yes", "No", "No internet service"])
    with c2:
        online_backup = st.selectbox("Online Backup", ["Yes", "No", "No internet service"])
    with c3:
        device_protection = st.selectbox("Device Protection", ["Yes", "No", "No internet service"])
    with c4:
        tech_support = st.selectbox("Tech Support", ["Yes", "No", "No internet service"])

    # --- 4. Streaming ---
    st.markdown("#### 📺 Streaming")
    c1, c2 = st.columns(2)
    with c1:
        streaming_tv = st.selectbox("Streaming TV", ["Yes", "No", "No internet service"])
    with c2:
        streaming_movies = st.selectbox("Streaming Movies", ["Yes", "No", "No internet service"])

    # --- 5. Account Info ---
    st.markdown("#### 💳 Account Info")
    c1, c2, c3 = st.columns(3)
    with c1:
        contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
    with c2:
        paperless_billing = st.selectbox("Paperless Billing", ["Yes", "No"])
    with c3:
        payment_method = st.selectbox(
            "Payment Method",
            ["Electronic check", "Mailed check", "Bank transfer", "Credit card"]
        )

    # --- 6. Charges ---
    st.markdown("#### 💰 Charges")
    c1, c2, c3 = st.columns(3)
    with c1:
        tenure = st.number_input("Tenure (months)", 0, 72, 8)
    with c2:
        monthly_charges = st.number_input("Monthly Charges", 0.0, 150.0, 67.0)
    with c3:
        total_charges = st.number_input("Total Charges", 0.0, 10000.0, 5999.0)

# Construct user_data dictionary (outside columns for scope access if needed, but variables are available)
user_data = {
    "gender": gender,
    "SeniorCitizen": 1 if senior_citizen == "Yes" else 0,
    "Partner": partner,
    "Dependents": dependents,
    "tenure": tenure,
    "PhoneService": phone_service,
    "MultipleLines": multiple_lines,
    "InternetService": internet_service,
    "OnlineSecurity": online_security,
    "OnlineBackup": online_backup,
    "DeviceProtection": device_protection,
    "TechSupport": tech_support,
    "StreamingTV": streaming_tv,
    "StreamingMovies": streaming_movies,
    "Contract": contract,
    "PaperlessBilling": paperless_billing,
    "PaymentMethod": payment_method,
    "MonthlyCharges": monthly_charges,
    "TotalCharges": total_charges
}

with col_right:
    # ===============================
    # INTELLIGENCE HUB
    # ===============================
    st.markdown("### 🧠 Intelligence Hub")
    
    # Metric Cards
    st.markdown("""
    <div style="background: rgba(255, 255, 255, 0.05); padding: 15px; border-radius: 10px; border: 1px solid rgba(255, 255, 255, 0.1); margin-bottom: 20px;">
        <h4 style="margin: 0; color: #94a3b8; font-size: 0.9rem;">Model Accuracy</h4>
        <p style="margin: 0; font-size: 1.5rem; font-weight: bold; color: #38bdf8;">82.0%</p>
    </div>
    <div style="background: rgba(255, 255, 255, 0.05); padding: 15px; border-radius: 10px; border: 1px solid rgba(255, 255, 255, 0.1); margin-bottom: 20px;">
        <h4 style="margin: 0; color: #94a3b8; font-size: 0.9rem;">Churn Threshold</h4>
        <p style="margin: 0; font-size: 1.5rem; font-weight: bold; color: #8b5cf6;">0.50</p>
    </div>
    """, unsafe_allow_html=True)

    # Key Drivers
    st.markdown("#### 🔑 Key Churn Drivers")
    st.info("1. **Contract Type**: Month-to-month contracts have higher churn.")
    st.info("2. **Tenure**: New customers are more likely to leave.")
    st.info("3. **Internet Service**: Fiber optic users show higher churn rates.")

    # Retention Tip
    st.markdown("#### 💡 Retention Tip")
    st.warning("Offering a 1-year contract discount can reduce churn probability by up to **40%** for new customers.")

user_df = pd.DataFrame([user_data])

# ===============================
# PREDICT + EXPLAIN
# ===============================
if st.button("🔮 Predict Churn & Get Insights"):

    # --- Ensure correct column order ---
    user_df = user_df[ALL_FEATURES]

    # --- ML PREPROCESSING ---
    try:
        X_processed = preprocessor.transform(user_df)

        # --- ML PREDICTION ---
        churn_prob = model.predict_proba(X_processed)[0][1]
        churn_pred = "Yes" if churn_prob >= 0.5 else "No"

        st.markdown("### 📊 Prediction")
        st.write(f"**Churn Prediction:** {churn_pred}")
        st.write(f"**Churn Probability:** {churn_prob*100:.2f}%")

        # --- GEMINI EXPLANATION ---
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
            response = llm.generate_content(prompt)

        st.markdown("### 🧠Explanation & Recommendations")
        st.write(response.text)
    except Exception as e:
        st.error(f"An error occurred during prediction: {e}")





