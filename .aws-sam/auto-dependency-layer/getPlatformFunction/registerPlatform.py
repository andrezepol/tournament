import json
import os
import psycopg2

def lambda_handler(event, context):
    conn = None
    cursor = None

    try:
        if "body" not in event or not event["body"]:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "No se recibió un cuerpo válido en la solicitud"})
            }

        body = json.loads(event["body"])
        nombre = body.get("nombre")

        if not nombre:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "El campo 'nombre' es obligatorio"})
            }

        conn = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
        cursor = conn.cursor()

        insert_query = """
        INSERT INTO plataformas (nombre)
        VALUES (%s)
        RETURNING id;
        """

        cursor.execute(insert_query, (nombre,))
        platform_id = cursor.fetchone()[0]

        conn.commit()

        return {
            "statusCode": 201,
            "body": json.dumps({"message": "Plataforma registrada exitosamente", "platform_id": platform_id})
        }

    except json.JSONDecodeError:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "El body no es un JSON válido"})
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
