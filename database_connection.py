import mysql.connector
from niche_details import *

def Database_Connection():
    db_connection = mysql.connector.connect(
    host = host,
    user = db_credential[niche]['user'],
    password = db_credential[niche]['password'],
    database = db_credential[niche]['database'],
    # auth_plugin='mysql_native_password'
    )
    
    db_cursor = db_connection.cursor()
    
    return db_connection,db_cursor

# db_connection,db_cursor = Database_Connection()
