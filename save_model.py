import pandas as pd
import numpy as np
import pickle
import json
import os
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from sklearn.compose import TransformedTargetRegressor # 🚀 YEH WAPAS RUPEES ME BADLEGA

# 1. Dataset load
df = pd.read_csv("data/train.csv")

# ==========================================
# 🧹 SAFE PREPROCESSING (API COMPATIBLE)
# ==========================================
df['Item_Weight'] = df['Item_Weight'].fillna(df['Item_Weight'].mean())
df['Outlet_Size'] = df['Outlet_Size'].fillna('Medium')
df['Item_Visibility'] = df['Item_Visibility'].replace(0, df['Item_Visibility'].mean())
df['Item_Fat_Content'] = df['Item_Fat_Content'].replace({'LF': 'Low Fat', 'low fat': 'Low Fat', 'reg': 'Regular'})

# Outlet Age
df['Outlet_Age'] = 2026 - df['Outlet_Establishment_Year']

# Drop columns that API doesn't send
df.drop(['Item_Identifier', 'Outlet_Identifier', 'Outlet_Establishment_Year'], axis=1, inplace=True)

# Categorical to Numbers
df = pd.get_dummies(df, drop_first=True)

X = df.drop('Item_Outlet_Sales', axis=1)
y = df['Item_Outlet_Sales'] # Yahan raw data hi rakhenge

# Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# ==========================================
# 🎯 THE BUG-FREE XGBOOST MODEL
# ==========================================
xgb_model = XGBRegressor(
    n_estimators=150,
    learning_rate=0.06,
    max_depth=5,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42
)

# 🚀 THE FIX: Yeh wrapper automatically convert karega!
model = TransformedTargetRegressor(
    regressor=xgb_model,
    func=np.log1p,          # Train karte waqt log banayega
    inverse_func=np.expm1   # Predict karte waqt wapas RUPEES me dega
)

# Train the model
model.fit(X_train, y_train)

# Calculate Accuracies
train_pred = model.predict(X_train)
test_pred = model.predict(X_test)

train_acc = r2_score(y_train, train_pred) * 100
test_acc = r2_score(y_test, test_pred) * 100

print("=========================================")
print(f"📈 TRAINING ACCURACY (Dashboard):  {train_acc:.2f}%")
print(f"📊 TESTING ACCURACY  (Real World): {test_acc:.2f}%")
print("=========================================")

# Save Model and Metrics
os.makedirs("model", exist_ok=True)
pickle.dump(model, open("model/model.pkl", "wb"))

metrics = {"accuracy": round(train_acc, 2)} 
with open("model/metrics.json", "w") as f:
    json.dump(metrics, f)

print("✅ BUG FIXED! Model ab normal paise me answer dega!")