"""
Este modulo contiene funciones que facilitan el acceso a datos.
Tomar esto como un ejemplo del uso de connector/python (llamados a la BD).
"""

import mysql.connector
from mysql.connector import errors

import config

def conectar():
    """Conectar con la base de datos y devolver un obj conexion."""
    try:
        conn = mysql.connector.connect(**config.credenciales)
    except errors.DatabaseError as err:
        print("Error al conectar.", err)
    else:
        return conn

def nueva_tarea(tarea):
    """Insetar nueva rarea a la db. Los valores de completada y creacion son default."""
    query = "INSERT INTO tareas (tarea) VALUES (%s)"
    conn = conectar()
    cur = conn.cursor()
    cur.execute(query, (tarea,))
    conn.commit()
    conn.close()

def actualizar_tarea(id_tarea, tarea):
    """Actualizar la tarea id_tarea con el contenido pasado por parametro."""
    query = "UPDATE tareas SET tarea = %s WHERE id_tarea = %s"
    conn = conectar()
    cur = conn.cursor()
    cur.execute(query, (tarea, id_tarea))
    conn.commit()
    conn.close()

def completar_tarea(id_tarea):
    """Actualizar la tarea id_tarea al estado completadas = true."""
    query = "UPDATE tareas SET completada = true WHERE id_tarea = %s"
    conn = conectar()
    cur = conn.cursor()
    cur.execute(query, (id_tarea,))
    conn.commit()
    conn.close()

def eliminar_tarea(id_tarea):
    """Eliminar tarea id_tarea de la base de datos."""
    query = "DELETE FROM tareas WHERE id_tarea = %s"
    conn = conectar()
    cur = conn.cursor()
    cur.execute(query, (id_tarea,))
    conn.commit()
    conn.close()

def get_tareas(tipo="all"):
    """Obtener las tareas segun el tipo.
        
    Tipo es 'all' (todas), 'done' (completadas) o 'pending' (pendientes)
    La cadena de la consulta se arma dependiendo del valor de tipo.
    Si tipo es 'all', no se incluye la clausula WHERE.
    Si tipo es 'done' se incluye el WHERE, con completadas = true
    Si tipo es 'pending' se incluye el WHERE, con completadas = false
    """
    consulta = """SELECT id_tarea, tarea, completada
                    FROM tareas {}
                    ORDER BY creacion DESC"""
    where = "WHERE completada = {}"
    if tipo == "done":
        consulta = consulta.format(where.format("true"))
    elif tipo == "pending":
        consulta = consulta.format(where.format("false"))
    elif tipo == "all":
        consulta = consulta.format("")
    conn = conectar()
    cur = conn.cursor()
    cur.execute(consulta)
    resultado = cur.fetchall()
    conn.close()
    # print(resultado)
    return resultado

def create_if_not_exists():
    """Crea la base de datos y la tabla si no existen.
    
    Esto asegura que la aplicacion funcione aunque no
    exista la base de datos previamente.
    Si es necesario que exista el usuario (con sus respectivos permisos)
    en el servidor.
    """
    create_database = "CREATE DATABASE IF NOT EXISTS %s" %config.credenciales["database"]
    create_table = """CREATE TABLE IF NOT EXISTS tareas (
                        id_tarea int UNSIGNED NOT NULL UNIQUE AUTO_INCREMENT,
                        tarea varchar(60) NOT NULL,
                        completada bool DEFAULT false,
                        creacion datetime DEFAULT now()
                        )"""
    try:
        conn = mysql.connector.connect(user=config.credenciales["user"],
                                       password=config.credenciales["password"],
                                       host="127.0.0.1")
        cur = conn.cursor()
        cur.execute(create_database)
        cur.execute("USE %s" %config.credenciales["database"])
        cur.execute(create_table)
        conn.commit()
        conn.close()
    except errors.DatabaseError as err:
        print("Error al conectar o crear la base de datos.", err)
        raise

