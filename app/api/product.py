from fastapi import APIRouter, Depends, HTTPException

from app.core.auth import get_current_user
from app.core.dependencies import get_product_service
from app.schemas.product import ProductCreate, ProductResponse
from app.services.product_service import ProductService

router = APIRouter(
    prefix="/products",
    tags=["Products"],
    dependencies=[
        Depends(get_current_user),
    ],
)


@router.get(
    "",
    response_model=list[ProductResponse],
)
def get_products(
    current_user=Depends(get_current_user),
    service: ProductService = Depends(get_product_service),
):
    return service.get_products(
        user_id=current_user.id,
    )


@router.post(
    "",
    response_model=ProductResponse,
)
def create_product(
    product: ProductCreate,
    current_user=Depends(get_current_user),
    service: ProductService = Depends(get_product_service),
):
    try:
        return service.create_product(
            product,
            current_user.id,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.get(
    "/{product_id}",
    response_model=ProductResponse,
)
def get_product(
    product_id: int,
    current_user=Depends(get_current_user),
    service: ProductService = Depends(get_product_service),
):
    return service.get_product(
        product_id,
        current_user.id,
    )


@router.put(
    "/{product_id}",
    response_model=ProductResponse,
)
def update_product(
    product_id: int,
    product: ProductCreate,
    current_user=Depends(get_current_user),
    service: ProductService = Depends(get_product_service),
):
    try:
        return service.update_product(
            product_id,
            product,
            current_user.id,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.delete(
    "/{product_id}",
    status_code=204,
)
def delete_product(
    product_id: int,
    current_user=Depends(get_current_user),
    service: ProductService = Depends(get_product_service),
):
    service.delete_product(
        product_id,
        current_user.id,
    )
