#include <Wire.h>
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include<SoftwareSerial.h> //Included SoftwareSerial Library

#define HOST "testbase26.000webhostapp.com"          // Enter HOST URL without "http:// "  and "/" at the end of URL
#define WIFI_SSID "Iphone"            // WIFI SSID here                                   
#define WIFI_PASSWORD "Jesus123"        // WIFI password here

// Declare global variables which will be uploaded to server

int val = 0;
String sendval, sendval2, sendval3, sendval4, postData;
SoftwareSerial s(3,1);

void setup() {
  Serial.begin(9600);
  s.begin(9600);
  
  pinMode(LED_BUILTIN, OUTPUT);     // initialize built in led on the board
  
  WiFi.mode(WIFI_STA);           
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);                                     //try to connect with wifi
  //Serial.print("Connecting to ");
  //Serial.print(WIFI_SSID);
  while (WiFi.status() != WL_CONNECTED) 
  { //Serial.print(".");
      delay(500); }

  delay(5000);
}

typedef union {
  float floatingPoint;
  byte binary[4];
} binaryFloat;

void loop() {
  HTTPClient http;    // http object of clas HTTPClient
  binaryFloat hi;
  
  // Convert integer variables to string
  val = s.read();
  sendval = String(val);
  val = s.read();
  sendval2 = String(val);
  val = s.read();
  sendval3 = String(val);
  val = s.read();
  sendval4 = String(val);
   
  postData = "sendval=" + sendval + "&sendval2=" + sendval2 + "&sendval3=" + sendval3 + "&sendval4=" + sendval4;
    
  http.begin("http://testbase26.000webhostapp.com/dbwrite.php");              // Connect to host where MySQL databse is hosted
  http.addHeader("Content-Type", "application/x-www-form-urlencoded");            //Specify content-type header  
   
  int httpCode = http.POST(postData);   // Send POST request to php file and store server response code in variable named httpCode
  
  // if connection eatablished then do this
  if (httpCode == 200) {
    s.write(httpCode);
  } else {
    s.write(httpCode);
    http.end(); 
    return;
  }

  delay(2000);
}
