import cv2
import numpy as np

def get_hsv_range(image, tolerance=20):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    hsv_mean = cv2.mean(hsv)[:3]

    lower = np.array([
        max(0, hsv_mean[0] - tolerance),
        max(0, hsv_mean[1] - tolerance),
        max(0, hsv_mean[2] - tolerance)
    ], dtype=np.uint8)

    upper = np.array([
        min(179, hsv_mean[0] + tolerance),
        min(255, hsv_mean[1] + tolerance),
        min(255, hsv_mean[2] + tolerance)
    ], dtype=np.uint8)

    return lower, upper

def count_matches_by_color(video_path, template_path, area_threshold=1000):
    image = cv2.imread(template_path)

    lower, upper = get_hsv_range(image)

    cap = cv2.VideoCapture(video_path)

    count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower, upper)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > area_threshold:
                count += 1
                break  

    cap.release()
    return count

img = "Primak.png"
video = "output.avi"

matches = count_matches_by_color(video, img)
print(f"Количество кадров {matches}")
