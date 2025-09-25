import os
from dotenv import load_dotenv
load_dotenv()

_database = {
    'local': {
        'host': 'sandbox.cn7ga2jfbmbs.us-east-1.rds.amazonaws.com',
        'user': 'admin',
        'password': 'd5758017c265',
        'database': 'ven_app_api',
        'port': 3306
    },
    'development': {
        'host': 'sandbox.cn7ga2jfbmbs.us-east-1.rds.amazonaws.com',
        'user': 'admin',
        'password': 'd5758017c265',
        'database': 'ven_app_api',
        'port': 3306
    },
    'production': {
        'host': 'production.cn7ga2jfbmbs.us-east-1.rds.amazonaws.com',
        'user': 'admin',
        'password': 'd5758017c265',
        'database': 'ven_app_api',
        'port': 3306
    }
}

configuration = {
    'database': _database[os.getenv('STAGE')],
    'truora': {
        'api_key_url': 'https://api.account.truora.com/v1/api-keys',
        'api_identity_url': "https://api.identity.truora.com/v1/processes/{process_id}/result",
        'base_url': 'https://identity.truora.com/?token='
        
    }
}

