import cv2
import numpy as np
import requests

# Discord Webhook URL
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1553835941649448996/yIFXH6xmHzzNdxitAsQFrNTRVHORWg0F-GOY8au6PXmcwjJgY_JRcgwZKje1zVpvWhFS"

cap = cv2.VideoCapture(0)

fire_frames = 0
ALARM_THRESHOLD = 8 
MIN_FIRE_AREA = 150   

while True:
    ret, frame = cap.read()
    if not ret:
        break
        
    frame = cv2.resize(frame, (640, 480))
    blur = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
    
    # Catch both deep red/orange and bright yellow/white-hot flames
    # 1. Mask for the intense orange/red aura (High saturation, High brightness)
    lower_orange = np.array([0, 150, 200], dtype=np.uint8)
    upper_orange = np.array([35, 255, 255], dtype=np.uint8)
    mask_orange = cv2.inRange(hsv, lower_orange, upper_orange)
    
    # 2. Mask for the white-hot core of the match (Low saturation, Max brightness)
    lower_white = np.array([0, 0, 230], dtype=np.uint8)
    upper_white = np.array([179, 60, 255], dtype=np.uint8)
    mask_white = cv2.inRange(hsv, lower_white, upper_white)
    
    # Combine both masks to get the full flame profile
    mask = cv2.bitwise_or(mask_orange, mask_white)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    fire_detected_this_frame = False
    
    for contour in contours:
        if cv2.contourArea(contour) > MIN_FIRE_AREA:
            fire_detected_this_frame = True
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
            cv2.putText(frame, "FIRE DETECTED", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            
    if fire_detected_this_frame:
        fire_frames += 1
        
        if fire_frames == ALARM_THRESHOLD and DISCORD_WEBHOOK_URL:
            print("Sending emergency alert...")
            requests.post(DISCORD_WEBHOOK_URL, json={"content": "🚨 **FIRE DETECTED ON CAMERA **"})
            
        if fire_frames >= ALARM_THRESHOLD:
            cv2.putText(frame, "STATUS: ALARM ACTIVE", (30, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
    else:
        
        if fire_frames > 0:
            fire_frames -= 1 
            
    cv2.imshow("Detection Feed", frame)
    cv2.imshow("Fire Mask (White = Detected)", mask)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()


