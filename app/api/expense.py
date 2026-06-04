from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_db
from app.repositories.expense_repository import ExpenseRepository
from app.schemas.expense import ExpenseCreate, ExpenseResponse
from app.services.expense_service import ExpenseService

router = APIRouter(
    prefix="/expenses",
    tags=["Expenses"],
)


@router.get(
    "",
    response_model=list[ExpenseResponse],
)
def get_expenses(
    db: Session = Depends(get_db),
):
    repository = ExpenseRepository(db)

    service = ExpenseService(repository)

    return service.get_expenses()


@router.post(
    "",
    response_model=ExpenseResponse,
)
def create_expense(
    expense: ExpenseCreate,
    db: Session = Depends(get_db),
):
    repository = ExpenseRepository(db)

    service = ExpenseService(repository)

    return service.create_expense(expense)

@router.get(
    "/{expense_id}",
    response_model=ExpenseResponse,
)
def get_expense(
    expense_id: int,
    db: Session = Depends(get_db),
):
    repository = ExpenseRepository(db)

    service = ExpenseService(repository)

    return service.get_expense(
        expense_id
    )


@router.delete(
    "/{expense_id}",
    status_code=204,
)
def delete_expense(
    expense_id: int,
    db: Session = Depends(get_db),
):
    repository = ExpenseRepository(db)

    service = ExpenseService(repository)

    service.delete_expense(
        expense_id
    )

@router.put(
    "/{expense_id}",
    response_model=ExpenseResponse,
)
def update_expense(
    expense_id: int,
    expense: ExpenseCreate,
    db: Session = Depends(get_db),
):
    repository = ExpenseRepository(db)

    service = ExpenseService(repository)

    return service.update_expense(
        expense_id,
        expense,
    )