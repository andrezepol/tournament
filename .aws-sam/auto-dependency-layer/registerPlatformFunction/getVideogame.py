import json
import os
import psycopg2

def lambda_handler(event, context):
    conn = None
    cursor = None

    try:
        videojuego_id = event.get("pathParameters", {}).get("videojuego_id")

        if not videojuego_id:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "El parámetro 'videojuego_id' es obligatorio"})
            }

        conn = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
        cursor = conn.cursor()

        select_query = "SELECT id, nombre, plataforma_id, tipo_id FROM videojuegos WHERE id = %s;"
        cursor.execute(select_query, (videojuego_id,))
        videojuego = cursor.fetchone()

        if videojuego is None:
            return {
                "statusCode": 404,
                "body": json.dumps({"error": "Videojuego no encontrado"})
            }

        return {
            "statusCode": 200,
            "body": json.dumps({
                "id": videojuego[0],
                "nombre": videojuego[1],
                "plataforma_id": videojuego[2],
                "tipo_id": videojuego[3]
            })
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
