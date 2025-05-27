import pymysql
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    return pymysql.connect(
        host=os.getenv('MYSQL_HOST', 'mysql-34fa5599-scvgden-9e65.b.aivencloud.com'),
        port=int(os.getenv('MYSQL_PORT', 10023)),
        user=os.getenv('MYSQL_USER', 'avnadmin'),
        password=os.getenv('MYSQL_PASSWORD', 'AVNS_OeD2WJJNW4UHZZOtCEi'),
        database=os.getenv('MYSQL_DATABASE', 'defaultdb'),
        ssl={'ssl_mode': 'REQUIRED'}
    )