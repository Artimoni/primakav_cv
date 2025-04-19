import matplotlib.pyplot as plt
import numpy as np
from skimage.measure import label
from skimage.morphology import (binary_closing, binary_opening, binary_dilation, binary_erosion)

data = np.load(r"wires6npy.txt") #r -  отключение интерпретации escape-последовательностей.

labeled = label(data) #маркируем
initial_parts = np.max(labeled) #считаем кол-во объектов

result = binary_erosion(data, np.ones(3).reshape(3, 1)) #разделить провода(файл wires) на части

labeled = label(result)
parts = np.max(labeled)

if parts > initial_parts:
    print(f"Порван на {parts} частей")
elif parts == initial_parts:
    print("Не порван")
else:
    print(f"Провод {parts} уничтожен")
plt.subplot(121)
plt.imshow(result)
plt.subplot(122)
plt.imshow(data)
plt.show()