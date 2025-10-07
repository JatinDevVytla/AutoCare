#!/usr/bin/env python3

import os
import sys
from database import init_database
import customer_manager as cm
import vehicle_manager as vm
import service_manager as sm
import billing
import reports

def clear_screen():
    os.system('clear' if os.name != 'nt' else 'cls')

def pause():
    input("\nPress Enter to continue...")

def print_header(title):
    print("\n" + "="*70)
    print(title.center(70))
    print("="*70)

def main_menu():
    while True:
        clear_screen()
        print_header("VEHICLE SERVICE MANAGEMENT SYSTEM")
        print("\n1.  Customer Management")
        print("2.  Vehicle Management")
        print("3.  Service Management")
        print("4.  Service Reminders")
        print("5.  Billing & Invoices")
        print("6.  Reports")
        print("7.  Exit")
        print("\n" + "="*70)
        
        choice = input("\nEnter your choice (1-7): ").strip()
        
        if choice == '1':
            customer_menu()
        elif choice == '2':
            vehicle_menu()
        elif choice == '3':
            service_menu()
        elif choice == '4':
            reminders_menu()
        elif choice == '5':
            billing_menu()
        elif choice == '6':
            reports_menu()
        elif choice == '7':
            print("\nThank you for using Vehicle Service Management System!")
            sys.exit(0)
        else:
            print("\nInvalid choice. Please try again.")
            pause()

def customer_menu():
    while True:
        clear_screen()
        print_header("CUSTOMER MANAGEMENT")
        print("\n1. Add Customer")
        print("2. Update Customer")
        print("3. Delete Customer")
        print("4. Search Customers")
        print("5. View All Customers")
        print("6. Back to Main Menu")
        print("\n" + "="*70)
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == '1':
            add_customer()
        elif choice == '2':
            update_customer()
        elif choice == '3':
            delete_customer()
        elif choice == '4':
            search_customers()
        elif choice == '5':
            view_all_customers()
        elif choice == '6':
            break
        else:
            print("\nInvalid choice. Please try again.")
            pause()

def add_customer():
    clear_screen()
    print_header("ADD NEW CUSTOMER")
    
    name = input("\nEnter customer name: ").strip()
    phone = input("Enter phone number: ").strip()
    email = input("Enter email (optional): ").strip()
    address = input("Enter address (optional): ").strip()
    
    if not email:
        email = None
    if not address:
        address = None
    
    success, message = cm.add_customer(name, phone, email, address)
    print(f"\n{message}")
    pause()

def update_customer():
    clear_screen()
    print_header("UPDATE CUSTOMER")
    
    try:
        customer_id = int(input("\nEnter customer ID: ").strip())
    except ValueError:
        print("\nInvalid customer ID.")
        pause()
        return
    
    print("\nLeave blank to keep current value:")
    name = input("Enter new name: ").strip()
    phone = input("Enter new phone: ").strip()
    email = input("Enter new email: ").strip()
    address = input("Enter new address: ").strip()
    
    success, message = cm.update_customer(
        customer_id,
        name if name else None,
        phone if phone else None,
        email if email else None,
        address if address else None
    )
    print(f"\n{message}")
    pause()

def delete_customer():
    clear_screen()
    print_header("DELETE CUSTOMER")
    
    try:
        customer_id = int(input("\nEnter customer ID to delete: ").strip())
    except ValueError:
        print("\nInvalid customer ID.")
        pause()
        return
    
    confirm = input(f"\nAre you sure you want to delete customer {customer_id}? (yes/no): ").strip().lower()
    if confirm == 'yes':
        success, message = cm.delete_customer(customer_id)
        print(f"\n{message}")
    else:
        print("\nDeletion cancelled.")
    pause()

def search_customers():
    clear_screen()
    print_header("SEARCH CUSTOMERS")
    
    search_term = input("\nEnter search term (name, phone, or email): ").strip()
    
    success, message, customers = cm.search_customers(search_term=search_term)
    print(f"\n{message}")
    cm.display_customers(customers)
    pause()

def view_all_customers():
    clear_screen()
    print_header("ALL CUSTOMERS")
    
    success, message, customers = cm.search_customers()
    print(f"\n{message}")
    cm.display_customers(customers)
    pause()

