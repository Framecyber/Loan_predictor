import streamlit as st
# FIX: Changed 'from app.utils import predict_loan' to a local import
from utils import predict_loan

st.set_page_config(page_title="Loan Approval Predictor", layout="centered")

st.markdown(
    """
    <style>
    .stButton>button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 10px;
    }
    .stSuccess {
        background-color: #d4edda;
        color: #155724;
        border-radius: 8px;
        padding: 15px;
        margin-top: 15px;
        border: 1px solid #c3e6cb;
    }
    .stInfo {
        background-color: #d1ecf1;
        color: #0c5460;
        border-radius: 8px;
        padding: 15px;
        margin-top: 10px;
        border: 1px solid #bee5eb;
    }
    </style>
    """, unsafe_allow_html=True
)

st.title("💰 Advanced Loan Approval Predictor Dashboard")
st.caption("Using an optimized Ensemble Model (Logistic Regression, Random Forest, XGBoost)")

# Input form layout using columns for a cleaner look
col1, col2 = st.columns(2)

with col1:
    Gender = st.selectbox("Gender", ["Male", "Female"])
    Married = st.selectbox("Married", ["Yes", "No"])
    Dependents = st.selectbox("Dependents", ["0", "1", "2", "3+"])
    Education = st.selectbox("Education", ["Graduate", "Not Graduate"])
    Self_Employed = st.selectbox("Self Employed", ["Yes", "No"])
    ApplicantIncome = st.number_input("Applicant Income ($)", 0.0, step=100.0)

with col2:
    CoapplicantIncome = st.number_input("Coapplicant Income ($)", 0.0, step=100.0)
    LoanAmount = st.number_input("Loan Amount ($)", 0.0, step=100.0)
    Loan_Amount_Term = st.number_input("Loan Term (Months)", 0.0, step=1.0)
    Credit_History = st.selectbox("Credit History (1=Good, 0=Bad)", [0.0, 1.0]) # Must be float for consistency
    Property_Area = st.selectbox("Property Area", ["Urban", "Semiurban", "Rural"])


# The 'Predict' button spans across the bottom
st.markdown("---")
if st.button("Predict Loan Approval"):
    # Ensure mandatory fields (like amounts/term) are non-zero before predicting
    if LoanAmount <= 0 or Loan_Amount_Term <= 0 or Credit_History is None:
        st.error("Please fill in Loan Amount, Loan Term, and Credit History accurately.")
    else:
        data = {
            "Gender": Gender,
            "Married": Married,
            "Dependents": Dependents, # Added Dependents
            "Education": Education,
            "Self_Employed": Self_Employed,
            "ApplicantIncome": ApplicantIncome,
            "CoapplicantIncome": CoapplicantIncome,
            "LoanAmount": LoanAmount,
            "Loan_Amount_Term": Loan_Amount_Term,
            "Credit_History": Credit_History,
            "Property_Area": Property_Area
        }
        
        try:
            result = predict_loan(data)
            
            # Display results
            if result['loan_status'] == 'Y':
                st.success(f"✅ Prediction: Loan Approved!")
            else:
                st.error(f"❌ Prediction: Loan Rejected.")

            st.info(f"Confidence (Approval Probability): **{result['approval_probability'] * 100:.2f}%**")
            
        except FileNotFoundError as e:
            st.error(f"Configuration Error: {e}")
        except Exception as e:
            st.error(f"An unexpected error occurred during prediction: {e}")
