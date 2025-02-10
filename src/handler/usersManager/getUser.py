import json
import os
import psycopg2

def lambda_handler(event, context):
    conn = None
    cursor = None
    try:
        # Extraer usuario desde el evento
        userId = event.get('userId', None)
        #userId = '1',
        if not userId:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Usuario no proporcionado'})
            }

        # Conectar a la base de datos usando variables de entorno
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE id = %s;", (userId,))
        users = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        users_list = []
        for user in users:
            users_list.append(dict(zip(column_names, user)))
        
        return {
            'statusCode': 200,
            'body': json.dumps(users_list, default=str)  # JSON serializable
        }
        
    except Exception as e:
        print("Error al conectar o ejecutar la consulta:", e)
        return json.dumps({"error": str(e)})
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()

        