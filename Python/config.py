# config.py

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
SERIAL_PORT = "COM3"  # Cambia por el puerto correcto en tu PC
BAUD_RATE = 9600

DB_CONFIG = {
    "dbname": "iot_db",
    "user": "admin",
    "password": "admin123",
    "host": "localhost",
    "port": 5432
}

ALERT_THRESHOLDS = {
    "temperatura": 30,
    "gas": 300,
    "distancia": 150,
    "movimiento": 1
}
