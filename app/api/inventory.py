from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.inventory import InventoryItemCreate, InventoryItemRead, InventoryItemUpdate
from app.services import inventory as inventory_service
from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/inventory", tags=["inventory"])


@router.get("/items", response_model=list[InventoryItemRead])
def list_inventory(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return inventory_service.list_items(db, current_user)


@router.post("/items", response_model=InventoryItemRead, status_code=status.HTTP_201_CREATED)
def create_inventory_item(
    payload: InventoryItemCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
) -> InventoryItemRead:
    return inventory_service.create_item(db, current_user, payload)


@router.patch("/items/{item_id}", response_model=InventoryItemRead)
def update_inventory_item(
    item_id: int,
    payload: InventoryItemUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
) -> InventoryItemRead:
    try:
        return inventory_service.update_item(db, current_user, item_id, payload)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_inventory_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
) -> None:
    try:
        inventory_service.delete_item(db, current_user, item_id)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
