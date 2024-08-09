import sqlite3 as lite


db = 'basic.db'

class BasicClass:
    def __init__(self) -> None:
        self.conn = lite.connect(db)
        self.cursor = self.conn.cursor()

    def check_admin(self, username):
        self.cursor.execute(
            "SELECT username FROM admins WHERE username = ?;", (username,)
        )
        admin = self.cursor.fetchone()
        if admin:
            return True
        else:
            return False

    def add_admin(self, name):
        self.cursor.execute(
            "INSERT INTO admins (username) VALUES (?);", (name,)
        )
        self.conn.commit()
        return True
    
    def get_admins(self):
        self.cursor.execute(
            "SELECT * FROM admins;"
        )
        admins = self.cursor.fetchall()
        return admins
    
    def delete_admins(self, name):
        try:
            self.cursor.execute(
                "DELETE FROM admins WHERE username = ?;", (name, )
            )
            self.conn.commit()
            return True
        except:
            return False
    
    def add_product(self, model, color, size, count, fabric, price, photo, description):
        try:
            self.cursor.execute(
                "INSERT INTO products (model, color, size, count, fabric, price, photo, description) VALUES (?, ?, ?, ?, ?, ?, ?, ?);", (model, color, size, count, fabric, price, photo, description, )
            )
            self.conn.commit()
            return True
        except:
            return False
        
    def delete_product(self, id):
        try:
            self.cursor.execute(
                "UPDATE products SET status = 0 WHERE id = ?;", (id, )
            )
            self.conn.commit()
            return True
        except:
            return False
        
    def get_delete_products(self):
        self.cursor.execute(
            "SELECT id, model, color, size, count, fabric, price, photo, description FROM products WHERE status = 0 ORDER BY id DESC;"
        )
        all_products = self.cursor.fetchall()
        return all_products
    
    def edit_deleted_products(self, id):
        try:
            self.cursor.execute(
                "UPDATE products SET status = 1 WHERE id = ?;", (id, )
            )
            self.conn.commit()
            return True
        except:
            return False        

    
    def get_products(self):
        self.cursor.execute(
            "SELECT id, model, color, size, count, fabric, price, photo, description FROM products WHERE status = 1 AND in_stock = 1 ORDER BY id DESC;"
        )
        all_products = self.cursor.fetchall()
        return all_products
    
    def edit_product_handler(self, query, value, id):
        try:
            sql = "UPDATE products SET {} = ? WHERE id = ?;".format(query)
            self.cursor.execute(sql, (value, id))
            self.conn.commit()
            return True
        except:
            return False

    def get_product_by_id(self, p_id):
        self.cursor.execute(
            "SELECT * FROM products WHERE id = ?;", (p_id,)
        )
        product = self.cursor.fetchone()
        if product:
            return product
        else:
            return False

        
    def create_order_handler(self, id, fio, phone_number, count, address, delivery_method, payment_method, order_date, user_id, user_username, sum, size, color):
        try:
            self.cursor.execute(
                "INSERT INTO orders (user_id, product_id, count, fio, phone_number, address, delivery_method, payment_method, order_date, username, sum, size, color) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", (user_id, id, count, fio, phone_number, address, delivery_method, payment_method, order_date, user_username, sum, size, color)
            )
            self.conn.commit()
            return True
        except:
            return False
    
    def set_count_handler(self, count, id):
        try:
            self.cursor.execute(
                "UPDATE products SET count = ? WHERE id = ?;", (count, id, )
            )
            self.conn.commit()
            return True
        except:
            return False
        
    def set_order_status_handler(self, order_id, value):
        try:
            self.cursor.execute(
                "UPDATE orders SET is_confirmed = ? WHERE id = ?;", (value, order_id, )
            )
            self.conn.commit()
            return True
        except:
            return False
        

    def get_order_by_id(self, o_id):
        try:
            self.cursor.execute(
                "SELECT * FROM orders WHERE id = ?;", (o_id,)
            )
            orders = self.cursor.fetchone()
            if orders:
                return orders
        except:
            return False
        
        
    def get_order_handler(self, user_id):
        self.cursor.execute(
            "SELECT * FROM orders WHERE user_id = ?;", (user_id, )
        )
        result = self.cursor.fetchall()
        if result:
            return result
        else:
            return False
    
    def get_orders(self):
        self.cursor.execute(
            "SELECT * FROM orders;"
        )
        orders = self.cursor.fetchall()
        if orders:
            return orders
        else:
            return False
    
    def status_changer(self, value, id):
        try:
            self.cursor.execute(
                "UPDATE orders SET is_confirmed = ? WHERE id = ?;", (value, id, )
            )
            self.conn.commit()
            return True
        except:
            return False
    
    def get_waiting_orders(self):
        try:
            self.cursor.execute(
                "SELECT * FROM orders WHERE is_confirmed = 0;"
            )
            order = self.cursor.fetchall()
            if order:
                return order
            else: 
                return False
        except:
            return False
    
    def get_working_orders(self):
        try:
            self.cursor.execute(
                "SELECT * FROM orders WHERE is_confirmed = 1;"
            )
            order = self.cursor.fetchall()
            return order
        except:
            return False
    
    def get_delivering_orders(self):
        try:
            self.cursor.execute(
                "SELECT * FROM orders WHERE is_confirmed = 2;"
            )
            order = self.cursor.fetchall()
            return order
        except:
            return False
        
    def get_finishing_orders(self):
        try:
            self.cursor.execute(
                "SELECT * FROM orders WHERE is_confirmed = 3;"
            )
            order = self.cursor.fetchall()
            return order
        except:
            return False
        
    def create_advertisiments(self, photo, title, content):
        try:
            self.cursor.execute(
                "INSERT INTO advertisiments (photo, title, content) VALUES (?, ?, ?);", (photo, title, content, )
            )
            self.conn.commit()
            return True
        except:
            return False
        
    def get_adver(self, id):
        self.cursor.execute(
            "SELECT * FROM users WHERE id = ?;", (id, )
        )
        adver = self.cursor.fetchall()
        if adver:
            return adver
        else:
            return False
        
    def create_user(self, user_id):
        self.cursor.execute(
            "INSERT INTO users (user_id) VALUES (?);", (user_id, )
        )
        self.conn.commit()
        return True
    
    def get_users(self):
        self.cursor.execute(
            "SELECT * FROM users;"
        )
        user = self.cursor.fetchall()
        if user:
            return user
        else:
            return False
        
    def add_info(self, photo, title, content):
        try:
            self.cursor.execute(
                "INSERT INTO info (photo, title, content) VALUES (?, ?, ?);", (photo, title, content, )
            )
            self.conn.commit()
            return True
        except:
            return False
        
    def get_info(self):
        self.cursor.execute(
            "SELECT * FROM info;"
        )
        info = self.cursor.fetchall()
        if info:
            return info
        else:
            return False