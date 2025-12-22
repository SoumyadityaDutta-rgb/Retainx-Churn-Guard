# 📊 RETAINX: Smart Churn Predictor & Advisor

**RETAINX** is an advanced analytics and prediction tool designed to help telecom companies reduce customer churn. By leveraging both traditional machine learning techniques (XGBoost, CatBoost) and cutting-edge Large Language Models (Google Gemini), RETAINX not only predicts *who* will leave but also explains *why* and suggests *how* to keep them.

## 🚀 Features

-   **🔮 Smart Churn Prediction**: Uses advanced ML algorithms to assess the likelihood of a customer leaving with high accuracy.
-   **🧠 AI-Powered Insights**: Integrated with **Google Gemini Pro** to provide qualitative analysis and actionable business strategies tailored to specific customer profiles.
-   **📊 Interactive Dashboard**: A user-friendly **Streamlit** web application for uploading datasets and testing individual customer scenarios.
-   **📈 Comprehensive Data Analysis**: Includes a Jupyter Notebook for deep-dive Exploratory Data Analysis (EDA) and model training.
-   **📉 Visual Analytics**: Includes a Power BI report for business intelligence visualization.

## 🛠️ Tech Stack

-   **Language**: Python 3.x
-   **Web Framework**: Streamlit
-   **AI/LLM**: Google Gemini API
-   **Machine Learning**: XGBoost, CatBoost, Scikit-learn
-   **Data Processing**: Pandas, NumPy
-   **Visualization**: Matplotlib, Seaborn, Power BI

## 📂 Project Structure

The project is organized as follows:

```
├── app/
│   └── doc1.py                 # Main Streamlit application script
├── data/
│   └── WA_Fn-UseC_-Telco-Customer-Churn.csv  # Dataset
├── models/
│   ├── churn_model.pkl         # Trained ML Model
│   └── preprocessor.pkl        # Data Preprocessor
├── notebooks/
│   └── RETAINX.ipynb           # EDA and Model Training Notebook
├── .streamlit/
│   └── secrets.toml            # API Keys (Not committed to Git)
├── datathon.pbix               # Power BI Dashboard
├── requirements.txt            # Project Dependencies
├── LICENSE                     # MIT License
└── README.md                   # Project Documentation
```

## ⚡ Installation & Setup

### 1. Clone the repository
```bash
git clone <repository-url>
cd <repository-folder>
```

### 2. Install Dependencies
Ensure you have Python installed. Install the required libraries using the provided `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 3. Configure API Key
This project uses **Google Gemini** for AI insights. You need to set up your API key securely.

1.  Create a file named `secrets.toml` inside the `.streamlit` folder (if it doesn't exist).
2.  Add your API key to the file:
    ```toml
    [general]
    GEMINI_API_KEY = "YOUR_GOOGLE_GEMINI_API_KEY"
    ```
    *(Note: This file is added to `.gitignore` to keep your key safe.)*

## 🖥️ Usage

### Running the Web App
To launch the interactive prediction tool, run the following command from the root directory:

```bash
streamlit run app/doc1.py
```

1.  **Input Customer Details**: Use the sidebar/form to enter specific details about a customer (e.g., Tenure, Contract Type, Monthly Charges).
2.  **Get Predictions**: Click **"Predict Churn & Get Suggestions"**. The app will use the ML model to predict churn probability and Gemini to provide strategic retention suggestions.

### Exploring the Notebook
To view the data analysis and model training process:
1.  Navigate to the `notebooks/` directory.
2.  Open `RETAINX.ipynb` in Jupyter Notebook or Google Colab.

## 📊 Dataset
The project uses the **Telco Customer Churn** dataset, which includes information about:
-   **Customer Demographics**: Gender, Senior Citizen, Partner, Dependents.
-   **Services**: Phone, Internet, Online Security, Streaming, etc.
-   **Account Information**: Tenure, Contract, Payment Method, Monthly/Total Charges.

## 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

1.  Fork the repository.
2.  Create your feature branch (`git checkout -b feature/AmazingFeature`).
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4.  Push to the branch (`git push origin feature/AmazingFeature`).
5.  Open a Pull Request.

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