def vehicle_menu():
    while True:
        clear_screen()
        print_header("VEHICLE MANAGEMENT")
        print("\n1. Add Vehicle")
        print("2. Update Vehicle")
        print("3. Delete Vehicle")
        print("4. Search Vehicles")
        print("5. View All Vehicles")
        print("6. View Customer Vehicles")
        print("7. Back to Main Menu")
        print("\n" + "="*70)
        
        choice = input("\nEnter your choice (1-7): ").strip()
        
        if choice == '1':
            add_vehicle()
        elif choice == '2':
            update_vehicle()
        elif choice == '3':
            delete_vehicle()
        elif choice == '4':
            search_vehicles()
        elif choice == '5':
            view_all_vehicles()
        elif choice == '6':
            view_customer_vehicles()
        elif choice == '7':
            break
        else:
            print("\nInvalid choice. Please try again.")
            pause()

def add_vehicle():
    clear_screen()
    print_header("ADD NEW VEHICLE")
    
    try:
        customer_id = int(input("\nEnter customer ID: ").strip())
    except ValueError:
        print("\nInvalid customer ID.")
        pause()
        return
    
    make = input("Enter vehicle make: ").strip()
    model = input("Enter vehicle model: ").strip()
    year = input("Enter vehicle year: ").strip()
    license_plate = input("Enter license plate: ").strip()
    vin = input("Enter VIN (optional): ").strip()
    
    if not vin:
        vin = None
    
    success, message = vm.add_vehicle(customer_id, make, model, year, license_plate, vin)
    print(f"\n{message}")
    pause()

def update_vehicle():
    clear_screen()
    print_header("UPDATE VEHICLE")
    
    try:
        vehicle_id = int(input("\nEnter vehicle ID: ").strip())
    except ValueError:
        print("\nInvalid vehicle ID.")
        pause()
        return
    
    print("\nLeave blank to keep current value:")
    make = input("Enter new make: ").strip()
    model = input("Enter new model: ").strip()
    year = input("Enter new year: ").strip()
    license_plate = input("Enter new license plate: ").strip()
    vin = input("Enter new VIN: ").strip()
    
    success, message = vm.update_vehicle(
        vehicle_id,
        make if make else None,
        model if model else None,
        year if year else None,
        license_plate if license_plate else None,
        vin if vin else None
    )
    print(f"\n{message}")
    pause()

def delete_vehicle():
    clear_screen()
    print_header("DELETE VEHICLE")
    
    try:
        vehicle_id = int(input("\nEnter vehicle ID to delete: ").strip())
    except ValueError:
        print("\nInvalid vehicle ID.")
        pause()
        return
    
    confirm = input(f"\nAre you sure you want to delete vehicle {vehicle_id}? (yes/no): ").strip().lower()
    if confirm == 'yes':
        success, message = vm.delete_vehicle(vehicle_id)
        print(f"\n{message}")
    else:
        print("\nDeletion cancelled.")
    pause()

def search_vehicles():
    clear_screen()
    print_header("SEARCH VEHICLES")
    
    search_term = input("\nEnter search term (make, model, or license plate): ").strip()
    
    success, message, vehicles = vm.search_vehicles(search_term=search_term)
    print(f"\n{message}")
    vm.display_vehicles(vehicles)
    pause()

def view_all_vehicles():
    clear_screen()
    print_header("ALL VEHICLES")
    
    success, message, vehicles = vm.search_vehicles()
    print(f"\n{message}")
    vm.display_vehicles(vehicles)
    pause()

def view_customer_vehicles():
    clear_screen()
    print_header("CUSTOMER VEHICLES")
    
    try:
        customer_id = int(input("\nEnter customer ID: ").strip())
    except ValueError:
        print("\nInvalid customer ID.")
        pause()
        return
    
    success, message, vehicles = vm.search_vehicles(customer_id=customer_id)
    print(f"\n{message}")
    vm.display_vehicles(vehicles)
    pause()

def service_menu():
    while True:
        clear_screen()
        print_header("SERVICE MANAGEMENT")
        print("\n1. Add Service Record")
        print("2. Update Service Record")
        print("3. Delete Service Record")
        print("4. View Vehicle Services")
        print("5. View All Services")
        print("6. Back to Main Menu")
        print("\n" + "="*70)
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == '1':
            add_service()
        elif choice == '2':
            update_service()
        elif choice == '3':
            delete_service()
        elif choice == '4':
            view_vehicle_services()
        elif choice == '5':
            view_all_services()
        elif choice == '6':
            break
        else:
            print("\nInvalid choice. Please try again.")
            pause()

