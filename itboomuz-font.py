import math
import os
import turtle
import numpy as np
from fontTools.ttLib import TTFont
from PIL import Image
from _3d import perspective, look_at
from _helpers import save_as_png

font = TTFont("./assets/blaster-regular.ttf")
projection_matrix = perspective(90, 1, -1000, 1000)


wn = turtle.Screen()
wn.bgcolor("black")
wn.title("itboom.uz")
wn.screensize(500, 500)

pen = turtle.Turtle()
pen.speed(0)
pen.hideturtle()

ANGLE = 30
TEXT_SCALE = 15
POINT_SCALE = 200
LETTER_SPACE = 10
TEXT = "itboom.uz"


def point3d_to_screen(view_matrix, point_3d):
    point_2d_homogeneous = np.dot(projection_matrix, np.dot(view_matrix, point_3d))
    return POINT_SCALE * point_2d_homogeneous[:2] / point_2d_homogeneous[3]


def letter_to_screen(view_matrix, point, glyp):
    point_3d = np.array([(point[0] - glyp.xMin) / TEXT_SCALE, (point[1] - glyp.yMin) / TEXT_SCALE, 0, 1])
    return point3d_to_screen(view_matrix, point_3d)


def draw_letter(view_matrix, glyp):
    first_index = 0
    for idx, p in enumerate(glyp.coordinates):
        pen.goto(letter_to_screen(view_matrix, p, glyp))
        if not pen.isdown():
            pen.down()

        if idx in glyp.endPtsOfContours:
            pen.goto(letter_to_screen(view_matrix, glyp.coordinates[first_index], glyp))
            pen.up()
            first_index = idx + 1


def draw_line(view_matrix, start, end, color):
    pen.color(color)
    start = point3d_to_screen(view_matrix, start)
    end = point3d_to_screen(view_matrix, end)
    pen.up()
    pen.goto(*start)
    pen.down()
    pen.goto(*end)


def get_glyp(letter):
    glyph_name = font.getBestCmap()[ord(letter)]
    return font['glyf'][glyph_name]


pen.clear()

a = math.radians(ANGLE)
view_matrix = look_at(np.array([250 * math.sin(a), 50, 250 * math.cos(a)]), np.array([0, 0, 0]), np.array([0, 1, 0]))

draw_line(view_matrix, [-250, 0, 0, 1], [250, 0, 0, 1], "#ff0000")
draw_line(view_matrix, [0, -250, 0, 1], [0, 250, 0, 1], "#00ff00")
draw_line(view_matrix, [0, 0, -250, 1], [0, 0, 250, 1], "#0000ff")

pen.color("#FF6F06")

text_size = 0
for letter in TEXT:
    glyp = get_glyp(letter)
    text_size += (glyp.xMax - glyp.xMin + LETTER_SPACE) / TEXT_SCALE

pos_x = -text_size / 2

for i, letter in enumerate(TEXT):
    glyp = get_glyp(letter)
    size = (glyp.xMax - glyp.xMin) / TEXT_SCALE

    transformation_matrix = np.array([
        [1, 0, 0, pos_x],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
    ])

    pen.up()
    draw_letter(np.dot(view_matrix, transformation_matrix), glyp)

    pos_x += size + LETTER_SPACE


# Rasm qilib saqlash
save_as_png("itboomuz-font", wn)
turtle.done()
