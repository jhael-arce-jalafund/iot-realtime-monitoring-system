# database.py

import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
from config import DB_CONFIG

def get_connection():
    return psycopg2.connect(**DB_CONFIG)

def init_db():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS sensores (
                    id SERIAL PRIMARY KEY,
                    sensor_id TEXT,
                    tipo TEXT,
                    valor DOUBLE PRECISION,
                    timestamp TIMESTAMP
                );
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS alertas (
                    id SERIAL PRIMARY KEY,
                    sensor_id TEXT,
                    tipo TEXT,
                    valor DOUBLE PRECISION,
                    mensaje TEXT,
                    timestamp TIMESTAMP
                );
            """)
            conn.commit()

def guardar_dato(sensor_id, tipo, valor, timestamp=None):
    timestamp = timestamp or datetime.now()
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO sensores (sensor_id, tipo, valor, timestamp)
                VALUES (%s, %s, %s, %s)
            """, (sensor_id, tipo, valor, timestamp))
            conn.commit()

def guardar_alerta(sensor_id, tipo, valor, mensaje, timestamp=None):
    timestamp = timestamp or datetime.now()
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO alertas (sensor_id, tipo, valor, mensaje, timestamp)
                VALUES (%s, %s, %s, %s, %s)
            """, (sensor_id, tipo, valor, mensaje, timestamp))
            conn.commit()
