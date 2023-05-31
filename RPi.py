import paho.mqtt.client as mqtt
import paho.mqtt.publish as publish
import RPi.GPIO as GPIO
import time

highTemp = 10
greenTemp = 11
lowTemp = 12

highHumidity = 36
greenHumidity = 38
lowHumidity = 40

GPIO.setmode(GPIO.BOARD)
GPIO.setup(highTemp, GPIO.OUT)
GPIO.setup(greenTemp, GPIO.OUT)
GPIO.setup(lowTemp, GPIO.OUT)
GPIO.setup(highHumidity, GPIO.OUT)
GPIO.setup(greenHumidity, GPIO.OUT)
GPIO.setup(lowHumidity, GPIO.OUT)

lowTempThreshold = 17.5
highTempThreshold = 22.5
lowHumidityThreshold = 30.5
highHumidityThreshold = 70.5

def processMessage(client, userdata, message):
    topic = str(message.topic)
    message = str(message.payload.decode("utf-8"))
    print(topic + " " + message)
    if topic == "snugnsound/temp":
        assessTemp(message)
    elif topic == "snugnsound/humidity":
        assessHumidity(message)

def assessTemp(tempString):
    if float(tempString) < lowTempThreshold:
        GPIO.output(lowTemp, GPIO.HIGH)
        GPIO.output(highTemp, GPIO.LOW)
        GPIO.output(greenTemp, GPIO.LOW)
        publish.single("snugnsound/temp/alerts", "The temperature is too low", hostname="test.mosquitto.org")
    elif float(tempString) > highTempThreshold:
        GPIO.output(lowTemp, GPIO.LOW)
        GPIO.output(highTemp, GPIO.HIGH)
        GPIO.output(greenTemp, GPIO.LOW)
        publish.single("snugnsound/temp/alerts", "The temperature is too high", hostname="test.mosquitto.org")
    else:
        GPIO.output(lowTemp, GPIO.LOW)
        GPIO.output(highTemp, GPIO.LOW)
        GPIO.output(greenTemp, GPIO.HIGH)
        
def assessHumidity(humidityString):
    if float(humidityString) < lowHumidityThreshold:
        GPIO.output(lowHumidity, GPIO.HIGH)
        GPIO.output(highHumidity, GPIO.LOW)
        GPIO.output(greenHumidity, GPIO.LOW)
        publish.single("snugnsound/humidity/alerts", "The humidity is too low", hostname="test.mosquitto.org")
    elif float(humidityString) > highHumidityThreshold:
        GPIO.output(lowHumidity, GPIO.LOW)
        GPIO.output(highHumidity, GPIO.HIGH)
        GPIO.output(greenHumidity, GPIO.LOW)
        publish.single("snugnsound/humidity/alerts", "The humidity is too high", hostname="test.mosquitto.org")
    else:
        GPIO.output(lowHumidity, GPIO.LOW)
        GPIO.output(highHumidity, GPIO.LOW)
        GPIO.output(greenHumidity, GPIO.HIGH)
    
    
client = mqtt.Client("rpi")
client.connect("test.mosquitto.org", 1883)
client.loop_start()
client.subscribe("snugnsound/temp")
client.subscribe("snugnsound/humidity")
client.subscribe("snugnsound/temp/alerts")
client.subscribe("snugnsound/humidity/alerts")
client.on_message = processMessage

while(1):
    time.sleep(1)
