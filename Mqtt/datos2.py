import paho.mqtt.client as mqtt
import serial
import json
import time
import threading

broker = "localhost"
puerto = 1883

topic_map = {
    "temperatura": "topic/temperatura",
    "gas": "topic/gas",
    "distancia": "topic/distancia",
    "movimiento": "topic/movimiento",
}

def on_message(client, userdata, msg):
    print(f"[Práctica 2] Mensaje recibido en {msg.topic}: {msg.payload.decode()}")

cliente = mqtt.Client()
cliente.on_message = on_message
cliente.connect(broker, puerto)
cliente.loop_start()
arduino = serial.Serial(port='COM3', baudrate=9600, timeout=1)
time.sleep(2)

def leer_serial():
    if arduino.in_waiting > 0:
        linea = arduino.readline().decode('utf-8').strip()
        try:
            datos = json.loads(linea)
            print(f"[Práctica 2] Datos recibidos: {datos}")

            for clave, topic in topic_map.items():
                if clave in datos:
                    cliente.publish(topic, str(datos[clave]))
                    print(f"[Práctica 2] Publicado {datos[clave]} en {topic}")
        except json.JSONDecodeError:
            print("[Práctica 2] Error al decodificar JSON:", linea)

    threading.Timer(1, leer_serial).start()

try:
    leer_serial()  
    while True:
        time.sleep(1) 
except KeyboardInterrupt:
    cliente.loop_stop()
    cliente.disconnect()
    arduino.close()
