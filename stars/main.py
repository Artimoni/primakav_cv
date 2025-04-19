import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import label, regionprops
from scipy.ndimage import binary_hit_or_miss

image = np.load("stars.npy")
binary = (image > 0.8).astype(np.uint8)
plus = np.array([
    [0, 1, 0],
    [1, 1, 1],
    [0, 1, 0]
], dtype=np.uint8)

cross = np.array([
    [1, 0, 1],
    [0, 1, 0],
    [1, 0, 1]
], dtype=np.uint8)

plus_match = binary_hit_or_miss(binary, plus)
cross_match = binary_hit_or_miss(binary, cross)
cross_match = np.logical_and(cross_match, np.logical_not(plus_match))
plus_count = label(plus_match).max()
cross_count = label(cross_match).max()

print(f"Plus: {plus_count}")
print(f"Cross: {cross_count}")

plt.figure(figsize=(10, 5))
plt.subplot(121)
plt.imshow(binary, cmap='gray')
plt.title(f"Plus: {plus_count} | Cross: {cross_count}")
plt.show()