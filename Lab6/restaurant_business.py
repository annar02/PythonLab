# Создание базы данных для ресторанного бизнеса с тремя таблицами: Restaurants, Dishes и Orders

import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Подключение к SQLite DB {db_file} успешно")
        return conn
    except Error as e:
        print(f"Ошибка при подключении к SQLite: {e}")
    return conn

def create_tables(conn):
    try:
        cursor = conn.cursor()
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Restaurants (
            restaurant_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            address TEXT NOT NULL,
            phone TEXT,
            rating REAL
        );
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Dishes (
            dish_id INTEGER PRIMARY KEY AUTOINCREMENT,
            restaurant_id INTEGER,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            category TEXT,
            FOREIGN KEY (restaurant_id) REFERENCES Restaurants(restaurant_id)
        );
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            restaurant_id INTEGER,
            customer_name TEXT NOT NULL,
            order_date TEXT NOT NULL,
            total_amount REAL NOT NULL,
            status TEXT DEFAULT 'new',
            FOREIGN KEY (restaurant_id) REFERENCES Restaurants(restaurant_id)
        );
        ''')
        
        print("Таблицы успешно созданы")
    except Error as e:
        print(f"Ошибка при создании таблиц: {e}")

def insert_sample_data(conn):
    try:
        cursor = conn.cursor()
        
        restaurants = [
            ('Итальянский уголок', 'ул. Пушкина, 10', '+79101234567', 4.5),
            ('Суши-бар Сакура', 'ул. Лермонтова, 15', '+79107654321', 4.7),
            ('Грузинский дворик', 'ул. Гоголя, 20', '+79109876543', 4.8)
        ]
        cursor.executemany('INSERT INTO Restaurants (name, address, phone, rating) VALUES (?, ?, ?, ?)', restaurants)
        
        dishes = [
            (1, 'Пицца Маргарита', 'Классическая пицца с томатами и моцареллой', 450, 'Основное'),
            (1, 'Паста Карбонара', 'Паста с соусом из яиц, сыра и бекона', 380, 'Основное'),
            (2, 'Ролл Филадельфия', 'Ролл с лососем и сыром Филадельфия', 320, 'Суши'),
            (2, 'Ролл Калифорния', 'Ролл с крабом и авокадо', 280, 'Суши'),
            (3, 'Хачапури по-аджарски', 'Хачапури в форме лодочки с яйцом', 350, 'Основное'),
            (3, 'Шашлык из свинины', 'Шашлык из свиной шеи с соусом', 420, 'Гриль')
        ]
        cursor.executemany('INSERT INTO Dishes (restaurant_id, name, description, price, category) VALUES (?, ?, ?, ?, ?)', dishes)
        
        orders = [
            (1, 'Иван Иванов', '2023-05-15', 1250, 'completed'),
            (2, 'Петр Петров', '2023-05-16', 890, 'in_progress'),
            (3, 'Сергей Сергеев', '2023-05-17', 1540, 'new')
        ]
        cursor.executemany('INSERT INTO Orders (restaurant_id, customer_name, order_date, total_amount, status) VALUES (?, ?, ?, ?, ?)', orders)
        
        conn.commit()
        print("Тестовые данные успешно добавлены")
    except Error as e:
        print(f"Ошибка при добавлении тестовых данных: {e}")

def execute_statistical_queries(conn):
    try:
        cursor = conn.cursor()
        
        print("\n1. Средний чек по каждому ресторану:")
        cursor.execute('''
        SELECT r.name, AVG(o.total_amount) as avg_check
        FROM Orders o
        JOIN Restaurants r ON o.restaurant_id = r.restaurant_id
        GROUP BY r.name
        ''')
        for row in cursor.fetchall():
            print(f"{row[0]}: {row[1]:.2f} руб.")
        
        print("\n2. Количество блюд в каждой категории:")
        cursor.execute('''
        SELECT category, COUNT(*) as dish_count
        FROM Dishes
        GROUP BY category
        ''')
        for row in cursor.fetchall():
            print(f"{row[0]}: {row[1]} блюд")
        
        print("\n3. Общая выручка по дням:")
        cursor.execute('''
        SELECT order_date, SUM(total_amount) as daily_revenue
        FROM Orders
        GROUP BY order_date
        ORDER BY order_date
        ''')
        for row in cursor.fetchall():
            print(f"{row[0]}: {row[1]} руб.")
            
    except Error as e:
        print(f"Ошибка при выполнении статистических запросов: {e}")

def main():
    database = "restaurant.db"
    
    conn = create_connection(database)
    
    if conn is not None:
        create_tables(conn)
        
        insert_sample_data(conn)
        
        execute_statistical_queries(conn)
        
        conn.close()
    else:
        print("Ошибка! Не удалось создать соединение с базой данных.")

if __name__ == '__main__':
    main()