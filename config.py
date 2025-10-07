import os
from dotenv import load_dotenv

load_dotenv()

DB_TYPE = os.getenv('DB_TYPE', 'postgresql')

if DB_TYPE == 'postgresql':
    DB_CONFIG = {
        'host': os.getenv('PGHOST', 'localhost'),
        'database': os.getenv('PGDATABASE', 'vehicle_service'),
        'user': os.getenv('PGUSER', 'postgres'),
        'password': os.getenv('PGPASSWORD', ''),
        'port': os.getenv('PGPORT', '5432')
    }
elif DB_TYPE == 'mysql':
    DB_CONFIG = {
        'host': os.getenv('MYSQL_HOST', 'localhost'),
        'database': os.getenv('MYSQL_DATABASE', 'vehicle_service'),
        'user': os.getenv('MYSQL_USER', 'root'),
        'password': os.getenv('MYSQL_PASSWORD', ''),
        'port': int(os.getenv('MYSQL_PORT', '3306'))
    }

TAX_RATE = 0.08
SERVICE_INTERVAL_DAYS = 90
REMINDER_DAYS = 7
