from decimal import Decimal

from pydantic import BaseModel

from app.enums.product_category import ProductCategory


class ProductCreate(BaseModel):
    name: str
    sku: str
    price: Decimal
    quantity: int
    description: str | None = None
    category: ProductCategory


class ProductResponse(BaseModel):
    id: int
    name: str
    sku: str
    price: Decimal
    quantity: int
    description: str | None
    category: ProductCategory

    model_config = {
        "from_attributes": True
    }
