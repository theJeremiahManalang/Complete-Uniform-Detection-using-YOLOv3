// Pin definitions
const int ledPins[4] = {2, 3, 4, 5};
const int gatePin = 6;
const int buzzerPin = 7;

// Track LED states
bool ledState[4] = {false, false, false, false};

void setup() {
  Serial.begin(9600);

  for(int i = 0; i < 4; i++){
    pinMode(ledPins[i], OUTPUT);
  }

  pinMode(gatePin, OUTPUT);
  pinMode(buzzerPin, OUTPUT);

  digitalWrite(gatePin, LOW);
  digitalWrite(buzzerPin, LOW);
}

void loop() {

  if(Serial.available() > 0){
    char data = Serial.read();

    if(data == 'A'){
      turnOnLED(0); // LED 2
    }
    else if(data == 'B'){
      turnOnLED(1); // LED 3
    }
    else if(data == 'C'){
      turnOnLED(2); // LED 4
    }
    else if(data == 'D'){
      turnOnLED(3); // LED 5
    }
    else if(data == 'E'){
      turnOffAll();
    }
  }

  if(rfidTapped()){
    if(allLEDsOn()){
      openGate();
    } else {
      buzzError();
    }
  }
}


// ---------------- FUNCTIONS ----------------
void turnOnLED(int index){
  ledState[index] = true;
  digitalWrite(ledPins[index], HIGH);
}

void turnOffAll(){
  for(int i = 0; i < 4; i++){
    ledState[i] = false;
    digitalWrite(ledPins[i], LOW);
  }
}

bool allLEDsOn(){
  for(int i = 0; i < 4; i++){
    if(!ledState[i]) return false;
  }
  return true;
}

void openGate(){
  digitalWrite(gatePin, HIGH); // OPEN
  delay(5000);
  digitalWrite(gatePin, LOW);  // CLOSE
}

void buzzError(){
  digitalWrite(buzzerPin, HIGH);
  delay(1000);
  digitalWrite(buzzerPin, LOW);
}


// -------- MOCK RFID FUNCTION --------
bool rfidTapped(){
  if(Serial.available() > 0){
    char c = Serial.read();
    if(c == 'T') return true; 
  }
  return false;
}