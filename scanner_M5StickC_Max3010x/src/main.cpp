// Function: Detection of heart rate and blood oxygen concentration
// Units used: M5StickCP, Heart(MAX30102)
// please install MAX3010x lib for MAX30102 by library manager first
// addr: https://github.com/sparkfun/SparkFun_MAX3010x_Sensor_Library
#include <M5StickC.h>
#include <Wire.h>
#include "MAX30105.h"
#include "heartRate.h"
#include "spo2_algorithm.h"

#include <WiFi.h>
#include <WiFiMulti.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>

#define MQTT_TOPIC_REQUEST "ict720/group8/request"
#define MQTT_TOPIC_USER    "ict720/group8/user_list"
#define MQTT_TOPIC_DATA    "ict720/group8/data"


const char *ssid     = "Xiaomi2020Laptop";
const char *password = "11112222";
const char* mqtt_server = "192.168.208.35";
const int healthPubInterval = 1000; //ms
int excercise_mode = 0; // 1: walking, 2: running

WiFiClient espClient;
PubSubClient client(espClient);

TFT_eSprite Disbuff = TFT_eSprite(&M5.Lcd);
MAX30105 Sensor;

#define MAX_BRIGHTNESS 255
#define bufferLength   100
const byte Button_A = 37;
const byte pulseLED = 26;

uint32_t irBuffer[bufferLength];
uint32_t redBuffer[bufferLength];

bool SOSFlag = false;
int8_t V_Button, flag_Reset;
int32_t spo2, heartRate, old_spo2;
int8_t validSPO2, validHeartRate;
const byte RATE_SIZE = 5;
uint16_t rate_begin  = 0;
uint16_t rates[RATE_SIZE];
byte rateSpot = 0;
float beatsPerMinute;
int beatAvg;
int user_id;
byte num_fail;
JsonDocument doc;

uint16_t line[2][320] = {0};

uint32_t red_pos = 0, ir_pos = 0;
uint16_t ir_max = 0, red_max = 0, ir_min = 0, red_min = 0, ir_last = 0, red_last = 0;
uint16_t ir_last_raw = 0, red_last_raw = 0;
uint16_t ir_disdata, red_disdata;
uint16_t Alpha = 0.3 * 256;
uint32_t t1, t2, last_beat, Program_freq;
// wait 1 minutes before sending the first health data
// as bpm increasing from 0.0
uint32_t lastPubTime = millis() + 60000; 

unsigned long lastMsg = 0;
#define MSG_BUFFER_SIZE (50)
char msg[MSG_BUFFER_SIZE];
bool userMessageReceived = false; // Flag to track if the message is received

void display_info();
void connectWifi();
void callback(char* topic, byte* payload, unsigned int length);
void reConnect();
void cleanScreen();

void callBack(void) {
    V_Button = digitalRead(Button_A);
    if (V_Button == 0) flag_Reset = 1;
    delay(10);
}


void setup() {
    // init M5
    M5.begin();                 // initialize M5StickCPlus
    Serial.begin(115200);       // initialize serial communication
    pinMode(25, INPUT_PULLUP);  // set pin mode
    pinMode(pulseLED, OUTPUT);
    pinMode(Button_A, INPUT);
    Wire.begin(0, 26);  // initialize I2C

    // set Lcd
    M5.Lcd.setRotation(3);
    M5.Lcd.setSwapBytes(false);
    Disbuff.createSprite(240, 135);
    Disbuff.setSwapBytes(true);
    Disbuff.createSprite(240, 135);

    // set WiFi & MQTT
    connectWifi();
    client.setServer(mqtt_server, 1883);
    client.setCallback(callback);  

    // Connect to MQTT broker and subscribe to the topic
    while (!client.connected()) {
        M5.Lcd.print("Attempting MQTT connection...");
        String clientId = "M5Stack-";
        clientId += String(random(0xffff), HEX);
        
        if (client.connect(clientId.c_str())) {
            M5.Lcd.println("Connected to MQTT");
            client.subscribe(MQTT_TOPIC_USER); // Subscribe to topic
        } 
        else {
            M5.Lcd.print("Failed, rc=");
            M5.Lcd.println(client.state());
            delay(5000); // Wait for 5 seconds before retrying
        }
    }
    // Stay in loop until the first message is received
    client.publish(MQTT_TOPIC_REQUEST, "user list needed");
    while (!userMessageReceived) {
        client.loop(); // Keep the connection alive and check for new messages
    }


    // initialize Sensor
    if (!Sensor.begin(Wire, I2C_SPEED_FAST)) {
        M5.Lcd.print("Init Failed");
        Serial.println(F("MAX30102 was not found. Please check wiring/power."));
        while (1);
    }
    Serial.println(F("Place your index finger on the Sensor with steady pressure"));
    attachInterrupt(Button_A, callBack, FALLING);
    Sensor.setup();
}

