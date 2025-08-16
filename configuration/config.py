import os
from schemas.database import DatabaseConfig
from dotenv import load_dotenv
load_dotenv()

_config_options = {
    'local': {
        'host': 'localhost',
        'user': 'admin',
        'password': 'd5758017c265',
        'database': 'ven_app_api',
        'port': 3306
    },
    'development': {
        'host': 'localhost',
        'user': 'admin',
        'password': 'd5758017c265',
        'database': 'ven_app_api',
        'port': 3306
    },
    'production': {
        'host': 'localhost',
        'user': 'admin',
        'password': 'd5758017c265',
        'database': 'ven_app_api',
        'port': 3306
    }
}

configuration: DatabaseConfig = _config_options[os.getenv('STAGE')]