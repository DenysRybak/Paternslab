import csv
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()

# Генерація унікальних клієнтів
def generate_clients(num_clients):
    clients = []
    for i in range(1, num_clients + 1):
        client = {
            "id": i,
            "name": fake.first_name(),
            "surname": fake.last_name(),
            "years_old": random.randint(18, 70),
            "contact_info": fake.phone_number(),
            "destination_country": fake.country()
        }
        clients.append(client)
    return clients

# Генерація унікальних страхових продуктів
def generate_insurance_products(num_products):
    coverages = ["медичне", "майнове", "життя", "подорожі", "від нещасного випадку"]
    risk_levels = ["Low", "Medium", "High"]
    products = []
    for i in range(1, num_products + 1):
        product = {
            "id_product": i,
            "name_product": f"{fake.word().capitalize()} {i}",
            "price": random.randint(100, 5000),
            "coverage": random.choice(coverages),
            "risk_level": random.choice(risk_levels),
            "name_company": fake.company()
        }
        products.append(product)
    return products

# Генерація замовлень
def generate_orders(num_orders, products, clients):
    orders = []
    for i in range(1, num_orders + 1):
        product = random.choice(products)
        client = random.choice(clients)
        order_date = fake.date_between(start_date='-3y', end_date='today')
        expiration_date = order_date + timedelta(days=random.randint(30, 365))
        order = {
            "order_id": i,
            "order_date": order_date.strftime("%Y-%m-%d"),
            "product": product["id_product"],
            "client": client["id"],
            "total_price": product["price"],
            "expiration_date": expiration_date.strftime("%Y-%m-%d")
        }
        orders.append(order)
    return orders

# Генерація оплат
def generate_payments(num_payments, orders):
    payment_types = ["Credit Card", "PayPal", "Bank Transfer"]
    payments = []
    used_orders = set()
    for i in range(1, num_payments + 1):
        # Гарантуємо, що кожна оплата відповідає одному замовленню
        order = random.choice(orders)
        while order["order_id"] in used_orders:
            order = random.choice(orders)
        used_orders.add(order["order_id"])

        payment_date = datetime.strptime(order["order_date"], "%Y-%m-%d") + timedelta(days=random.randint(0, 14))
        payment = {
            "payment_id": i,
            "type_payment": random.choice(payment_types),
            "date_payment": payment_date.strftime("%Y-%m-%d"),
            "order_id": order["order_id"]
        }
        payments.append(payment)
    return payments

# Запис у CSV
def save_to_csv(data, filename, fieldnames):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

# Генерація CSV файлів
def generate_csv_files():
    clients = generate_clients(1000)
    save_to_csv(clients, 'data/clients.csv', ['id', 'name', 'surname', 'years_old', 'contact_info', 'destination_country'])

    products = generate_insurance_products(1000)
    save_to_csv(products, 'data/insurance_products.csv', ['id_product', 'name_product', 'price', 'coverage', 'risk_level', 'name_company'])

    orders = generate_orders(1000, products, clients)
    save_to_csv(orders, 'data/orders.csv', ['order_id', 'order_date', 'product', 'client', 'total_price', 'expiration_date'])

    payments = generate_payments(1000, orders)
    save_to_csv(payments, 'data/payments.csv', ['payment_id', 'type_payment', 'date_payment', 'order_id'])

# Запуск
generate_csv_files()
