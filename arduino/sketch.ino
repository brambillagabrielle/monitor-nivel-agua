// pinos conectados no Arduino
// const int led_vermelho = 2;
// const int led_verde = 3;
const int trig_pin = 4;
const int echo_pin = 5;

// variáveis que vão ser utilizadas para medir a distância
float duracao_pulso, distancia_cm;

void setup() {

  Serial.begin(9600);

  // configura os pinos como entrada e saída para o sensor ultrassônico
  pinMode(trig_pin, OUTPUT);
  pinMode(echo_pin, INPUT);

}

void loop() {

  // gera pulsos no sensor
  digitalWrite(trig_pin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trig_pin, LOW);

  // mede a duração do pulso
  duracao_pulso = pulseIn(echo_pin, HIGH);

  // calcula a distância utilizando a duração do pulso
  distancia_cm = 0.017 * duracao_pulso;

  // Envia a distância calculada para o código Python
  Serial.println(distancia_cm);

  // Recebe mensagem avisando da alteração identificada, alterando a cor dos leds
  /*
  char cmd = Serial.read();
  if (cmd == '1') {
    digitalWrite(led_vermelho, HIGH);
    digitalWrite(led_verde, LOW);
  } else {
    digitalWrite(led_vermelho, LOW);
    digitalWrite(led_verde, HIGH);
  }*/

  // coleta a distância à cada 5 segundos (5000 milissegundos)
  delay(5000);

}