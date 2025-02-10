import json
import os
import psycopg2

def   lambda_handler(event, lambda_context):
    conn = None
    cursor = None

    try:
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
        cursor = conn.cursor()
        query = "SELECT * FROM usuarios;"
        cursor.execute(query)
        users = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        users_list = []
        for user in users:
            users_list.append(dict(zip(column_names, user)))
        
        json_result = json.dumps(users_list, default=str)
        return json_result
        
    except Exception as e:
        print("Error al conectar o ejecutar la consulta:", e)
        return json.dumps({"error": str(e)})
    finally:
        if cursor: 
            cursor.close()
        if conn:
            conn.close()
