from enum import Enum


class ExpenseCategory(
    str,
    Enum,
):
    FOOD = "FOOD"
    TRAVEL = "TRAVEL"
    SHOPPING = "SHOPPING"
    BILLS = "BILLS"
    ENTERTAINMENT = "ENTERTAINMENT"