import csv
from itertools import product

from models import Client, InsuranceProduct, Order, Payment
from interfaces.repository_interface import IClientRepository, IInsuranceProductRepository, IOrderRepository, IPaymentRepository
from datetime import datetime

class CSVLoader:
    def __init__(self, client_repo: IClientRepository, product_repo: IInsuranceProductRepository,
                 order_repo: IOrderRepository, payment_repo: IPaymentRepository):
        self.client_repo = client_repo
        self.product_repo = product_repo
        self.order_repo = order_repo
        self.payment_repo = payment_repo

    def load_clients(self, file_path: str):
        """Завантаження клієнтів з CSV"""
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                client = Client(

                    name=row['name'],
                    surname=row['surname'],
                    years_old=int(row['years_old']),
                    contact_info=row['contact_info'],
                    destination_country=row['destination_country']
                )
                self.client_repo.save(client)
                print(f"Клієнт {client.name} {client.surname} доданий.")

    def load_insurance_products(self, file_path: str):
        """Завантаження страхових продуктів з CSV"""
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                product = InsuranceProduct(
                    id_product=row['id_product'],
                    name_product=row['name_product'],
                    price=int(row['price']),
                    coverage=row['coverage'],
                    risk_level=row['risk_level'],
                    name_company=row['name_company']
                )
                try:
                    self.product_repo.save(product)
                    print(f"[✅] Продукт {product.name_product} доданий.")
                except Exception as e:
                    print(f"[❌] Продукт {product.id_product} не доданий. Причина: {e}")

    def load_orders(self, file_path: str):
        """Завантаження замовлень з CSV"""
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if self.order_repo.exists(row['order_id']):
                    print(f"[⚠️] Замовлення {row['order_id']} вже існує. Пропущено.")
                    continue

                order_date = datetime.strptime(row['order_date'], '%Y-%m-%d')
                expiration_date = datetime.strptime(row['expiration_date'], '%Y-%m-%d')
                product_id = row['product']  # <-- тут просто беремо назву як є

                order = Order(
                    order_id=row['order_id'],
                    order_date=order_date,
                    product_id=product_id,
                    total_price=int(row['total_price']),
                    expiration_date=expiration_date
                )

                self.order_repo.save(order)
                print(f"[✅] Замовлення {order.order_id} додано.")

    def load_payments(self, file_path: str):
        """Завантаження оплат з CSV"""
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                date_payment = datetime.strptime(row['date_payment'], '%Y-%m-%d')

                payment = Payment(
                    payment_id=row['payment_id'],
                    type_payment=row['type_payment'],
                    date_payment=date_payment
                )
                self.payment_repo.save(payment)
                print(f"[✅] Оплата {payment.payment_id} додана.")

