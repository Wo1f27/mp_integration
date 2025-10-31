from sqlalchemy import String, Boolean, Integer, Float, Text, DateTime, JSON, ForeignKey
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
    date_added: Mapped[DateTime] = mapped_column(DateTime(timezone=False), server_default=func.now())
    status: Mapped[int] = mapped_column(Integer, ForeignKey('statuses.id'))
    partner: Mapped[int] = mapped_column(Integer, ForeignKey('partners.id'))
    total_sum: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    address: Mapped[str] = mapped_column(Text)
    date_ship: Mapped[DateTime] = mapped_column(DateTime(timezone=False))


    order_items: Mapped[list["OrderItem"]] = relationship("OrderItem", back_populates='order')
    retail_order: Mapped["RetailOrder"] = relationship("RetailOrder", back_populates='order')
    order_status: Mapped["Status"] = relationship('Status', back_populates='order')
    order_partner: Mapped["Partner"] = relationship('Partner', back_populates='orders')


class OrderItem(Base):
    __tablename__ = 'order_items'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    order_id: Mapped[int] = mapped_column(Integer, ForeignKey('orders.id'))
    sku: Mapped[int] = mapped_column(Integer, nullable=False)
    qty: Mapped[int] = mapped_column(Integer)
    price: Mapped[int] = mapped_column(Float, default=0.0)

    order: Mapped["Order"] = relationship("Order", back_populates='order_items')


class Status(Base):
    __tablename__ = 'statuses'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    sysname: Mapped[str] = mapped_column(Text, nullable=False)

    order: Mapped["Order"] = relationship('Order', back_populates='order_status')
    retail_order: Mapped["RetailOrder"] = relationship('RetailOrder', back_populates='order_status')


class RetailPartner(Base):
    __tablename__ = 'retail_partners'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)

    retail_order: Mapped[list["RetailOrder"]] = relationship('RetailOrder', back_populates='retail_partner_obj')


class Marketplace(Base):
    __tablename__ = 'marketplaces'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)

    retail_order: Mapped[list["RetailOrder"]] = relationship('RetailOrder', back_populates='marketplace_obj')


class Partner(Base):
    __tablename__ = 'partners'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    date_create: Mapped[DateTime] = mapped_column(DateTime(timezone=False), server_default=func.now())

    orders: Mapped[list["Order"]] = relationship('Order', back_populates='order_partner')
