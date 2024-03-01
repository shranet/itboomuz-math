import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
from matplotlib.animation import FuncAnimation

img1 = Image.open("../assets/image-1.png")
img1_data = np.array(img1)
img2_data = np.array(Image.open("../assets/image-2.png"))

FRAMES = 100
alpha_0 = np.tile(np.arange(100), (img1.width, 1)).T / 100
alpha_1 = 1 - alpha_0

alpha_0_3 = np.repeat(alpha_0[:, :, np.newaxis], 3, axis=2)
alpha_1_3 = np.repeat(alpha_1[:, :, np.newaxis], 3, axis=2)


def update_transition(frame):
    w = int(img1.width * frame / FRAMES)
    if w > 0:
        data1 = img1_data[:w]

        w2 = min(100, img1.height - w)
        if w2 > 0:
            data1_alpha = img1_data[w:w + w2] * alpha_1_3[:w2]
            data2_alpha = img2_data[w:w + w2] * alpha_0_3[:w2]
            data2 = img2_data[w + w2:]

            im.set_array(np.concatenate((data1, (data1_alpha + data2_alpha).astype(int), data2), axis=0))
    return im


fig, ax = plt.subplots()
ani = FuncAnimation(fig, update_transition, frames=FRAMES, interval=50)

im = plt.imshow(img2_data)
plt.title('itboom.uz')
plt.axis('off')  # Hide the axis
plt.show()
