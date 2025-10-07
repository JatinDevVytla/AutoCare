from database import Database, PLACEHOLDER
from prettytable import PrettyTable
import re
import config

def validate_phone(phone):
    pattern = r'^\+?[\d\s\-\(\)]+$'
    return re.match(pattern, phone) is not None

def validate_email(email):
    if not email:
        return True
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def add_customer(name, phone, email=None, address=None):
    if not name or not name.strip():
        return False, "Name cannot be empty"
    
    if not phone or not phone.strip():
        return False, "Phone number cannot be empty"
    
    if not validate_phone(phone):
        return False, "Invalid phone number format"
    
    if email and not validate_email(email):
        return False, "Invalid email format"
    
    db = Database()
    if not db.connect():
        return False, "Database connection failed"
    
    try:
        if db.execute(
            f"SELECT customer_id FROM customers WHERE phone = {PLACEHOLDER}",
            (phone,)
        ):
            if db.fetchone():
                db.disconnect()
                return False, "Customer with this phone number already exists"
        
        query = f"""
        INSERT INTO customers (name, phone, email, address)
        VALUES ({PLACEHOLDER}, {PLACEHOLDER}, {PLACEHOLDER}, {PLACEHOLDER})
        """
        
        if config.DB_TYPE == 'postgresql':
            query += " RETURNING customer_id"
        
        if db.execute(query, (name, phone, email, address)):
            if config.DB_TYPE == 'postgresql':
                customer_id = db.get_last_insert_id()
            else:
                customer_id = db.get_last_insert_id()
            
            db.commit()
            db.disconnect()
            return True, f"Customer added successfully (ID: {customer_id})"
        else:
            db.disconnect()
            return False, "Failed to add customer"
    except Exception as e:
        db.disconnect()
        return False, f"Error: {str(e)}"

def update_customer(customer_id, name=None, phone=None, email=None, address=None):
    if not customer_id:
        return False, "Customer ID is required"
    
    db = Database()
    if not db.connect():
        return False, "Database connection failed"
    
    if db.execute(f"SELECT customer_id FROM customers WHERE customer_id = {PLACEHOLDER}", (customer_id,)):
        if not db.fetchone():
            db.disconnect()
            return False, "Customer not found"
    
    updates = []
    values = []
    
    if name and name.strip():
        updates.append(f"name = {PLACEHOLDER}")
        values.append(name)
    
    if phone and phone.strip():
        if not validate_phone(phone):
            db.disconnect()
            return False, "Invalid phone number format"
        updates.append(f"phone = {PLACEHOLDER}")
        values.append(phone)
    
    if email is not None:
        if email and not validate_email(email):
            db.disconnect()
            return False, "Invalid email format"
        updates.append(f"email = {PLACEHOLDER}")
        values.append(email)
    
    if address is not None:
        updates.append(f"address = {PLACEHOLDER}")
        values.append(address)
    
    if not updates:
        db.disconnect()
        return False, "No fields to update"
    
    values.append(customer_id)
    query = f"UPDATE customers SET {', '.join(updates)} WHERE customer_id = {PLACEHOLDER}"
    
    if db.execute(query, tuple(values)):
        db.commit()
        db.disconnect()
        return True, "Customer updated successfully"
    else:
        db.disconnect()
        return False, "Failed to update customer"

def delete_customer(customer_id):
    if not customer_id:
        return False, "Customer ID is required"
    
    db = Database()
    if not db.connect():
        return False, "Database connection failed"
    
    if db.execute(f"SELECT customer_id FROM customers WHERE customer_id = {PLACEHOLDER}", (customer_id,)):
        if not db.fetchone():
            db.disconnect()
            return False, "Customer not found"
    
    if db.execute(f"DELETE FROM customers WHERE customer_id = {PLACEHOLDER}", (customer_id,)):
        db.commit()
        db.disconnect()
        return True, "Customer deleted successfully (all associated vehicles and services removed)"
    else:
        db.disconnect()
        return False, "Failed to delete customer"

def search_customers(search_term=None, customer_id=None):
    db = Database()
    if not db.connect():
        return False, "Database connection failed", []
    
    if customer_id:
        query = f"SELECT * FROM customers WHERE customer_id = {PLACEHOLDER}"
        db.execute(query, (customer_id,))
    elif search_term:
        query = f"""
        SELECT * FROM customers 
        WHERE name ILIKE {PLACEHOLDER} OR phone LIKE {PLACEHOLDER} OR email ILIKE {PLACEHOLDER}
        """ if config.DB_TYPE == 'postgresql' else f"""
        SELECT * FROM customers 
        WHERE name LIKE {PLACEHOLDER} OR phone LIKE {PLACEHOLDER} OR email LIKE {PLACEHOLDER}
        """
        search_pattern = f"%{search_term}%"
        db.execute(query, (search_pattern, search_pattern, search_pattern))
    else:
        query = "SELECT * FROM customers ORDER BY customer_id"
        db.execute(query)
    
    customers = db.fetchall()
    db.disconnect()
    
    return True, f"Found {len(customers)} customer(s)", customers

def display_customers(customers):
    if not customers:
        print("\nNo customers found.")
        return
    
    table = PrettyTable()
    table.field_names = ["ID", "Name", "Phone", "Email", "Address", "Created"]
    
    for customer in customers:
        table.add_row([
            customer[0],
            customer[1][:30] if len(customer[1]) > 30 else customer[1],
            customer[2],
            customer[3] if customer[3] else "N/A",
            customer[4][:30] if customer[4] and len(customer[4]) > 30 else (customer[4] if customer[4] else "N/A"),
            str(customer[5])[:19] if customer[5] else "N/A"
        ])
    
    print("\n" + str(table))
