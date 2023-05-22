import sqlite3

class DbShop:
    def __init__(self) -> None:
        self.db_path = None

    def db_initialize(self):
        print('Database was started')
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

    def db_close_conn(self):
        print('Database was closed')
        self.conn.close()


    def db_get_products_where_location(self, id):
        self.cursor.execute("SELECT * FROM products WHERE location_id = ? AND bought_at = FALSE",(id,))
        result = self.cursor.fetchall()
        return result


    def db_get_all_users(self):
        self.cursor.execute('SELECT * FROM users')
        result = self.cursor.fetchall()
        return result


    def db_get_all_products(self):
        self.cursor.execute('SELECT * FROM products WHERE bought_at = FALSE')
        self.result = self.cursor.fetchall()
        return self.result
    
    def db_get_count_productions(self):
        self.cursor.execute("SELECT COUNT(*) FROM products WHERE bought_at = FALSE")
        self.result = self.cursor.fetchone()
        return self.result
    
    def db_check_and_create_user(self, user_id, username):
        self.cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        in_db_user = self.cursor.fetchone()
        if in_db_user is None:
            self.cursor.execute('''
                INSERT INTO users (id, username) VALUES (?, ?) ''', (user_id, username))
            self.conn.commit()
            print('To DB added new user')


    def db_ban_user(self, user_id):
        self.cursor.execute("UPDATE users SET banned = TRUE WHERE id = ?",(user_id,))
        self.conn.commit()
        print(f'User {user_id} was banned')


    def db_get_full_list_location(self):
        self.cursor.execute("SELECT * FROM locations")
        self.result = self.cursor.fetchall()
        return self.result
    
    def db_location_ids_list(self):
        self.cursor.execute("SELECT id FROM locations")
        self.result = self.cursor.fetchall()
        return self.result
    
    def db_add_location(self, name):
        try:
            self.cursor.execute('INSERT INTO locations (location) VALUES (?)',(name,))
            self.conn.commit()
            print("Added new location")
            return True
        except sqlite3.IntegrityError:
            return False
        
    
    def db_get_location_id(self, name):
        self.cursor.execute("SELECT id FROM locations WHERE location = ?",(name,))
        result = self.cursor.fetchone()
        return result
        

    def db_get_location_name(self, id):
        self.cursor.execute("SELECT location FROM locations WHERE id = (?)",(id,))
        result = self.cursor.fetchone()
        return result
    
    def db_delete_product(self, id):
        self.cursor.execute("DELETE FROM products WHERE id = ?", (id,))
        self.conn.commit()
        return True
    
    def db_get_purchases(self):
        self.cursor.execute('SELECT * FROM purchases')
        self.result = self.cursor.fetchall()
        print('выданы все покупки')
        return self.result


    def db_add_product_to_db(self, product_data):
        name = product_data['name']
        weight = product_data['weight']
        location = product_data['location_id']
        price = int(product_data['price'])
        image_path1 = product_data['image_path1']
        image_path2 = product_data['image_path2']
        self.cursor.execute("INSERT INTO products (name, weight, location_id, price, image_path1, image_path2) VALUES (?, ?, ?, ?, ?, ?)", 
                            (name, weight, location, price, image_path1, image_path2))
        self.conn.commit()
        return True

    
    def db_get_loc_where_product_now_count(self):
        loc_name_count = {}
        self.cursor.execute('SELECT location_id FROM products WHERE bought_at = FALSE')
        self.loc_ids_list = self.cursor.fetchall()
        for i in self.loc_ids_list:
            self.cursor.execute(f"SELECT location FROM locations WHERE id = (?)", (i[0],))
            name = self.cursor.fetchone()
            self.cursor.execute(f"SELECT COUNT(*) FROM products WHERE location_id = (?) AND bought_at = FALSE", (i[0],))
            count = self.cursor.fetchone()
            loc_name_count[name] = count
        return loc_name_count
    

    def db_get_product_info(self, id):
        self.cursor.execute('SELECT * FROM products WHERE id = ?',(id,))
        result = self.cursor.fetchall() 
        return result
    
    def db_get_user_balance(self, id):
        self.cursor.execute("SELECT balance FROM users WHERE id = ?",(id,))
        result = self.cursor.fetchone()
        return result
    

    def db_get_product_price(self, id):
        self.cursor.execute("SELECT price FROM products WHERE id = ?",(id,))
        result = self.cursor.fetchone()
        return result
    

    def db_update_user_bal(self, id, bal):
        self.cursor.execute('UPDATE users SET balance = ? WHERE id = ?', (bal, id))
        self.conn.commit()
        print(f'Balance of user {id} was changed and = {bal}')
    

    def db_set_bought_for_prod(self, id):
        self.cursor.execute("UPDATE products SET bought_at = TRUE WHERE id = ?", (id,))
        self.conn.commit()
        print(f'product with id = {id} was bought')


    def db_add_purchase(self, user_id, prod_id):
        self.cursor.execute("INSERT INTO purchases (user_id, product_id) VALUES (?, ?)", (user_id, prod_id))
        self.conn.commit()
        print(f'{user_id} was bough {prod_id}')


    def db_get_user_info(self, user_id):
        self.cursor.execute("SELECT * FROM users WHERE id = ?",(user_id,))
        result = self.cursor.fetchone()
        return result
    

    def db_get_user_purchase(self, user_id):
        self.cursor.execute("SELECT * FROM purchases WHERE user_id = ?",(user_id,))
        result = self.cursor.fetchall()
        return result


    def db_check_and_create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT,
                balance INTEGER DEFAULT 0,
                registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                banned BOOLEAN DEFAULT FALCE,
            )''')
        self.conn.commit()
        print('Table users was created')
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT,
            weight REAL,
            location_id INTEGER,
            price INTEGER,
            image_path1 TEXT,
            image_path2 TEXT,
            adding_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            bought_at BOOLEAN DEFAULT FALSE,
            FOREIGN KEY (location_id) REFERENCES locations(id)
            );""")
        self.conn.commit()
        print('Table products was created')
        self.cursor.execute("""CREATE TABLE locations (
            id INTEGER PRIMARY KEY,
            location TEXT,
            UNIQUE (location)
            );""")
        self.conn.commit()
        print('Table locations was created')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS purchases (
            user_id INTEGER,
            product_id INTEGER,
            purchase_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (product_id) REFERENCES products(id)
            )''')
        self.conn.commit()
        print('Table purchases was created')

    

