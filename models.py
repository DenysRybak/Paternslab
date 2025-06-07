from database import Base
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship


# Модель для Клієнта
class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    surname = Column(String)
    years_old = Column(Integer)
    contact_info = Column(String)
    destination_country = Column(String)

    def get_info(self):
        return f"Client {self.name} {self.surname}, {self.years_old} years old, Contact: {self.contact_info}, Destination: {self.destination_country}"

# Модель для Страхового Продукту
class InsuranceProduct(Base):
    __tablename__ = 'insurance_products'

    id_product = Column(Integer, primary_key=True, index=True)
    name_product = Column(String)
    price = Column(Integer)
    coverage = Column(String)
    risk_level = Column(String)
    name_company = Column(String)

    def get_product_details(self):
        return f"Product: {self.name_product}, Coverage: {self.coverage}, Price: {self.price}, Risk Level: {self.risk_level}, Company: {self.name_company}"

# Модель для Оформлення Страхівки
class Order(Base):
    __tablename__ = 'orders'

    order_id = Column(Integer, primary_key=True, index=True)
    order_date = Column(Date)
    product_id = Column(Integer)
    total_price = Column(Integer)
    expiration_date = Column(Date)

    def confirm_order(self):
        return f"Order {self.order_id} confirmed for product with ID {self.product_id}."

    def cancel_order(self):
        return f"Order {self.order_id} canceled."

# Модель для Оплати
class Payment(Base):
    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True, index=True)
    type_payment = Column(String)
    date_payment = Column(Date)

    def make_payment(self):
        return f"Payment {self.payment_id} made using {self.type_payment}."

    def cancel_payment(self):
        return f"Payment {self.payment_id} canceled."


