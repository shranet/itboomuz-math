from PIL import Image
import os

dir = "./output"
files = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f)) and f.endswith(".ps")]

for f in files:
    print(f)

    output_file = os.path.join(dir, f"png/{f}.png")
    if not os.path.isfile(output_file):
        img = Image.open(os.path.join(dir, f))
        img.save(output_file)


