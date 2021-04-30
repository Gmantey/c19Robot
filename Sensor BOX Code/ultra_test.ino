#include <Wire.h>
#include <Adafruit_AMG88xx.h>

Adafruit_AMG88xx amg;

#define echoPin 2 // attach pin D2 Arduino to pin Echo of HC-SR04
#define trigPin 3 //attach pin D3 Arduino to pin Trig of HC-SR04
#define echoPin2 5 // attach pin D2 Arduino to pin Echo of HC-SR04
#define trigPin2 6 //attach pin D3 Arduino to pin Trig of HC-SR04
#define echoPin3 10 // attach pin D2 Arduino to pin Echo of HC-SR04
#define trigPin3 11 //attach pin D3 Arduino to pin Trig of HC-SR04

// defines variables
long duration; // variable for the duration of sound wave travel
int distance1; // variable for the distance measurement
int distance2; // variable for the distance measurement
int distance3; // variable for the distance measurement

void setup() {
  pinMode(trigPin, OUTPUT); // Sets the trigPin as an OUTPUT
  pinMode(echoPin, INPUT); // Sets the echoPin as an INPUT
  pinMode(trigPin2, OUTPUT); // Sets the trigPin as an OUTPUT
  pinMode(echoPin2, INPUT); // Sets the echoPin as an INPUT
  pinMode(trigPin3, OUTPUT); // Sets the trigPin as an OUTPUT
  pinMode(echoPin3, INPUT); // Sets the echoPin as an INPUT
  Serial.begin(9600); // // Serial Communication is starting with 9600 of baudrate speed
  Serial.println("Ultrasonic Sensor HC-SR04 Test"); // print some text in Serial Monitor
  Serial.println("with Arduino UNO R3");
  Serial.println(F("AMG88xx test"));

    bool status;
    
    // default settings
    status = amg.begin();
    if (!status) {
        Serial.println("Could not find a valid AMG88xx sensor, check wiring!");
        while (1);
    }
    
    Serial.println("-- Thermistor Test --");

    Serial.println();

    delay(5000); // let sensor boot up
}

typedef union {
  float floatingPoint;
  byte binary[4];
} binaryFloat;

void loop() {
  // Clears the trigPin condition
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  // Sets the trigPin HIGH (ACTIVE) for 10 microseconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  // Reads the echoPin, returns the sound wave travel time in microseconds
  duration = pulseIn(echoPin, HIGH);
  // Calculating the distance
  distance1 = duration * 0.034 / 2; // Speed of sound wave divided by 2 (go and back)

  digitalWrite(trigPin2, LOW);
  delayMicroseconds(2);
  // Sets the trigPin2 HIGH (ACTIVE) for 10 microseconds
  digitalWrite(trigPin2, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin2, LOW);
  // Reads the echoPin2, returns the sound wave travel time in microseconds
  duration = pulseIn(echoPin2, HIGH);
  // Calculating the distance
  distance2 = duration * 0.034 / 2; // Speed of sound wave divided by 2 (go and back)

  digitalWrite(trigPin3, LOW);
  delayMicroseconds(2);
  // Sets the trigPin2 HIGH (ACTIVE) for 10 microseconds
  digitalWrite(trigPin3, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin3, LOW);
  // Reads the echoPin2, returns the sound wave travel time in microseconds
  duration = pulseIn(echoPin3, HIGH);
  // Calculating the distance
  distance3 = duration * 0.034 / 2; // Speed of sound wave divided by 2 (go and back)
  
  binaryFloat hi;
  hi.floatingPoint = amg.readThermistor();

  Serial.write(distance1);
  Serial.write(distance2);
  Serial.write(distance3);
  hi.floatingPoint = (9 / 5.0) * hi.floatingPoint + 32;
  distance1 = (int) hi.floatingPoint; // Fahrenheit
  Serial.write(distance1);
  Serial.print(hi.floatingPoint);
  Serial.println("");
  Serial.println(Serial.read());
  Serial.println("Sent output!!!!");

  delay(2000);
}
