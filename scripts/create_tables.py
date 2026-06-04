from app.core.database import Base, engine

# Import models so SQLAlchemy registers them
from app.models.expense import Expense


def main() -> None:
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully")


if __name__ == "__main__":
    main()