from fastapi import HTTPException

from app.repositories.product_repository import ProductRepository
from app.schemas.product import ProductCreate


class ProductService:
    def __init__(
        self,
        repository: ProductRepository,
    ) -> None:
        self.repository = repository

    def create_product(
        self,
        product: ProductCreate,
        user_id: int,
    ):
        if product.price <= 0:
            raise ValueError(
                "Product price must be greater than zero"
            )

        if product.quantity < 0:
            raise ValueError(
                "Product quantity must be non-negative"
            )

        existing_product = self.repository.get_by_sku(product.sku)
        if existing_product is not None:
            raise ValueError(
                "Product with this SKU already exists"
            )

        return self.repository.create(
            name=product.name,
            sku=product.sku,
            price=product.price,
            quantity=product.quantity,
            description=product.description,
            user_id=user_id,
            category=product.category,
        )

    def get_products(
        self,
        user_id: int,
    ):
        return self.repository.get_all_by_user(
            user_id=user_id,
        )

    def get_product(
        self,
        product_id: int,
        user_id: int,
    ):
        product = self.repository.get_by_id_and_user(
            product_id,
            user_id,
        )

        if product is None:
            raise HTTPException(
                status_code=404,
                detail="Product not found",
            )

        return product

    def update_product(
        self,
        product_id: int,
        product_data: ProductCreate,
        user_id: int,
    ):
        product = self.repository.get_by_id_and_user(
            product_id,
            user_id,
        )

        if product is None:
            raise HTTPException(
                status_code=404,
                detail="Product not found",
            )

        if product_data.price <= 0:
            raise ValueError(
                "Product price must be greater than zero"
            )

        if product_data.quantity < 0:
            raise ValueError(
                "Product quantity must be non-negative"
            )

        existing_product = self.repository.get_by_sku(product_data.sku)
        if existing_product is not None and existing_product.id != product_id:
            raise ValueError(
                "Product with this SKU already exists"
            )

        return self.repository.update(
            product=product,
            name=product_data.name,
            sku=product_data.sku,
            price=product_data.price,
            quantity=product_data.quantity,
            description=product_data.description,
            category=product_data.category,
        )

    def delete_product(
        self,
        product_id: int,
        user_id: int,
    ) -> None:
        product = self.repository.get_by_id_and_user(
            product_id,
            user_id,
        )

        if product is None:
            raise HTTPException(
                status_code=404,
                detail="Product not found",
            )

        self.repository.delete(
            product,
        )
