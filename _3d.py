import numpy as np


def perspective(fov, aspect_ratio, near, far):
    f = 1.0 / np.tan(np.radians(fov) / 2)
    return np.array([
        [f / aspect_ratio, 0, 0, 0],
        [0, f, 0, 0],
        [0, 0, (far + near) / (near - far), (2 * far * near) / (near - far)],
        [0, 0, -1, 0]
    ], np.float32)


def look_at(eye, target, up):
    zaxis = eye - target
    zaxis = zaxis / np.linalg.norm(zaxis)

    xaxis = np.cross(up, zaxis)
    xaxis = xaxis / np.linalg.norm(xaxis)

    yaxis = np.cross(zaxis, xaxis)
    zaxis = zaxis / np.linalg.norm(zaxis)
    xaxis = xaxis / np.linalg.norm(xaxis)
    yaxis = yaxis / np.linalg.norm(yaxis)

    return np.array([[xaxis[0], xaxis[1], xaxis[2], -np.dot(xaxis, eye)],
                     [yaxis[0], yaxis[1], yaxis[2], -np.dot(yaxis, eye)],
                     [zaxis[0], zaxis[1], zaxis[2], -np.dot(zaxis, eye)],
                     [0, 0, 0, 1]])

