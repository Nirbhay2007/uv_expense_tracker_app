from decimal import Decimal
from math import ceil

from pydantic import BaseModel, Field

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


class PaginationMeta(BaseModel):
    """Pagination metadata included in paginated responses."""
    page: int
    limit: int
    total: int
    pages: int


class PaginatedExpenseResponse(BaseModel):
    """Paginated list of expenses with metadata."""
    items: list[ExpenseResponse]
    page: int
    limit: int
    total: int
    pages: int

    @classmethod
    def build(
        cls,
        items: list,
        page: int,
        limit: int,
        total: int,
    ) -> "PaginatedExpenseResponse":
        """Factory method to construct a paginated response from raw data."""
        return cls(
            items=[ExpenseResponse.model_validate(item) for item in items],
            page=page,
            limit=limit,
            total=total,
            pages=ceil(total / limit) if limit > 0 else 0,
        )


class ExpenseFilterParams(BaseModel):
    """Query parameters for filtering, searching, and pagination."""
    category: ExpenseCategory | None = None
    min_amount: Decimal | None = None
    max_amount: Decimal | None = None
    search: str | None = None
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=20, ge=1, le=100)


class MonthlyReportResponse(BaseModel):
    """Monthly expense summary with category breakdown."""
    year: int
    month: int
    total_spent: Decimal
    expense_count: int
    average_expense: Decimal
    category_breakdown: dict[str, Decimal]