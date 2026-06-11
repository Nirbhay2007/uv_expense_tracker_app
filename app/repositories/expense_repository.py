from decimal import Decimal

from sqlalchemy.orm import Session

from app.enums.expense_category import ExpenseCategory
from app.models.expense import Expense


class ExpenseRepository:
    def __init__(
        self,
        db: Session,
    ) -> None:
        self.db = db

    def create(
        self,
        description: str,
        amount: Decimal,
        user_id: int,
        category: ExpenseCategory,
    ) -> Expense:
        expense = Expense(
            description=description,
            amount=amount,
            user_id=user_id,
            category=category,
        )

        self.db.add(expense)
        self.db.commit()
        self.db.refresh(expense)

        return expense

    def get_all_by_user(
        self,
        user_id: int,
    ) -> list[Expense]:
        return (
            self.db.query(Expense)
            .filter(Expense.user_id == user_id)
            .all()
        )

    def get_by_id(
        self,
        expense_id: int,
    ) -> Expense | None:
        return self.db.get(
            Expense,
            expense_id,
        )

    def get_by_id_and_user(
        self,
        expense_id: int,
        user_id: int,
    ) -> Expense | None:
        return (
            self.db.query(Expense)
            .filter(
                Expense.id == expense_id,
                Expense.user_id == user_id,
            )
            .first()
        )

    def update(
        self,
        expense: Expense,
        description: str,
        amount: Decimal,
        category: ExpenseCategory,
    ) -> Expense:
        expense.description = description
        expense.amount = amount
        expense.category = category

        self.db.commit()
        self.db.refresh(expense)

        return expense

    def delete(
        self,
        expense: Expense,
    ) -> None:
        self.db.delete(expense)
        self.db.commit()