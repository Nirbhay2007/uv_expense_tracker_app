from collections.abc import Generator

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.repositories.product_repository import ProductRepository
from app.services.product_service import ProductService


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def get_product_service(
    db: Session = Depends(get_db),
) -> ProductService:
    repository = ProductRepository(db)

    return ProductService(
        repository
    )