#include <Arduino.h>
#include <M5StickC.h>

#include "power.h"

void setup() {
  M5.begin();
  M5.Lcd.println("Press Btn B to power off.");

}

void loop() {
  M5.update();
  if (M5.BtnB.wasPressed()) {
    powerOff();
  }
}