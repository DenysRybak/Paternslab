from typing import List
from fastapi import FastAPI, Depends, HTTPException, Request, Form
from sqlalchemy.orm import Session
from sqlalchemy import inspect
import os

from starlette.responses import RedirectResponse

from database import get_db, Base, engine, SessionLocal
from models import Client, InsuranceProduct, Order
from models import Payment as PaymentModel
from repositories import ClientRepository, OrderRepository
from shemas import InsuranceProductCreate, InsuranceProductRead, ClientCreate, ClientRead
from shemas import OrderCreate, OrderRead
from shemas import PaymentRead, PaymentCreate

from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse


# ===== Перевірка наявності БД =====
DATABASE_FILE = "newdatabase.db"
def check_database_exists():
    if not os.path.exists(DATABASE_FILE):
        raise HTTPException(status_code=404, detail="Database file not found")

# ===== Перевірка наявності таблиці =====
def check_table_exists(table_model):
    def checker(db: Session = Depends(get_db)):
        inspector = inspect(db.bind)
        if not inspector.has_table(table_model.__tablename__):
            raise HTTPException(status_code=404, detail=f"Table '{table_model.__tablename__}' not found")
    return checker

# ===== ROUTES =====
app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def read_main(request: Request, db: Session = Depends(get_db)):
    products = db.query(InsuranceProduct).all()
    return templates.TemplateResponse("index.html", {"request": request, "products": products})



# --- Insurance Products ---
@app.get("/insurance_products", response_model=List[InsuranceProductRead])
def get_all_insurance_products(
    db_check: None = Depends(check_database_exists),
    table_check: None = Depends(check_table_exists(InsuranceProduct)),
    db: Session = Depends(get_db)):
    return db.query(InsuranceProduct).all()

@app.get("/insurance_products/{product_id}", response_model=InsuranceProductRead)
def get_insurance_product(
    product_id: int,
    db_check: None = Depends(check_database_exists),
    table_check: None = Depends(check_table_exists(InsuranceProduct)),
    db: Session = Depends(get_db)):
    return db.query(InsuranceProduct).filter(InsuranceProduct.id_product == product_id).first()

