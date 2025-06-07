# schemas.py
from pydantic import BaseModel

class InsuranceProductBase(BaseModel):
    name_product: str
    price: int
    coverage: str
    risk_level: str
    name_company: str

class InsuranceProductCreate(InsuranceProductBase):
    pass

class InsuranceProductRead(InsuranceProductBase):
    id_product: int

    class Config:
        orm_mode = True

# schemas.py (додай ці класи)
class ClientBase(BaseModel):
    name: str
    surname: str
    years_old: int
    contact_info: str
    destination_country: str

class ClientCreate(ClientBase):
    pass

class ClientRead(ClientBase):
    id: int

    class Config:
        orm_mode = True

# schemas.py (додай ці класи)
from datetime import date

class OrderBase(BaseModel):
    order_date: date
    product_id: int
    total_price: int
    expiration_date: date

class OrderCreate(OrderBase):
    pass

class OrderRead(OrderBase):
    order_id: int

    class Config:
        orm_mode = True


class PaymentBase(BaseModel):
    type_payment: str
    date_payment: date

class PaymentCreate(PaymentBase):
    pass

class PaymentRead(PaymentBase):
    id: int

    class Config:
        orm_mode = True