void loop() {
    uint16_t ir, red;
    // reset the sensor buffer by clean the data in FIFO
    if (flag_Reset) {
        Sensor.clearFIFO();
        delay(5);
        flag_Reset = 0;
    }
    while (flag_Reset == 0) {
        while (Sensor.available() == false) {
            delay(10);
            Sensor.check();
        }
        while (true) {
            red = Sensor.getRed();
            ir  = Sensor.getIR();
            if ((ir > 1000) && (red > 1000)) {
                num_fail = 0;
                t1 = millis();

                // push the data into the buffer
                redBuffer[(red_pos + 100) % 100] = red;
                irBuffer[(ir_pos + 100) % 100]   = ir;

                // calculate the heart rate
                t2 = millis();
                Program_freq++;
                if (checkForBeat(ir) == true) {
                    long delta = millis() - last_beat - (t2 - t1) * (Program_freq - 1);
                    last_beat = millis();

                    Program_freq   = 0;
                    beatsPerMinute = 60 / (delta / 1000.0);
                    if ((beatsPerMinute > 30) && (beatsPerMinute < 120)) {
                        rate_begin++;
                        if ((abs(beatsPerMinute - beatAvg) > 15) && ((beatsPerMinute < 55) || (beatsPerMinute > 95)))
                            beatsPerMinute = beatAvg * 0.9 + beatsPerMinute * 0.1;
                        if ((abs(beatsPerMinute - beatAvg) > 10) && (beatAvg > 60) && ((beatsPerMinute < 65) || (beatsPerMinute > 90)))
                            beatsPerMinute = beatsPerMinute * 0.4 + beatAvg * 0.6;
                        rates[rateSpot++] = (byte) beatsPerMinute;  // Store this reading in the array
                        rateSpot %= RATE_SIZE;  // Wrap variable

                        // Take average of readings
                        beatAvg = 0;
                        if ((beatsPerMinute == 0) && (heartRate > 60) && (heartRate < 90))
                            beatsPerMinute = heartRate;
                        if (rate_begin > RATE_SIZE) {
                            for (byte x = 0; x < RATE_SIZE; x++)
                                beatAvg += rates[x];
                            beatAvg /= RATE_SIZE;
                        } else {
                            for (byte x = 0; x < rate_begin; x++)
                                beatAvg += rates[x];
                            beatAvg /= rate_begin;
                        }
                    }
                }
            }
            else {
                num_fail++;
            }
            line[0][(red_pos + 240) % 320] = (red_last_raw * (256 - Alpha) + red * Alpha) / 256;
            line[1][(ir_pos + 240) % 320] = (ir_last_raw * (256 - Alpha) + ir * Alpha) / 256;
            red_last_raw = line[0][(red_pos + 240) % 320];
            ir_last_raw  = line[1][(ir_pos + 240) % 320];
            red_pos++;
            ir_pos++;
            if ((Sensor.check() == false) || flag_Reset) break;
        }
        Sensor.clearFIFO();
        display_info();

        if (((millis() - lastPubTime) > healthPubInterval) && (beatAvg > 20)) {
            lastPubTime = millis();
            char payload[100];
            doc.clear();
            doc["timestamp"] = millis();
            doc["user_id"] = user_id;
            doc["spo2"] = spo2;
            doc["bpm"] = beatAvg;
            doc["excercise_mode"] = excercise_mode;
            serializeJson(doc, payload);
            client.publish(MQTT_TOPIC_DATA, payload);
        }
        M5.update();
        if (M5.BtnA.wasReleasefor(1000)) {  // The button B is pressed for 3s
            M5.Lcd.fillScreen(BLACK);  
            M5.Lcd.setCursor(0, 0);
            M5.Lcd.println("!!!!SOS!!!");
            client.publish("ict720/group8/sos", "SOS");
            delay(5000);
        }

        if (!client.connected()) {
            reConnect();
        }
        client.loop();
    
        // unsigned long now = millis();
        // if (now - lastMsg > 2000) {
        //     lastMsg = now;
        //     ++value;
        //     snprintf(msg, MSG_BUFFER_SIZE, "hello world #%ld", value);
        //     M5.Lcd.print("Publish message: ");
        //     M5.Lcd.println(msg);
        //     client.publish("M5Stack", msg);
        //     if (value % 4 == 0) {
        //         M5.Lcd.fillScreen(BLACK);
        //         M5.Lcd.setCursor(0, 0);
        //     }
        // }
    }
}

