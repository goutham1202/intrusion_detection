from flask import Flask, jsonify
import cv2
import smtplib
import imghdr
from email.message import EmailMessage
import time

app = Flask(__name__)

# Email Configuration
EMAIL_SENDER = "anjan23102002@gmail.com"
EMAIL_PASSWORD = "btsufisfwygrasom"
EMAIL_RECEIVER = "shreedivya1920@gmail.com"

# Intrusion Logs
intrusion_logs = []

def log_intrusion(message):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    intrusion_logs.append(f"{timestamp} - {message}")
    print(f"[LOG] {message}")

def send_email(image_path):
    msg = EmailMessage()
    msg["Subject"] = "🚨 Intrusion Alert!"
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER
    msg.set_content("Intrusion detected! See the attached image.")

    with open(image_path, "rb") as f:
        file_data = f.read()
        file_type = imghdr.what(f.name)
        file_name = f.name

    msg.add_attachment(file_data, maintype="image", subtype=file_type, filename=file_name)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
        smtp.send_message(msg)

@app.route("/capture", methods=["GET"])
def capture_image():
    cap = cv2.VideoCapture(0)  # Open laptop camera
    ret, frame = cap.read()
    image_path = "intruder.jpg"

    if ret:
        cv2.imwrite(image_path, frame)  # Save the captured image
        send_email(image_path)  # Send the image via email
        log_intrusion("Intrusion detected! Email sent with image.")
        message = "🚀 Intrusion Alert Sent!"
    else:
        log_intrusion("Failed to capture image.")
        message = "❌ Failed to Capture Image"

    cap.release()
    return jsonify({"message": message})

@app.route("/logs", methods=["GET"])
def get_logs():
    return jsonify({"logs": intrusion_logs})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
