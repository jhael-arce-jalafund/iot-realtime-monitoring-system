# alerts.py

from config import ALERT_THRESHOLDS
from database import guardar_alerta
from datetime import datetime

def verificar_alertas(sensor_id, tipo, valor):
    umbral = ALERT_THRESHOLDS.get(tipo)
    if umbral is not None and valor > umbral:
        mensaje = f"⚠ ALERTA: {tipo} del sensor {sensor_id} supera el umbral ({valor} > {umbral})"
        timestamp = datetime.now().isoformat()
        print(mensaje)
        guardar_alerta(sensor_id, tipo, valor, mensaje, timestamp)
