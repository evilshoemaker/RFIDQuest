const uint8_t MAGNET_SENSOR1_PIN = 2;
const uint8_t MAGNET_SENSOR2_PIN = 3;
const uint8_t MAGNET_SENSOR3_PIN = 4;
const uint8_t RELAY_PIN = 5;

const uint32_t DELAY_OPEN = 2000;

uint32_t beginMagnetic = 0;

void setup() {
    pinMode(MAGNET_SENSOR1_PIN, INPUT);
    pinMode(MAGNET_SENSOR1_PIN, INPUT);
    pinMode(MAGNET_SENSOR1_PIN, INPUT);
    
    pinMode(RELAY_PIN, OUTPUT);
    digitalWrite(RELAY_PIN, LOW);
}

void loop() {
    if (isMagnetic() 
            && (millis() - beginMagnetic) > 2000)       
    {
        digitalWrite(RELAY_PIN, HIGH);
    }
    else
    {
        digitalWrite(RELAY_PIN, LOW);     
        beginMagnetic = millis();
    }
}

bool isMagnetic()
{
    return digitalRead(MAGNET_SENSOR1_PIN)
            && digitalRead(MAGNET_SENSOR1_PIN)
            && digitalRead(MAGNET_SENSOR1_PIN);
}

