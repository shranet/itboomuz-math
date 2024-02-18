import math
import turtle
import numpy as np
from _3d import perspective, look_at
from _helpers import save_as_png


projection_matrix = perspective(90, 1, -1000, 1000)


wn = turtle.Screen()
wn.bgcolor("white")
wn.title("itboom.uz")
wn.screensize(500, 500)

pen = turtle.Turtle()
pen.speed(0)
pen.hideturtle()

BOX_SIZE = 10


def draw_3d(pen, projection_matrix, view_matrix, points, scale=200):
    for point in points:
        jump = False
        if len(point) == 4:
            jump = True
            point = point[:3]

        point_3d = np.array([*point, 1])
        point_2d_homogeneous = np.dot(projection_matrix, np.dot(view_matrix, point_3d))
        point_2d = scale * point_2d_homogeneous[:2] / point_2d_homogeneous[3]

        if jump:
            pen.penup()

        pen.goto(point_2d)
        if jump:
            pen.pendown()


def letter_i(vm):
    draw_3d(pen, projection_matrix, vm, [
        (-0.5 * BOX_SIZE, 3 * BOX_SIZE, 0, True),
        (-0.5 * BOX_SIZE, 2 * BOX_SIZE, 0),
        (0.5 * BOX_SIZE, 2 * BOX_SIZE, 0),
        (0.5 * BOX_SIZE, 3 * BOX_SIZE, 0),
        (-0.5 * BOX_SIZE, 3 * BOX_SIZE, 0),

        (-0.5 * BOX_SIZE, 1 * BOX_SIZE, 0, True),
        (-0.5 * BOX_SIZE, -3 * BOX_SIZE, 0),
        (0.5 * BOX_SIZE, -3 * BOX_SIZE, 0),
        (0.5 * BOX_SIZE, 1 * BOX_SIZE, 0),
        (-0.5 * BOX_SIZE, 1 * BOX_SIZE, 0),
    ])


def letter_t(vm):
    draw_3d(pen, projection_matrix, vm, [
        (-0.5 * BOX_SIZE, 3 * BOX_SIZE, 0, True),
        (-0.5 * BOX_SIZE, 2 * BOX_SIZE, 0),
        (-1.5 * BOX_SIZE, 2 * BOX_SIZE, 0),
        (-1.5 * BOX_SIZE, 1 * BOX_SIZE, 0),
        (-0.5 * BOX_SIZE, 1 * BOX_SIZE, 0),
        (-0.5 * BOX_SIZE, -3 * BOX_SIZE, 0),
        (1.5 * BOX_SIZE, -3 * BOX_SIZE, 0),
        (1.5 * BOX_SIZE, -2 * BOX_SIZE, 0),
        (0.5 * BOX_SIZE, -2 * BOX_SIZE, 0),
        (0.5 * BOX_SIZE, 1 * BOX_SIZE, 0),
        (1.5 * BOX_SIZE, 1 * BOX_SIZE, 0),
        (1.5 * BOX_SIZE, 2 * BOX_SIZE, 0),
        (0.5 * BOX_SIZE, 2 * BOX_SIZE, 0),
        (0.5 * BOX_SIZE, 3 * BOX_SIZE, 0),
        (-0.5 * BOX_SIZE, 3 * BOX_SIZE, 0),
    ])


def letter_b(vm):
    draw_3d(pen, projection_matrix, vm, [
        (-1.5 * BOX_SIZE, 3 * BOX_SIZE, 0, True),
        (-1.5 * BOX_SIZE, -3 * BOX_SIZE, 0),
        (1.5 * BOX_SIZE, -3 * BOX_SIZE, 0),
        (1.5 * BOX_SIZE, 1 * BOX_SIZE, 0),
        (-0.5 * BOX_SIZE, 1 * BOX_SIZE, 0),
        (-0.5 * BOX_SIZE, 3 * BOX_SIZE, 0),
        (-1.5 * BOX_SIZE, 3 * BOX_SIZE, 0),

        (-0.5 * BOX_SIZE, 0, 0, True),
        (-0.5 * BOX_SIZE, -2 * BOX_SIZE, 0),
        (0.5 * BOX_SIZE, -2 * BOX_SIZE, 0),
        (0.5 * BOX_SIZE, 0, 0),
        (-0.5 * BOX_SIZE, 0, 0),
    ])


def letter_o(vm):
    draw_3d(pen, projection_matrix, vm, [
        (-1.5 * BOX_SIZE, 1 * BOX_SIZE, 0, True),
        (-1.5 * BOX_SIZE, -3 * BOX_SIZE, 0),
        (1.5 * BOX_SIZE, -3 * BOX_SIZE, 0),
        (1.5 * BOX_SIZE, 1 * BOX_SIZE, 0),
        (-1.5 * BOX_SIZE, 1 * BOX_SIZE, 0),

        (-0.5 * BOX_SIZE, 0, 0, True),
        (-0.5 * BOX_SIZE, -2 * BOX_SIZE, 0),
        (0.5 * BOX_SIZE, -2 * BOX_SIZE, 0),
        (0.5 * BOX_SIZE, 0, 0),
        (-0.5 * BOX_SIZE, 0, 0),
    ])


