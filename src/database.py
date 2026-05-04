import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "../data/cleannews.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def crear_tablas():
    conn = get_connection()
    cursor = conn.cursor()

    # Tabla Modelo
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Modelo (
            id_modelo    INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre       TEXT NOT NULL,
            algoritmo    TEXT NOT NULL,
            fecha        TEXT NOT NULL
        )
    """)

    # Tabla News
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS News (
            id_noticia   INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo       TEXT,
            texto        TEXT NOT NULL,
            fecha        TEXT
        )
    """)

    # Tabla Prediccion
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Prediccion (
            id_prediccion INTEGER PRIMARY KEY AUTOINCREMENT,
            prediccion    TEXT NOT NULL,
            confianza     REAL NOT NULL,
            fecha         TEXT NOT NULL,
            id_modelo     INTEGER NOT NULL,
            id_noticia    INTEGER NOT NULL,
            FOREIGN KEY (id_modelo)  REFERENCES Modelo(id_modelo),
            FOREIGN KEY (id_noticia) REFERENCES News(id_noticia)
        )
    """)

    conn.commit()
    conn.close()
    print("✅ Tablas creadas correctamente")

def insertar_modelo(nombre, algoritmo, fecha):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Modelo (nombre, algoritmo, fecha)
        VALUES (?, ?, ?)
    """, (nombre, algoritmo, fecha))
    conn.commit()
    id_modelo = cursor.lastrowid
    conn.close()
    return id_modelo

def insertar_noticia(titulo, texto, fecha):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO News (titulo, texto, fecha)
        VALUES (?, ?, ?)
    """, (titulo, texto, fecha))
    conn.commit()
    id_noticia = cursor.lastrowid
    conn.close()
    return id_noticia

def insertar_prediccion(prediccion, confianza, fecha, id_modelo, id_noticia):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Prediccion (prediccion, confianza, fecha, id_modelo, id_noticia)
        VALUES (?, ?, ?, ?, ?)
    """, (prediccion, confianza, fecha, id_modelo, id_noticia))
    conn.commit()
    conn.close()

def obtener_predicciones():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.id_prediccion, n.titulo, p.prediccion, p.confianza, p.fecha, m.nombre
        FROM Prediccion p
        JOIN News n    ON p.id_noticia = n.id_noticia
        JOIN Modelo m  ON p.id_modelo  = m.id_modelo
        ORDER BY p.fecha DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows

if __name__ == "__main__":
    crear_tablas()