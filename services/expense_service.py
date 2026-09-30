from repositories import expense_repository

def create_expense(expense):
    df = expense_repository.get_all()
    existing_ids = df["id"].tolist()
    next_id = max(existing_ids) + 1

    new_expense= {
        "id": next_id,
        "date": expense.date,
        "category":expense.category,
        "amount":expense.amount,
        "payment_method": expense.payment_method,
        "description":expense.description,
    }

    return expense_repository.add_expense(new_expense)