# mqtt_client.py

import json
import serial
import paho.mqtt.client as mqtt
from datetime import datetime

from config import ALERT_THRESHOLDS, SERIAL_PORT, BAUD_RATE, MQTT_BROKER, MQTT_PORT
from database import init_db, guardar_dato
from alerts import verificar_alertas
from actuator_control import encender_ventilador

# Inicializar base de datos
#init_db()

# Conectar a puerto serial
ser = serial.Serial(SERIAL_PORT, BAUD_RATE)

# Cliente MQTT
mqtt_client = mqtt.Client()
mqtt_client.connect(MQTT_BROKER, MQTT_PORT)

print("📡 Sistema de monitoreo iniciado...")

while True:
    try:
        linea = ser.readline().decode("utf-8").strip()
        if linea:
            data = json.loads(linea)
            sensor_id = data.get("sensor_id")
            timestamp = datetime.now().isoformat()

            for key in ["temperatura", "gas", "distancia", "movimiento"]:
                valor = data.get(key)
                if valor is not None:
                    topic = f"iot/{sensor_id}/{key}"
                    mqtt_client.publish(topic, valor)
                    print(f"📤 {topic} → {valor}")

                    #guardar_dato(sensor_id, key, valor, timestamp)
                    #verificar_alertas(sensor_id, key, valor)
                    
                             # Alerta simple sin DB
                    if key in ALERT_THRESHOLDS:
                        umbral = ALERT_THRESHOLDS[key]
                        if float(valor) > umbral:
                            print(f"⚠ ALERTA: {key} = {valor} supera umbral ({umbral})")
                            
                    # Ejemplo: actuar si temperatura es muy alta
                    if key == "temperatura" and valor > 30:
                        encender_ventilador(sensor_id)

    except Exception as e:
        print("❌ Error:", e)
