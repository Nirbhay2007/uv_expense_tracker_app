from enum import Enum


class ProductCategory(str, Enum):
    ELECTRONICS = "ELECTRONICS"
    CLOTHING = "CLOTHING"
    FOOD = "FOOD"
    BOOKS = "BOOKS"
    BEAUTY = "BEAUTY"
    HOUSEHOLD = "HOUSEHOLD"
