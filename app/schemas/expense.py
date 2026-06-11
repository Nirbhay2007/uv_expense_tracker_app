from decimal import Decimal

from pydantic import BaseModel

from app.enums.expense_category import ExpenseCategory


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