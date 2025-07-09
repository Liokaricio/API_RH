from flask import Flask, request, jsonify
import pyodbc
import datetime


app = Flask(__name__)
# JAJAJ QUE MEQUETREFE X2
# jotos los del becas y credito.
# Configuración de la conexión a la base de datos Access
DATABASE_PATH = r"./att2000.mdb"  # Cambia esto por la ubicación real
DB_CONNECTION_STRING = (
    r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
    rf"DBQ={DATABASE_PATH};"
)

# Función para conectar a la base de datos
def get_db_connection():
    return pyodbc.connect(DB_CONNECTION_STRING)

# Ruta para obtener los usuarios (GET)
@app.route('/api/usuarios', methods=['GET'])
def obtener_usuarios():
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT userid, Badgenumber, name FROM USERINFO"
    cursor.execute(query)

    # Obtener todos los Badgenumber en una lista de diccionarios
    usuarios = [{"Badgenumber": row.Badgenumber, "USERID": row.userid, "NAME": row.name} for row in cursor.fetchall()]

    conn.close()
    
    return jsonify(usuarios)


# resgistros aqui
@app.route('/api/registros', methods=['GET'])
def obtener_registros():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Obtener el año y mes actual
    hoy = datetime.datetime.now()
    anio_actual = 2025

    # Consulta para filtrar por año y mes actual
    query = """
        SELECT c.userid, c.checktime, c.checktype, u.Badgenumber
        FROM checkinout c
        INNER JOIN USERINFO u ON c.userid = u.userid
        WHERE FORMAT(c.checktime, 'yyyy') = ?
    """
    
    cursor.execute(query, (str(anio_actual)))  # Mes en formato "01", "02", ..., "12"

    registros = [
        {
            "userid": row.userid,
            "tiempo_checada": row.checktime.strftime("%Y-%m-%d %H:%M:%S"),
            "tipo_chequeo": row.checktype,
            "numero_empleado": row.Badgenumber
        }
        for row in cursor.fetchall()
    ]

    conn.close()
    return jsonify(registros)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)