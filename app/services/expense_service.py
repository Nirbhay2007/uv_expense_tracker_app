from fastapi import HTTPException

from app.core.logger import get_logger
from app.repositories.expense_repository import ExpenseRepository
from app.schemas.expense import ExpenseCreate

logger = get_logger(__name__)


class ExpenseService:
    def __init__(
        self,
        repository: ExpenseRepository,
    ) -> None:
        self.repository = repository

    def create_expense(
        self,
        expense: ExpenseCreate,
    ):
        if expense.amount <= 0:
            raise HTTPException(
                status_code=400,
                detail="Expense amount must be greater than zero",
            )

        logger.info(
            "Creating expense description=%s amount=%s",
            expense.description,
            expense.amount,
        )

        return self.repository.create(
            description=expense.description,
            amount=expense.amount,
        )

    def get_expenses(
        self,
    ):
        logger.info(
            "Fetching all expenses",
        )

        return self.repository.get_all()

    def get_expense(
        self,
        expense_id: int,
    ):
        logger.info(
            "Fetching expense id=%s",
            expense_id,
        )

        expense = self.repository.get_by_id(
            expense_id,
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
    ):
        logger.info(
            "Updating expense id=%s",
            expense_id,
        )

        expense = self.repository.get_by_id(
            expense_id,
        )

        if expense is None:
            raise HTTPException(
                status_code=404,
                detail="Expense not found",
            )

        if expense_data.amount <= 0:
            raise HTTPException(
                status_code=400,
                detail="Expense amount must be greater than zero",
            )

        return self.repository.update(
            expense=expense,
            description=expense_data.description,
            amount=expense_data.amount,
        )

    def delete_expense(
        self,
        expense_id: int,
    ) -> None:
        logger.info(
            "Deleting expense id=%s",
            expense_id,
        )

        expense = self.repository.get_by_id(
            expense_id,
        )

        if expense is None:
            raise HTTPException(
                status_code=404,
                detail="Expense not found",
            )

        self.repository.delete(
            expense,
        )