import sqlite3
import cgi
import cgitb
from http.server import CGIHTTPRequestHandler, HTTPServer
import json
import xml.etree.ElementTree as ET

cgitb.enable()  # Включаем отладку CGI

PORT = 9000

class RestaurantRequestHandler(CGIHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            
            # Главная страница с меню
            html = """
            <html>
            <head>
                <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
                <title>Ресторанный бизнес - Управление</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 20px; }
                    h1 { color: #333; }
                    .menu { margin-bottom: 20px; }
                    .menu a { display: inline-block; margin-right: 15px; text-decoration: none; color: #0066cc; }
                    table { border-collapse: collapse; width: 100%; margin-top: 20px; }
                    th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                    th { background-color: #f2f2f2; }
                    form { margin-top: 20px; }
                    input, select, textarea { margin-bottom: 10px; width: 100%; padding: 8px; }
                    button { background-color: #4CAF50; color: white; padding: 10px 15px; border: none; cursor: pointer; }
                    button:hover { background-color: #45a049; }
                </style>
            </head>
            <body>
                <h1>Управление ресторанным бизнесом</h1>
                <div class="menu">
                    <a href="/view_restaurants">Рестораны</a>
                    <a href="/view_dishes">Блюда</a>
                    <a href="/view_orders">Заказы</a>
                    <a href="/add_restaurant">Добавить ресторан</a>
                    <a href="/add_dish">Добавить блюдо</a>
                    <a href="/add_order">Добавить заказ</a>
                    <a href="/export_json">Экспорт в JSON</a>
                    <a href="/export_xml">Экспорт в XML</a>
                </div>
            </body>
            </html>
            """
            self.wfile.write(html.encode('utf-8'))
            
        elif self.path == '/view_restaurants':
            self.show_table('Restaurants')
            
        elif self.path == '/view_dishes':
            self.show_table('Dishes')
            
        elif self.path == '/view_orders':
            self.show_table('Orders')
            
        elif self.path == '/add_restaurant':
            self.show_add_form('Restaurants')
            
        elif self.path == '/add_dish':
            self.show_add_form('Dishes')
            
        elif self.path == '/add_order':
            self.show_add_form('Orders')
            
        elif self.path == '/export_json':
            self.export_to_json()
            
        elif self.path == '/export_xml':
            self.export_to_xml()
            
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'404 Not Found')
    
    def do_POST(self):
        if self.path == '/add_restaurant':
            self.add_restaurant()
        elif self.path == '/add_dish':
            self.add_dish()
        elif self.path == '/add_order':
            self.add_order()
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'404 Not Found')
    
    def get_db_connection(self):
        conn = sqlite3.connect('restaurant.db')
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA encoding = 'UTF-8'")
        return conn
    
    def show_table(self, table_name):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(f'SELECT * FROM {table_name}')
        rows = cursor.fetchall()
        conn.close()
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        
        html = f"""
        <html>
        <head>
            <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
            <title>{table_name}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1 {{ color: #333; }}
                table {{ border-collapse: collapse; width: 100%; margin-top: 20px; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
                a {{ display: inline-block; margin-top: 20px; text-decoration: none; color: #0066cc; }}
            </style>
        </head>
        <body>
            <h1>{table_name}</h1>
            <table>
                <tr>
        """
        
        for description in cursor.description:
            html += f"<th>{description[0]}</th>"
        html += "</tr>"
        
        for row in rows:
            html += "<tr>"
            for value in row:
                html += f"<td>{str(value) if value is not None else ''}</td>"
            html += "</tr>"
        
        html += """
            </table>
            <a href="/">На главную</a>
        </body>
        </html>
        """
        
        self.wfile.write(html.encode('utf-8'))
    
    def show_add_form(self, table_name):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        if table_name == 'Restaurants':
            form = """
            <form method="post" action="/add_restaurant">
                <h2>Добавить ресторан</h2>
                <label for="name">Название:</label>
                <input type="text" id="name" name="name" required>
                
                <label for="address">Адрес:</label>
                <input type="text" id="address" name="address" required>
                
                <label for="phone">Телефон:</label>
                <input type="text" id="phone" name="phone">
                
                <label for="rating">Рейтинг:</label>
                <input type="number" id="rating" name="rating" step="0.1" min="0" max="5">
                
                <button type="submit">Добавить</button>
            </form>
            """
        elif table_name == 'Dishes':
            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT restaurant_id, name FROM Restaurants')
            restaurants = cursor.fetchall()
            conn.close()
            
            options = ""
            for restaurant in restaurants:
                options += f'<option value="{restaurant["restaurant_id"]}">{restaurant["name"]}</option>'
            
            form = f"""
            <form method="post" action="/add_dish">
                <h2>Добавить блюдо</h2>
                
                <label for="restaurant_id">Ресторан:</label>
                <select id="restaurant_id" name="restaurant_id" required>
                    {options}
                </select>
                
                <label for="name">Название блюда:</label>
                <input type="text" id="name" name="name" required>
                
                <label for="description">Описание:</label>
                <textarea id="description" name="description"></textarea>
                
                <label for="price">Цена:</label>
                <input type="number" id="price" name="price" step="0.01" min="0" required>
                
                <label for="category">Категория:</label>
                <input type="text" id="category" name="category">
                
                <button type="submit">Добавить</button>
            </form>
            """
        elif table_name == 'Orders':
            conn = self.get_db_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT restaurant_id, name FROM Restaurants')
            restaurants = cursor.fetchall()
            conn.close()
            
            options = ""
            for restaurant in restaurants:
                options += f'<option value="{restaurant["restaurant_id"]}">{restaurant["name"]}</option>'
            
            form = f"""
            <form method="post" action="/add_order">
                <h2>Добавить заказ</h2>
                
                <label for="restaurant_id">Ресторан:</label>
                <select id="restaurant_id" name="restaurant_id" required>
                    {options}
                </select>
                
                <label for="customer_name">Имя клиента:</label>
                <input type="text" id="customer_name" name="customer_name" required>
                
                <label for="order_date">Дата заказа:</label>
                <input type="date" id="order_date" name="order_date" required>
                
                <label for="total_amount">Сумма заказа:</label>
                <input type="number" id="total_amount" name="total_amount" step="0.01" min="0" required>
                
                <label for="status">Статус:</label>
                <select id="status" name="status">
                    <option value="new">Новый</option>
                    <option value="in_progress">В процессе</option>
                    <option value="completed">Завершен</option>
                    <option value="cancelled">Отменен</option>
                </select>
                
                <button type="submit">Добавить</button>
            </form>
            """
        
        html = f"""
        <html>
        <head>
            <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
            <title>Добавить запись</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1 {{ color: #333; }}
                form {{ margin-top: 20px; }}
                input, select, textarea {{ margin-bottom: 10px; width: 100%; padding: 8px; }}
                button {{ background-color: #4CAF50; color: white; padding: 10px 15px; border: none; cursor: pointer; }}
                button:hover {{ background-color: #45a049; }}
                a {{ display: inline-block; margin-top: 20px; text-decoration: none; color: #0066cc; }}
            </style>
        </head>
        <body>
            <h1>Добавить запись в таблицу {table_name}</h1>
            {form}
            <a href="/">На главную</a>
        </body>
        </html>
        """
        
        self.wfile.write(html.encode('utf-8'))
    
    def add_restaurant(self):
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST'}
        )
        
        name = form.getvalue('name')
        address = form.getvalue('address')
        phone = form.getvalue('phone')
        rating = form.getvalue('rating', 0.0)
        
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO Restaurants (name, address, phone, rating) VALUES (?, ?, ?, ?)',
            (name, address, phone, float(rating))
        )
        conn.commit()
        conn.close()
        
        self.send_response(303)
        self.send_header('Location', '/view_restaurants')
        self.end_headers()
    
    def add_dish(self):
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST'}
        )
        
        restaurant_id = form.getvalue('restaurant_id')
        name = form.getvalue('name')
        description = form.getvalue('description')
        price = form.getvalue('price')
        category = form.getvalue('category')
        
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO Dishes (restaurant_id, name, description, price, category) VALUES (?, ?, ?, ?, ?)',
            (restaurant_id, name, description, float(price), category)
        )
        conn.commit()
        conn.close()
        
        self.send_response(303)
        self.send_header('Location', '/view_dishes')
        self.end_headers()
    
    def add_order(self):
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD': 'POST'}
        )
        
        restaurant_id = form.getvalue('restaurant_id')
        customer_name = form.getvalue('customer_name')
        order_date = form.getvalue('order_date')
        total_amount = form.getvalue('total_amount')
        status = form.getvalue('status', 'new')
        
        conn = self.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO Orders (restaurant_id, customer_name, order_date, total_amount, status) VALUES (?, ?, ?, ?, ?)',
            (restaurant_id, customer_name, order_date, float(total_amount), status)
        )
        conn.commit()
        conn.close()
        
        self.send_response(303)
        self.send_header('Location', '/view_orders')
        self.end_headers()
    
    # Экспорт в JSON
    def export_to_json(self):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM Restaurants')
        restaurants = [dict(row) for row in cursor.fetchall()]
        
        cursor.execute('SELECT * FROM Dishes')
        dishes = [dict(row) for row in cursor.fetchall()]
        
        cursor.execute('SELECT * FROM Orders')
        orders = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        
        data = {
            'restaurants': restaurants,
            'dishes': dishes,
            'orders': orders
        }
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Content-Disposition', 'attachment; filename="restaurant_data.json"')
        self.end_headers()
        
        self.wfile.write(json.dumps(data, indent=2).encode('utf-8'))
    
    # Экспорт в XML
    def export_to_xml(self):
        conn = self.get_db_connection()
        cursor = conn.cursor()
        
        # Создаем корневой элемент
        root = ET.Element('RestaurantData')
        
        # Добавляем рестораны
        restaurants_elem = ET.SubElement(root, 'Restaurants')
        cursor.execute('SELECT * FROM Restaurants')
        for row in cursor.fetchall():
            restaurant = ET.SubElement(restaurants_elem, 'Restaurant')
            for key, value in dict(row).items():
                ET.SubElement(restaurant, key).text = str(value)
        
        # Добавляем блюда
        dishes_elem = ET.SubElement(root, 'Dishes')
        cursor.execute('SELECT * FROM Dishes')
        for row in cursor.fetchall():
            dish = ET.SubElement(dishes_elem, 'Dish')
            for key, value in dict(row).items():
                ET.SubElement(dish, key).text = str(value)
        
        # Добавляем заказы
        orders_elem = ET.SubElement(root, 'Orders')
        cursor.execute('SELECT * FROM Orders')
        for row in cursor.fetchall():
            order = ET.SubElement(orders_elem, 'Order')
            for key, value in dict(row).items():
                ET.SubElement(order, key).text = str(value)
        
        conn.close()
        
        # Создаем XML-дерево
        tree = ET.ElementTree(root)
        
        self.send_response(200)
        self.send_header('Content-type', 'application/xml')
        self.send_header('Content-Disposition', 'attachment; filename="restaurant_data.xml"')
        self.end_headers()
        
        # Записываем XML в ответ
        ET.indent(tree, space="\t", level=0)
        tree.write(self.wfile, encoding='utf-8', xml_declaration=True)

def run_server():
    server_address = ('', PORT)
    httpd = HTTPServer(server_address, RestaurantRequestHandler)
    print(f"Сервер запущен на порту {PORT}")
    print(f"Откройте http://localhost:{PORT} в браузере")
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()