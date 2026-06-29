from decimal import Decimal

from sqlalchemy.orm import Session

from app.enums.product_category import ProductCategory
from app.models.product import Product


class ProductRepository:
    def __init__(
        self,
        db: Session,
    ) -> None:
        self.db = db

    def create(
        self,
        name: str,
        sku: str,
        price: Decimal,
        quantity: int,
        description: str | None,
        user_id: int,
        category: ProductCategory,
    ) -> Product:
        product = Product(
            name=name,
            sku=sku,
            price=price,
            quantity=quantity,
            description=description,
            user_id=user_id,
            category=category,
        )

        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)

        return product

    def get_all_by_user(
        self,
        user_id: int,
    ) -> list[Product]:
        return (
            self.db.query(Product)
            .filter(Product.user_id == user_id)
            .all()
        )

    def get_by_id_and_user(
        self,
        product_id: int,
        user_id: int,
    ) -> Product | None:
        return (
            self.db.query(Product)
            .filter(
                Product.id == product_id,
                Product.user_id == user_id,
            )
            .first()
        )

    def get_by_sku(
        self,
        sku: str,
    ) -> Product | None:
        return (
            self.db.query(Product)
            .filter(Product.sku == sku)
            .first()
        )

    def update(
        self,
        product: Product,
        name: str,
        sku: str,
        price: Decimal,
        quantity: int,
        description: str | None,
        category: ProductCategory,
    ) -> Product:
        product.name = name
        product.sku = sku
        product.price = price
        product.quantity = quantity
        product.description = description
        product.category = category

        self.db.commit()
        self.db.refresh(product)

        return product

    def delete(
        self,
        product: Product,
    ) -> None:
        self.db.delete(product)
        self.db.commit()
