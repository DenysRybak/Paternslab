from sqlalchemy.orm import Session
from models import Client, InsuranceProduct, Order, Payment

# Репозиторій для клієнтів
class ClientRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, client: Client):
        self.db.add(client)
        self.db.commit()
        return client

    def get_by_id(self, client_id: int):
        return self.db.query(Client).filter(Client.id == client_id).first()

    def get_all(self):
        return self.db.query(Client).all()

# Репозиторій для страхових продуктів

class InsuranceProductRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, product: InsuranceProduct):
        existing = self.db.query(InsuranceProduct).filter(InsuranceProduct.id_product == product.id_product).first()
        if existing:
            print(f"[ℹ️] Продукт з ID {product.id_product} вже існує. Пропускаємо.")
            return existing
        self.db.add(product)
        self.db.commit()
        return product

    def get_by_id(self, product_id: int):
        return self.db.query(InsuranceProduct).filter(InsuranceProduct.id_product == product_id).first()

    def get_all_products(self):
        # Отримуємо всі продукти з бази даних
        return self.db_session.query(InsuranceProduct).all()

    def add_product(self, product):
        self.db_session.add(product)
        self.db_session.commit()

# Репозиторій для замовлень
class OrderRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, order: Order):
        self.db.add(order)
        self.db.commit()
        return order

    def get_by_id(self, order_id: int):
        return self.db.query(Order).filter(Order.id == order_id).first()

    def get_all(self):
        return self.db.query(Order).all()

    def exists(self, order_id: int) -> bool:
        return self.db.query(Order).filter(Order.order_id == order_id).first() is not None


class PaymentRepository:
    def __init__(self, db: Session):
        self.db = db

    def save(self, payment: Payment):
        # Перевіряємо, чи такий payment вже є
        existing_payment = self.db.query(Payment).filter(Payment.payment_id == payment.payment_id).first()
        if existing_payment:
            print(f"[ℹ️] Оплата з ID {payment.payment_id} вже існує. Пропускаємо.")
            return existing_payment
        self.db.add(payment)
        self.db.commit()
        return payment

    def get_by_id(self, payment_id: int):
        return self.db.query(Payment).filter(Payment.payment_id == payment_id).first()

    def get_all(self):
        return self.db.query(Payment).all()
