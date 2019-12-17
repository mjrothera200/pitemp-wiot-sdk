import wiotp.sdk.device
import RPi.GPIO as GPIO
import dht11
import time


# initialize GPIO
GPIO.setwarnings(True)
GPIO.setmode(GPIO.BCM)


# read data using pin 17
instance = dht11.DHT11(pin=17)

myConfig = { 
    "identity": {
        "orgId": "cg3orm",
        "typeId": "pitemp",
        "deviceId": "pi1"
    },
    "auth": {
        "token": "12345678"
    }
}
client = wiotp.sdk.device.DeviceClient(config=myConfig)

client.connect()


while True:
	time.sleep(6)
	result = instance.read()
	if result.is_valid():
		temp_c = result.temperature
		temp_f = (result.temperature * 9)/5 + 32
		humidity = result.humidity
		message = { 'd': {'temp_c': temp_c, 'temp_f': temp_f, 'humidity': humidity } }
		client.publishEvent(eventId="environmentals", msgFormat="json", data=message, qos=0, onPublish=None)


