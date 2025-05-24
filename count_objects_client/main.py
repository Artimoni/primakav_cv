import cv2
import zmq
import numpy as np

address = "84.237.21.36"
port = 6002

ctx = zmq.Context()
subscriber = ctx.socket(zmq.SUB)
subscriber.setsockopt(zmq.SUBSCRIBE, b"")
subscriber.connect(f"tcp://{address}:{port}")

cv2.namedWindow("ClientWindow", cv2.WINDOW_GUI_NORMAL)
frame_counter = 0

struct_elem = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))

while True:
    raw_msg = subscriber.recv()
    img = cv2.imdecode(np.frombuffer(raw_msg, np.uint8), cv2.IMREAD_COLOR)
    frame_counter += 1

    blurred_img = cv2.GaussianBlur(img, (7, 7), 0)
    hsv_img = cv2.cvtColor(blurred_img, cv2.COLOR_BGR2HSV)
    gray_img = cv2.cvtColor(hsv_img, cv2.COLOR_BGR2GRAY)
    _, binary_img = cv2.threshold(gray_img, 90, 255, cv2.THRESH_BINARY)
    eroded_img = cv2.erode(binary_img, struct_elem, iterations=2)

    contours, _ = cv2.findContours(eroded_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    total_objects = len(contours)
    count_circles = 0
    count_rects = 0

    for cnt in contours:
        epsilon_val = 0.03 * cv2.arcLength(cnt, True)
        approx_poly = cv2.approxPolyDP(cnt, epsilon_val, True)

        for pt in approx_poly:
            cv2.circle(eroded_img, tuple(pt[0]), 6, (0, 255, 0), 2)

        if len(approx_poly) <= 5:
            count_rects += 1
        else:
            count_circles += 1

    cv2.putText(
        img,
        f"Frame: {frame_counter}",
        (10, 60),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 0, 0),
        2,
    )
    cv2.putText(
        img,
        f"Objects: {total_objects}",
        (10, 120),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 0, 0),
        2,
    )
    cv2.putText(
        img,
        f"Circles: {count_circles}",
        (10, 180),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 0, 0),
        2,
    )
    cv2.putText(
        img,
        f"Rectangles: {count_rects}",
        (10, 240),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (255, 0, 0),
        2,
    )

    cv2.imshow("ClientWindow", img)
    cv2.imshow("ContoursMask", eroded_img)

    if cv2.waitKey(1) == ord("q"):
        break

cv2.destroyAllWindows()
