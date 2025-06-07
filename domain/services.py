from models import Client, InsuranceProduct, Order, Payment
from interfaces.repository_interface import IClientRepository, IInsuranceProductRepository, IOrderRepository, IPaymentRepository
from typing import List

class ClientService:
    def __init__(self, client_repo: IClientRepository):
        self.client_repo = client_repo

    def get_all_clients(self) -> List[Client]:
        return self.client_repo.get_all_clients()

    def add_client(self, client: Client):
        self.client_repo.add_client(client)


class ProductService:
    def __init__(self, product_repo: IInsuranceProductRepository):
        self.product_repo = product_repo

    def get_all_products(self) -> List[InsuranceProduct]:
        return self.product_repo.get_all_products()

    def add_product(self, product: InsuranceProduct):
        self.product_repo.add_product(product)

    def filter_by_risk_level(self, level: str) -> List[InsuranceProduct]:
        return self.product_repo.filter_by_risk_level(level)


class OrderService:
    def __init__(self, order_repo: IOrderRepository):
        self.order_repo = order_repo

    def get_all_orders(self) -> List[Order]:
        return self.order_repo.get_all_orders()

    def add_order(self, order: Order):
        self.order_repo.add_order(order)


class PaymentService:
    def __init__(self, payment_repo: IPaymentRepository):
        self.payment_repo = payment_repo

    def get_all_payments(self) -> List[Payment]:
        return self.payment_repo.get_all_payments()

    def add_payment(self, payment: Payment):
        self.payment_repo.add_payment(payment)
