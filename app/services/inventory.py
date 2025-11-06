from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import InventoryItem, User
from app.schemas.inventory import InventoryItemCreate, InventoryItemUpdate


def list_items(db: Session, user: User) -> list[InventoryItem]:
    statement = select(InventoryItem).where(InventoryItem.user_id == user.id).order_by(InventoryItem.name.asc())
    return db.execute(statement).scalars().all()


def create_item(db: Session, user: User, payload: InventoryItemCreate) -> InventoryItem:
    item = InventoryItem(
        user_id=user.id,
        name=payload.name,
        quantity=payload.quantity,
        unit=payload.unit,
        metadata=payload.metadata,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def update_item(db: Session, user: User, item_id: int, payload: InventoryItemUpdate) -> InventoryItem:
    item = db.get(InventoryItem, item_id)
    if item is None or item.user_id != user.id:
        raise ValueError("Item not found")
    if payload.quantity is not None:
        item.quantity = payload.quantity
    if payload.unit is not None:
        item.unit = payload.unit
    if payload.metadata is not None:
        item.metadata = payload.metadata
    db.commit()
    db.refresh(item)
    return item


def delete_item(db: Session, user: User, item_id: int) -> None:
    item = db.get(InventoryItem, item_id)
    if item is None or item.user_id != user.id:
        raise ValueError("Item not found")
    db.delete(item)
    db.commit()
