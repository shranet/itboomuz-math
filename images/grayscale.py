import matplotlib.pyplot as plt
from PIL import Image
import numpy as np

img = Image.open("../assets/image-1.png")
img_data = np.array(img)

for y in range(img.height):
    for x in range(img.width // 2, img.width):
        r, g, b = map(int, img_data[y, x])
        # uchta rangning o'rta arifmetigi
        k = (r + g + b) // 3
        img_data[y, x] = (k, k, k)

plt.imshow(img_data)
plt.title('itboom.uz')
plt.axis('off')  # Hide the axis
plt.show()
