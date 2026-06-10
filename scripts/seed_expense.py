from decimal import Decimal

from app.core.database import SessionLocal
from app.models.expense import Expense


def main() -> None:
    with SessionLocal() as session:
        expense = Expense(
            description="Coffee",
            amount=Decimal("120.00"),
        )



        session.add(expense)
        session.commit()

        print("Expense inserted successfully")


if __name__ == "__main__":
    main()