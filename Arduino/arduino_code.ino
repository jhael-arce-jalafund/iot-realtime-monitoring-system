void setup() { 
  Serial.begin(9600);
  randomSeed(analogRead(0));  
}

void loop() {
  float temperatura = getTemperatura();  
  int gas = getGas();                     
  int distancia = getDistancia();        
  bool movimiento = getMovimiento();     

  String json = "{";
  json += "\"temperatura\": " + String(temperatura, 1) + ",";
  json += "\"gas\": " + String(gas) + ",";
  json += "\"distancia\": " + String(distancia) + ",";
  json += "\"movimiento\": " + String(movimiento ? "true" : "false");
  json += "}";

  Serial.println(json);

  delay(3000);  
}

float getTemperatura() {
  return random(200, 350) / 10.0; 
}

int getGas() {
  return random(100, 300); 
}

int getDistancia() {
  return random(10, 200); 
}

bool getMovimiento() {
  return random(0, 2); 