void display_info() {
    for (int i = 0; i < 240; i++) {
        if (i == 0) {
            red_max = red_min = line[0][(red_pos + i) % 320];
            ir_max = ir_min = line[1][(ir_pos + i) % 320];
        } 
        else {
            red_max = (line[0][(red_pos + i) % 320] > red_max)? line[0][(red_pos + i) % 320] : red_max;
            red_min = (line[0][(red_pos + i) % 320] < red_min)? line[0][(red_pos + i) % 320] : red_min;
            ir_max = (line[1][(ir_pos + i) % 320] > ir_max) ? line[1][(ir_pos + i) % 320] : ir_max;
            ir_min = (line[1][(ir_pos + i) % 320] < ir_min) ? line[1][(ir_pos + i) % 320] : ir_min;
        }
        if (flag_Reset) break;
    }
    Disbuff.fillRect(0, 0, 240, 135, BLACK);

    for (int i = 0; i < 240; i++) {
        red_disdata = map(line[0][(red_pos + i) % 320], red_max, red_min, 0, 135);
        ir_disdata = map(line[1][(ir_pos + i) % 320], ir_max, ir_min, 0, 135);
        {
            Disbuff.drawLine(i, red_last, i + 1, red_disdata, RED);
            Disbuff.drawLine(i, ir_last, i + 1, ir_disdata, BLUE);
        }
        ir_last  = ir_disdata;
        red_last = red_disdata;
        if (flag_Reset) break;
    }
    old_spo2 = spo2;
    if (red_pos > 100)
        maxim_heart_rate_and_oxygen_saturation(irBuffer, bufferLength,
                                               redBuffer, &spo2, &validSPO2,
                                               &heartRate, &validHeartRate);
    if (!validSPO2) spo2 = old_spo2;

    Disbuff.setTextSize(1);
    Disbuff.setTextColor(RED);
    Disbuff.setCursor(5, 5);
    Disbuff.printf("red:%d,%d,%d", red_max, red_min, red_max - red_min);
    Disbuff.setTextColor(BLUE);
    Disbuff.setCursor(5, 15);
    Disbuff.printf("ir:%d,%d,%d", ir_max, ir_min, ir_max - ir_min);
    Disbuff.setCursor(5, 25);
    if (num_fail < 10) {
        Disbuff.setTextColor(GREEN);
        Disbuff.printf("spo2:%d,", spo2);
        Disbuff.setCursor(60, 25);
        Disbuff.printf(" BPM:%d", beatAvg);
    } else {
        Disbuff.setTextColor(RED);
        Disbuff.printf("No Finger!!");
    }

    Disbuff.pushSprite(0, 0);
}

void connectWifi() {
    WiFiMulti WiFiMulti;
    int sum = 0;
    WiFiMulti.addAP(ssid, password);  // Add wifi configuration information.
    M5.lcd.printf("Waiting connect to WiFi: %s ...", ssid);  // Serial port output format string.
    while (WiFiMulti.run() != WL_CONNECTED) {  // If the connection to wifi is not established successfully.
        M5.lcd.print(".");
        delay(1000);
        sum += 1;
        if (sum == 8) M5.lcd.print("Conncet failed!");
    }
    M5.lcd.println("\nWiFi connected");
    M5.lcd.print("IP: ");
    M5.lcd.println(WiFi.localIP());  
    delay(3000);
    cleanScreen();
}

void callback(char* topic, byte* payload, unsigned int length) {
    userMessageReceived = true;  
    cleanScreen();
    M5.Lcd.println("Please select your user:");

    String message = "";
    for (int i = 0; i < length; i++) {
        message += (char)payload[i];
    }
    M5.Lcd.println(message);

    // Count the number of users (rows) in the message
    int user_count = 0;
    for (int i = 0; i < message.length(); i++) {
        if (message[i] == '\n') {
        user_count++;
        }
    }
    // Add one because the last line won't end with a newline character
    if (message.length() > 0) {
        user_count++;
    }
    M5.Lcd.println("Press btn A to move and hold it to select.");
    int i = 0;
    while (1) {
        M5.update();
        if (M5.BtnA.wasReleased()) {
            M5.Lcd.setCursor(7, 70);
            i++;
            if (i > user_count) i = 1;
            M5.Lcd.printf("Select user %d?", i);
        } 
        else if (M5.BtnA.wasReleasefor(500)) {
            cleanScreen();
            M5.Lcd.printf("User %d is selected!!!!\n", i);
            user_id = i-1;
            delay(3000);
            break;
        }
    }
    
    // select excercise mode
    int j = 0;
    M5.Lcd.println(" Please select your exercise mode: ");
    M5.Lcd.println(" 1. Walking");
    M5.Lcd.println(" 2. Running");
    while (1) {
        M5.update();
        if (M5.BtnA.wasReleased()) {
            M5.Lcd.setCursor(7, 70);
            j++;
            if (j > 2) j = 1;
            M5.Lcd.printf(" Select mode %d?", j);
        } 
        else if (M5.BtnA.wasReleasefor(500)) {
            cleanScreen();
            M5.Lcd.printf(" Mode %d is selected!!!!\n", j);
            excercise_mode = j;
            delay(3000);
            break;
        }
    }
}

void reConnect() {
    while (!client.connected()) {
        M5.Lcd.print("Attempting MQTT connection...");
        // Create a random client ID.
        String clientId = "M5Stack-";
        clientId += String(random(0xffff), HEX);
        // Attempt to connect.
        if (client.connect(clientId.c_str())) {
            M5.Lcd.printf("\nSuccess\n");
        } 
        else {
            M5.Lcd.print("failed, rc=");
            M5.Lcd.print(client.state());
            M5.Lcd.println("try again in 5 seconds");
            delay(5000);
        }
    }
}

void cleanScreen() {
    M5.Lcd.fillScreen(BLACK);
    M5.Lcd.setCursor(0, 0);
}