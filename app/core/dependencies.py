from collections.abc import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.repositories.expense_repository import ExpenseRepository
from app.services.expense_service import ExpenseService


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def get_expense_service(
    db: Session = Depends(get_db),
) -> ExpenseService:
    repository = ExpenseRepository(db)

    return ExpenseService(
        repository
    )