import { useEffect, useState, useRef } from "react";
import {
  LineChart, Line, XAxis, YAxis, Tooltip, Legend, CartesianGrid,
} from "recharts";

const MAX_POINTS = 20;

export default function App() {
  type DatoSensor = {
  tiempo: string;
  temperatura: number;
  gas: number;
  distancia: number;
  movimiento: number;
};

const [data, setData] = useState<DatoSensor[]>([]);
  const ws = useRef<WebSocket | null>(null);

  useEffect(() => {
  ws.current = new WebSocket("ws://localhost:8000/ws");

  ws.current.onmessage = (event) => {
    const payload = JSON.parse(event.data);

    setData(prev => {
        const timestamp = new Date().toLocaleTimeString();
        const newEntry = { 
          tiempo: timestamp,
          temperatura: parseFloat(payload.temperatura),
          gas: parseFloat(payload.gas),
          distancia: parseFloat(payload.distancia),
          movimiento: parseFloat(payload.movimiento),
        };
        const nuevaLista = [...prev, newEntry];
        return nuevaLista.slice(-MAX_POINTS);
      });
    };

    return () => {
      if (ws.current) {
        ws.current.close();
      }
    };
  }, []);

  return (
    <div className="p-4">
      <h1 style={{ fontSize: "1.5rem", fontWeight: "bold" }}>Monitoreo en Tiempo Real</h1>

      <LineChart width={1500} height={500} data={data}>
        <CartesianGrid stroke="#ccc" />
        <XAxis dataKey="tiempo" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Line type="monotone" dataKey="temperatura" stroke="#f97316" />
        <Line type="monotone" dataKey="gas" stroke="#22c55e" />
        <Line type="monotone" dataKey="distancia" stroke="#3b82f6" />
        <Line type="monotone" dataKey="movimiento" stroke="#ec4899" />
      </LineChart>
    </div>
  );
}

