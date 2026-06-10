from decimal import Decimal

from pydantic import BaseModel


class ExpenseCreate(BaseModel):
    description: str
    amount: Decimal


class ExpenseResponse(BaseModel):
    id: int
    description: str
    amount: Decimal

    model_config = {
        "from_attributes": True
    }