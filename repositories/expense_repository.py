from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
CSV_FILE = BASE_DIR/ "sample_expenses.csv"

def get_all():
    return pd.read_csv(CSV_FILE)

def get_by_id(expense_id:int):
    df = pd.read_csv(CSV_FILE)
    print(df.columns)
    print(df["id"].head())
    print(expense_id)
    print(df["id"]==expense_id)
    expense = df[df["id"]==expense_id]

    if expense.empty:
        return None
    return expense.iloc[0].to_dict()

def add_expense(expense):
    df = pd.read_csv(CSV_FILE)
    df.loc[len(df)] = expense
    df.to_csv(CSV_FILE, index=False)
    return expense
