// SIFSM - Alerta Energetico. Arduino Uno / Tinkercad, Serial 9600.
// Comandos terminados por Enter: SET 000 ate SET 111; BTN volta aos botoes.
const byte BOTAO_A = 2, BOTAO_B = 3, BOTAO_C = 4;
const byte LED = 8, BUZZER = 9;
bool remoto = false, aRemoto = false, bRemoto = false, cRemoto = false;
char comando[16];
byte tamanho = 0;
bool excedeu = false;
int anterior = -1;

bool verificarAlerta(bool a, bool b, bool c) { return (a && b) || c; }

void receberComando() {
  while (Serial.available() > 0) {
    char ch = Serial.read();
    if (ch == '\r' || ch == '\n') {
      if (tamanho == 0 && !excedeu) continue;
      comando[tamanho] = '\0';
      if (!excedeu && tamanho == 3 && comando[0]=='B' && comando[1]=='T' && comando[2]=='N') {
        remoto = false;
        anterior = -1;
      } else if (!excedeu && tamanho == 7 && comando[0]=='S' && comando[1]=='E' && comando[2]=='T' && comando[3]==' '
                 && (comando[4]=='0' || comando[4]=='1') && (comando[5]=='0' || comando[5]=='1')
                 && (comando[6]=='0' || comando[6]=='1')) {
        aRemoto = comando[4]=='1'; bRemoto = comando[5]=='1'; cRemoto = comando[6]=='1';
        remoto = true;
        anterior = -1;
      } else {
        Serial.println("ERRO: use SET 000..111 ou BTN. Estado preservado.");
      }
      tamanho = 0; excedeu = false;
    } else if (tamanho < sizeof(comando)-1) {
      comando[tamanho++] = ch;
    } else {
      excedeu = true;
    }
  }
}

void setup() {
  pinMode(BOTAO_A, INPUT_PULLUP); pinMode(BOTAO_B, INPUT_PULLUP); pinMode(BOTAO_C, INPUT_PULLUP);
  pinMode(LED, OUTPUT); pinMode(BUZZER, OUTPUT);
  Serial.begin(9600);
  Serial.println("SIFSM: botoes ativos. SET ABC para dados Python; BTN para botoes.");
}

void loop() {
  receberComando();
  bool a = remoto ? aRemoto : digitalRead(BOTAO_A)==LOW;
  bool b = remoto ? bRemoto : digitalRead(BOTAO_B)==LOW;
  bool c = remoto ? cRemoto : digitalRead(BOTAO_C)==LOW;
  bool alerta = verificarAlerta(a, b, c);
  digitalWrite(LED, alerta ? HIGH : LOW);
  if (alerta) tone(BUZZER, 1000); else noTone(BUZZER);
  int estado = (a ? 4 : 0) + (b ? 2 : 0) + (c ? 1 : 0);
  if (estado != anterior) {
    Serial.print("A="); Serial.print(a); Serial.print(" B="); Serial.print(b);
    Serial.print(" C="); Serial.print(c); Serial.print(" | Alerta="); Serial.print(alerta);
    Serial.print(" | Modo="); Serial.println(remoto ? "SERIAL" : "BOTOES");
    anterior = estado;
  }
  delay(10);
}
