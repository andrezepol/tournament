import json
import os
import psycopg2

def lambda_handler(event, context):
    conn = None
    cursor = None

    try:
        platform_id = event.get("pathParameters", {}).get("platform_id")

        if not platform_id:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "El parámetro 'platform_id' es obligatorio"})
            }

        conn = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
        cursor = conn.cursor()

        select_query = "SELECT id, nombre FROM plataformas WHERE id = %s;"
        cursor.execute(select_query, (platform_id,))
        platform = cursor.fetchone()

        if platform is None:
            return {
                "statusCode": 404,
                "body": json.dumps({"error": "Plataforma no encontrada"})
            }

        return {
            "statusCode": 200,
            "body": json.dumps({
                "id": platform[0],
                "nombre": platform[1]
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
