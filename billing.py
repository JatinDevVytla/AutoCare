from database import Database, PLACEHOLDER
from prettytable import PrettyTable
from datetime import datetime
import config

def generate_invoice(service_id):
    db = Database()
    if not db.connect():
        return False, "Database connection failed"
    
    query = f"""
    SELECT 
        s.service_id, s.service_date, s.description, s.labor_cost, s.parts_cost, s.total_cost,
        v.make, v.model, v.year, v.license_plate,
        c.customer_id, c.name, c.phone, c.email, c.address
    FROM services s
    JOIN vehicles v ON s.vehicle_id = v.vehicle_id
    JOIN customers c ON v.customer_id = c.customer_id
    WHERE s.service_id = {PLACEHOLDER}
    """
    
    if not db.execute(query, (service_id,)):
        db.disconnect()
        return False, "Failed to fetch service details"
    
    service = db.fetchone()
    db.disconnect()
    
    if not service:
        return False, "Service not found"
    
    invoice = generate_invoice_text(service)
    return True, invoice

def generate_invoice_text(service):
    service_id = service[0]
    service_date = service[1]
    description = service[2]
    labor_cost = service[3]
    parts_cost = service[4]
    total_cost = service[5]
    
    vehicle = f"{service[6]} {service[7]} {service[8]}"
    license_plate = service[9]
    
    customer_id = service[10]
    customer_name = service[11]
    customer_phone = service[12]
    customer_email = service[13] if service[13] else "N/A"
    customer_address = service[14] if service[14] else "N/A"
    
    subtotal = labor_cost + parts_cost
    tax = subtotal * config.TAX_RATE
    
    invoice = f"""
{'='*70}
                        VEHICLE SERVICE INVOICE
{'='*70}

Invoice #: {service_id}
Date: {service_date}
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

{'-'*70}
CUSTOMER INFORMATION
{'-'*70}
Customer ID: {customer_id}
Name: {customer_name}
Phone: {customer_phone}
Email: {customer_email}
Address: {customer_address}

{'-'*70}
VEHICLE INFORMATION
{'-'*70}
Vehicle: {vehicle}
License Plate: {license_plate}

{'-'*70}
SERVICE DETAILS
{'-'*70}
Description: {description}

{'-'*70}
CHARGES
{'-'*70}
Labor Cost:                                  ${labor_cost:>10.2f}
Parts Cost:                                  ${parts_cost:>10.2f}
                                             {'-'*15}
Subtotal:                                    ${subtotal:>10.2f}
Tax ({config.TAX_RATE*100}%):                                      ${tax:>10.2f}
                                             {'='*15}
TOTAL:                                       ${total_cost:>10.2f}
                                             {'='*15}

{'='*70}
                    Thank you for your business!
{'='*70}
"""
    return invoice

def calculate_bill(labor_cost, parts_cost):
    try:
        labor = float(labor_cost)
        parts = float(parts_cost)
        
        if labor < 0 or parts < 0:
            return False, "Costs cannot be negative", None
        
        subtotal = labor + parts
        tax = subtotal * config.TAX_RATE
        total = subtotal + tax
        
        bill_details = {
            'labor_cost': labor,
            'parts_cost': parts,
            'subtotal': subtotal,
            'tax': tax,
            'tax_rate': config.TAX_RATE * 100,
            'total': total
        }
        
        return True, "Bill calculated successfully", bill_details
    except ValueError:
        return False, "Invalid cost values", None

def display_bill(bill_details):
    if not bill_details:
        print("\nNo bill details to display.")
        return
    
    print("\n" + "="*50)
    print("               BILL CALCULATION")
    print("="*50)
    print(f"Labor Cost:                      ${bill_details['labor_cost']:>10.2f}")
    print(f"Parts Cost:                      ${bill_details['parts_cost']:>10.2f}")
    print("-"*50)
    print(f"Subtotal:                        ${bill_details['subtotal']:>10.2f}")
    print(f"Tax ({bill_details['tax_rate']}%):                           ${bill_details['tax']:>10.2f}")
    print("="*50)
    print(f"TOTAL:                           ${bill_details['total']:>10.2f}")
    print("="*50)

def get_customer_billing_summary(customer_id):
    db = Database()
    if not db.connect():
        return False, "Database connection failed", None
    
    query = f"""
    SELECT 
        c.customer_id, c.name, c.phone,
        COUNT(s.service_id) as total_services,
        SUM(s.total_cost) as total_spent
    FROM customers c
    LEFT JOIN vehicles v ON c.customer_id = v.customer_id
    LEFT JOIN services s ON v.vehicle_id = s.vehicle_id
    WHERE c.customer_id = {PLACEHOLDER}
    GROUP BY c.customer_id, c.name, c.phone
    """
    
    if not db.execute(query, (customer_id,)):
        db.disconnect()
        return False, "Failed to fetch billing summary", None
    
    summary = db.fetchone()
    db.disconnect()
    
    if not summary:
        return False, "Customer not found", None
    
    return True, "Billing summary retrieved", summary

def display_billing_summary(summary):
    if not summary:
        print("\nNo billing summary available.")
        return
    
    print("\n" + "="*60)
    print("              CUSTOMER BILLING SUMMARY")
    print("="*60)
    print(f"Customer ID: {summary[0]}")
    print(f"Name: {summary[1]}")
    print(f"Phone: {summary[2]}")
    print("-"*60)
    print(f"Total Services: {summary[3] if summary[3] else 0}")
    print(f"Total Amount Spent: ${summary[4] if summary[4] else 0:.2f}")
    print("="*60)
