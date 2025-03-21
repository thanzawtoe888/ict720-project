#ifndef POWER_MODULE_h
#define POWER_MODULE_h

#include <Arduino.h>
#include <M5StickC.h>

// Function to turn off the device
class PowerModule {
    public:
        // PowerModule () {
        //     M5.Lcd.println("Press Btn B to power off.\n");
        // }
        void off() {
            M5.Lcd.println("Powering off...");
            delay(1000);
            M5.Axp.PowerOff();
        }
};

#endif
