from decimal import Decimal

from fastapi import HTTPException

from app.models.expense import ExpenseCategory
from app.repositories.expense_repository import ExpenseRepository
from app.schemas.expense import ExpenseCreate


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
        category: ExpenseCategory | None = None,
        min_amount: Decimal | None = None,
        max_amount: Decimal | None = None,
    ):
        return self.repository.get_all_by_user(
            user_id=user_id,
            category=category,
            min_amount=min_amount,
            max_amount=max_amount,
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