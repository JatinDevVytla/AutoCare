# Vehicle Service Management System

A Python-based Vehicle Service Management System for managing customers, vehicles, service records, billing, and reporting. Built with PostgreSQL/MySQL database support and a user-friendly CLI interface.

## Features

- **Customer Management**: Add, update, delete, and search customers
- **Vehicle Registration**: Link vehicles to customers with detailed information
- **Service Logging**: Track service records with automatic cost calculations
- **Service Reminders**: 7-day advance reminders for upcoming services
- **Billing & Invoices**: Generate detailed invoices with tax calculations
- **Reports**: View and export service history by customer or vehicle
- **Database Flexibility**: Easy switching between PostgreSQL and MySQL

## Installation

### Prerequisites

- Python 3.6 or higher
- PostgreSQL or MySQL database

### Install Dependencies

```bash
pip install python-dotenv psycopg2-binary prettytable mysql-connector-python
```

## Configuration

### For PostgreSQL (Default)

Create a `.env` file in the project root:

```
DB_TYPE=postgresql
PGHOST=localhost
PGDATABASE=vehicle_service
PGUSER=postgres
PGPASSWORD=your_password
PGPORT=5432
```

### For MySQL

Create a `.env` file in the project root:

```
DB_TYPE=mysql
MYSQL_HOST=localhost
MYSQL_DATABASE=vehicle_service
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_PORT=3306
```

## Usage

Run the application:

```bash
python main.py
```

The system will automatically:
1. Initialize the database and create tables if needed
2. Display the main menu
3. Guide you through operations with numbered menu options

## Menu Options

1. **Customer Management** - Add, update, delete, search customers
2. **Vehicle Management** - Register and manage vehicles
3. **Service Management** - Log and track service records
4. **Service Reminders** - View vehicles due for service
5. **Billing & Invoices** - Generate invoices and billing summaries
6. **Reports** - View and export service history

## Database Schema

### Tables

- **customers**: Customer information (ID, name, phone, email, address)
- **vehicles**: Vehicle details linked to customers
- **services**: Service records linked to vehicles

### Relationships

- One customer → Many vehicles
- One vehicle → Many services
- Cascade delete: Deleting a customer removes their vehicles and services

## Configuration Options

Edit `config.py` to customize:

- `TAX_RATE`: Tax percentage (default: 8%)
- `SERVICE_INTERVAL_DAYS`: Days between services (default: 90)
- `REMINDER_DAYS`: Reminder advance notice (default: 7)

## Switching Between PostgreSQL and MySQL

Simply change the `DB_TYPE` in your `.env` file:

- For PostgreSQL: `DB_TYPE=postgresql`
- For MySQL: `DB_TYPE=mysql`

No code changes required! The database abstraction layer handles the differences automatically.

## File Structure

```
.
├── main.py                 # Main application entry point
├── config.py              # Configuration settings
├── database.py            # Database abstraction layer
├── customer_manager.py    # Customer management module
├── vehicle_manager.py     # Vehicle management module
├── service_manager.py     # Service management module
├── billing.py             # Billing and invoice generation
├── reports.py             # Reporting and export functionality
└── .env                   # Environment configuration (create this)
```

## License

This project is open source and available for educational and commercial use.