def add_service():
    clear_screen()
    print_header("ADD SERVICE RECORD")
    
    try:
        vehicle_id = int(input("\nEnter vehicle ID: ").strip())
    except ValueError:
        print("\nInvalid vehicle ID.")
        pause()
        return
    
    service_date = input("Enter service date (YYYY-MM-DD): ").strip()
    description = input("Enter service description: ").strip()
    
    try:
        labor_cost = float(input("Enter labor cost: ").strip())
        parts_cost = float(input("Enter parts cost: ").strip())
    except ValueError:
        print("\nInvalid cost value.")
        pause()
        return
    
    success, message = sm.add_service(vehicle_id, service_date, description, labor_cost, parts_cost)
    print(f"\n{message}")
    pause()

def update_service():
    clear_screen()
    print_header("UPDATE SERVICE RECORD")
    
    try:
        service_id = int(input("\nEnter service ID: ").strip())
    except ValueError:
        print("\nInvalid service ID.")
        pause()
        return
    
    print("\nLeave blank to keep current value:")
    service_date = input("Enter new service date (YYYY-MM-DD): ").strip()
    description = input("Enter new description: ").strip()
    labor_cost = input("Enter new labor cost: ").strip()
    parts_cost = input("Enter new parts cost: ").strip()
    
    success, message = sm.update_service(
        service_id,
        service_date if service_date else None,
        description if description else None,
        float(labor_cost) if labor_cost else None,
        float(parts_cost) if parts_cost else None
    )
    print(f"\n{message}")
    pause()

def delete_service():
    clear_screen()
    print_header("DELETE SERVICE RECORD")
    
    try:
        service_id = int(input("\nEnter service ID to delete: ").strip())
    except ValueError:
        print("\nInvalid service ID.")
        pause()
        return
    
    confirm = input(f"\nAre you sure you want to delete service {service_id}? (yes/no): ").strip().lower()
    if confirm == 'yes':
        success, message = sm.delete_service(service_id)
        print(f"\n{message}")
    else:
        print("\nDeletion cancelled.")
    pause()

def view_vehicle_services():
    clear_screen()
    print_header("VEHICLE SERVICES")
    
    try:
        vehicle_id = int(input("\nEnter vehicle ID: ").strip())
    except ValueError:
        print("\nInvalid vehicle ID.")
        pause()
        return
    
    success, message, services = sm.search_services(vehicle_id=vehicle_id)
    print(f"\n{message}")
    sm.display_services(services)
    pause()

def view_all_services():
    clear_screen()
    print_header("ALL SERVICES")
    
    success, message, services = sm.search_services()
    print(f"\n{message}")
    sm.display_services(services)
    pause()

def reminders_menu():
    clear_screen()
    print_header("SERVICE REMINDERS")
    
    success, message, reminders = sm.get_service_reminders()
    print(f"\n{message}")
    sm.display_reminders(reminders)
    pause()

def billing_menu():
    while True:
        clear_screen()
        print_header("BILLING & INVOICES")
        print("\n1. Generate Invoice")
        print("2. Calculate Bill")
        print("3. Customer Billing Summary")
        print("4. Back to Main Menu")
        print("\n" + "="*70)
        
        choice = input("\nEnter your choice (1-4): ").strip()
        
        if choice == '1':
            generate_invoice()
        elif choice == '2':
            calculate_bill()
        elif choice == '3':
            customer_billing_summary()
        elif choice == '4':
            break
        else:
            print("\nInvalid choice. Please try again.")
            pause()

def generate_invoice():
    clear_screen()
    print_header("GENERATE INVOICE")
    
    try:
        service_id = int(input("\nEnter service ID: ").strip())
    except ValueError:
        print("\nInvalid service ID.")
        pause()
        return
    
    success, invoice = billing.generate_invoice(service_id)
    if success:
        print(invoice)
        
        save = input("\nSave invoice to file? (yes/no): ").strip().lower()
        if save == 'yes':
            filename = input("Enter filename (press Enter for default): ").strip()
            if not filename:
                from datetime import datetime
                filename = f"invoice_{service_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            
            try:
                with open(filename, 'w') as f:
                    f.write(invoice)
                print(f"\nInvoice saved to {filename}")
            except Exception as e:
                print(f"\nFailed to save invoice: {e}")
    else:
        print(f"\n{invoice}")
    
    pause()

