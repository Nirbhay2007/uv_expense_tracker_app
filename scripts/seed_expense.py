from app.core.database import SessionLocal
from app.models.expense import Expense


def main() -> None:
    session = SessionLocal()

    expense = Expense(
        description="Coffee",
        amount=120.00,
    )

    session.add(expense)
    session.commit()

    print("Expense inserted successfully")


if __name__ == "__main__":
    main()