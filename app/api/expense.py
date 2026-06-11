from decimal import Decimal

from fastapi import APIRouter, Depends, Query

from app.core.auth import get_current_user
from app.core.dependencies import get_expense_service
from app.models.expense import ExpenseCategory
from app.schemas.expense import (
    ExpenseCreate,
    ExpenseFilterParams,
    ExpenseResponse,
    ExpenseSummary,
    MonthlyReportResponse,
    PaginatedExpenseResponse,
)
from app.services.expense_service import ExpenseService

router = APIRouter(
    prefix="/expenses",
    tags=["Expenses"],
    dependencies=[
        Depends(get_current_user),
    ],
)


@router.get(
    "",
    response_model=PaginatedExpenseResponse,
)
def get_expenses(
    category: ExpenseCategory | None = None,
    min_amount: Decimal | None = None,
    max_amount: Decimal | None = None,
    search: str | None = None,
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
    current_user=Depends(get_current_user),
    service: ExpenseService = Depends(get_expense_service),
):
    filters = ExpenseFilterParams(
        category=category,
        min_amount=min_amount,
        max_amount=max_amount,
        search=search,
        page=page,
        limit=limit,
    )

    return service.get_expenses(
        user_id=current_user.id,
        filters=filters,
    )


@router.get(
    "/summary",
    response_model=ExpenseSummary,
)
def get_expense_summary(
    current_user=Depends(get_current_user),
    service: ExpenseService = Depends(get_expense_service),
):
    return service.get_expense_summary(
        current_user.id,
    )


@router.get(
    "/category-summary",
    response_model=dict[str, Decimal],
)
def get_category_breakdown(
    current_user=Depends(get_current_user),
    service: ExpenseService = Depends(get_expense_service),
):
    return service.get_category_breakdown(
        current_user.id,
    )


@router.get(
    "/monthly-summary",
    response_model=MonthlyReportResponse,
)
def get_monthly_summary(
    year: int = Query(..., ge=1900, le=2100),
    month: int = Query(..., ge=1, le=12),
    current_user=Depends(get_current_user),
    service: ExpenseService = Depends(get_expense_service),
):
    return service.get_monthly_report(
        user_id=current_user.id,
        year=year,
        month=month,
    )


@router.post(
    "",
    response_model=ExpenseResponse,
)
def create_expense(
    expense: ExpenseCreate,
    current_user=Depends(get_current_user),
    service: ExpenseService = Depends(get_expense_service),
):
    return service.create_expense(
        expense,
        current_user.id,
    )


@router.get(
    "/{expense_id}",
    response_model=ExpenseResponse,
)
def get_expense(
    expense_id: int,
    current_user=Depends(get_current_user),
    service: ExpenseService = Depends(get_expense_service),
):
    return service.get_expense(
        expense_id,
        current_user.id,
    )


@router.put(
    "/{expense_id}",
    response_model=ExpenseResponse,
)
def update_expense(
    expense_id: int,
    expense: ExpenseCreate,
    current_user=Depends(get_current_user),
    service: ExpenseService = Depends(get_expense_service),
):
    return service.update_expense(
        expense_id,
        expense,
        current_user.id,
    )


@router.delete(
    "/{expense_id}",
    status_code=204,
)
def delete_expense(
    expense_id: int,
    current_user=Depends(get_current_user),
    service: ExpenseService = Depends(get_expense_service),
):
    service.delete_expense(
        expense_id,
        current_user.id,
    )