def calculate_bill():
    clear_screen()
    print_header("CALCULATE BILL")
    
    try:
        labor_cost = float(input("\nEnter labor cost: ").strip())
        parts_cost = float(input("Enter parts cost: ").strip())
    except ValueError:
        print("\nInvalid cost value.")
        pause()
        return
    
    success, message, bill_details = billing.calculate_bill(labor_cost, parts_cost)
    if success:
        billing.display_bill(bill_details)
    else:
        print(f"\n{message}")
    pause()

def customer_billing_summary():
    clear_screen()
    print_header("CUSTOMER BILLING SUMMARY")
    
    try:
        customer_id = int(input("\nEnter customer ID: ").strip())
    except ValueError:
        print("\nInvalid customer ID.")
        pause()
        return
    
    success, message, summary = billing.get_customer_billing_summary(customer_id)
    if success:
        billing.display_billing_summary(summary)
    else:
        print(f"\n{message}")
    pause()

def reports_menu():
    while True:
        clear_screen()
        print_header("REPORTS")
        print("\n1. Service History by Customer")
        print("2. Service History by Vehicle")
        print("3. All Services Report")
        print("4. Export Service History")
        print("5. Back to Main Menu")
        print("\n" + "="*70)
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            service_history_by_customer()
        elif choice == '2':
            service_history_by_vehicle()
        elif choice == '3':
            all_services_report()
        elif choice == '4':
            export_service_history()
        elif choice == '5':
            break
        else:
            print("\nInvalid choice. Please try again.")
            pause()

def service_history_by_customer():
    clear_screen()
    print_header("SERVICE HISTORY BY CUSTOMER")
    
    try:
        customer_id = int(input("\nEnter customer ID: ").strip())
    except ValueError:
        print("\nInvalid customer ID.")
        pause()
        return
    
    success, message, history = reports.get_service_history_by_customer(customer_id)
    if success:
        reports.display_service_history(history, "SERVICE HISTORY BY CUSTOMER")
    else:
        print(f"\n{message}")
    pause()

def service_history_by_vehicle():
    clear_screen()
    print_header("SERVICE HISTORY BY VEHICLE")
    
    try:
        vehicle_id = int(input("\nEnter vehicle ID: ").strip())
    except ValueError:
        print("\nInvalid vehicle ID.")
        pause()
        return
    
    success, message, history = reports.get_service_history_by_vehicle(vehicle_id)
    if success:
        reports.display_service_history(history, "SERVICE HISTORY BY VEHICLE")
    else:
        print(f"\n{message}")
    pause()

def all_services_report():
    clear_screen()
    print_header("ALL SERVICES REPORT")
    
    success, message, services = reports.get_all_services_report()
    if success:
        reports.display_all_services_report(services)
    else:
        print(f"\n{message}")
    pause()

def export_service_history():
    clear_screen()
    print_header("EXPORT SERVICE HISTORY")
    
    print("\n1. Export by Customer")
    print("2. Export by Vehicle")
    choice = input("\nEnter your choice (1-2): ").strip()
    
    history = []
    
    if choice == '1':
        try:
            customer_id = int(input("\nEnter customer ID: ").strip())
            success, message, history = reports.get_service_history_by_customer(customer_id)
        except ValueError:
            print("\nInvalid customer ID.")
            pause()
            return
    elif choice == '2':
        try:
            vehicle_id = int(input("\nEnter vehicle ID: ").strip())
            success, message, history = reports.get_service_history_by_vehicle(vehicle_id)
        except ValueError:
            print("\nInvalid vehicle ID.")
            pause()
            return
    else:
        print("\nInvalid choice.")
        pause()
        return
    
    if history:
        filename = input("\nEnter filename (press Enter for default): ").strip()
        if not filename:
            filename = None
        
        success, message = reports.export_service_history(history, filename)
        print(f"\n{message}")
    else:
        print("\nNo data to export.")
    
    pause()

if __name__ == "__main__":
    print("Initializing Vehicle Service Management System...")
    
    if not init_database():
        print("\nFailed to initialize database. Please check your database configuration.")
        sys.exit(1)
    
    print("Database initialized successfully!")
    pause()
    
    main_menu()
