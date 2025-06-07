from infrastructure.csv_loader import CSVLoader
from interfaces.repository_interface import IClientRepository, IInsuranceProductRepository, IOrderRepository, IPaymentRepository

class ImportService:
    def __init__(self, client_repo: IClientRepository, product_repo: IInsuranceProductRepository,
                 order_repo: IOrderRepository, payment_repo: IPaymentRepository):
        self.csv_loader = CSVLoader(client_repo, product_repo, order_repo, payment_repo)

    def import_clients(self, file_path: str):
        """Імпорт клієнтів з CSV"""
        print("Імпорт клієнтів...")
        self.csv_loader.load_clients(file_path)
        print("Імпорт клієнтів завершено.")

    def import_insurance_products(self, file_path: str):
        """Імпорт страхових продуктів з CSV"""
        print("Імпорт страхових продуктів...")
        self.csv_loader.load_insurance_products(file_path)
        print("Імпорт страхових продуктів завершено.")

    def import_orders(self, file_path: str):
        """Імпорт замовлень з CSV"""
        print("Імпорт замовлень...")
        self.csv_loader.load_orders(file_path)
        print("Імпорт замовлень завершено.")

    def import_payments(self, file_path: str):
        """Імпорт оплат з CSV"""
        print("Імпорт оплат...")
        self.csv_loader.load_payments(file_path)
        print("Імпорт оплат завершено.")
