from fastapi import FastAPI
import pandas as pd
from pathlib import Path
from fastapi import FastAPI, HTTPException

BASE_DIR = Path(__file__).resolve().parent
CSV_FILE = BASE_DIR / "sample_expenses.csv"

app= FastAPI(
    title ="Expense API",
    version="1.0.0",
)

@app.get("/")
def root():
    return{
        "message":"Expense API is running"
    }

@app.get("/health")
def health_check():
    return{
        "status":"healthy"
    }


@app.get("/expenses")
def get_expenses():
    df = pd.read_csv(CSV_FILE)
    return df.to_dict(orient = "records")

@app.get("/expenses/{expense_id}")
def get_expenses(expense_id: int):
    df = pd.read_csv(CSV_FILE)
    expense = df[df["id"] == expense_id]

    if expense.empty:
        raise HTTPException(
            status_code = 404,
            detail="Expense not found"
        )
    return expense.iloc[0].to_dict()