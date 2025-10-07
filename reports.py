from database import Database, PLACEHOLDER
from prettytable import PrettyTable
from datetime import datetime

def get_service_history_by_customer(customer_id):
    db = Database()
    if not db.connect():
        return False, "Database connection failed", []
    
    query = f"""
    SELECT 
        s.service_id, s.service_date, s.description, s.labor_cost, s.parts_cost, s.total_cost,
        v.make, v.model, v.license_plate, c.name
    FROM services s
    JOIN vehicles v ON s.vehicle_id = v.vehicle_id
    JOIN customers c ON v.customer_id = c.customer_id
    WHERE c.customer_id = {PLACEHOLDER}
    ORDER BY s.service_date DESC
    """
    
    if not db.execute(query, (customer_id,)):
        db.disconnect()
        return False, "Failed to fetch service history", []
    
    history = db.fetchall()
    db.disconnect()
    
    return True, f"Found {len(history)} service record(s)", history

def get_service_history_by_vehicle(vehicle_id):
    db = Database()
    if not db.connect():
        return False, "Database connection failed", []
    
    query = f"""
    SELECT 
        s.service_id, s.service_date, s.description, s.labor_cost, s.parts_cost, s.total_cost,
        v.make, v.model, v.license_plate, c.name
    FROM services s
    JOIN vehicles v ON s.vehicle_id = v.vehicle_id
    JOIN customers c ON v.customer_id = c.customer_id
    WHERE v.vehicle_id = {PLACEHOLDER}
    ORDER BY s.service_date DESC
    """
    
    if not db.execute(query, (vehicle_id,)):
        db.disconnect()
        return False, "Failed to fetch service history", []
    
    history = db.fetchall()
    db.disconnect()
    
    return True, f"Found {len(history)} service record(s)", history

def display_service_history(history, title="SERVICE HISTORY"):
    if not history:
        print(f"\nNo service history found.")
        return
    
    print(f"\n{'='*80}")
    print(f"{title.center(80)}")
    print(f"{'='*80}")
    
    if history:
        print(f"Customer: {history[0][9]}")
        print(f"Vehicle: {history[0][6]} {history[0][7]} ({history[0][8]})")
        print(f"{'='*80}")
    
    table = PrettyTable()
    table.field_names = ["ID", "Date", "Description", "Labor", "Parts", "Total"]
    
    total_labor = 0
    total_parts = 0
    total_cost = 0
    
    for record in history:
        table.add_row([
            record[0],
            str(record[1]),
            record[2][:35] if len(record[2]) > 35 else record[2],
            f"${record[3]:.2f}",
            f"${record[4]:.2f}",
            f"${record[5]:.2f}"
        ])
        total_labor += record[3]
        total_parts += record[4]
        total_cost += record[5]
    
    print(str(table))
    print(f"{'='*80}")
    print(f"TOTALS - Labor: ${total_labor:.2f} | Parts: ${total_parts:.2f} | Total: ${total_cost:.2f}")
    print(f"{'='*80}")

def export_service_history(history, filename=None):
    if not history:
        return False, "No data to export"
    
    if not filename:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"service_history_{timestamp}.txt"
    
    try:
        with open(filename, 'w') as f:
            f.write("="*80 + "\n")
            f.write("SERVICE HISTORY REPORT\n")
            f.write("="*80 + "\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("="*80 + "\n\n")
            
            if history:
                f.write(f"Customer: {history[0][9]}\n")
                f.write(f"Vehicle: {history[0][6]} {history[0][7]} ({history[0][8]})\n")
                f.write("-"*80 + "\n\n")
            
            total_labor = 0
            total_parts = 0
            total_cost = 0
            
            for record in history:
                f.write(f"Service ID: {record[0]}\n")
                f.write(f"Date: {record[1]}\n")
                f.write(f"Description: {record[2]}\n")
                f.write(f"Labor Cost: ${record[3]:.2f}\n")
                f.write(f"Parts Cost: ${record[4]:.2f}\n")
                f.write(f"Total Cost: ${record[5]:.2f}\n")
                f.write("-"*80 + "\n")
                
                total_labor += record[3]
                total_parts += record[4]
                total_cost += record[5]
            
            f.write("\n" + "="*80 + "\n")
            f.write(f"SUMMARY\n")
            f.write(f"Total Labor Cost: ${total_labor:.2f}\n")
            f.write(f"Total Parts Cost: ${total_parts:.2f}\n")
            f.write(f"Total Amount: ${total_cost:.2f}\n")
            f.write(f"Number of Services: {len(history)}\n")
            f.write("="*80 + "\n")
        
        return True, f"Report exported successfully to {filename}"
    except Exception as e:
        return False, f"Failed to export report: {str(e)}"

def get_all_services_report():
    db = Database()
    if not db.connect():
        return False, "Database connection failed", []
    
    query = """
    SELECT 
        s.service_id, s.service_date, s.description, s.labor_cost, s.parts_cost, s.total_cost,
        v.make, v.model, v.license_plate, c.name, c.phone
    FROM services s
    JOIN vehicles v ON s.vehicle_id = v.vehicle_id
    JOIN customers c ON v.customer_id = c.customer_id
    ORDER BY s.service_date DESC
    """
    
    if not db.execute(query):
        db.disconnect()
        return False, "Failed to fetch services report", []
    
    services = db.fetchall()
    db.disconnect()
    
    return True, f"Found {len(services)} service record(s)", services

def display_all_services_report(services):
    if not services:
        print("\nNo services found.")
        return
    
    print(f"\n{'='*100}")
    print("ALL SERVICES REPORT".center(100))
    print(f"{'='*100}")
    
    table = PrettyTable()
    table.field_names = ["ID", "Date", "Customer", "Vehicle", "Description", "Labor", "Parts", "Total"]
    
    total_labor = 0
    total_parts = 0
    total_cost = 0
    
    for service in services:
        vehicle_info = f"{service[6]} {service[7]}"
        table.add_row([
            service[0],
            str(service[1]),
            service[9][:15] if len(service[9]) > 15 else service[9],
            vehicle_info[:20] if len(vehicle_info) > 20 else vehicle_info,
            service[2][:25] if len(service[2]) > 25 else service[2],
            f"${service[3]:.2f}",
            f"${service[4]:.2f}",
            f"${service[5]:.2f}"
        ])
        total_labor += service[3]
        total_parts += service[4]
        total_cost += service[5]
    
    print(str(table))
    print(f"{'='*100}")
    print(f"TOTALS - Services: {len(services)} | Labor: ${total_labor:.2f} | Parts: ${total_parts:.2f} | Total: ${total_cost:.2f}")
    print(f"{'='*100}")
