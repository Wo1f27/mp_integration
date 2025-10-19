from abc import ABC, abstractmethod
from typing import TypeVar, Any, Generic
from sqlalchemy.orm import Session


T = TypeVar('T')


class BaseRepository(ABC):
    def __init__(self, session: Session):
        self.session = session

    @abstractmethod
    def get(self, id: int) -> T | None:
        pass

    @abstractmethod
    def create(self, entity: T) -> T:
        pass

    @abstractmethod
    def list(self, limit: int = 100, skip: int = 0) -> list[T]:
        pass

    @abstractmethod
    def update(self, id: int, entity_data: dict[str, Any]) -> T | None:
        pass

    @abstractmethod
    def delete(self, id: int) -> bool:
        pass


class BaseProductRepository(ABC):
    def __init__(self, session: Session):
        self.session = session

    @abstractmethod
    def get_by_sku(self, sku: int | str) -> T | None:
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> T | None:
        pass


class BaseOrderRepository(ABC):
    def __init__(self, session: Session):
        self.session = session

    @abstractmethod
    def get_by_id(self, id: int) -> T | None:
        pass

    @abstractmethod
    def get_list_orders(self, limit: int = 100, skip: int = 0):
        pass
