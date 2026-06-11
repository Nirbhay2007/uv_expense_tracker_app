from decimal import Decimal

from pydantic import BaseModel

from app.models.expense import ExpenseCategory


class ExpenseCreate(BaseModel):
    description: str
    amount: Decimal
    category: ExpenseCategory


class ExpenseResponse(BaseModel):
    id: int
    description: str
    amount: Decimal
    category: ExpenseCategory

    model_config = {
        "from_attributes": True
    }


class ExpenseSummary(BaseModel):
    total_spent: Decimal
    expense_count: int
    average_expense: Decimal