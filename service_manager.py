from database import Database, PLACEHOLDER
from prettytable import PrettyTable
from datetime import datetime, timedelta
import config

def validate_date(date_str):
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except:
        return False

def validate_cost(cost):
    try:
        cost = float(cost)
        return cost >= 0
    except:
        return False

def calculate_next_service_date(service_date_str):
    try:
        service_date = datetime.strptime(service_date_str, '%Y-%m-%d')
        next_date = service_date + timedelta(days=config.SERVICE_INTERVAL_DAYS)
        return next_date.strftime('%Y-%m-%d')
    except:
        return None

def add_service(vehicle_id, service_date, description, labor_cost=0, parts_cost=0):
    if not vehicle_id:
        return False, "Vehicle ID is required"
    
    if not service_date or not validate_date(service_date):
        return False, "Invalid service date (use YYYY-MM-DD format)"
    
    if not description or not description.strip():
        return False, "Description cannot be empty"
    
    if not validate_cost(labor_cost):
        return False, "Invalid labor cost"
    
    if not validate_cost(parts_cost):
        return False, "Invalid parts cost"
    
    db = Database()
    if not db.connect():
        return False, "Database connection failed"
    
    if db.execute(f"SELECT vehicle_id FROM vehicles WHERE vehicle_id = {PLACEHOLDER}", (vehicle_id,)):
        if not db.fetchone():
            db.disconnect()
            return False, "Vehicle not found"
    
    labor_cost = float(labor_cost)
    parts_cost = float(parts_cost)
    subtotal = labor_cost + parts_cost
    tax = subtotal * config.TAX_RATE
    total_cost = subtotal + tax
    
    next_service_date = calculate_next_service_date(service_date)
    
    query = f"""
    INSERT INTO services (vehicle_id, service_date, description, labor_cost, parts_cost, total_cost, next_service_date)
    VALUES ({PLACEHOLDER}, {PLACEHOLDER}, {PLACEHOLDER}, {PLACEHOLDER}, {PLACEHOLDER}, {PLACEHOLDER}, {PLACEHOLDER})
    """
    
    if config.DB_TYPE == 'postgresql':
        query += " RETURNING service_id"
    
    if db.execute(query, (vehicle_id, service_date, description, labor_cost, parts_cost, total_cost, next_service_date)):
        if config.DB_TYPE == 'postgresql':
            service_id = db.get_last_insert_id()
        else:
            service_id = db.get_last_insert_id()
        
        db.commit()
        db.disconnect()
        return True, f"Service added successfully (ID: {service_id}, Total: ${total_cost:.2f}, Next Service: {next_service_date})"
    else:
        db.disconnect()
        return False, "Failed to add service"

def update_service(service_id, service_date=None, description=None, labor_cost=None, parts_cost=None):
    if not service_id:
        return False, "Service ID is required"
    
    db = Database()
    if not db.connect():
        return False, "Database connection failed"
    
    if db.execute(f"SELECT * FROM services WHERE service_id = {PLACEHOLDER}", (service_id,)):
        service = db.fetchone()
        if not service:
            db.disconnect()
            return False, "Service not found"
    else:
        db.disconnect()
        return False, "Failed to fetch service"
    
    current_labor = service[4]
    current_parts = service[5]
    
    updates = []
    values = []
    
    if service_date:
        if not validate_date(service_date):
            db.disconnect()
            return False, "Invalid service date (use YYYY-MM-DD format)"
        updates.append(f"service_date = {PLACEHOLDER}")
        values.append(service_date)
        next_service_date = calculate_next_service_date(service_date)
        updates.append(f"next_service_date = {PLACEHOLDER}")
        values.append(next_service_date)
    
    if description and description.strip():
        updates.append(f"description = {PLACEHOLDER}")
        values.append(description)
    
    if labor_cost is not None:
        if not validate_cost(labor_cost):
            db.disconnect()
            return False, "Invalid labor cost"
        current_labor = float(labor_cost)
        updates.append(f"labor_cost = {PLACEHOLDER}")
        values.append(current_labor)
    
    if parts_cost is not None:
        if not validate_cost(parts_cost):
            db.disconnect()
            return False, "Invalid parts cost"
        current_parts = float(parts_cost)
        updates.append(f"parts_cost = {PLACEHOLDER}")
        values.append(current_parts)
    
    if labor_cost is not None or parts_cost is not None:
        subtotal = current_labor + current_parts
        tax = subtotal * config.TAX_RATE
        total_cost = subtotal + tax
        updates.append(f"total_cost = {PLACEHOLDER}")
        values.append(total_cost)
    
    if not updates:
        db.disconnect()
        return False, "No fields to update"
    
    values.append(service_id)
    query = f"UPDATE services SET {', '.join(updates)} WHERE service_id = {PLACEHOLDER}"
    
    if db.execute(query, tuple(values)):
        db.commit()
        db.disconnect()
        return True, "Service updated successfully"
    else:
        db.disconnect()
        return False, "Failed to update service"

