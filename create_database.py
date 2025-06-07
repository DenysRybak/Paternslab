from sqlalchemy import create_engine
from models import Base  # Імпортуй Base з того файлу, де ти створюєш моделі

# НАЗВА нової бази (може бути будь-якою)
engine = create_engine('sqlite:///newdatabase.db')

# Створення таблиць на основі моделей
Base.metadata.create_all(engine)
