from flask import Flask, render_template, request, redirect, url_for
from database import SessionLocal
from repositories import InsuranceProductRepository
from domain.services  import ProductService

app = Flask(__name__)

# Ініціалізація бази даних та сервісів
db = SessionLocal()
product_repo = InsuranceProductRepository(db)
product_service = ProductService(product_repo)

# Маршрут для головної сторінки

@app.route("/insurance_products")
def insurance_products():
    products = product_service.get_all_products()  # Отримуємо усі продукти
    return render_template("insurance_products.html", products=products)  # Відображаємо на сторінці

@app.route("/add_product", methods=["GET", "POST"])
def add_product():
    if request.method == "POST":
        # Отримуємо дані з форми
        name_product = request.form["name_product"]
        price = request.form["price"]
        coverage = request.form["coverage"]
        risk_level = request.form["risk_level"]
        name_company = request.form["name_company"]

        # Додаємо новий продукт через сервіс
        product_service.add_product(name_product, price, coverage, risk_level, name_company)
        return redirect(url_for("insurance_products"))  # Переходимо на сторінку з продуктами

    return render_template("product_form.html")  # Якщо GET, відображаємо форму

@app.route("/edit_product/<int:product_id>", methods=["GET", "POST"])
def edit_product(product_id):
    product = product_service.get_product_by_id(product_id)  # Отримуємо продукт по ID
    if request.method == "POST":
        # Отримуємо дані з форми
        name_product = request.form["name_product"]
        price = request.form["price"]
        coverage = request.form["coverage"]
        risk_level = request.form["risk_level"]
        name_company = request.form["name_company"]

        # Оновлюємо продукт через сервіс
        product_service.update_product(product_id, name_product, price, coverage, risk_level, name_company)
        return redirect(url_for("insurance_products"))  # Переходимо на сторінку з продуктами

    return render_template("product_form.html", product=product)  # Якщо GET, відображаємо форму для редагування

@app.route("/delete_product/<int:product_id>")
def delete_product(product_id):
    product_service.delete_product(product_id)  # Видаляємо продукт через сервіс
    return redirect(url_for("insurance_products"))  # Переходимо на сторінку з продуктами



if __name__ == "__main__":
    app.run(debug=True)
