from fastapi import APIRouter, Depends

from app.core.dependencies import get_expense_service
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
    service: ExpenseService = Depends(get_expense_service),
):
    return service.get_expenses()


@router.post(
    "",
    response_model=ExpenseResponse,
)
def create_expense(
    expense: ExpenseCreate,
    service: ExpenseService = Depends(get_expense_service),
):
    return service.create_expense(expense)


@router.get(
    "/{expense_id}",
    response_model=ExpenseResponse,
)
def get_expense(
    expense_id: int,
    service: ExpenseService = Depends(get_expense_service),
):
    return service.get_expense(
        expense_id
    )


@router.put(
    "/{expense_id}",
    response_model=ExpenseResponse,
)
def update_expense(
    expense_id: int,
    expense: ExpenseCreate,
    service: ExpenseService = Depends(get_expense_service),
):
    return service.update_expense(
        expense_id,
        expense,
    )


@router.delete(
    "/{expense_id}",
    status_code=204,
)
def delete_expense(
    expense_id: int,
    service: ExpenseService = Depends(get_expense_service),
):
    service.delete_expense(
        expense_id
    )