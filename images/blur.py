import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
import math


img = Image.open("../assets/image-2.png")
img_data = np.array(img)
radius = 30
sigma = radius // 2

rwidth = 2 * radius + 1
kernel = np.zeros((rwidth, rwidth), np.float32)


def claim(v, mn, mx):
    return max(min(v, mx), mn)


for y in range(-radius, radius + 1):
    for x in range(-radius, radius + 1):
        expNum = -(x ** 2 + y ** 2)
        expDen = 2 * sigma ** 2
        e = pow(math.e, expNum / expDen)
        value = e / (2 * math.pi * sigma ** 2)
        kernel[y + radius, x + radius] = value


kernel = kernel / kernel.sum()
kernel_3 = np.repeat(kernel[:, :, np.newaxis], 3, axis=2)


def render(y):
    result = img_data[y]

    for x in range(img.width // 2, img.width):
        sx, sy = max(x - radius, 0), max(y - radius, 0)
        wx, wy = min(sx + rwidth, img.width), min(sy + rwidth, img.height)

        data = img_data[sy:wy, sx:wx] * kernel_3[:wy - sy, :wx - sx]

        r = np.sum(data[:, :, 0])
        g = np.sum(data[:, :, 1])
        b = np.sum(data[:, :, 2])

        result[x] = (int(r), int(g), int(b))


if __name__ == "__main__":
    for y in range(img.height):
        render(y)

    plt.imshow(img_data)
    plt.title('itboom.uz')
    plt.axis('off')  # Hide the axis
    plt.show()
