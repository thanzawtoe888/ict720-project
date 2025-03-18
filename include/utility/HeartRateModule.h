#ifndef HEARTRATE_MODULE_H
#define HEARTRATE_MODULE_H



// class HeartRateModule {
//     private:
//         byte* rates; // Pointer to dynamically allocated array
//         byte rateSpot = 0;
//         long lastBeat = 0;
//         float beatsPerMinute = 0.0;
//         int beatAvg = 0;
//         byte rateSize; // Store the dynamic array size
//         long irValue = 0;
//     public:
//         // Constructor: Dynamically allocate memory for the array
//         HeartRateModule(byte size) {
//             rateSize = size; // Set the array size
//             rates = new byte[rateSize]; // Allocate memory dynamically
//             for (byte i = 0; i < rateSize; i++) {
//                 rates[i] = 0; // Initialize values
//             }
//         }
//         // Destructor: Free allocated memory
//         ~HeartRateModule() {
//             delete[] rates;
//         }
  
//         bool detectHeartbeat() {
//             irValue = sensor.getIR();
//             return irValue;
//         }
//         bool isHeartbeatDetected(long irValue) {
//             return checkForBeat(irValue);
//         }
//         float calculateBPM(long lastBeat) {
//             //We sensed a beat!
//             long delta = millis() - lastBeat;
//             lastBeat = millis();

//             beatsPerMinute = 60 / (delta / 1000.0);

//             return beatsPerMinute;
//         }

//         float computeHeartRate(long lastBeat, byte RATE_SIZE) {
//             if (beatsPerMinute < 255 && beatsPerMinute > 20)
//             {
//               rates[rateSpot++] = (byte)beatsPerMinute; //Store this reading in the array
//               rateSpot %= RATE_SIZE; //Wrap variable
        
//               //Take average of readings
//               beatAvg = 0;
//               for (byte x = 0 ; x < RATE_SIZE ; x++)
//                 beatAvg += rates[x];
//               beatAvg /= RATE_SIZE;
//               return beatAvg;
//             }
//             return 0;
//         }

//         void logHeartRate(byte beatsPerMinute) {
//             Serial.print("IR=");
//             Serial.print(irValue);
//         }
//         void logBPM(byte beatsPerMinute) {
//             Serial.print(", BPM=");
//             Serial.print(beatsPerMinute);
//         }

//         void logAverageBPM(byte beatsPerMinute) {
//             Serial.print(", Avg BPM=");
//             Serial.print(beatAvg);
//         }



//         void detect() {
//             irValue = detectHeartbeat();
//             if (isHeartbeatDetected(irValue)) {
//                 calculateBPM(lastBeat);
//                 computeHeartRate(lastBeat, rateSize);
//             }
        
//             logHeartRate(beatsPerMinute);
//             logBPM(beatsPerMinute);
//             logAverageBPM(beatsPerMinute);
//             if (irValue < 50000)
//               Serial.print(" No finger?");
          
//             Serial.println();
//         }
// };

#endif