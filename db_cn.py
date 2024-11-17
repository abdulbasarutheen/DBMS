import mysql.connector

def connect_to_database():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="fishandahook",
        database="hm_ms"
    )

def execute_query(query, params=None):
    con = connect_to_database()
    cursor = con.cursor()

    cursor.execute(query, params)

    if query.strip().lower().startswith(('insert', 'update', 'delete')):
        con.commit()
        return True
    
    if query.strip().lower().startswith('select'):
        return cursor.fetchall()

    cursor.close()  
    con.close() 