#ifndef Power_h
#define Power_h

#include <Arduino.h>
#include <M5StickC.h>

// Function to turn off the device
void powerOff() {
    M5.Lcd.println("Powering off...");
    delay(1000);
    M5.Axp.PowerOff();
}

#endif // Power_h