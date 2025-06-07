from abc import ABC, abstractmethod
from typing import List
from models import Client, InsuranceProduct, Order, Payment

class IClientRepository(ABC):

    @abstractmethod
    def get_all_clients(self) -> List[Client]:
        pass

    @abstractmethod
    def add_client(self, client: Client) -> None:
        pass

class IInsuranceProductRepository(ABC):

    @abstractmethod
    def get_all_products(self) -> List[InsuranceProduct]:
        pass

    @abstractmethod
    def add_product(self, product: InsuranceProduct) -> None:
        pass

    @abstractmethod
    def filter_by_risk_level(self, level: str) -> List[InsuranceProduct]:
        pass

class IOrderRepository(ABC):

    @abstractmethod
    def get_all_orders(self) -> List[Order]:
        pass

    @abstractmethod
    def add_order(self, order: Order) -> None:
        pass

class IPaymentRepository(ABC):

    @abstractmethod
    def get_all_payments(self) -> List[Payment]:
        pass

    @abstractmethod
    def add_payment(self, payment: Payment) -> None:
        pass
