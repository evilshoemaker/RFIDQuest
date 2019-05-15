const uint8_t MAGNET_SENSOR1_PIN = 2;
const uint8_t MAGNET_SENSOR2_PIN = 3;
const uint8_t MAGNET_SENSOR3_PIN = 4;
const uint8_t RELAY_PIN = 5;

const uint32_t DELAY_OPEN = 2000;

uint32_t beginMagnetic = 0;

void setup() {
    pinMode(MAGNET_SENSOR1_PIN, INPUT);
    pinMode(MAGNET_SENSOR2_PIN, INPUT);
    pinMode(MAGNET_SENSOR3_PIN, INPUT);
    
    pinMode(RELAY_PIN, OUTPUT);
    digitalWrite(RELAY_PIN, LOW);

    //Serial.begin(9600);
}

void loop() {
    bool magnetic = isMagnetic();

    /*Serial.print("R1");
    Serial.println(digitalRead(MAGNET_SENSOR1_PIN));

    Serial.print("R2");
    Serial.println(digitalRead(MAGNET_SENSOR2_PIN));

    Serial.print("R3");
    Serial.println(digitalRead(MAGNET_SENSOR3_PIN));*/
    
    if (magnetic 
            && (millis() - beginMagnetic) > 2000)       
    {
        digitalWrite(RELAY_PIN, HIGH);
    }
    else if (!magnetic)
    {
        digitalWrite(RELAY_PIN, LOW);     
        beginMagnetic = millis();
    }
}

bool isMagnetic()
{
    return digitalRead(MAGNET_SENSOR1_PIN)
            && digitalRead(MAGNET_SENSOR2_PIN)
            && digitalRead(MAGNET_SENSOR3_PIN);
}