def letter_m(vm):
    draw_3d(pen, projection_matrix, vm, [
        (-2.5 * BOX_SIZE, 0 * BOX_SIZE, 0, True),
        (-2.5 * BOX_SIZE, -3 * BOX_SIZE, 0),
        (-1.5 * BOX_SIZE, -3 * BOX_SIZE, 0),
        (-1.5 * BOX_SIZE, 0 * BOX_SIZE, 0),
        (-0.5 * BOX_SIZE, 0 * BOX_SIZE, 0),
        (-0.5 * BOX_SIZE, -3 * BOX_SIZE, 0),
        (0.5 * BOX_SIZE, -3 * BOX_SIZE, 0),
        (0.5 * BOX_SIZE, 0 * BOX_SIZE, 0),
        (1.5 * BOX_SIZE, 0 * BOX_SIZE, 0),
        (1.5 * BOX_SIZE, -3 * BOX_SIZE, 0),
        (2.5 * BOX_SIZE, -3 * BOX_SIZE, 0),
        (2.5 * BOX_SIZE, 0 * BOX_SIZE, 0),
        (1.5 * BOX_SIZE, 1 * BOX_SIZE, 0),
        (0.5 * BOX_SIZE, 1 * BOX_SIZE, 0),
        (0 * BOX_SIZE, 0.5 * BOX_SIZE, 0),
        (-0.5 * BOX_SIZE, 1 * BOX_SIZE, 0),
        (-1.5 * BOX_SIZE, 1 * BOX_SIZE, 0),
        (-2.5 * BOX_SIZE, 0 * BOX_SIZE, 0),
    ])


def letter_point(vm):
    draw_3d(pen, projection_matrix, vm, [
        (-0.5 * BOX_SIZE, -2 * BOX_SIZE, 0, True),
        (-0.5 * BOX_SIZE, -3 * BOX_SIZE, 0),
        (0.5 * BOX_SIZE, -3 * BOX_SIZE, 0),
        (0.5 * BOX_SIZE, -2 * BOX_SIZE, 0),
        (-0.5 * BOX_SIZE, -2 * BOX_SIZE, 0),
    ])


def letter_u(vm):
    draw_3d(pen, projection_matrix, vm, [
        (-1.5 * BOX_SIZE, 1 * BOX_SIZE, 0, True),
        (-1.5 * BOX_SIZE, -2 * BOX_SIZE, 0),
        (-0.5 * BOX_SIZE, -3 * BOX_SIZE, 0),
        (1.5 * BOX_SIZE, -3 * BOX_SIZE, 0),
        (1.5 * BOX_SIZE, 1 * BOX_SIZE, 0),
        (0.5 * BOX_SIZE, 1 * BOX_SIZE, 0),
        (0.5 * BOX_SIZE, -2 * BOX_SIZE, 0),
        (-0.5 * BOX_SIZE, -2 * BOX_SIZE, 0),
        (-0.5 * BOX_SIZE, 1 * BOX_SIZE, 0),
        (-1.5 * BOX_SIZE, 1 * BOX_SIZE, 0),
    ])


def letter_z(vm):
    draw_3d(pen, projection_matrix, vm, [
        (-1.5 * BOX_SIZE, 1 * BOX_SIZE, 0, True),
        (-1.5 * BOX_SIZE, 0 * BOX_SIZE, 0),
        (0.5 * BOX_SIZE, 0 * BOX_SIZE, 0),
        (-1.5 * BOX_SIZE, -2 * BOX_SIZE, 0),
        (-1.5 * BOX_SIZE, -3 * BOX_SIZE, 0),
        (1.5 * BOX_SIZE, -3 * BOX_SIZE, 0),
        (1.5 * BOX_SIZE, -2 * BOX_SIZE, 0),
        (-0.5 * BOX_SIZE, -2 * BOX_SIZE, 0),
        (1.5 * BOX_SIZE, 0 * BOX_SIZE, 0),
        (1.5 * BOX_SIZE, 1 * BOX_SIZE, 0),
        (-1.5 * BOX_SIZE, 1 * BOX_SIZE, 0),
    ])


LETTER_SIZE = {
    "i": 1,
    "t": 3,
    "b": 3,
    "o": 3,
    "m": 5,
    ".": 1,
    "u": 3,
    "z": 3
}

text = "itboom.uz"

total_size = 0
for letter in text:
    total_size += LETTER_SIZE[letter] * BOX_SIZE + BOX_SIZE

for angle in range(0, 361, 20):
    pen.clear()
    pen.color("#FF6F06")

    a = math.radians(angle)
    view_matrix = look_at(np.array([200 * math.sin(a), 50, 200 * math.cos(a)]), np.array([0, 0, 0]), np.array([0, 1, 0]))

    pos_x = -total_size / 2

    for i, letter in enumerate(text):
        half_size = LETTER_SIZE[letter] * BOX_SIZE / 2.0
        pos_x += half_size

        transformation_matrix = np.array([
            [1, 0, 0, pos_x],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ])

        fn = "letter_" + ("point" if letter == "." else letter)
        locals()[fn](np.dot(view_matrix, transformation_matrix))

        pos_x += half_size + BOX_SIZE

    if angle == 40:
        save_as_png("itboomuz", wn)

    # canvas = wn.getcanvas()
    # canvas.postscript(file=f"./output/{angle:03}.ps", colormode='color')

turtle.done()

