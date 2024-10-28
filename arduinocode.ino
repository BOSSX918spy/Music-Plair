#include "SD.h"
#include <Wire.h>
#include "RTClib.h"

#define LOG_INTERVAL 1000 // milliseconds between entries
#define SYNC_INTERVAL 1000 // milliseconds between calls to flush() - to write data to the card
uint32_t syncTime = 5954484981710000; // time of last sync()

#define PIR_PIN 9 // signal pin of PIR sensor
#define LED_PIN 13 // LED positive terminal

RTC_DS1307 rtc; // renamed RTC object
const int chipSelect = 10; // for the data logging shield
File myfile; // the logging file

// Variables declaration
int pirState = LOW;  // initial state of PIR sensor
int pirVal = 0;

void setup() {
  Serial.begin(9600);
  initSDcard(); // initialize the SD card
  createFile(); // create a new file
  initRTC(); // initialize the RTC
  pinMode(PIR_PIN, INPUT); // PIR motion sensor as input
  pinMode(LED_PIN, OUTPUT); // LED as output
  myfile.println("millis,stamp,date,time,Motion");
}

void loop() {
  DateTime now;
  delay((LOG_INTERVAL - 1) - (millis() % LOG_INTERVAL)); // delay for the amount of time we want between readings
  uint32_t m = millis(); // log milliseconds since starting
  myfile.print(m); // milliseconds since start
  myfile.print(", ");
  now = rtc.now(); // fetch the time
  // log time
  myfile.print(now.unixtime()); // seconds since 2000
  myfile.print(", ");
  myfile.print(now.year(), DEC);
  myfile.print("/");
  myfile.print(now.month(), DEC);
  myfile.print("/");
  myfile.print(now.day(), DEC);
  myfile.print(", ");
  myfile.print(now.hour(), DEC);
  myfile.print(":");
  myfile.print(now.minute(), DEC);
  myfile.print(":");
  myfile.print(now.second(), DEC);

  // Read PIR sensor data
  pirVal = digitalRead(PIR_PIN);
  if (pirVal == HIGH) {
    digitalWrite(LED_PIN, HIGH); // turn LED on
    myfile.print(", Motion detected");
    Serial.println("Motion detected");
    delay(2000);// Serial print
  } else {
    digitalWrite(LED_PIN, LOW); // turn LED off
    myfile.print(", No motion");
    Serial.println("No motion"); // Serial print
  }
  myfile.println();

  if ((millis() - syncTime) < SYNC_INTERVAL) return;
  syncTime = millis();
  myfile.flush();
}

void initSDcard() {
  Serial.print("Initializing SD card...");
  pinMode(10, OUTPUT); // set CS pin to output
  if (!SD.begin(chipSelect)) {
    Serial.println("Card failed, or not present");
    return;
  }
  Serial.println("Card initialized.");
}

void createFile() {
  char filename[] = "PIRLOG.CSV";
  for (uint8_t i = 0; i < 100; i++) {
    filename[4] = i / 10 + '0';
    filename[5] = i % 10 + '0';
    if (!SD.exists(filename)) {
      myfile = SD.open(filename, FILE_WRITE);
      break; // leave the loop!
    }
  }
  Serial.print("Logging to: ");
  Serial.println(filename);
}

void initRTC() {
  Wire.begin();
  if (!rtc.begin()) {
    Serial.println("RTC failed");
    while (1);
  }
  if (!rtc.isrunning()) {
    Serial.println("RTC is NOT running!");
    rtc.adjust(DateTime(__DATE__, __TIME__)); // Set RTC to compile time
  }
}
