#ifndef NETWORK_MODULE_H
#define NETWORK_MODULE_H

#include <WiFi.h>

class NetworkModule  {
    private:
        const char* ssid = WIFI_SSID;
        const char* password = WIFI_PASSWORD;
    public:
        NetworkModule() {}
        NetworkModule(const char* ssid, const char* password) {
            this->ssid = ssid;
            this->password = password;
        }
        void connect() {
            Serial.print("Connecting to WiFi...");
            WiFi.begin(ssid, password);
            while (WiFi.status() != WL_CONNECTED) {
                delay(1000);
                Serial.print(".");
            }
            Serial.println("Connected to WiFi");
            Serial.printf("IP address: %s\n", WiFi.localIP().toString().c_str());
            Serial.printf("RSSI: %d\n", WiFi.RSSI());
        }
        bool isConnected() {
            return WiFi.status() == WL_CONNECTED;
        }
};
#endif