import json
import os
import psycopg2

def lambda_handler(event, context):
    conn = None
    cursor = None
    # Datos recibidos desde la API
    body = json.loads(event["body"])
    nombre = body.get("nombre")
    correo = body.get("correo")
    contrasena = body.get("contrasena")
    num_torneo_creado = body.get("num_torneo_creado", 0)

    if not nombre or not correo or not contrasena:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Faltan datos obligatorios"})
        }
    
    body = json.loads(event["body"]) if event["body"] else {}

    try:
        # Conexión a PostgreSQL con variables de entorno
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
        cursor = conn.cursor()

        # Query de inserción
        insert_query = """
        INSERT INTO usuarios (nombre, correo, contrasena, num_torneo_creado)
        VALUES (%s, %s, %s, %s)
        RETURNING id;
        """

        cursor.execute(insert_query, (nombre, correo, contrasena, num_torneo_creado))
        user_id = cursor.fetchone()[0]

        conn.commit()  # Confirmar la transacción

        return {
            "statusCode": 201,
            "body": json.dumps({"message": "Usuario creado exitosamente", "user_id": user_id})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
