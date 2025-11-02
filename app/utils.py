import pickle
import numpy as np

# Load model and encoders
model = pickle.load(open("../models/loan_model.pkl", "rb"))
label_encoders = pickle.load(open("../models/label_encoders.pkl", "rb"))
target_encoder = pickle.load(open("../models/target_encoder.pkl", "rb"))

# Preprocess input dict
def preprocess_input(data: dict):
    arr = []
    for key, value in data.items():
        if key in label_encoders:
            le = label_encoders[key]
            arr.append(le.transform([value])[0])
        else:
            arr.append(value)
    return np.array(arr).reshape(1, -1)

# Predict
def predict_loan(data: dict):
    X = preprocess_input(data)
    prob = model.predict_proba(X)[0][1]
    pred = 1 if prob > 0.5 else 0
    status = target_encoder.inverse_transform([pred])[0]
    return {"loan_status": status, "approval_probability": float(prob)}
