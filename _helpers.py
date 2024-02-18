import os
from PIL import Image


def save_as_png(name, wn):
    output_ps_file = os.path.join(f"./output/{name}.ps")
    canvas = wn.getcanvas()
    canvas.postscript(file=output_ps_file, colormode='color')

    img = Image.open(os.path.join(output_ps_file))
    img.save(f"./output/{name}.png")
