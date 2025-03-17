import numpy as np
import matplotlib.pyplot as plt

external = np.diag([1, 1, 1, 1]).reshape(4, 2, 2)
internal = np.logical_not(external)
cross = np.array([[[1, 0], [0, 1]], [[0, 1], [1, 0]]])

def match(a, masks):
    for mask in masks:
        if np.all(a == mask):
            return True
    return False

def count_objects(image):
    threshold = np.mean(image)
    binary_image = (image > threshold).astype(int)
    E = 0
    for y in range(0, image.shape[0] - 1):
        for x in range(0, image.shape[1] - 1):
            sub = binary_image[y : y + 2, x : x + 2]
            external_match = np.sum(sub) == 0
            internal_match = np.sum(sub) == 4
            if sub.ndim == 2:
                cross_match = np.sum(sub) == 2 and np.array_equal(np.diag(sub), np.diag(np.fliplr(sub)))
            else:
                cross_match = False
            if external_match:
                E += 1
            elif internal_match:
                E -= 1
            elif cross_match:
                E += 2
    return E / 4

image1 = np.load("example2.npy")
image2 = np.load("example2.npy")
images = [image1, image2]

for i, image in enumerate(images):
    count = count_objects(image)
    print(f"Количество объектов на изображении {i+1}: {count}")

plt.figure()
plt.imshow(image1, cmap='gray')
plt.show()
