import streamlit as st
import requests
import time
from PIL import Image
import os

# Server URL (Laptop Flask API)
LAPTOP_SERVER_URL = "http://127.0.0.1:5000"

st.set_page_config(page_title="Intrusion Detection System", layout="wide")

st.title("🔒 Intrusion Detection System")
st.write("Monitor motion and sound detection in real-time.")

# Buttons to start/stop monitoring
col1, col2 = st.columns(2)

if col1.button("🟢 Start Monitoring"):
    st.session_state["monitoring"] = True

if col2.button("🔴 Stop Monitoring"):
    st.session_state["monitoring"] = False

# Display Latest Intruder Image
st.subheader("📷 Last Captured Intruder Image")

image_path = "intruder.jpg"
if os.path.exists(image_path):
    st.image(Image.open(image_path), caption="Intruder Detected!", use_column_width=True)
else:
    st.write("No intruder detected yet.")

# Real-time Intrusion Logs
st.subheader("📜 Intrusion Logs")

log_placeholder = st.empty()

# Continuously fetch intrusion logs
while st.session_state.get("monitoring", False):
    response = requests.get(f"{LAPTOP_SERVER_URL}/logs")
    logs = response.json().get("logs", [])
    log_placeholder.write("\n".join(logs[-10:]))  # Show last 10 logs
    time.sleep(2)