@app.post("/insurance_products", response_model=InsuranceProductRead)
def create_insurance_product(
    product: InsuranceProductCreate,
    db_check: None = Depends(check_database_exists),
    table_check: None = Depends(check_table_exists(InsuranceProduct)),
    db: Session = Depends(get_db)):
    db_product = InsuranceProduct(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.put("/insurance_products/{product_id}", response_model=InsuranceProductRead)
def update_insurance_product(
    product_id: int,
    product: InsuranceProductCreate,
    db_check: None = Depends(check_database_exists),
    table_check: None = Depends(check_table_exists(InsuranceProduct)),
    db: Session = Depends(get_db)):
    db_product = db.query(InsuranceProduct).filter(InsuranceProduct.id_product == product_id).first()
    if db_product:
        for key, value in product.dict().items():
            setattr(db_product, key, value)
        db.commit()
        db.refresh(db_product)
        return db_product
    raise HTTPException(status_code=404, detail="Product not found")

@app.delete("/insurance_products/{product_id}")
def delete_insurance_product(
    product_id: int,
    db_check: None = Depends(check_database_exists),
    table_check: None = Depends(check_table_exists(InsuranceProduct)),
    db: Session = Depends(get_db)):
    db_product = db.query(InsuranceProduct).filter(InsuranceProduct.id_product == product_id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
        return {"message": f"Product {product_id} deleted successfully"}
    raise HTTPException(status_code=404, detail="Product not found")

# --- Clients ---
@app.get("/clients")
def get_all_clients(
    db_check: None = Depends(check_database_exists),
    table_check: None = Depends(check_table_exists(Client)),
    db: Session = Depends(get_db)):
    repo = ClientRepository(db)
    return repo.get_all()

@app.get("/clients/{client_id}", response_model=ClientRead)
def get_client(
    client_id: int,
    db_check: None = Depends(check_database_exists),
    table_check: None = Depends(check_table_exists(Client)),
    db: Session = Depends(get_db)):
    db_client = db.query(Client).filter(Client.id == client_id).first()
    if not db_client:
        raise HTTPException(status_code=404, detail="Client not found")
    return db_client

@app.post("/clients", response_model=ClientRead)
def create_client(
    client: ClientCreate,
    db_check: None = Depends(check_database_exists),
    table_check: None = Depends(check_table_exists(Client)),
    db: Session = Depends(get_db)):
    db_client = Client(**client.dict())
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

@app.put("/clients/{client_id}", response_model=ClientRead)
def update_client(
    client_id: int,
    client_data: ClientCreate,
    db_check: None = Depends(check_database_exists),
    table_check: None = Depends(check_table_exists(Client)),
    db: Session = Depends(get_db)):
    db_client = db.query(Client).filter(Client.id == client_id).first()
    if not db_client:
        raise HTTPException(status_code=404, detail="Client not found")
    for key, value in client_data.dict().items():
        setattr(db_client, key, value)
    db.commit()
    db.refresh(db_client)
    return db_client

@app.delete("/clients/{client_id}")
def delete_client(
    client_id: int,
    db_check: None = Depends(check_database_exists),
    table_check: None = Depends(check_table_exists(Client)),
    db: Session = Depends(get_db)):
    db_client = db.query(Client).filter(Client.id == client_id).first()
    if not db_client:
        raise HTTPException(status_code=404, detail="Client not found")
    db.delete(db_client)
    db.commit()
    return {"message": "Client deleted successfully"}

# --- Orders ---
@app.get("/orders/{order_id}", response_model=OrderRead)
def get_order(
    order_id: int,
    db_check: None = Depends(check_database_exists),
    table_check: None = Depends(check_table_exists(Order)),
    db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.order_id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@app.put("/orders/{order_id}", response_model=OrderRead)
def update_order(
    order_id: int,
    order_data: OrderCreate,
    db_check: None = Depends(check_database_exists),
    table_check: None = Depends(check_table_exists(Order)),
    db: Session = Depends(get_db)):
    db_order = db.query(Order).filter(Order.order_id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    for key, value in order_data.dict().items():
        setattr(db_order, key, value)
    db.commit()
    db.refresh(db_order)
    return db_order

@app.delete("/orders/{order_id}")
def delete_order(
    order_id: int,
    db_check: None = Depends(check_database_exists),
    table_check: None = Depends(check_table_exists(Order)),
    db: Session = Depends(get_db)):
    db_order = db.query(Order).filter(Order.order_id == order_id).first()
    if not db_order:
        raise HTTPException(status_code=404, detail="Order not found")
    db.delete(db_order)
    db.commit()
    return {"message": f"Order {order_id} deleted successfully"}

# --- Payments ---
@app.get("/payments", response_model=List[PaymentRead])
def get_payments(
    db_check: None = Depends(check_database_exists),
    table_check: None = Depends(check_table_exists(PaymentModel)),
    db: Session = Depends(get_db)):
    return db.query(PaymentModel).all()

@app.post("/payments", response_model=PaymentRead)
def create_payment(
    payment: PaymentCreate,
    db_check: None = Depends(check_database_exists),
    table_check: None = Depends(check_table_exists(PaymentModel)),
    db: Session = Depends(get_db)):
    db_payment = PaymentModel(**payment.dict())
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment

@app.put("/payments/{payment_id}", response_model=PaymentRead)
def update_payment(
    payment_id: int,
    payment: PaymentCreate,
    db_check: None = Depends(check_database_exists),
    table_check: None = Depends(check_table_exists(PaymentModel)),
    db: Session = Depends(get_db)):
    db_payment = db.query(PaymentModel).filter(PaymentModel.id == payment_id).first()
    if not db_payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    for key, value in payment.dict().items():
        setattr(db_payment, key, value)
    db.commit()
    db.refresh(db_payment)
    return db_payment

@app.delete("/payments/{payment_id}")
def delete_payment(
    payment_id: int,
    db_check: None = Depends(check_database_exists),
    table_check: None = Depends(check_table_exists(PaymentModel)),
    db: Session = Depends(get_db)):
    db_payment = db.query(PaymentModel).filter(PaymentModel.id == payment_id).first()
    if not db_payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    db.delete(db_payment)
    db.commit()
    return {"ok": True}


#      ====== UI/UX PART ======

from fastapi import FastAPI, Request, Form, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse, Response, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError
from starlette.exceptions import HTTPException as StarletteHTTPException

from database import get_db
from models import InsuranceProduct

app = FastAPI()

# ====== UI/UX PART ======
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# ====== ERROR HANDLERS ======

@app.exception_handler(OperationalError)
async def db_exception_handler(request: Request, exc: OperationalError):
    return templates.TemplateResponse("404.html", {"request": request}, status_code=404)

@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        return templates.TemplateResponse("404.html", {"request": request}, status_code=404)
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)

# ====== MAIN MENU ======
@app.get("/", response_class=HTMLResponse)
def show_main_menu(request: Request):
    return templates.TemplateResponse("main_menu.html", {"request": request})

@app.post("/select_table", response_class=HTMLResponse)
def select_table(request: Request, table_name: str = Form(...)):
    if table_name.strip().lower() == "insurance products":
        return RedirectResponse("/insurance_products", status_code=302)
    return templates.TemplateResponse("404.html", {"request": request}, status_code=404)

@app.get("/table/{table_name}")
async def read_table(table_name: str, request: Request):
    if table_name.lower() != "insuranceproducts":
        return templates.TemplateResponse("404.html", {"request": request}, status_code=404)

# ====== INSURANCE PRODUCTS ======

@app.get("/insurance_products", response_class=HTMLResponse)
def read_insurance_products(request: Request, db: Session = Depends(get_db)):
    products = db.query(InsuranceProduct).all()
    return templates.TemplateResponse("index.html", {"request": request, "products": products})

@app.get("/edit_product/{product_id}", response_class=HTMLResponse)
async def edit_product(request: Request, product_id: int, db: Session = Depends(get_db)):
    product = db.query(InsuranceProduct).filter(InsuranceProduct.id_product == product_id).first()
    if not product:
        return templates.TemplateResponse("404.html", {"request": request}, status_code=404)
    return templates.TemplateResponse("edit_product.html", {"request": request, "product": product})

@app.post("/edit_product/{product_id}")
async def update_product(
    product_id: int,
    name_product: str = Form(...),
    price: float = Form(...),
    coverage: str = Form(...),
    risk_level: str = Form(...),
    name_company: str = Form(...),
    db: Session = Depends(get_db)
):
    product = db.query(InsuranceProduct).filter(InsuranceProduct.id_product == product_id).first()
    if product:
        product.name_product = name_product
        product.price = price
        product.coverage = coverage
        product.risk_level = risk_level
        product.name_company = name_company
        db.commit()
    else:
        return templates.TemplateResponse("404.html", {"request": Request}, status_code=404)
    return RedirectResponse(url="/insurance_products", status_code=303)

@app.post("/delete_product/{product_id}")
async def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(InsuranceProduct).filter(InsuranceProduct.id_product == product_id).first()
    if product:
        db.delete(product)
        db.commit()
    else:
        return templates.TemplateResponse("404.html", {"request": Request}, status_code=404)
    return RedirectResponse(url="/insurance_products", status_code=303)

@app.get("/add_product", response_class=HTMLResponse)
async def add_product_form(request: Request):
    return templates.TemplateResponse("add_product.html", {"request": request})

@app.post("/add_product")
async def create_product(
    name_product: str = Form(...),
    price: float = Form(...),
    coverage: str = Form(...),
    risk_level: str = Form(...),
    name_company: str = Form(...),
    db: Session = Depends(get_db)
):
    new_product = InsuranceProduct(
        name_product=name_product,
        price=price,
        coverage=coverage,
        risk_level=risk_level,
        name_company=name_company
    )
    db.add(new_product)
    db.commit()
    return RedirectResponse(url="/insurance_products", status_code=303)
