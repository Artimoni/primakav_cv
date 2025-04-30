import numpy as np
import cv2

all_pencils = 0
for i in range(1, 13):
    pencils = 0
    image = cv2.imread(f"pencils/images/img ({i}).jpg",  cv2.IMREAD_GRAYSCALE) 
    thresh = cv2.bitwise_not(cv2.erode(cv2.threshold(image, 120, 255,cv2.THRESH_BINARY)[1], None, iterations = 40))

    mask = np.zeros(thresh.shape, dtype="uint8")

    output = cv2.connectedComponentsWithStats(thresh, 4, cv2.CV_32S)
    (numLabels, labels, stats, centroids) = output
    for j in range(1, numLabels):
        x, y, w, h = stats[j, cv2.CC_STAT_LEFT], stats[j, cv2.CC_STAT_TOP], stats[j, cv2.CC_STAT_WIDTH], stats[j, cv2.CC_STAT_HEIGHT]
        area = stats[j, cv2.CC_STAT_AREA]
        (cX, cY) = centroids[j]

        if area > 500000 and area < 700000:
            pencils += 1
            all_pencils += 1
        
    print(f"On the picture {i} {pencils} pencils")   
print(f"{all_pencils} on the all pictures") 
