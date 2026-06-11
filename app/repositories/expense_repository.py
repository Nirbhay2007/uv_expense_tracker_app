from decimal import Decimal

from sqlalchemy import extract, func
from sqlalchemy.orm import Session

from app.models.expense import Expense, ExpenseCategory


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

    def _build_filtered_query(
        self,
        user_id: int,
        category: ExpenseCategory | None = None,
        min_amount: Decimal | None = None,
        max_amount: Decimal | None = None,
        search: str | None = None,
    ):
        """Build a base query with all filters applied.

        This is the single source of truth for filtering logic,
        reused by both get_all_by_user (data) and count_by_user (count).
        """
        query = self.db.query(Expense).filter(Expense.user_id == user_id)

        if category is not None:
            query = query.filter(Expense.category == category)
        if min_amount is not None:
            query = query.filter(Expense.amount >= min_amount)
        if max_amount is not None:
            query = query.filter(Expense.amount <= max_amount)
        if search is not None:
            query = query.filter(
                Expense.description.ilike(f"%{search}%")
            )

        return query

    def get_all_by_user(
        self,
        user_id: int,
        category: ExpenseCategory | None = None,
        min_amount: Decimal | None = None,
        max_amount: Decimal | None = None,
        search: str | None = None,
        offset: int = 0,
        limit: int = 20,
    ) -> list[Expense]:
        """Fetch expenses with filtering, search, and pagination."""
        query = self._build_filtered_query(
            user_id=user_id,
            category=category,
            min_amount=min_amount,
            max_amount=max_amount,
            search=search,
        )

        return query.offset(offset).limit(limit).all()

    def count_by_user(
        self,
        user_id: int,
        category: ExpenseCategory | None = None,
        min_amount: Decimal | None = None,
        max_amount: Decimal | None = None,
        search: str | None = None,
    ) -> int:
        """Count expenses matching the same filters (for pagination metadata)."""
        query = self._build_filtered_query(
            user_id=user_id,
            category=category,
            min_amount=min_amount,
            max_amount=max_amount,
            search=search,
        )

        return query.count()

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

    def get_summary_by_user(
        self,
        user_id: int,
    ) -> dict:
        result = (
            self.db.query(
                func.sum(Expense.amount).label("total_spent"),
                func.count(Expense.id).label("expense_count"),
                func.avg(Expense.amount).label("average_expense"),
            )
            .filter(Expense.user_id == user_id)
            .first()
        )

        return {
            "total_spent": result.total_spent or Decimal("0.0"),
            "expense_count": result.expense_count or 0,
            "average_expense": result.average_expense or Decimal("0.0"),
        }

    def get_category_breakdown_by_user(
        self,
        user_id: int,
    ) -> dict[str, Decimal]:
        results = (
            self.db.query(
                Expense.category,
                func.sum(Expense.amount).label("total"),
            )
            .filter(Expense.user_id == user_id)
            .group_by(Expense.category)
            .all()
        )

        return {
            category.value: (total or Decimal("0.0"))
            for category, total in results
        }

    def get_monthly_summary(
        self,
        user_id: int,
        year: int,
        month: int,
    ) -> dict:
        """Aggregate expense data for a specific month.

        Uses SQLAlchemy extract() so the date filtering is done in the
        database, not in Python.
        """
        result = (
            self.db.query(
                func.sum(Expense.amount).label("total_spent"),
                func.count(Expense.id).label("expense_count"),
                func.avg(Expense.amount).label("average_expense"),
            )
            .filter(
                Expense.user_id == user_id,
                extract("year", Expense.created_at) == year,
                extract("month", Expense.created_at) == month,
            )
            .first()
        )

        return {
            "total_spent": result.total_spent or Decimal("0.0"),
            "expense_count": result.expense_count or 0,
            "average_expense": round(
                result.average_expense or Decimal("0.0"), 2
            ),
        }

    def get_monthly_category_breakdown(
        self,
        user_id: int,
        year: int,
        month: int,
    ) -> dict[str, Decimal]:
        """Per-category totals for a specific month."""
        results = (
            self.db.query(
                Expense.category,
                func.sum(Expense.amount).label("total"),
            )
            .filter(
                Expense.user_id == user_id,
                extract("year", Expense.created_at) == year,
                extract("month", Expense.created_at) == month,
            )
            .group_by(Expense.category)
            .all()
        )

        return {
            category.value: (total or Decimal("0.0"))
            for category, total in results
        }