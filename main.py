from fastapi import FastAPI
import pandas as pd
from pathlib import Path
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

class ExpenseCreate(BaseModel):
    date:str
    category: str
    amount: float
    payment_method: str
    description: str

class ExpenseUpdate(BaseModel):
    date:Optional[str] = None
    category: Optional[str] = None
    amount: Optional[float] = None
    payment_method: Optional[str] = None
    description: Optional[str] = None


BASE_DIR = Path(__file__).resolve().parent
CSV_FILE = BASE_DIR / "sample_expenses.csv"

app= FastAPI(
    title ="Expense API",
    version="1.0.0",
)


@app.patch("/expenses/{expense_id}")
def update_expense(expense_id:int,expense:ExpenseUpdate):
    df = pd.read_csv(CSV_FILE)
    expense_index = df.index[df["id"]==expense_id]
    if expense_index.empty:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    updates = expense.model_dump(exclude_unset=True)
    for field, value in updates.items():
        df.loc[expense_index[0],field] = value
    df.to_csv(CSV_FILE,index=False)
    return df.loc[expense_index[0]].to_dict()

@app.delete("/expenses/{expense_id}")
def delete_expense(expense_id:int):
    df=pd.read_csv(CSV_FILE)
    expense_index =  df.index[df["id"]==expense_id]

    if expense_index.empty:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )
    df = df.drop(expense_index)
    df.to_csv(CSV_FILE, index=False)

    return{
        "message":"Expense deleted",
        "expense_id": expense_id
    }


@app.post("/expenses")
def create_expense(expense:ExpenseCreate):
    df = pd.read_csv(CSV_FILE)
    existing_ids = df["id"].tolist()
    next_id = max(existing_ids) + 1
    print(next_id)
    new_expense = {
    "id": next_id,
    "date": expense.date,
    "category": expense.category,
    "amount": expense.amount,
    "payment_method": expense.payment_method,
    "description": expense.description,
    }
    df.loc[len(df)] = new_expense
    df.to_csv(CSV_FILE, index= False)
    return new_expense

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