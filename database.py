import config

if config.DB_TYPE == 'postgresql':
    import psycopg2 as db_connector
    from psycopg2 import Error as DBError
    PLACEHOLDER = '%s'
elif config.DB_TYPE == 'mysql':
    import mysql.connector as db_connector
    from mysql.connector import Error as DBError
    PLACEHOLDER = '%s'

class Database:
    def __init__(self):
        self.connection = None
        self.cursor = None
    
    def connect(self):
        try:
            if config.DB_TYPE == 'postgresql':
                self.connection = db_connector.connect(**config.DB_CONFIG)
            elif config.DB_TYPE == 'mysql':
                self.connection = db_connector.connect(**config.DB_CONFIG)
            
            self.cursor = self.connection.cursor()
            return True
        except Exception as e:
            print(f"Error connecting to database: {e}")
            return False
    
    def disconnect(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
    
    def execute(self, query, params=None):
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return True
        except Exception as e:
            print(f"Error executing query: {e}")
            return False
    
    def fetchall(self):
        try:
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error fetching data: {e}")
            return []
    
    def fetchone(self):
        try:
            return self.cursor.fetchone()
        except Exception as e:
            print(f"Error fetching data: {e}")
            return None
    
    def commit(self):
        try:
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error committing transaction: {e}")
            return False
    
    def rollback(self):
        try:
            self.connection.rollback()
            return True
        except Exception as e:
            print(f"Error rolling back transaction: {e}")
            return False
    
    def get_last_insert_id(self):
        if config.DB_TYPE == 'postgresql':
            return self.cursor.fetchone()[0] if self.cursor.rowcount > 0 else None
        elif config.DB_TYPE == 'mysql':
            return self.cursor.lastrowid

def init_database():
    db = Database()
    if not db.connect():
        return False
    
    if config.DB_TYPE == 'postgresql':
        serial_type = 'SERIAL'
        auto_increment = ''
    else:
        serial_type = 'INT'
        auto_increment = 'AUTO_INCREMENT'
    
    customers_table = f"""
    CREATE TABLE IF NOT EXISTS customers (
        customer_id {serial_type} PRIMARY KEY {auto_increment},
        name VARCHAR(100) NOT NULL,
        phone VARCHAR(20) NOT NULL,
        email VARCHAR(100),
        address TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """
    
    vehicles_table = f"""
    CREATE TABLE IF NOT EXISTS vehicles (
        vehicle_id {serial_type} PRIMARY KEY {auto_increment},
        customer_id INT NOT NULL,
        make VARCHAR(50) NOT NULL,
        model VARCHAR(50) NOT NULL,
        year INT NOT NULL,
        license_plate VARCHAR(20) NOT NULL UNIQUE,
        vin VARCHAR(50),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE
    )
    """
    
    services_table = f"""
    CREATE TABLE IF NOT EXISTS services (
        service_id {serial_type} PRIMARY KEY {auto_increment},
        vehicle_id INT NOT NULL,
        service_date DATE NOT NULL,
        description TEXT NOT NULL,
        labor_cost DECIMAL(10, 2) DEFAULT 0.00,
        parts_cost DECIMAL(10, 2) DEFAULT 0.00,
        total_cost DECIMAL(10, 2) DEFAULT 0.00,
        next_service_date DATE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (vehicle_id) REFERENCES vehicles(vehicle_id) ON DELETE CASCADE
    )
    """
    
    tables = [customers_table, vehicles_table, services_table]
    
    for table_sql in tables:
        if not db.execute(table_sql):
            db.disconnect()
            return False
    
    db.commit()
    db.disconnect()
    return True
