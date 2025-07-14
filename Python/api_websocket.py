import json
import asyncio
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import paho.mqtt.client as mqtt
from typing import List

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

websocket_clients: List[WebSocket] = []

datos_actuales = {
    "temperatura": None,
    "gas": None,
    "distancia": None,
    "movimiento": None
}

# === MQTT CALLBACK ===
loop = asyncio.get_event_loop()

def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode()

    print(f"[MQTT] Recibido en {topic}: {payload}")

    for clave, mapped_topic in topic_map.items():
        if topic == mapped_topic:
            datos_actuales[clave] = payload

    data_json = json.dumps(datos_actuales)

    for ws in websocket_clients:
        asyncio.run_coroutine_threadsafe(ws.send_text(data_json), loop)

# === MQTT CONFIG ===
broker = "localhost"
puerto = 1883
topic_map = {
    "temperatura": "topic/temperatura",
    "gas": "topic/gas",
    "distancia": "topic/distancia",
    "movimiento": "topic/movimiento",
}

cliente = mqtt.Client()
cliente.on_message = on_message
cliente.connect(broker, puerto)
for topic in topic_map.values():
    cliente.subscribe(topic)
cliente.loop_start()

# === WebSocket endpoint ===
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    websocket_clients.append(websocket)
    print("[WebSocket] Cliente conectado")
    try:
        while True:
            await asyncio.sleep(1)
    except Exception as e:
        print("[WebSocket] Cliente desconectado:", e)
    finally:
        websocket_clients.remove(websocket)
