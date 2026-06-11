from decimal import Decimal

from app.core.database import SessionLocal
from app.models.expense import Expense, ExpenseCategory
from app.models.user import User


def main() -> None:
    with SessionLocal() as session:
        user = session.query(User).first()
        if not user:
            print("No user found in database. Create a user before seeding expenses.")
            return

        expense = Expense(
            description="Coffee",
            amount=Decimal("120.00"),
            user_id=user.id,
            category=ExpenseCategory.FOOD,
        )



        session.add(expense)
        session.commit()

        print("Expense inserted successfully")


if __name__ == "__main__":
    main()