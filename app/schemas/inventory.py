from datetime import datetime

from pydantic import BaseModel

from app.schemas.base import ORMBase


class InventoryItemCreate(BaseModel):
    name: str
    quantity: float
    unit: str | None = None
    metadata: dict[str, str] | None = None


class InventoryItemUpdate(BaseModel):
    quantity: float | None = None
    unit: str | None = None
    metadata: dict[str, str] | None = None


class InventoryItemRead(ORMBase):
    id: int
    name: str
    quantity: float
    unit: str | None
    metadata: dict[str, str] | None
    updated_at: datetime
