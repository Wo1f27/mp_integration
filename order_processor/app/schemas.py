from pydantic import BaseModel, validators
from typing import Any
from datetime import datetime


class OrderItemCreate(BaseModel):
    sku: int
    price: float
    qty: int
    order_id: int


class OrderItem(OrderItemCreate):
    id: int


class OrderCreate(BaseModel):
    partner: int
    address: str | None
    date_ship: datetime
    status: int
    total_sum: float


class Order(OrderCreate):
    id: int
    date_added: datetime
