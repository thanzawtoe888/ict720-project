// https://github.com/m5stack/M5StickC-Plus/blob/master/examples/Hat/HEART_RATE_MAX30102/HEART_RATE_MAX30102.ino

#include <Arduino.h>
#include <M5StickC.h>
#include <MAX30105.h>
#include <Wire.h>
#include <WiFiClient.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include "utility/NetworkModule.h"
#include "utility/PowerModule.h"
// #include "utility/HeartRateModule.h"

#include "heartRate.h"




// Share varaibles
const byte Button_A = 37;
const byte pulseLED = 26;
// HeartRate Variables
const byte RATE_SIZE = 4; //Increase this for more averaging. 4 is good.
byte rates[RATE_SIZE]; //Array of heart rates
byte rateSpot = 0;
long lastBeat = 0; //Time at which the last beat occurred

long irValue;
float beatsPerMinute;
int beatAvg;
// Modules
NetworkModule network_module;
PowerModule power_module;
// MQTT Module.
WiFiClient espClient;
JsonDocument doc;
PubSubClient mqtt_client(espClient);
// Instantiate a MAX30102 sensor.
MAX30105 Sensor;

// For HeartRate Module.
void hearterate_detect();
// For MQTT Module.
void mqtt_setup();
void on_message(char* topic, byte* payload, unsigned int length);


void setup() {
  M5.begin();
  Serial.begin(115200);
  pinMode(25, INPUT_PULLUP);  // set pin mode
  pinMode(pulseLED, OUTPUT);
  pinMode(Button_A, INPUT);
  Wire.begin(0, 26);  // initialize I2C
  Serial.println("\nI2C Scanner");
  Serial.println("Starting setup...");
  if (!Sensor.begin(Wire, I2C_SPEED_FAST)) {
    // init fail
    M5.Lcd.print("Init Failed");
    Serial.println(F("MAX30102 was not found. Please check wiring/power."));
    // while (1) {
    //   delay(1000);
    //   Serial.print(".");
    // }
  }
  
  Sensor.setup(); //Configure sensor with default settings
  Sensor.setPulseAmplitudeRed(0x0A); //Turn Red LED to low to indicate sensor is running
  Sensor.setPulseAmplitudeGreen(0); //Turn off Green LED
  // Network
  network_module.connect();
  mqtt_setup();
  // Serial.printf("Is network connected: %d\n", network_module.isConnected());
  M5.Lcd.println("Press Btn B to power off.\n");

}

void loop() {
  if (M5.BtnB.wasPressed()) {
    power_module.off();
  }
  hearterate_detect();
  M5.update();
  mqtt_client.loop();
  // Serial.print(" R[");
  // Serial.print(Sensor.getRed());
  // Serial.print("] IR[");
  // Serial.print(Sensor.getIR());
  // Serial.print("] G[");
  // Serial.print(Sensor.getGreen());
  // Serial.print("]");
  // Serial.println();
}


void hearterate_detect() {
   
    irValue = Sensor.getIR();

    if (checkForBeat(irValue) == true)
    {
      //We sensed a beat!
      long delta = millis() - lastBeat;
      lastBeat = millis();
  
      beatsPerMinute = 60 / (delta / 1000.0);
  
      if (beatsPerMinute < 255 && beatsPerMinute > 20)
      {
        rates[rateSpot++] = (byte)beatsPerMinute; //Store this reading in the array
        rateSpot %= RATE_SIZE; //Wrap variable
  
        //Take average of readings
        beatAvg = 0;
        for (byte x = 0 ; x < RATE_SIZE ; x++)
          beatAvg += rates[x];
        beatAvg /= RATE_SIZE;
      }
    }
  
    Serial.print("IR=");
    Serial.print(irValue);
    Serial.print(", BPM=");
    Serial.print(beatsPerMinute);
    Serial.print(", Avg BPM=");
    Serial.print(beatAvg);
  
    if (irValue < 50000)
      Serial.print(" No finger?");
  
    Serial.println();
}

void mqtt_setup() {
  mqtt_client.setServer(MQTT_SERVER,1883);
  mqtt_client.setCallback(on_message);
  mqtt_client.connect(MQTT_DOMAIN);
  mqtt_client.subscribe(MQTT_SUPSCRIPTION);
  Serial.println("Conneted to MQTT broker");
}

void on_message(char* topic, byte* payload, unsigned int length) {
  char buf[200];
  memcpy(buf, payload, length);
  buf[length] = '\0';
  Serial.printf("Received message from topic %s: %s\n", topic, buf);
  deserializeJson(doc, buf);
  if (doc["cmd"] == "listen") {
  // do something
  Serial.println("Start listening");
  doc.clear();
  doc["status"] = "200";
  doc["irValue"] = irValue;
  doc["BPM"] = beatsPerMinute;
  doc["BPM_Average"] = beatAvg;
  doc["No Finger"] = irValue < 50000;
  // for (int i = 0; i < 12; i++) {
  //   doc["party_values"].add(bin[i]);
  // }
  serializeJson(doc, buf);
  mqtt_client.publish(MQTT_SUPSCRIPTION, buf);
  }
}