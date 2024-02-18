from concurrent.futures import ProcessPoolExecutor
from multiprocessing import freeze_support

from fontTools.ttLib import TTFont
import math
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from shapely.geometry import Polygon, Point, MultiPolygon

font = TTFont("./assets/blaster-regular.ttf")
# font = TTFont("./assets/bardy.ttf")

glyph_name = font.getBestCmap()[ord('C')]
glyph = font['glyf'][glyph_name]
TEXT_SCALE = 200
TEXT = "itboom.uz"
LETTER_SPACE = 0.8

# Ko'rish burchagi
FOV = 90

# Rasm o'lchami
WIDTH = 1280
HEIGHT = 720

RENDER_WORKERS = 20

# Rasm pixellarini saqlash uchun massiv
img_data = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)


def get_glyp(letter):
    glyph_name = font.getBestCmap()[ord(letter)]
    return font['glyf'][glyph_name]


def glyp_point_normalize(glyp, point):
    x = point[0] - glyp.xMin
    return x / TEXT_SCALE, point[1] / TEXT_SCALE


def glyp_to_polygon(glyp):
    polygons = []
    shell = []
    holes = []
    points = []

    for idx, p in enumerate(glyp.coordinates):
        points.append(glyp_point_normalize(glyp, p))

        if idx in glyp.endPtsOfContours:
            p = Polygon(points)
            if not p.exterior.is_ccw:
                if shell:
                    polygons.append((shell, holes))
                    holes = []
                shell = points
            else:
                holes.append(points)

            points = list()

    if shell:
        polygons.append((shell, holes))

    if len(polygons) == 1:
        return Polygon(*polygons[0])

    return MultiPolygon(polygons)


def normalize(v):
    return v / np.linalg.norm(v)


def reflect(I, N):
    return I - 2 * np.dot(I, N) * N


class Ray:
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = normalize(direction)


class Light:
    def __init__(self, center, color, max_distance, intensity):
        self.center = np.array(center)
        self.intensity = intensity
        self.max_distance = max_distance
        self.color = np.array(color)
        self.radius = 0.25

    def fn(self, distance):
        if self.max_distance is None:
            return 1

        if distance > self.max_distance:
            return 0

        return (self.max_distance - distance) / self.max_distance

    def ray_intersect(self, ray: Ray):
        to_center = self.center - ray.origin
        # aylana markazidan direction yo'nalishidagi nurga tushgan
        # perpendekulyar kesishgan nuqtagacha bo'lgan masofa
        n = np.dot(to_center, ray.direction)

        # markazdan direction yo'nalishidagi nurga tushgan
        # perpendekulyar uzunligi
        tcl = np.linalg.norm(to_center)
        # aslida pl = math.sqrt(tcl * tcl - n * n) bo'lishi kerak
        # lekin sqrt ishlatmaslik uchun radius kvadratga ko'tarilyapti
        pl = tcl * tcl - n * n
        if pl >= self.radius ** 2:
            return None

        # aylanani kesib o'tgan nurning aylana chegarasidan
        # perpendekulyar bilan kesishgan nuqtagacha bo'lgan masofa
        t = math.sqrt(self.radius ** 2 - pl)

        # Shar bilan kesishgan ikkita nuqtagacha bo'lgan masofa
        d1 = n - t
        d2 = n + t
        if d1 < 0:
            d1 = d2

        if d1 < 0:
            return None

        point = ray.origin + ray.direction * d1
        return point, d1, normalize(point - self.center)


class Plane:
    def __init__(self, center, size, normal):
        self.center = np.array(center)
        self.size = size
        self.normal = np.array(normal)

    def ray_intersect(self, ray: Ray):
        # Ikkita vectorning DOT PRODUCT qiymati ularning kesishishi haqida ma'lumot beradi
        # To'liq: https://www.youtube.com/watch?v=LyGKycYT2v0
        # Agar 0 ga teng bo'lsa, perpendekulyar
        # Agar 0 dan katta bo'lsa, ikkalasining o'rtasidagi burcha 90 dan kichik
        # Agar 0 dan kichik bo'lsa, 90 dan katta bo'ladi
        # Bizning holatda biz tekislikka qarab turibmiz, demak
        # 90 dan katta bo'lishi kerak
        k = np.dot(self.normal, ray.direction)
        if k >= 0:
            return None

        # Uzunlikni topish,
        # np.dot(self.normal, self.center - ray.origin)
        # bu self.center - ray.origin vektorning normal vectordagi proyeksiyasi
        # uzunligiga teng, k ga bo'lish aslida
        # o'xshash uchburchaklardan kelib chiqqan
        # ya'ni d = np.dot(self.normal, self.center - ray.origin) * np.linalg.norm(ray.direction) / k
        # bizda np.linalg.norm(ray.direction) = 1 ga teng bo'lganligi bois, tashlab ketilgan
        distance = np.dot(self.normal, self.center - ray.origin) / k

        # Nurning tekishlik bilan keshish nuqtasi
        p = ray.origin + ray.direction * distance
        for i in range(3):
            if self.normal[i] != 0:
                continue

            if p[i] < self.center[i] - self.size[i] / 2 or p[i] > self.center[i] + self.size[i] / 2:
                return None

        return p, distance, self.normal


