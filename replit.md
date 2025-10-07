# Vehicle Service Management System

## Overview

This is a Vehicle Service Management System built with Python that handles customer management, vehicle tracking, service records, billing, and reporting. The application provides a command-line interface for managing automotive service operations, including customer data, vehicle information, service history, invoicing, and automated service reminders.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Application Architecture
- **Type**: Command-line interface (CLI) application
- **Language**: Python 3
- **Design Pattern**: Modular architecture with separation of concerns
- **Module Structure**: 
  - Each major feature area (customers, vehicles, services, billing, reports) is isolated in its own module
  - Database operations are centralized in a dedicated database wrapper class
  - Configuration is externalized to a separate config module

### Database Layer
- **Database Abstraction**: Custom Database wrapper class that supports multiple database backends
- **Supported Databases**: PostgreSQL and MySQL
- **Connection Management**: Manual connection/disconnection pattern with cursor management
- **Query Pattern**: Parameterized queries using database-specific placeholders to prevent SQL injection
- **Database Selection**: Runtime database type selection via environment variables

**Design Rationale**: The abstraction layer allows switching between PostgreSQL and MySQL without code changes, providing flexibility for different deployment environments. The PLACEHOLDER pattern ensures queries work across different database parameter styles.

### Data Model
- **Core Entities**:
  - Customers: Stores customer contact information (name, phone, email, address)
  - Vehicles: Links to customers, stores vehicle details (make, model, year, license plate, VIN)
  - Services: Links to vehicles, tracks service records (date, description, costs, totals)

- **Relationships**:
  - One-to-Many: Customer → Vehicles
  - One-to-Many: Vehicle → Services
  - Implicit: Customer → Services (through Vehicle)

### Business Logic
- **Validation Layer**: Input validation for phone numbers, emails, dates, costs, and years
- **Calculation Engine**: 
  - Automatic total cost calculation (labor + parts)
  - Tax rate application (configurable at 8%)
  - Next service date calculation based on configurable service intervals (90 days default)
  
- **Service Reminders**: Automated reminder system based on service intervals and configurable reminder threshold (7 days before due)

### Configuration Management
- **Environment-based Configuration**: Uses dotenv for environment variable management
- **Configurable Parameters**:
  - Database type and connection settings
  - Tax rates
  - Service interval days
  - Reminder threshold days
- **Multi-environment Support**: Different configurations for PostgreSQL vs MySQL deployments

### User Interface
- **CLI Pattern**: Menu-driven interface with numbered options
- **Display**: PrettyTable library for formatted data display
- **Screen Management**: Cross-platform screen clearing (Windows/Unix)
- **User Flow**: Hierarchical menu system with main menu and sub-menus for each feature area

**Design Rationale**: CLI approach provides simplicity and ease of deployment without web server requirements, suitable for small service shop environments.

### Error Handling
- **Pattern**: Tuple return pattern (success_boolean, message_string, optional_data)
- **Validation**: Pre-execution validation of all user inputs
- **Database Errors**: Caught and converted to user-friendly messages
- **Rollback Strategy**: Implicit through transaction management at database connector level

## External Dependencies

### Python Libraries
- **psycopg2**: PostgreSQL database adapter for Python
- **mysql-connector-python**: MySQL database adapter for Python
- **python-dotenv**: Environment variable management from .env files
- **prettytable**: ASCII table formatting for console output

### Database Systems
- **PostgreSQL**: Primary supported relational database (default)
- **MySQL**: Alternative supported relational database
- **Schema Requirements**: Tables for customers, vehicles, and services with appropriate foreign key relationships

### Environment Variables
- **DB_TYPE**: Database system selection ('postgresql' or 'mysql')
- **PostgreSQL Settings**: PGHOST, PGDATABASE, PGUSER, PGPASSWORD, PGPORT
- **MySQL Settings**: MYSQL_HOST, MYSQL_DATABASE, MYSQL_USER, MYSQL_PASSWORD, MYSQL_PORT

### External Services
None - this is a self-contained application with no external API integrations or third-party services beyond the database.