import sqlite3
import os

DATABASE_NAME = 'crud_app.db'

def get_db_connection():
    """Создает и возвращает соединение с базой данных."""
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row # Позволяет обращаться к столбцам по имени
    return conn

def initialize_database():
    """Инициализирует базу данных и создает таблицу, если она не существует."""
    if not os.path.exists(DATABASE_NAME):
        print("Creating database...")
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT
            );
        """)
        conn.commit()
        conn.close()
        print("Database created successfully.")
    else:
        # Убедимся, что таблица существует, даже если файл БД уже есть
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT
            );
        """)
        conn.commit()
        conn.close()


def add_item(name, description):
    """Добавляет новый элемент в базу данных."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO items (name, description) VALUES (?, ?)", (name, description))
    conn.commit()
    conn.close()

def get_all_items():
    """Извлекает все элементы из базы данных."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, description FROM items")
    items = cursor.fetchall()
    conn.close()
    return items

def update_item(item_id, name, description):
    """Обновляет существующий элемент в базе данных."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE items SET name = ?, description = ? WHERE id = ?", (name, description, item_id))
    conn.commit()
    conn.close()

def delete_item(item_id):
    """Удаляет элемент из базы данных по его ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))
    conn.commit()
    conn.close()

def get_item_by_id(item_id):
    """Извлекает один элемент по его ID."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, description FROM items WHERE id = ?", (item_id,))
    item = cursor.fetchone()
    conn.close()
    return item

# Инициализация БД при первом импорте модуля
initialize_database()