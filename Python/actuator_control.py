# actuator_control.py

import paho.mqtt.client as mqtt
from config import MQTT_BROKER, MQTT_PORT

client = mqtt.Client()
client.connect(MQTT_BROKER, MQTT_PORT)

def encender_ventilador(sensor_id):
    topic = f"iot/{sensor_id}/actuador"
    client.publish(topic, "ON")
    print(f"[ACTUADOR] Encendiendo ventilador para {sensor_id}")

def apagar_ventilador(sensor_id):
    topic = f"iot/{sensor_id}/actuador"
    client.publish(topic, "OFF")
    print(f"[ACTUADOR] Apagando ventilador para {sensor_id}")
