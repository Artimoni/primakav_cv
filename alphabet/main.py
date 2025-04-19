from skimage.measure import label
from skimage.measure import regionprops
from skimage.morphology import binary_closing, binary_dilation, binary_opening, binary_erosion
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
from pathlib import Path

def filling_factor(region):
    return np.sum(region.image) / region.image.size

def has_line(region, horizontal=True):
    return 1. in np.mean(region.image, int(horizontal))

def count_holes(region):
    holes = 0
    labeled = label(np.logical_not(region.image))
    regions = regionprops(labeled)
    for region in regions:
        not_bound = True
        coords = np.where(labeled == region.label)
        for y, x in zip(*coords):
            if y == 0 or x == 0 or y == labeled.shape[0] - 1 or x == labeled.shape[1] - 1:
                not_bound = False
        holes += not_bound
    return holes

def recognize(region):
    if filling_factor(region) == 1.0:
        return '-'
    else:
        holes = count_holes(region)
        if holes == 2: #B 8
            if has_line(region, False) and region.image[0, 0] > 0:
                return 'B'
            else: 
                return '8'
        if holes == 1: #A 0
            ny, nx = region.centroid_local[0]/region.image.shape[0], region.centroid_local[1]/region.image.shape[1]
            if np.isclose(ny, nx, 0.05):
                if has_line(region, False):
                    if ny >= 0.4:
                        return 'D'
                    else:
                        return 'P'
                return '0'
            else:
                if has_line(region, False):
                    if ny >= 0.4:
                        return 'D'
                    else:
                        return 'P'
                return 'A'
        else: # W X / * 1
            if has_line(region, False):
                return '1'
            if has_line(region):
                return '*'
            inv = np.logical_not(region.image)
            labeled = label(inv)
            holes = np.max(labeled)
            match holes:
                case 2: return '/'
                case 4: return 'X'
                case _: return 'W'
    return '_'

image = plt.imread('symbols.png')
image = np.mean(image, 2)
image[image>0] = 1

labeled = label(image)
symbols = np.max(labeled)
regions = regionprops(labeled)
result = defaultdict(lambda: 0)

path = Path('.') / 'result'
path.mkdir(exist_ok=True)

plt.figure()
for i, region in enumerate(regionprops(labeled)):
    symbol = recognize(region)
    #if symbol == 'P' or symbol == 'D':
    result[symbol] += 1

    plt.clf()
    plt.title(f'{symbol=}')
    plt.imshow(region.image)
    plt.tight_layout()
    plt.savefig(path/f'{i}.png')

print(result, sum(result.values()))
#plt.title(f'Holes = {count_holes(regions[nfig])}')
#plt.imshow(regions[nfig].image)
#plt.show()