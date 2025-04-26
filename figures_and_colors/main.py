import numpy as np
import matplotlib.pyplot as plt
from skimage import color
from skimage.measure import regionprops, label

def calculate_means(hsv_image):
    epsilon = np.diff(np.unique(hsv_image[:, :, 0])).mean()
    return [np.mean(vals) * 360 for vals in np.array_split(np.unique(hsv_image[:, :, 0]), np.where(np.diff(np.unique(hsv_image[:, :, 0])) > epsilon)[0] + 1)]

def calculate_midpoints(values):
    return [(v1 + v2) / 2 for v1, v2 in zip(values, values[1:] + [values[0] + 360])]

def determine_figure_color(region, hsv_image, border_values):
    color_value = hsv_image[int(region.centroid[0]), int(region.centroid[1]), 0] * 360
    colors = ['красный', 'желтый', 'зеленый', 'светло-зеленый', 'синий', 'фиолетовый']
    for i, border_color in enumerate(border_values):
        if color_value < border_color:
            if i < len(colors):
                return colors[i]
            else:
                return 'Неизвестный цвет'
    return 'red'

image = plt.imread('balls_and_rects.png')
hsv_image = color.rgb2hsv(image)
binary_mask = (np.sum(image, 2) > 0).astype(int)
labeled_regions = label(binary_mask)
regions_info = regionprops(labeled_regions)

color_means = calculate_means(hsv_image)
border_values = calculate_midpoints(color_means)

figures_circle = {}
figures_rect = {}

for region in regions_info:
    color_figure = determine_figure_color(region, hsv_image, border_values)
    figures_dict = figures_circle if np.all(region.image) else figures_rect
    figures_dict[color_figure] = figures_dict.get(color_figure, 0) + 1

print('Total Regions:', labeled_regions.max())
print('Circles:', figures_circle)
print('Rectangles:', figures_rect)
print('Rectangles:', figures_rect)
