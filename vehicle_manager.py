from database import Database, PLACEHOLDER
from prettytable import PrettyTable
import config

def validate_year(year):
    try:
        year = int(year)
        return 1900 <= year <= 2030
    except:
        return False

def validate_license_plate(plate):
    return plate and len(plate.strip()) > 0

def add_vehicle(customer_id, make, model, year, license_plate, vin=None):
    if not customer_id:
        return False, "Customer ID is required"
    
    if not make or not make.strip():
        return False, "Make cannot be empty"
    
    if not model or not model.strip():
        return False, "Model cannot be empty"
    
    if not validate_year(year):
        return False, "Invalid year (must be between 1900 and 2030)"
    
    if not validate_license_plate(license_plate):
        return False, "License plate cannot be empty"
    
    db = Database()
    if not db.connect():
        return False, "Database connection failed"
    
    if db.execute(f"SELECT customer_id FROM customers WHERE customer_id = {PLACEHOLDER}", (customer_id,)):
        if not db.fetchone():
            db.disconnect()
            return False, "Customer not found"
    
    if db.execute(f"SELECT vehicle_id FROM vehicles WHERE license_plate = {PLACEHOLDER}", (license_plate,)):
        if db.fetchone():
            db.disconnect()
            return False, "Vehicle with this license plate already exists"
    
    query = f"""
    INSERT INTO vehicles (customer_id, make, model, year, license_plate, vin)
    VALUES ({PLACEHOLDER}, {PLACEHOLDER}, {PLACEHOLDER}, {PLACEHOLDER}, {PLACEHOLDER}, {PLACEHOLDER})
    """
    
    if config.DB_TYPE == 'postgresql':
        query += " RETURNING vehicle_id"
    
    if db.execute(query, (customer_id, make, model, int(year), license_plate, vin)):
        if config.DB_TYPE == 'postgresql':
            vehicle_id = db.get_last_insert_id()
        else:
            vehicle_id = db.get_last_insert_id()
        
        db.commit()
        db.disconnect()
        return True, f"Vehicle added successfully (ID: {vehicle_id})"
    else:
        db.disconnect()
        return False, "Failed to add vehicle"

def update_vehicle(vehicle_id, make=None, model=None, year=None, license_plate=None, vin=None):
    if not vehicle_id:
        return False, "Vehicle ID is required"
    
    db = Database()
    if not db.connect():
        return False, "Database connection failed"
    
    if db.execute(f"SELECT vehicle_id FROM vehicles WHERE vehicle_id = {PLACEHOLDER}", (vehicle_id,)):
        if not db.fetchone():
            db.disconnect()
            return False, "Vehicle not found"
    
    updates = []
    values = []
    
    if make and make.strip():
        updates.append(f"make = {PLACEHOLDER}")
        values.append(make)
    
    if model and model.strip():
        updates.append(f"model = {PLACEHOLDER}")
        values.append(model)
    
    if year:
        if not validate_year(year):
            db.disconnect()
            return False, "Invalid year (must be between 1900 and 2030)"
        updates.append(f"year = {PLACEHOLDER}")
        values.append(int(year))
    
    if license_plate:
        if not validate_license_plate(license_plate):
            db.disconnect()
            return False, "License plate cannot be empty"
        updates.append(f"license_plate = {PLACEHOLDER}")
        values.append(license_plate)
    
    if vin is not None:
        updates.append(f"vin = {PLACEHOLDER}")
        values.append(vin)
    
    if not updates:
        db.disconnect()
        return False, "No fields to update"
    
    values.append(vehicle_id)
    query = f"UPDATE vehicles SET {', '.join(updates)} WHERE vehicle_id = {PLACEHOLDER}"
    
    if db.execute(query, tuple(values)):
        db.commit()
        db.disconnect()
        return True, "Vehicle updated successfully"
    else:
        db.disconnect()
        return False, "Failed to update vehicle"

def delete_vehicle(vehicle_id):
    if not vehicle_id:
        return False, "Vehicle ID is required"
    
    db = Database()
    if not db.connect():
        return False, "Database connection failed"
    
    if db.execute(f"SELECT vehicle_id FROM vehicles WHERE vehicle_id = {PLACEHOLDER}", (vehicle_id,)):
        if not db.fetchone():
            db.disconnect()
            return False, "Vehicle not found"
    
    if db.execute(f"DELETE FROM vehicles WHERE vehicle_id = {PLACEHOLDER}", (vehicle_id,)):
        db.commit()
        db.disconnect()
        return True, "Vehicle deleted successfully (all associated services removed)"
    else:
        db.disconnect()
        return False, "Failed to delete vehicle"

def search_vehicles(search_term=None, vehicle_id=None, customer_id=None):
    db = Database()
    if not db.connect():
        return False, "Database connection failed", []
    
    if vehicle_id:
        query = f"""
        SELECT v.*, c.name as customer_name 
        FROM vehicles v 
        JOIN customers c ON v.customer_id = c.customer_id 
        WHERE v.vehicle_id = {PLACEHOLDER}
        """
        db.execute(query, (vehicle_id,))
    elif customer_id:
        query = f"""
        SELECT v.*, c.name as customer_name 
        FROM vehicles v 
        JOIN customers c ON v.customer_id = c.customer_id 
        WHERE v.customer_id = {PLACEHOLDER}
        """
        db.execute(query, (customer_id,))
    elif search_term:
        query = f"""
        SELECT v.*, c.name as customer_name 
        FROM vehicles v 
        JOIN customers c ON v.customer_id = c.customer_id 
        WHERE v.make ILIKE {PLACEHOLDER} OR v.model ILIKE {PLACEHOLDER} OR v.license_plate ILIKE {PLACEHOLDER}
        """ if config.DB_TYPE == 'postgresql' else f"""
        SELECT v.*, c.name as customer_name 
        FROM vehicles v 
        JOIN customers c ON v.customer_id = c.customer_id 
        WHERE v.make LIKE {PLACEHOLDER} OR v.model LIKE {PLACEHOLDER} OR v.license_plate LIKE {PLACEHOLDER}
        """
        search_pattern = f"%{search_term}%"
        db.execute(query, (search_pattern, search_pattern, search_pattern))
    else:
        query = """
        SELECT v.*, c.name as customer_name 
        FROM vehicles v 
        JOIN customers c ON v.customer_id = c.customer_id 
        ORDER BY v.vehicle_id
        """
        db.execute(query)
    
    vehicles = db.fetchall()
    db.disconnect()
    
    return True, f"Found {len(vehicles)} vehicle(s)", vehicles

def display_vehicles(vehicles):
    if not vehicles:
        print("\nNo vehicles found.")
        return
    
    table = PrettyTable()
    table.field_names = ["ID", "Customer", "Make", "Model", "Year", "License Plate", "VIN"]
    
    for vehicle in vehicles:
        table.add_row([
            vehicle[0],
            vehicle[7][:20] if len(vehicle[7]) > 20 else vehicle[7],
            vehicle[2],
            vehicle[3],
            vehicle[4],
            vehicle[5],
            vehicle[6] if vehicle[6] else "N/A"
        ])
    
    print("\n" + str(table))
