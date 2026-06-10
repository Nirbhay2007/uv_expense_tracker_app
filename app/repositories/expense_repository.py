from decimal import Decimal

from sqlalchemy.orm import Session

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
    ) -> Expense:
        expense = Expense(
            description=description,
            amount=amount,
        )

        self.db.add(expense)
        self.db.commit()
        self.db.refresh(expense)

        return expense

    def get_all(
        self,
    ) -> list[Expense]:
        return self.db.query(Expense).all()

    def get_by_id(
        self,
        expense_id: int,
    ) -> Expense | None:
        return self.db.get(
            Expense,
            expense_id,
        )

    def update(
        self,
        expense: Expense,
        description: str,
        amount: Decimal,
    ) -> Expense:
        expense.description = description
        expense.amount = amount
        self.db.commit()
        self.db.refresh(expense)

        return expense

    def delete(
        self,
        expense: Expense,
    ) -> None:
        self.db.delete(expense)
        self.db.commit()