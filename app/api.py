from fastapi import FastAPI
from pydantic import BaseModel
from app.utils import predict_loan

app = FastAPI(title="Advanced Loan Approval Predictor API")

# Request schema
class LoanRequest(BaseModel):
    Gender: str
    Married: str
    Education: str
    Self_Employed: str
    ApplicantIncome: float
    CoapplicantIncome: float
    LoanAmount: float
    Loan_Amount_Term: float
    Credit_History: int
    Property_Area: str

@app.post("/predict")
def predict(data: LoanRequest):
    result = predict_loan(data.dict())
    return result
