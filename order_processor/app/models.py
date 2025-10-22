from sqlalchemy import String, Integer, Float, Text, DateTime, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from .database import Base


class RetailOrder(Base):
    __tablename__ = 'retail_orders'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    date_added: Mapped[DateTime] = mapped_column(DateTime(timezone=False), server_default=func.now())
    comment: Mapped[str] = mapped_column(Text)
    order_id: Mapped[int] = mapped_column(Integer, ForeignKey('orders.id'))
    site_order_id: Mapped[int] = mapped_column(Integer, nullable=False)
    additional_order_id: Mapped[str] = mapped_column(Text)
    market_status: Mapped[str] = mapped_column(Text, nullable=False)
    order_status_id: Mapped[int] = mapped_column(Integer, ForeignKey('statuses.id'))
    marketplace: Mapped[int] = mapped_column(Integer, ForeignKey('marketplaces.id'))
    delivery_kind: Mapped[int] = mapped_column(Integer, default=1)
    retail_partner: Mapped[int] = mapped_column(Integer, ForeignKey('retail_partners.id'))
    supply_id: Mapped[str] = mapped_column(Text)

    order: Mapped["Order"] = relationship("Order", back_populates='retail_order')
    order_status: Mapped["Status"] = relationship("Status", back_populates='retail_order')
    marketplace_obj: Mapped["Marketplace"] = relationship("Marketplace", back_populates='retail_order')
    retail_partner_obj: Mapped["RetailPartner"] = relationship("RetailPartner", back_populates='retail_order')


class Order(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    order_items: Mapped[list["OrderItem"]] = relationship("OrderItem", back_populates='order')
    retail_order: Mapped["RetailOrder"] = relationship("RetailOrder", back_populates='order')


class OrderItem(Base):
    __tablename__ = 'order_items'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    order_id: Mapped[int] = mapped_column(Integer, ForeignKey('orders.id'))

    order: Mapped["Order"] = relationship("Order", back_populates='order_items')
