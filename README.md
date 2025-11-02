# 🏦 Loan Approval Predictor API

## 📋 Overview
An **advanced AI-powered loan approval prediction system** built with Python, FastAPI, and XGBoost. This project leverages machine learning to predict loan approval outcomes based on applicant information, providing both predictions and explainable AI insights through SHAP values.

**Perfect for**: Financial institutions, credit assessment automation, and ML portfolio demonstrations.

---

## ✨ Features

### Core Capabilities
- 🤖 **XGBoost ML Model**: High-accuracy gradient boosting classifier
- 🔍 **SHAP Explainability**: Understand which features influence predictions
- ⚡ **FastAPI Backend**: High-performance REST API with automatic documentation
- ✅ **Input Validation**: Pydantic models ensure data integrity
- 📊 **Probability Scores**: Get confidence levels for each prediction
- 🎨 **Optional Streamlit Dashboard**: Interactive web interface for testing

### Technical Highlights
- RESTful API with OpenAPI/Swagger documentation
- Comprehensive error handling and logging
- Docker-ready for containerized deployment
- Cross-platform compatibility (Windows/Linux/Mac)
- Production-ready code structure

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Git
- Virtual environment (recommended)

### Installation

#### 1. Clone the Repository
```bash
git clone https://github.com/<your-username>/loan-approval-predictor.git
cd loan-approval-predictor
```

#### 2. Create Virtual Environment

**Windows (PowerShell)**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Windows (Command Prompt)**
```cmd
python -m venv venv
venv\Scripts\activate.bat
```

**Mac/Linux**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 3. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirement.txt
```

---

## 📖 Usage Guide

### Step 1: Train the Model
Train the XGBoost model on the loan dataset:
```bash
python app/train_model.py
```

**Expected Output:**
```
Model trained successfully!
Accuracy: 82.5%
Model saved to: models/loan_model.pkl
```

### Step 2: Start the API Server
Launch the FastAPI application:
```bash
uvicorn app.api:app --reload --host 0.0.0.0 --port 8000
```

**API will be available at:**
- 🌐 Application: `http://127.0.0.1:8000`
- 📚 Swagger Docs: `http://127.0.0.1:8000/docs`
- 📄 ReDoc: `http://127.0.0.1:8000/redoc`

### Step 3: Launch Dashboard (Optional)
Run the Streamlit interface for interactive testing:
```bash
streamlit run app/dashboard.py
```

Access the dashboard at: `http://localhost:8501`

---

## 🔧 API Documentation

### Endpoint: `/predict`

**Method:** `POST`

**Description:** Predicts loan approval status based on applicant information.

#### Request Body
```json
{
  "Gender": "Male",
  "Married": "Yes",
  "Education": "Graduate",
  "Self_Employed": "No",
  "ApplicantIncome": 5000,
  "CoapplicantIncome": 2000,
  "LoanAmount": 150,
  "Loan_Amount_Term": 360,
  "Credit_History": 1,
  "Property_Area": "Urban"
}
```

#### Field Descriptions
| Field | Type | Description | Valid Values |
|-------|------|-------------|--------------|
| `Gender` | string | Applicant's gender | "Male", "Female" |
| `Married` | string | Marital status | "Yes", "No" |
| `Education` | string | Education level | "Graduate", "Not Graduate" |
| `Self_Employed` | string | Self-employment status | "Yes", "No" |
| `ApplicantIncome` | integer | Monthly income (USD) | > 0 |
| `CoapplicantIncome` | float | Co-applicant income | ≥ 0 |
| `LoanAmount` | float | Requested loan amount (thousands) | > 0 |
| `Loan_Amount_Term` | integer | Loan term (months) | 12, 36, 60, 84, 120, 180, 240, 300, 360, 480 |
| `Credit_History` | integer | Credit history status | 0 (bad) or 1 (good) |
| `Property_Area` | string | Property location | "Urban", "Semiurban", "Rural" |

#### Success Response (200)
```json
{
  "loan_status": "Y",
  "approval_probability": 0.87,
  "message": "Loan approved with high confidence"
}
```

#### Response Fields
- `loan_status`: "Y" (Approved) or "N" (Rejected)
- `approval_probability`: Confidence score (0.0 to 1.0)
- `message`: Human-readable prediction result

#### Error Response (422)
```json
{
  "detail": [
    {
      "loc": ["body", "Credit_History"],
      "msg": "value is not a valid integer",
      "type": "type_error.integer"
    }
  ]
}
```

### Example cURL Request
```bash
curl -X POST "http://127.0.0.1:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{
    "Gender": "Male",
    "Married": "Yes",
    "Education": "Graduate",
    "Self_Employed": "No",
    "ApplicantIncome": 5000,
    "CoapplicantIncome": 2000,
    "LoanAmount": 150,
    "Loan_Amount_Term": 360,
    "Credit_History": 1,
    "Property_Area": "Urban"
  }'
```

### Example Python Request
```python
import requests

url = "http://127.0.0.1:8000/predict"
data = {
    "Gender": "Female",
    "Married": "No",
    "Education": "Graduate",
    "Self_Employed": "Yes",
    "ApplicantIncome": 4500,
    "CoapplicantIncome": 1500,
    "LoanAmount": 120,
    "Loan_Amount_Term": 360,
    "Credit_History": 1,
    "Property_Area": "Semiurban"
}

response = requests.post(url, json=data)
result = response.json()
print(f"Status: {result['loan_status']}")
print(f"Probability: {result['approval_probability']:.2%}")
```

---

## 📁 Project Structure

