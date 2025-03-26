import RPi.GPIO as GPIO
import time
import requests

# Define GPIO Pins
PIR_PIN = 17     # PIR Sensor Pin
SOUND_PIN = 27   # Sound Sensor Pin
LED_PIN = 22     # LED Indicator Pin

# Server URL (Laptop API)
LAPTOP_SERVER_URL = "http:// 172.17.10.206:5000/capture"

# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN)
GPIO.setup(SOUND_PIN, GPIO.IN)
GPIO.setup(LED_PIN, GPIO.OUT)

def detect_intrusion():
    while True:
        motion_detected = GPIO.input(PIR_PIN)
        sound_detected = GPIO.input(SOUND_PIN)

        if motion_detected or sound_detected:
            print("🚨 Intrusion Detected!")
            GPIO.output(LED_PIN, GPIO.HIGH)  # Turn ON LED

            try:
                response = requests.get(LAPTOP_SERVER_URL)
                print(response.json()["message"])
            except:
                print("❌ Failed to notify the laptop.")

            time.sleep(5)  # Wait before checking again
            GPIO.output(LED_PIN, GPIO.LOW)  # Turn OFF LED

try:
    detect_intrusion()
except KeyboardInterrupt:
    print("Exiting...")
    GPIO.cleanup()
