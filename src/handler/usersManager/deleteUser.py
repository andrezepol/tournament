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
        user_id = body.get("user_id")

        if not user_id:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "El campo 'user_id' es obligatorio"})
            }

        # Conexión a PostgreSQL con variables de entorno
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
        cursor = conn.cursor()

        delete_query = "DELETE FROM usuarios WHERE id = %s RETURNING id;"
        cursor.execute(delete_query, (user_id,))
        deleted_user = cursor.fetchone()

        if deleted_user is None:
            return {
                "statusCode": 404,
                "body": json.dumps({"error": "Usuario no encontrado"})
            }

        conn.commit()

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Usuario eliminado exitosamente", "user_id": deleted_user[0]})
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
