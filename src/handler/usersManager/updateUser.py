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
        user_id = body.get("id")
        nombre = body.get("nombre")
        correo = body.get("correo")
        contrasena = body.get("contrasena")
        num_torneo_creado = body.get("num_torneo_creado")

        # Validar que se envió id
        if not user_id:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "El campo 'id' es obligatorio"})
            }

        update_fields = []
        update_values = []

        if nombre:
            update_fields.append("nombre = %s")
            update_values.append(nombre)
        if correo:
            update_fields.append("correo = %s")
            update_values.append(correo)
        if contrasena:
            update_fields.append("contrasena = %s")
            update_values.append(contrasena)
        if num_torneo_creado is not None:
            update_fields.append("num_torneo_creado = %s")
            update_values.append(num_torneo_creado)

        if not update_fields:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Debe proporcionar al menos un campo para actualizar"})
            }

        update_values.append(user_id)

        update_query = f"""
        UPDATE usuarios
        SET {', '.join(update_fields)}
        WHERE id = %s
        RETURNING id;
        """
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
        cursor = conn.cursor()

        cursor.execute(update_query, tuple(update_values))
        updated_user = cursor.fetchone()

        if updated_user is None:
            return {
                "statusCode": 404,
                "body": json.dumps({"error": "Usuario no encontrado"})
            }

        conn.commit()

        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Usuario actualizado exitosamente", "id": updated_user[0]})
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
