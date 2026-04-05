from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pickle
import pandas as pd
import os
from typing import List, Dict, Any
import hashlib
from pydantic import BaseModel

# ─── MongoDB setup ke andar ek naya collection add karein ───
try:
    from pymongo import MongoClient
    _client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=2000)
    _client.server_info()
    _db = _client["bigmart_db"]
    _col = _db["predictions"]
    _users_col = _db["users"]  # NAYA: Users save karne ke liye
    MONGO_OK = True
    print("✅ MongoDB connected")
except Exception:
    _col = None
    _users_col = None
    MONGO_OK = False
    print("⚠️  MongoDB not available — results won't be persisted")

# ─── FastAPI Init ─────────────────────────────────────────────────────────────
app = FastAPI(
    title="Big Mart Intelligence API",
    description="AI-powered sales prediction, shelf analysis & optimization engine",
    version="2.0.0"
)

# CORS — allow Streamlit frontend to call freely
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Load Model ───────────────────────────────────────────────────────────────
model_path = os.path.join(os.path.dirname(__file__), "../model/model.pkl")
try:
    model = pickle.load(open(model_path, "rb"))
    print("✅ Model loaded successfully")
except FileNotFoundError:
    model = None
    print("⚠️  model.pkl not found — predictions will return dummy values")

# ─── MongoDB (optional) ───────────────────────────────────────────────────────
try:
    from pymongo import MongoClient
    _client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=2000)
    _client.server_info()
    _db = _client["bigmart_db"]
    _col = _db["predictions"]
    MONGO_OK = True
    print("✅ MongoDB connected")
except Exception:
    _col = None
    MONGO_OK = False
    print("⚠️  MongoDB not available — results won't be persisted")


def _save(doc: dict):
    """Best-effort MongoDB save."""
    if MONGO_OK and _col is not None:
        try:
            _col.insert_one(doc)
        except Exception:
            pass


# ─── Helpers ─────────────────────────────────────────────────────────────────

def _prepare(df: pd.DataFrame) -> pd.DataFrame:
    """Add Outlet_Age and align columns to model features."""
    if "Outlet_Age" not in df.columns and "Outlet_Establishment_Year" in df.columns:
        df["Outlet_Age"] = 2026 - df["Outlet_Establishment_Year"]

    if model is None:
        return df

    for col in model.feature_names_in_:
        if col not in df.columns:
            df[col] = 0
    return df[model.feature_names_in_]


def _predict_values(df: pd.DataFrame) -> list:
    """Return predictions; falls back to dummy if model missing."""
    if model is None:
        return [round(float(row.get("Item_MRP", 100)) * 15 + 500, 2) for _, row in df.iterrows()]
    return list(model.predict(df))


def _shelf_analysis(visibility: float, prediction: float):
    if visibility > 0.12 and prediction < 1500:
        return (
            "Underperforming Asset: High visibility but low conversion. Needs quality review.",
            "warning"
        )
    elif visibility < 0.05 and prediction > 2500:
        return (
            "High-Potential Asset: Strong organic demand despite low visibility. Boost shelf space.",
            "upgrade"
        )
    return (
        "Stable Asset: Item attributes and sales are well balanced.",
        "optimal"
    )


def _opt_strategy(prediction: float, mrp: float):
    units = prediction / max(mrp, 1)
    if units < 10:
        return ("Clearance Strategy: Apply 15–20% discount to clear excess inventory.", "discount")
    elif units >= 30:
        return ("Profit Maximize: High demand — keep 100+ units stocked. No discount needed.", "profit")
    return ("Balanced Strategy: Maintain regular stock. Optional 5% promotional discount.", "balanced")


# ─── Endpoints ────────────────────────────────────────────────────────────────

@app.get("/")
def home():
    return {
        "message": "Big Mart Intelligence Backend v2.0 — Running ✅",
        "model_loaded": model is not None,
        "mongo_connected": MONGO_OK
    }


@app.post("/predict")
def predict(data: dict):
    try:
        df = pd.DataFrame([data])
        prepared = _prepare(df.copy())
        prediction = float(_predict_values(prepared)[0])

        visibility = float(data.get("Item_Visibility", 0))
        mrp = float(data.get("Item_MRP", 1))

        shelf_action, shelf_status = _shelf_analysis(visibility, prediction)
        opt_action, opt_status = _opt_strategy(prediction, mrp)

        result = {
            "prediction": round(prediction, 2),
            "shelf_action": shelf_action,
            "shelf_status": shelf_status,
            "opt_action": opt_action,
            "opt_status": opt_status,
        }

        _save({"type": "single", "input": data, **result})
        return result

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/predict_bulk")
def predict_bulk(data_list: List[Dict[str, Any]]):
    if not data_list:
        raise HTTPException(status_code=400, detail="Empty payload.")

    try:
        df = pd.DataFrame(data_list)
        prepared = _prepare(df.copy())
        preds = _predict_values(prepared)
        df["Predicted_Sales"] = [round(float(p), 2) for p in preds]

        shelf_actions, shelf_statuses = [], []
        opt_actions, opt_statuses = [], []

        for _, row in df.iterrows():
            sa, ss = _shelf_analysis(float(row.get("Item_Visibility", 0)), row["Predicted_Sales"])
            oa, os_ = _opt_strategy(row["Predicted_Sales"], float(row.get("Item_MRP", 1)))
            shelf_actions.append(sa)
            shelf_statuses.append(ss)
            opt_actions.append(oa)
            opt_statuses.append(os_)

        df["Shelf_Action"] = shelf_actions
        df["Shelf_Status"] = shelf_statuses
        df["Optimization_Strategy"] = opt_actions
        df["Opt_Status"] = opt_statuses

        _save({"type": "bulk", "count": len(data_list)})

        return {"results": df.to_dict(orient="records"), "count": len(df)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    # ─── Auth Endpoints ────────────────────────────────────────────────────────────

class UserCreds(BaseModel):
    email: str
    password: str

# Password secure rakhne ke liye hash function
def hash_password(password: str):
    return hashlib.sha256(password.encode()).hexdigest()

@app.post("/register")
def register(creds: UserCreds):
    if not MONGO_OK:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    # Check if email already exists
    if _users_col.find_one({"email": creds.email}):
        raise HTTPException(status_code=400, detail="Email is already registered!")
        
    # Save new user
    _users_col.insert_one({
        "email": creds.email,
        "password": hash_password(creds.password)
    })
    return {"message": "Account created successfully!"}

@app.post("/login")
def login(creds: UserCreds):
    if not MONGO_OK:
        raise HTTPException(status_code=500, detail="Database connection failed")
        
    user = _users_col.find_one({"email": creds.email})
    
    # Match email and hashed password
    if not user or user["password"] != hash_password(creds.password):
        raise HTTPException(status_code=401, detail="Invalid Email or Password!")
        
    return {"success": True, "email": user["email"]}
@app.post("/reset-password")
def reset_password(creds: UserCreds):
    if not MONGO_OK:
        raise HTTPException(status_code=500, detail="Database connection failed")
        
    user = _users_col.find_one({"email": creds.email})
    if not user:
        raise HTTPException(status_code=404, detail="Email not found! Please create an account first.")
        
    # Update the password in MongoDB
    _users_col.update_one(
        {"email": creds.email},
        {"$set": {"password": hash_password(creds.password)}}
    )
    return {"message": "Password updated successfully!"}