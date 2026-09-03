try:
    from app.database import get_database_connection
except ImportError:
    from database import get_database_connection


connection = get_database_connection()

print("Database connection successful!")

connection.close()