class Letter:
    def __init__(self, letter, center):
        self.center = np.array(center)
        self.polygon = glyp_to_polygon(get_glyp(letter))
        self.normal = np.array([0, 0, 1])

    def ray_intersect(self, ray: Ray):
        k = np.dot(self.normal, ray.direction)
        if int(k * 1000) == 0:
            return None

        normal = self.normal  # * (-1 if k < 0 else 1)

        hit_distance = np.dot(normal, self.center - ray.origin) / k
        hit_point = ray.origin + ray.direction * hit_distance

        polygon_point_3d = hit_point - self.center
        if not self.polygon.intersects(Point(polygon_point_3d[0], polygon_point_3d[1])):
            return None

        return hit_point, hit_distance, normal


scene_objects = [
    Plane([0, -3, -100], [200, 0, 200], [0, 1, 0]),
]

text_size = 0
letter_size = dict()
for letter in TEXT:
    if letter in letter_size:
        text_size += letter_size[letter]
        continue

    glyp = get_glyp(letter)
    min_point = glyp_point_normalize(glyp, [glyp.xMin, glyp.yMin])
    max_point = glyp_point_normalize(glyp, [glyp.xMax, glyp.yMax])
    letter_size[letter] = size = max_point[0] - min_point[0]
    text_size += size + LETTER_SPACE


pos_x = -text_size / 2
for letter in TEXT:
    size = letter_size[letter]
    scene_objects.append(Letter(letter, [pos_x, 0, -13]))
    pos_x += size + LETTER_SPACE


lights = [
    Light([0, 20, 0], [1, 1, 1], None, 1),
    Light([-13, 3.5, -10], [1, 1, 1], 10, 4),
    Light([-5, 3.5, -10], [1, 0, 0], 10, 7),
    Light([0, 3.5, -10], [0, 1, 0], 10, 7),
    Light([5, 3.5, -10], [0, 0, 1], 10, 7),
    Light([13, 3.5, -10], [1, 1, 1], 10, 4),
]


def scene_intersection(ray: Ray, skip):
    hit_object = hit_distance = hit_point = hit_normal = None

    # Nur bilan eng yaqin keshshgan obyektni topamiz
    for obj in scene_objects + lights:
        if obj == skip:
            continue

        data = obj.ray_intersect(ray)
        if data is None:
            continue

        point, distance, normal = data
        if hit_object is None or distance < hit_distance:
            hit_object, hit_distance, hit_point, hit_normal = obj, distance, point, normal

    return hit_object, hit_distance, hit_point, hit_normal, hit_object in lights


def cast_ray(ray: Ray, skip=None, depth=0):
    hit_object, hit_distance, hit_point, hit_normal, is_light = scene_intersection(ray, skip)

    if hit_object is None or depth >= 2:
        return np.array([0.2, 0.2, 0.2])

    if is_light:
        to_center = hit_object.center - ray.origin
        distance_to_perpendicular = np.dot(to_center, ray.direction)
        perpendicular_length = math.sqrt(np.linalg.norm(to_center) ** 2 - distance_to_perpendicular ** 2)
        k = perpendicular_length / hit_object.radius
        return (1 - hit_object.color) * (1 - k) + hit_object.color

    reflection_normal = reflect(ray.direction, hit_normal)
    reflection_color = cast_ray(Ray(hit_point, reflection_normal), hit_object, depth + 1)

    diffuse_color = np.array([0.0, 0.0, 0.0])

    for light in lights:
        light_dir = normalize(light.center - hit_point)
        light_distance = abs(np.linalg.norm(light.center - hit_point))

        _, shadow_distance, _, _, is_light = scene_intersection(Ray(hit_point, light_dir), hit_object)
        if not is_light and shadow_distance is not None:
            if shadow_distance < light_distance:
                continue

        diffuse_light_intensity = light.intensity * light.fn(light_distance) * max(0, np.dot(light_dir, hit_normal))
        diffuse_color += light.color * diffuse_light_intensity

    return diffuse_color / len(lights) * 0.8 + reflection_color * 0.2


def render(j):
    result = []

    for i in range(WIDTH):
        # 0 dan 1 gacha qiymatga o‘tkazish
        ndc_x, ndc_y = (i + 0.5) / WIDTH, (j + 0.5) / HEIGHT
        # -1 dan 1 iymatga o‘tkazish, faqat bu yerda y ni yuqoridan pastga emas
        # aksincha, pastda yuqoriga qarab o‘sib boradigan qilingan
        screen_x, screen_y = 2 * ndc_x - 1, 1 - 2 * ndc_y
        # ko‘rish burchagi qiymati
        # Shu havolada to'liq yoritilgan
        # https://www.scratchapixel.com/lessons/3d-basic-rendering/ray-tracing-generating-camera-rays/generating-camera-rays.html
        k = math.tan(math.radians(FOV / 2))

        # CameraWorld dagi i, j nuqtaning joylashuvi
        # k dan kelib chiqib -n dan n gacha oraliqda bo'ladi
        camera_x, camera_y = screen_x * WIDTH / HEIGHT * k, screen_y * k
        ray = Ray(np.array((0, 0, 0)), np.array((camera_x, camera_y, -1)))

        result.append(cast_ray(ray) * 255)

    return result


if __name__ == '__main__':
    # Har bir pixelni hisoblab chiqish iternatsiyasi
    # for j in range(HEIGHT):
    #     img_data[j] = render(j)

    with ProcessPoolExecutor(max_workers=RENDER_WORKERS) as executor:
        futures = [executor.submit(render, j) for j in range(HEIGHT)]

        for j, future in enumerate(futures):
            img_data[j] = future.result()

    img = Image.fromarray(img_data)
    img.save("./output/itboomuz-front-ray-tracing.png")

    # Natijani ko'rsatish
    plt.imshow(img_data)
    plt.title('itboom.uz')
    plt.axis('off')  # Hide the axis
    plt.show()
