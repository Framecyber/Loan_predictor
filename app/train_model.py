import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from xgboost import XGBClassifier
import warnings
import os

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

# Load data (Path relative to project root 'load_predictor')
df = pd.read_csv("data/loan_data.csv")
df = df.dropna()

# Encode categorical features (Added 'Dependents')
categorical_cols = ['Gender', 'Married', 'Education', 'Self_Employed', 'Property_Area', 'Dependents']
label_encoders = {}
for col in categorical_cols:
    if col in df.columns:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        label_encoders[col] = le
    else:
        print(f"Warning: Column '{col}' not found in DataFrame.")


# Encode target
le_target = LabelEncoder()
df['Loan_Status'] = le_target.fit_transform(df['Loan_Status'])

# Split (Dropped 'Loan_ID' from features)
X = df.drop(['Loan_Status', 'Loan_ID'], axis=1)
y = df['Loan_Status']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# --- Ensemble and Tuning Setup ---

# 1. Create pipelines for each model
# Logistic Regression needs scaled data
pipe_lr = Pipeline([
    ('scaler', StandardScaler()),
    ('lr', LogisticRegression(random_state=42, max_iter=1000))
])

# Random Forest
pipe_rf = Pipeline([
    ('rf', RandomForestClassifier(random_state=42))
])

# XGBoost
base_score = y_train.mean()
pipe_xgb = Pipeline([
    ('xgb', XGBClassifier(random_state=42, base_score=base_score))
])

# 2. Create the Voting Classifier
voting_clf = VotingClassifier(
    estimators=[
        ('lr', pipe_lr),
        ('rf', pipe_rf),
        ('xgb', pipe_xgb)
    ],
    voting='soft'  # 'soft' uses predicted probabilities, often better
)

# 3. Define a parameter grid for GridSearchCV
# FIX: Parameters must target the estimator inside the pipeline: 'voting_estimator__pipeline_step__param'
param_grid = {
    'rf__rf__n_estimators': [100, 200],      # RF: targets the 'rf' step inside the 'rf' pipeline
    'xgb__xgb__n_estimators': [100, 200],    # XGB: targets the 'xgb' step inside the 'xgb' pipeline
    'xgb__xgb__max_depth': [4, 6]            # XGB: targets the 'xgb' step inside the 'xgb' pipeline
}

# 4. Create and run the GridSearchCV
print("Starting hyperparameter tuning with GridSearchCV...")
grid_search = GridSearchCV(
    estimator=voting_clf,
    param_grid=param_grid,
    cv=5,  # 5-fold cross-validation
    scoring='accuracy',
    n_jobs=-1, # Use all available CPU cores
    verbose=1  # Show some progress
)

grid_search.fit(X_train, y_train)

print(f"Best parameters found: {grid_search.best_params_}")

# The best model is the one found by grid search
best_model = grid_search.best_estimator_

# Accuracy
print(f"Best Model Accuracy: {best_model.score(X_test, y_test)}")

# Create models directory if it doesn't exist
# This path works when running `python app/train_model.py` from the root
models_dir = "models"
os.makedirs(models_dir, exist_ok=True)

# Save model and encoders
pickle.dump(best_model, open(os.path.join(models_dir, "loan_model.pkl"), "wb"))
pickle.dump(label_encoders, open(os.path.join(models_dir, "label_encoders.pkl"), "wb"))
pickle.dump(le_target, open(os.path.join(models_dir, "target_encoder.pkl"), "wb"))

print(f"Model and encoders saved successfully in {os.path.abspath(models_dir)}")
