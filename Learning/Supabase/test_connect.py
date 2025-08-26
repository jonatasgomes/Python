import psycopg2
import env

connection = None
USER = env.USER
PASSWORD = env.PASSWORD
HOST = env.HOST
PORT = env.PORT
DBNAME = env.DBNAME

try:
    connection = psycopg2.connect(
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=PORT,
        dbname=DBNAME
    )
    print("Connection successful!")
    
    cursor = connection.cursor()
    cursor.execute("SELECT TO_CHAR(NOW(), 'DD-Mon-YYYY HH24:MI:SS');")
    result = cursor.fetchone()
    print("Current Time:", result[0])
    cursor.close()
    connection.close()
    print("Connection closed.")
except Exception as e:
    if connection:
        connection.close()
        print("Connection closed.")
    print(f"Failed to connect: {e}")
