// This #include statement was automatically added by the Particle IDE.
#include <MQTT.h>

#include "Adafruit_DHT.h"

#define DHTPIN D2     // DHT data pin set as D2 on the Argon

#define DHTTYPE DHT22

MQTT client("test.mosquitto.org", 1883, callback);

void callback(char* topic, byte* payload, unsigned int length)
{}

DHT dht(DHTPIN, DHTTYPE);   // create a DHT object to work with

float t = 0;
float h = 0;

void setup() {

	dht.begin(); // start the DHT object
	client.connect("argonThermometer");
	
}

void loop() {
    // Wait a few seconds between measurements.
	delay(2000);
	
	if(client.isConnected())

	h = dht.getHumidity();
// Read temperature as Celsius
	t = dht.getTempCelcius();

	client.publish("snugnsound/temp", String(t));
	client.publish("snugnsound/humidity", String(h));
}