def delete_service(service_id):
    if not service_id:
        return False, "Service ID is required"
    
    db = Database()
    if not db.connect():
        return False, "Database connection failed"
    
    if db.execute(f"SELECT service_id FROM services WHERE service_id = {PLACEHOLDER}", (service_id,)):
        if not db.fetchone():
            db.disconnect()
            return False, "Service not found"
    
    if db.execute(f"DELETE FROM services WHERE service_id = {PLACEHOLDER}", (service_id,)):
        db.commit()
        db.disconnect()
        return True, "Service deleted successfully"
    else:
        db.disconnect()
        return False, "Failed to delete service"

def search_services(vehicle_id=None, service_id=None):
    db = Database()
    if not db.connect():
        return False, "Database connection failed", []
    
    if service_id:
        query = f"""
        SELECT s.*, v.make, v.model, v.license_plate, c.name as customer_name
        FROM services s
        JOIN vehicles v ON s.vehicle_id = v.vehicle_id
        JOIN customers c ON v.customer_id = c.customer_id
        WHERE s.service_id = {PLACEHOLDER}
        """
        db.execute(query, (service_id,))
    elif vehicle_id:
        query = f"""
        SELECT s.*, v.make, v.model, v.license_plate, c.name as customer_name
        FROM services s
        JOIN vehicles v ON s.vehicle_id = v.vehicle_id
        JOIN customers c ON v.customer_id = c.customer_id
        WHERE s.vehicle_id = {PLACEHOLDER}
        ORDER BY s.service_date DESC
        """
        db.execute(query, (vehicle_id,))
    else:
        query = """
        SELECT s.*, v.make, v.model, v.license_plate, c.name as customer_name
        FROM services s
        JOIN vehicles v ON s.vehicle_id = v.vehicle_id
        JOIN customers c ON v.customer_id = c.customer_id
        ORDER BY s.service_date DESC
        """
        db.execute(query)
    
    services = db.fetchall()
    db.disconnect()
    
    return True, f"Found {len(services)} service(s)", services

def display_services(services):
    if not services:
        print("\nNo services found.")
        return
    
    table = PrettyTable()
    table.field_names = ["ID", "Vehicle", "Customer", "Date", "Description", "Labor", "Parts", "Total", "Next Service"]
    
    for service in services:
        vehicle_info = f"{service[9]} {service[10]} ({service[11]})"
        table.add_row([
            service[0],
            vehicle_info[:25] if len(vehicle_info) > 25 else vehicle_info,
            service[12][:15] if len(service[12]) > 15 else service[12],
            str(service[2]),
            service[3][:20] if len(service[3]) > 20 else service[3],
            f"${service[4]:.2f}",
            f"${service[5]:.2f}",
            f"${service[6]:.2f}",
            str(service[7]) if service[7] else "N/A"
        ])
    
    print("\n" + str(table))

def get_service_reminders():
    db = Database()
    if not db.connect():
        return False, "Database connection failed", []
    
    today = datetime.now().date()
    reminder_date = (today + timedelta(days=config.REMINDER_DAYS)).strftime('%Y-%m-%d')
    
    query = f"""
    SELECT s.*, v.make, v.model, v.license_plate, c.name as customer_name, c.phone
    FROM services s
    JOIN vehicles v ON s.vehicle_id = v.vehicle_id
    JOIN customers c ON v.customer_id = c.customer_id
    WHERE s.next_service_date IS NOT NULL 
    AND s.next_service_date <= {PLACEHOLDER}
    AND s.next_service_date >= {PLACEHOLDER}
    ORDER BY s.next_service_date
    """
    
    db.execute(query, (reminder_date, today.strftime('%Y-%m-%d')))
    reminders = db.fetchall()
    db.disconnect()
    
    return True, f"Found {len(reminders)} reminder(s)", reminders

def display_reminders(reminders):
    if not reminders:
        print("\nNo service reminders for the next 7 days.")
        return
    
    table = PrettyTable()
    table.field_names = ["Vehicle", "License Plate", "Customer", "Phone", "Next Service Date", "Days Left"]
    
    today = datetime.now().date()
    
    for reminder in reminders:
        next_service = datetime.strptime(str(reminder[7]), '%Y-%m-%d').date()
        days_left = (next_service - today).days
        
        vehicle_info = f"{reminder[9]} {reminder[10]}"
        table.add_row([
            vehicle_info[:25] if len(vehicle_info) > 25 else vehicle_info,
            reminder[11],
            reminder[12][:20] if len(reminder[12]) > 20 else reminder[12],
            reminder[13],
            str(reminder[7]),
            days_left
        ])
    
    print("\n=== SERVICE REMINDERS (Next 7 Days) ===")
    print(str(table))
