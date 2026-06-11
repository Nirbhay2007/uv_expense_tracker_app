from decimal import Decimal

from fastapi import HTTPException

from app.models.expense import ExpenseCategory
from app.repositories.expense_repository import ExpenseRepository
from app.schemas.expense import (
    ExpenseCreate,
    ExpenseFilterParams,
    PaginatedExpenseResponse,
)


class ExpenseService:
    def __init__(
        self,
        repository: ExpenseRepository,
    ) -> None:
        self.repository = repository

    def create_expense(
        self,
        expense: ExpenseCreate,
        user_id: int,
    ):
        if expense.amount <= 0:
            raise ValueError(
                "Expense amount must be greater than zero"
            )

        return self.repository.create(
            description=expense.description,
            amount=expense.amount,
            user_id=user_id,
            category=expense.category,
        )

    def get_expenses(
        self,
        user_id: int,
        filters: ExpenseFilterParams,
    ) -> PaginatedExpenseResponse:
        """Fetch filtered, searched, and paginated expenses.

        Validates filter inputs, delegates query building to the
        repository, and assembles the paginated response.
        """
        # Validate: min_amount must not exceed max_amount
        if (
            filters.min_amount is not None
            and filters.max_amount is not None
            and filters.min_amount > filters.max_amount
        ):
            raise HTTPException(
                status_code=400,
                detail="min_amount cannot be greater than max_amount",
            )

        # Validate: amounts must be non-negative
        if filters.min_amount is not None and filters.min_amount < 0:
            raise HTTPException(
                status_code=400,
                detail="min_amount must be non-negative",
            )
        if filters.max_amount is not None and filters.max_amount < 0:
            raise HTTPException(
                status_code=400,
                detail="max_amount must be non-negative",
            )

        # Calculate offset from page and limit
        offset = (filters.page - 1) * filters.limit

        # Fetch total count (for pagination metadata)
        total = self.repository.count_by_user(
            user_id=user_id,
            category=filters.category,
            min_amount=filters.min_amount,
            max_amount=filters.max_amount,
            search=filters.search,
        )

        # Fetch paginated results
        items = self.repository.get_all_by_user(
            user_id=user_id,
            category=filters.category,
            min_amount=filters.min_amount,
            max_amount=filters.max_amount,
            search=filters.search,
            offset=offset,
            limit=filters.limit,
        )

        return PaginatedExpenseResponse.build(
            items=items,
            page=filters.page,
            limit=filters.limit,
            total=total,
        )

    def get_expense(
        self,
        expense_id: int,
        user_id: int,
    ):
        expense = self.repository.get_by_id_and_user(
            expense_id,
            user_id,
        )

        if expense is None:
            raise HTTPException(
                status_code=404,
                detail="Expense not found",
            )

        return expense

    def update_expense(
        self,
        expense_id: int,
        expense_data: ExpenseCreate,
        user_id: int,
    ):
        expense = self.repository.get_by_id_and_user(
            expense_id,
            user_id,
        )

        if expense is None:
            raise HTTPException(
                status_code=404,
                detail="Expense not found",
            )

        if expense_data.amount <= 0:
            raise ValueError(
                "Expense amount must be greater than zero"
            )

        return self.repository.update(
            expense=expense,
            description=expense_data.description,
            amount=expense_data.amount,
            category=expense_data.category,
        )

    def delete_expense(
        self,
        expense_id: int,
        user_id: int,
    ) -> None:
        expense = self.repository.get_by_id_and_user(
            expense_id,
            user_id,
        )

        if expense is None:
            raise HTTPException(
                status_code=404,
                detail="Expense not found",
            )

        self.repository.delete(
            expense,
        )

    def get_expense_summary(
        self,
        user_id: int,
    ):
        return self.repository.get_summary_by_user(user_id)

    def get_category_breakdown(
        self,
        user_id: int,
    ):
        return self.repository.get_category_breakdown_by_user(user_id)

    def get_monthly_report(
        self,
        user_id: int,
        year: int,
        month: int,
    ) -> dict:
        """Build a complete monthly report with category breakdown.

        Validates month/year inputs, fetches aggregated data from the
        repository, and assembles the response dict.
        """
        if month < 1 or month > 12:
            raise HTTPException(
                status_code=400,
                detail="month must be between 1 and 12",
            )

        if year < 1900 or year > 2100:
            raise HTTPException(
                status_code=400,
                detail="year must be between 1900 and 2100",
            )

        summary = self.repository.get_monthly_summary(
            user_id=user_id,
            year=year,
            month=month,
        )

        category_breakdown = self.repository.get_monthly_category_breakdown(
            user_id=user_id,
            year=year,
            month=month,
        )

        return {
            "year": year,
            "month": month,
            "total_spent": summary["total_spent"],
            "expense_count": summary["expense_count"],
            "average_expense": summary["average_expense"],
            "category_breakdown": category_breakdown,
        }