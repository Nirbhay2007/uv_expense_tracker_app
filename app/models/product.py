from decimal import Decimal

from sqlalchemy import Enum, ForeignKey, Numeric, String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.enums.product_category import ProductCategory


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    sku: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
    )

    price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    category: Mapped[ProductCategory] = mapped_column(
        Enum(ProductCategory),
        nullable=False,
    )
