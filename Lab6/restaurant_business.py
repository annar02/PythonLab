import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        conn.execute("PRAGMA encoding = 'UTF-8';")
        conn.execute("PRAGMA foreign_keys = ON;")
        print(f"Подключение к SQLite DB {db_file} успешно")
        return conn
    except Error as e:
        print(f"Ошибка при подключении к SQLite: {e}")
    return conn

def clear_tables(conn):
    try:
        cursor = conn.cursor()
        
        cursor.execute("PRAGMA foreign_keys = OFF;")
        
        cursor.execute("DELETE FROM Orders;")
        cursor.execute("DELETE FROM Dishes;")
        cursor.execute("DELETE FROM Restaurants;")
        
        cursor.execute("DELETE FROM sqlite_sequence;")
        
        cursor.execute("PRAGMA foreign_keys = ON;")
        
        conn.commit()
        print("Все таблицы успешно очищены")
    except Error as e:
        conn.rollback()
        print(f"Ошибка при очистке таблиц: {e}")

def create_tables(conn):
    try:
        cursor = conn.cursor()
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Restaurants (
            restaurant_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL COLLATE NOCASE,
            address TEXT NOT NULL,
            phone TEXT,
            rating REAL CHECK (rating BETWEEN 0 AND 5)
        );
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Dishes (
            dish_id INTEGER PRIMARY KEY AUTOINCREMENT,
            restaurant_id INTEGER NOT NULL,
            name TEXT NOT NULL COLLATE NOCASE,
            description TEXT,
            price REAL NOT NULL CHECK (price > 0),
            category TEXT,
            FOREIGN KEY (restaurant_id) REFERENCES Restaurants(restaurant_id) ON DELETE CASCADE
        );
        ''')
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS Orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            restaurant_id INTEGER NOT NULL,
            customer_name TEXT NOT NULL COLLATE NOCASE,
            order_date TEXT NOT NULL,
            total_amount REAL NOT NULL CHECK (total_amount > 0),
            status TEXT DEFAULT 'new' CHECK (status IN ('new', 'in_progress', 'completed', 'cancelled')),
            FOREIGN KEY (restaurant_id) REFERENCES Restaurants(restaurant_id) ON DELETE CASCADE
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
        cursor.executemany(
            'INSERT INTO Restaurants (name, address, phone, rating) VALUES (?, ?, ?, ?)', 
            restaurants
        )
        
        dishes = [
            (1, 'Пицца Маргарита', 'Классическая пицца с томатами и моцареллой', 450, 'Основное'),
            (1, 'Паста Карбонара', 'Паста с соусом из яиц, сыра и бекона', 380, 'Основное'),
            (2, 'Ролл Филадельфия', 'Ролл с лососем и сыром Филадельфия', 320, 'Суши'),
            (2, 'Ролл Калифорния', 'Ролл с крабом и авокадо', 280, 'Суши'),
            (3, 'Хачапури по-аджарски', 'Хачапури в форме лодочки с яйцом', 350, 'Основное'),
            (3, 'Шашлык из свинины', 'Шашлык из свиной шеи с соусом', 420, 'Гриль')
        ]
        cursor.executemany(
            'INSERT INTO Dishes (restaurant_id, name, description, price, category) VALUES (?, ?, ?, ?, ?)', 
            dishes
        )
        
        orders = [
            (1, 'Иван Иванов', '2023-05-15', 1250, 'completed'),
            (2, 'Петр Петров', '2023-05-16', 890, 'in_progress'),
            (3, 'Сергей Сергеев', '2023-05-17', 1540, 'new')
        ]
        cursor.executemany(
            'INSERT INTO Orders (restaurant_id, customer_name, order_date, total_amount, status) VALUES (?, ?, ?, ?, ?)', 
            orders
        )
        
        conn.commit()
        print("Тестовые данные успешно добавлены")
    except Error as e:
        conn.rollback()
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
        ORDER BY dish_count DESC
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
    conn.execute("PRAGMA encoding = 'UTF-8'")

    if conn is not None:
        try:
            create_tables(conn)
            
            clear_tables(conn)
            
            insert_sample_data(conn)
            
            execute_statistical_queries(conn)
        finally:
            conn.close()
    else:
        print("Ошибка! Не удалось создать соединение с базой данных.")

if __name__ == '__main__':
    main()