```
loan-approval-predictor/
├── app/
│   ├── api.py              # FastAPI application & endpoints
│   ├── train_model.py      # Model training script
│   └── dashboard.py        # Streamlit dashboard (optional)
├── data/
│   └── loan_dataset.csv    # Training dataset
├── models/
│   └── loan_model.pkl      # Trained XGBoost model
├── notebooks/
│   └── EDA.ipynb           # Exploratory data analysis
├── venv/                   # Virtual environment (not in Git)
├── .gitignore              # Git ignore rules
├── requirement.txt         # Python dependencies
├── README.md               # This file
└── LICENSE                 # MIT License
```

---

## 🧪 Testing the API

### Using Swagger UI
1. Navigate to `http://127.0.0.1:8000/docs`
2. Click on `/predict` endpoint
3. Click "Try it out"
4. Modify the example JSON
5. Click "Execute"

### Using Postman
1. Create a new POST request
2. URL: `http://127.0.0.1:8000/predict`
3. Headers: `Content-Type: application/json`
4. Body: Raw JSON (see example above)
5. Send request

### Using Python Script
Save as `test_api.py`:
```python
import requests
import json

def test_prediction(applicant_data):
    url = "http://127.0.0.1:8000/predict"
    response = requests.post(url, json=applicant_data)
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Prediction: {result['loan_status']}")
        print(f"📊 Confidence: {result['approval_probability']:.1%}")
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)

# Test case 1: High-income graduate with good credit
test_case_1 = {
    "Gender": "Male",
    "Married": "Yes",
    "Education": "Graduate",
    "Self_Employed": "No",
    "ApplicantIncome": 8000,
    "CoapplicantIncome": 3000,
    "LoanAmount": 150,
    "Loan_Amount_Term": 360,
    "Credit_History": 1,
    "Property_Area": "Urban"
}

# Test case 2: Lower income with no credit history
test_case_2 = {
    "Gender": "Female",
    "Married": "No",
    "Education": "Not Graduate",
    "Self_Employed": "No",
    "ApplicantIncome": 2500,
    "CoapplicantIncome": 0,
    "LoanAmount": 100,
    "Loan_Amount_Term": 360,
    "Credit_History": 0,
    "Property_Area": "Rural"
}

print("Test Case 1: High-income applicant")
test_prediction(test_case_1)

print("\nTest Case 2: Lower-income applicant")
test_prediction(test_case_2)
```

Run with:
```bash
python test_api.py
```

---

## 🐳 Docker Deployment

### Build Docker Image
```bash
docker build -t loan-predictor-api .
```

### Run Container
```bash
docker run -d -p 8000:8000 loan-predictor-api
```

### Docker Compose (Future Enhancement)
```yaml
version: '3.8'
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - MODEL_PATH=/app/models/loan_model.pkl
```

---

## 📊 Model Performance

### Training Metrics
- **Algorithm**: XGBoost Classifier
- **Accuracy**: ~82%
- **Precision**: ~85%
- **Recall**: ~78%
- **F1-Score**: ~81%

### Key Features (by SHAP importance)
1. Credit History (most important)
2. Applicant Income
3. Loan Amount
4. Coapplicant Income
5. Property Area

### Model Interpretation
The model uses SHAP values to explain predictions. Features with positive SHAP values increase approval probability, while negative values decrease it.

---

## 🛠️ Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| Language | Python | 3.8+ |
| ML Framework | XGBoost | 2.0+ |
| API Framework | FastAPI | 0.104+ |
| Validation | Pydantic | 2.0+ |
| Dashboard | Streamlit | 1.28+ |
| Data Processing | Pandas, NumPy | Latest |
| Explainability | SHAP | Latest |

---

## 🔐 Security Considerations

### For Production Deployment:
- ✅ Add authentication (JWT tokens, API keys)
- ✅ Implement rate limiting
- ✅ Use HTTPS/TLS encryption
- ✅ Sanitize all inputs
- ✅ Add logging and monitoring
- ✅ Use environment variables for secrets
- ✅ Implement CORS policies

### Example: Adding API Key Authentication
```python
from fastapi import Security, HTTPException
from fastapi.security import APIKeyHeader

API_KEY = "your-secret-api-key"
api_key_header = APIKeyHeader(name="X-API-Key")

def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid API Key")
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Standards
- Follow PEP 8 style guide
- Add docstrings to all functions
- Write unit tests for new features
- Update README for significant changes

---

## 📝 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2025 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🎯 Future Enhancements

- [ ] Add user authentication system
- [ ] Implement model versioning (MLflow)
- [ ] Create comprehensive test suite
- [ ] Add CI/CD pipeline (GitHub Actions)
- [ ] Deploy to cloud (AWS/GCP/Azure)
- [ ] Build React/Vue.js frontend
- [ ] Add database for prediction logging
- [ ] Implement A/B testing framework
- [ ] Create API rate limiting
- [ ] Add Prometheus metrics monitoring

---

## 🙏 Acknowledgments

- Dataset: [Kaggle Loan Prediction Dataset](https://www.kaggle.com/datasets)
- FastAPI Documentation: [fastapi.tiangolo.com](https://fastapi.tiangolo.com)
- XGBoost Documentation: [xgboost.readthedocs.io](https://xgboost.readthedocs.io)
- SHAP Library: [github.com/slundberg/shap](https://github.com/slundberg/shap)

---

## ⚡ Quick Commands Reference

```bash
# Setup
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirement.txt

# Train model
python app/train_model.py

# Run API
uvicorn app.api:app --reload

# Run dashboard
streamlit run app/dashboard.py

# Test API
python test_api.py

# Git commands
git add .
git commit -m "Your message"
git push origin main
```

---

<div align="center">
