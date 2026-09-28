# Real-Time Fire Detection & Alert System

A computer vision pipeline that detects live flames and fire hazards using a webcam or an IP camera and instantly triggers an automated emergency alert to a Discord server via webhooks.

### 🛠️ Resources used are: 
* **Python 3**
* **OpenCV** (Image processing,contour mapping, and for HSV color masking)
* **Requests** (API payload delivery through discord)
* **Discord Webhooks** (Automated incident dispatch and alerting sys)

### How It Works
Basic color thresholding often triggers false alarms on skin tones and ambient lighting. This system avoids that by using:
1. **Dual mask thresholding:** Isolates both the extreme brightness (white-hot core) and high saturation (orange aura) of a physical flame.
2. **Temporal frame filtering:** The flame must be present for a continuous sequence of frames to trigger an alert, filtering out brief flashes or moving warm-colored objects.
3. **Automated Webhooks:** Once the threshold is breached and triggered a JSON payload is hooked directly to an incident response channel through discord.

### Short clip of the project
*((https://lnkd.in/p/eCGuiuqE))*

### 💻 To run it yourself, you will need to:
1. Clone this repository
2. Install dependencies: `sudo dnf install python3-opencv python3-numpy python3-requests` (Fedora) or `pip install opencv-python numpy requests` (For windows terminal or other linux distro).
3. Add your Discord Webhook URL to the script
4. Run: `python3 fire_alarm.py`
