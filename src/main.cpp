#include <Arduino.h>
#include <M5StickC.h>
#include "power.h"
#include "utility/NetworkModule.h"

NetworkModule network_module;
void setup() {
  // env_load("..", false);

  M5.begin();
  M5.Lcd.println("Press Btn B to power off.\n");


  Serial.begin(115200);
  delay(1000);  // Add delay to give time for Serial Monitor to open
  
  Serial.println("Starting setup...");  // This will print in the Serial Monitor

  network_module.connect();

}

void loop() {
  if (M5.BtnB.wasPressed()) {
    powerOff();
  }
  M5.update();
  delay(2000);
  Serial.printf("Is network connected: %d\n", network_module.isConnected());
}