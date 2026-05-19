from picamera2 import Picamera2
import time

# Initialize camera
picam2 = Picamera2()
picam2.start()

# Wait for camera to warm up
time.sleep(2)

# Capture image
picam2.capture_file("Javeriana_test.jpg")
print("Image captured: Javeriana_test.jpg")

# Stop camera
picam2.stop()
picam2.close()
