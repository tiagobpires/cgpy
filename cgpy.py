import pygame
from pygame import gfxdraw
from math import sin, ceil, floor, pi, cos
import numpy as np
import time
from PIL import Image
import random
import os

cg_dir = os.getcwd()


class Color:
    def __init__(self, values: tuple[int]) -> None:
        self.r = values[0]
        self.g = values[1]
        self.b = values[2]
        self.a = values[3] if len(values) == 4 else 255

    @classmethod
    def get_default_colors(cls) -> dict[str, "Color"]:
        return {
            "red": Color((255, 0, 0)),
            "green": Color((0, 255, 0)),
            "green_pastel1": Color((181, 255, 172)),
            "green_pastel2": Color((72, 181, 163)),
            "blue": Color((0, 0, 255)),
            "blue_pastel": Color((111, 183, 214)),
            "purple_pastel": Color((165, 137, 193)),
            "red_pastel": Color((255, 150, 129)),
            "blank": Color((255, 255, 255)),
            "black": Color((0, 0, 0)),
        }

    def get_color(self):
        return (self.r, self.g, self.b, self.a)

    def with_alpha(self, a) -> "Color":
        return Color((self.r, self.g, self.b, a))

    def sub_color_gradient(self, color, t) -> "Color":
        return Color(
            (
                int((color.r - self.r) * t + self.r),
                int((color.g - self.g) * t + self.g),
                int((color.b - self.b) * t + self.b),
                int((color.a - self.a) * t + self.a),
            )
        )

    def __eq__(self, color) -> bool:
        return self.r == color.r and self.g == color.g and self.b == color.b

    def __ne__(self, color) -> bool:
        return not (self.r == color.r and self.g == color.g and self.b == color.b)

    def __sub__(self, color) -> "Color":
        return Color((self.r - color.r, self.g - color.g, self.b - color.b))

    def __repr__(self) -> str:
        return f"({self.r}, {self.g}, {self.b}, {self.a})"


class Polygon:
    def __init__(self, points: list[list[int, int, Color]] = []) -> None:
        self.points = points

    def insert_points(self, points: list[list[int, int, Color]]) -> None:
        self.points += points

    def update_point(self, pos: int, point: list[int, int, Color]) -> None:
        self.points[pos] = point

    def y_min(self) -> int:
        return min(int(row[1]) for row in self.points)

    def y_max(self) -> int:
        return max(int(row[1]) for row in self.points)

    def get_rectangle_bounds(self):
        x_coords = [point[0] for point in self.points]
        y_coords = [point[1] for point in self.points]

        x1 = min(x_coords)
        y1 = min(y_coords)
        x2 = max(x_coords)
        y2 = max(y_coords)

        return x1, y1, x2, y2


class TexturePolygon:
    def __init__(self, points: list[list[int, int, float, float]] = []) -> None:
        self.points = points

    def insert_points(self, points: list[list[int, int, float, float]]) -> None:
        self.points += points

    def y_min(self) -> int:
        return min(int(row[1]) for row in self.points)

    def y_max(self) -> int:
        return max(int(row[1]) for row in self.points)

    def center(self) -> tuple[int, int]:
        x_sum = sum(row[0] for row in self.points)
        y_sum = sum(row[1] for row in self.points)
        num_points = len(self.points)

        center_x = int(x_sum / num_points)
        center_y = int(y_sum / num_points)

        return center_x, center_y

    def check_collision(self, rectangle):
        rect1_x1, rect1_y1, rect1_x2, rect1_y2 = self.get_rectangle_bounds()
        rect2_x1, rect2_y1, rect2_x2, rect2_y2 = rectangle.get_rectangle_bounds()

        # print(self.points)
        # print(rect1_x1, rect1_y1, rect1_x2, rect1_y2)

        return (
            rect1_x1 <= rect2_x2
            and rect1_x2 >= rect2_x1
            and rect1_y1 <= rect2_y2
            and rect1_y2 >= rect2_y1
        )

    def get_rectangle_bounds(self):
        x_coords = [point[0] for point in self.points]
        y_coords = [point[1] for point in self.points]

        x1 = min(x_coords)
        y1 = min(y_coords)
        x2 = max(x_coords)
        y2 = max(y_coords)

        return x1, y1, x2, y2


class Game:
    def __init__(self, height: int, width: int, caption: str = "Trabalho CG") -> None:
        self.height = height
        self.width = width

        pygame.init()
        pygame.display.set_caption(caption)

        self.surface = pygame.display.set_mode((width, height))
        self.surface.fill((0, 0, 0))

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            pygame.display.update()

    def check_for_quit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

    def set_pixel(self, x: int, y: int, color: Color) -> None:
        x = int(min(max(x, 0), self.width - 1))
        y = int(min(max(y, 0), self.height - 1))

        gfxdraw.pixel(self.surface, x, y, color.get_color())

    def get_pixel(self, x: int, y: int) -> tuple[int]:
        color = self.surface.get_at((x, y))

        return (color[0], color[1], color[2], color[3])

    def get_pixel_with_texture(
        self, texture: np.ndarray, x: int, y: int
    ) -> tuple[int, int, int]:
        num_rows, num_cols, _ = texture.shape

        x = max(min(x, 1), 0)
        y = max(min(y, 1), 0)

        x = int(x * (num_cols - 1))
        y = int(y * (num_rows - 1))

        color = texture[y][x]

        return (color[0], color[1], color[2])

    def sin(self) -> None:
        for x in range(self.width):
            y = int((self.height / 2) + 25 * sin(x * 0.05))

            self.set_pixel(x, y, (255, 0, 0))

    def line(self, xi: int, yi: int, xf: int, yf: int, color: Color) -> None:
        dx = xf - xi
        dy = yf - yi

        if dx == 0 and dy == 0:
            self.set_pixel(xi, yi, color)
            return

        changed = False

        if abs(dy) > abs(dx):
            dx, dy = dy, dx
            xi, yi = yi, xi

            changed = True

        a = dy / dx

        for vx in range(abs(dx)):
            if dx < 0:
                vx = -vx

            vy = a * vx

            x = xi + vx
            y = yi + vy

            if changed:
                self.set_pixel(x, y, color)
            else:
                self.set_pixel(y, x, color)

    def line_DDA(self, xi: int, yi: int, xf: int, yf: int, color: Color) -> None:
        dx = xf - xi
        dy = yf - yi

        steps = max(abs(dx), abs(dy))

        if steps == 0:
            self.set_pixel(xi, yi, color)
            return

        step_x = dx / steps
        step_y = dy / steps

        for i in range(steps):
            x = xi + i * step_x
            y = yi + i * step_y

            self.set_pixel(x, y, color)

    def line_DDAAA(self, xi: int, yi: int, xf: int, yf: int, color: Color) -> None:
        dx = xf - xi
        dy = yf - yi

        steps = max(abs(dx), abs(dy))

        if steps == 0:
            self.set_pixel(xi, yi, color)
            return

        step_x = dx / steps
        step_y = dy / steps

        for i in range(steps):
            x = xi + i * step_x
            y = yi + i * step_y

            if abs(ceil(step_x)) == 1:
                yd = y - floor(y)

                a = ceil((1 - yd) * 255)
                self.set_pixel(ceil(x), floor(y), color.with_alpha(a))

                a = ceil(yd * 255)
                self.set_pixel(ceil(x), floor(y + 1), color.with_alpha(a))
            else:
                xd = x - floor(x)

                a = ceil((1 - xd) * 255)
                self.set_pixel(floor(x), ceil(y), color.with_alpha(a))

                a = ceil(xd * 255)
                self.set_pixel(floor(x + 1), ceil(y), color.with_alpha(a))

    def line_bresenham(self, xi: int, yi: int, xf: int, yf: int, color: Color) -> None:
        dx = xf - xi
        dy = yf - yi

        x_sign = 1 if dx > 0 else -1
        y_sign = 1 if dy > 0 else -1

        dx = abs(dx)
        dy = abs(dy)

        if dx > dy:
            xx, xy, yx, yy = x_sign, 0, 0, y_sign
        else:
            dx, dy = dy, dx
            xx, xy, yx, yy = 0, y_sign, x_sign, 0

        dx2 = 2 * dx
        dy2 = 2 * dy

        p = dy2 - dx
        y = 0

        for x in range(dx):
            self.set_pixel(xi + x * xx + y * yx, yi + x * xy + y * yy, color)

            if p >= 0:
                y += 1
                p -= dx2

            p += dy2

    def circumference(self, xc: int, yc: int, r: int, color: Color) -> None:
        x = 0
        y = r

        sectors = [(1, 1), (-1, 1), (1, -1), (-1, -1)]

        p = 3 - 2 * r

        while y >= x:
            x_aux, y_aux = y, x

            for x_signal, y_signal in sectors:
                self.set_pixel(xc + x_signal * x, yc + y_signal * y, color)
                self.set_pixel(xc + x_signal * x_aux, yc + y_signal * y_aux, color)

            x += 1

            if p > 0:
                y -= 1
                p += 4 * (x - y) + 10
            else:
                p += 4 * x + 6

    def ellipse(self, xc: int, yc: int, rx: int, ry: int, color: Color) -> None:
        x = 0
        y = abs(ry)

        sectors = [(1, 1), (-1, 1), (1, -1), (-1, -1)]

        rx_squared = rx**2
        ry_squared = ry**2

        px = 0
        py = 2 * rx_squared * y

        p = ry_squared - (rx_squared * ry) + (0.25 * rx_squared)

        while px <= py:
            x_aux, y_aux = x, y

            for x_signal, y_signal in sectors:
                self.set_pixel(xc + x_signal * x, yc + y_signal * y, color)
                self.set_pixel(xc + x_signal * x_aux, yc + y_signal * y_aux, color)

            x += 1
            px += 2 * ry_squared

            if p < 0:
                p += ry_squared + px
            else:
                y -= 1
                py -= 2 * rx_squared
                p += ry_squared + px - py

        p = (
            ry_squared * (x + 0.5) ** 2
            + rx_squared * (y - 1) ** 2
            - rx_squared * ry_squared
        )

        while y >= 0:
            x_aux, y_aux = x, y

            for x_signal, y_signal in sectors:
                self.set_pixel(xc + x_signal * x, yc + y_signal * y, color)
                self.set_pixel(xc + x_signal * x_aux, yc + y_signal * y_aux, color)

            y -= 1
            py -= 2 * rx_squared

            if p > 0:
                p += rx_squared - py
            else:
                x += 1
                px += 2 * ry_squared
                p += rx_squared - py + px

    def flood_fill(self, x: int, y: int, color: Color, animation: bool = False) -> None:
        initial_color = Color(self.get_pixel(x, y))

        if color == initial_color:
            return

        stack = [(x, y)]

        while stack:
            x, y = stack.pop()

            if Color(self.get_pixel(x, y)) != initial_color:
                continue

            if animation:
                time.sleep(0.000001)
                pygame.display.update()

            self.set_pixel(x, y, color)

            if x + 1 < self.width:
                stack.append((x + 1, y))

            if x >= 1:
                stack.append((x - 1, y))

            if y + 1 < self.height:
                stack.append((x, y + 1))

            if y >= 1:
                stack.append((x, y - 1))

    def boundary_fill(
        self, x: int, y: int, color: Color, border_color: Color = None
    ) -> None:
        stack = [(x, y)]

        if not border_color:
            border_color = color

        while stack:
            x, y = stack.pop()

            color_aux = Color(self.get_pixel(x, y))

            if color_aux in [border_color, color]:
                continue

            self.set_pixel(x, y, color)

            if x + 1 < self.width:
                stack.append((x + 1, y))

            if x >= 1:
                stack.append((x - 1, y))

            if y + 1 < self.height:
                stack.append((x, y + 1))

            if y >= 1:
                stack.append((x, y - 1))

    def draw_polygon(self, polygon: Polygon | TexturePolygon, color: Color) -> None:
        for i in range(len(polygon.points)):
            xi, yi = polygon.points[i][:2]
            xf, yf = polygon.points[(i + 1) % len(polygon.points)][:2]

            self.line_DDA(int(xi), int(yi), int(xf), int(yf), color)

    def intersection_base(self, y: int, segment: list[list[int]]) -> int:
        xi = segment[0][0]
        yi = segment[0][1]
        xf = segment[1][0]
        yf = segment[1][1]

        # Horizontal segment (has no intersection)
        if yi == yf:
            return -1

        # Secure starting point on top
        if yi > yf:
            xi, xf = xf, xi
            yi, yf = yf, yi

        t = (y - yi) / (yf - yi)

        return int(xi + t * (xf - xi)) if t > 0 and t <= 1 else -1

    def scanline_base(self, polygon: Polygon | TexturePolygon, color: Color) -> None:
        y_min = polygon.y_min()
        y_max = polygon.y_max()

        for y in range(y_min, y_max + 1):
            intersections = []

            pix = polygon.points[0][0]
            piy = polygon.points[0][1]

            for p in range(1, len(polygon.points)):
                pfx = polygon.points[p][0]
                pfy = polygon.points[p][1]

                xi = self.intersection_base(y, [[pix, piy], [pfx, pfy]])

                if xi >= 0:
                    intersections.append(xi)

                pix = pfx
                piy = pfy

            pfx = polygon.points[0][0]
            pfy = polygon.points[0][1]

            xi = self.intersection_base(y, [[pix, piy], [pfx, pfy]])

            if xi >= 0:
                intersections.append(xi)

            for pi in range(0, len(intersections), 2):
                x1 = intersections[pi]
                x2 = intersections[pi + 1]

                if x2 < x1:
                    x1, x2 = x2, x1

                for xk in range(x1, x2 + 1):
                    self.set_pixel(xk, y, color)

    def intersection_with_color_gradient(
        self, y: int, segment: list[list[int, int, Color]]
    ) -> tuple[int, Color]:
        xi = segment[0][0]
        yi = segment[0][1]
        c1 = segment[0][2]

        xf = segment[1][0]
        yf = segment[1][1]
        c2 = segment[1][2]

        # Horizontal segment (has no intersection)
        if yi == yf:
            return -1, c1

        # Secure starting point on top
        if yi > yf:
            xi, xf = xf, xi
            yi, yf = yf, yi
            c1, c2 = c2, c1

        t = (y - yi) / (yf - yi)

        if t > 0 and t <= 1:
            c = c1.sub_color_gradient(c2, t)
            return int(xi + t * (xf - xi)), c

        return -1, c1

    def scanline_with_color_gradient(self, polygon: Polygon) -> None:
        y_min = polygon.y_min()
        y_max = polygon.y_max()

        for y in range(y_min, y_max + 1):
            intersections: tuple[int, Color] = []

            for p in range(len(polygon.points)):
                xi, xic = self.intersection_with_color_gradient(
                    y,
                    [polygon.points[p], polygon.points[(p + 1) % len(polygon.points)]],
                )

                if xi >= 0:
                    intersections.append((xi, xic))

            intersections.sort(key=lambda intersection: intersection[0])

            for pi in range(0, len(intersections), 2):
                x1, c1 = intersections[pi]
                x2, c2 = intersections[pi + 1]

                if x1 == x2:
                    continue

                if x2 < x1:
                    x1, x2 = x2, x1
                    c1, c2 = c2, c1

                for xk in range(x1, x2 + 1):
                    p = (xk - x1) / (x2 - x1)

                    interpolated_color = c1.sub_color_gradient(c2, p)

                    self.set_pixel(xk, y, interpolated_color)

    def intersection_with_texture(self, y: int, segment: list[list[int]]) -> list[int]:
        pi = segment[0]
        pf = segment[1]

        # Horizontal segment (has no intersection)
        if pi[1] == pf[1]:
            return [-1, 0, 0, 0]

        # Secure starting point on top
        if pi[1] > pf[1]:
            pi, pf = pf, pi

        t = (y - pi[1]) / (pf[1] - pi[1])

        if t > 0 and t <= 1:
            x = pi[0] + t * (pf[0] - pi[0])

            tx = pi[2] + t * (pf[2] - pi[2])
            ty = pi[3] + t * (pf[3] - pi[3])

            return [x, y, tx, ty]

        return [-1, 0, 0, 0]

    def scanline_with_texture(
        self, polygon: TexturePolygon, texture: np.ndarray
    ) -> None:
        y_min = polygon.y_min()
        y_max = polygon.y_max()

        for y in range(y_min, y_max + 1):
            intersections: list[list[int, int, int, int]] = []

            for p in range(len(polygon.points)):
                pi = polygon.points[p]
                pf = polygon.points[(p + 1) % len(polygon.points)]

                intersection = self.intersection_with_texture(y, [pi, pf])

                if intersection[0] >= 0:
                    intersections.append(intersection)

            intersections.sort(key=lambda intersection: intersection[0])

            for pi in range(0, len(intersections), 2):
                p1 = intersections[pi]
                p2 = intersections[pi + 1]

                x1 = p1[0]
                x2 = p2[0]

                if x1 == x2:
                    continue

                if x2 < x1:
                    p1, p2 = p2, p1

                for xk in range(int(p1[0]), int(p2[0]) + 1):
                    pc = (xk - p1[0]) / (p2[0] - p1[0])

                    tx = p1[2] + pc * (p2[2] - p1[2])
                    ty = p1[3] + pc * (p2[3] - p1[3])

                    color = Color(self.get_pixel_with_texture(texture, tx, ty))

                    self.set_pixel(xk, y, color)

    def create_transformation_matrix(self) -> np.ndarray:
        return np.identity(3)

    def compose_translation(
        self, matrix: np.ndarray, tx: float, ty: float
    ) -> np.ndarray:
        return (
            np.array(
                [
                    [1, 0, tx],
                    [0, 1, ty],
                    [0, 0, 1],
                ]
            )
            @ matrix
        )

    def compose_scale(self, matrix: np.ndarray, sx: float, sy: float) -> np.ndarray:
        return (
            np.array(
                [
                    [sx, 0, 0],
                    [0, sy, 0],
                    [0, 0, 1],
                ]
            )
            @ matrix
        )

    def compose_rotation(self, matrix: np.ndarray, ang: float) -> np.ndarray:
        ang = (ang * pi) / 180

        return np.array(
            [
                [cos(ang), -sin(ang), 0],
                [sin(ang), cos(ang), 0],
                [0, 0, 1],
            ]
            @ matrix
        )

    def apply_transformation(
        self, polygon: Polygon | TexturePolygon, matrix: np.ndarray
    ) -> Polygon | TexturePolygon:
        points = []

        for i in range(len(polygon.points)):
            pt = polygon.points[i][:2]
            pt.append(1)
            pt = np.transpose(pt)

            transformed_pt = matrix @ pt

            transformed_pt = np.transpose(transformed_pt)
            points.append(transformed_pt[:2].tolist())

            for j in range(2, len(polygon.points[i])):
                points[i].append(polygon.points[i][j])

        if type(polygon) is Polygon:
            return Polygon(points)
        return TexturePolygon(points)

    def map_window(
        self,
        p: Polygon,
        window: tuple[int, int, int, int],
        viewport: tuple[int, int, int, int],
    ) -> Polygon | TexturePolygon:
        xiv = viewport[0]
        yiv = viewport[1]
        xfv = viewport[2]
        yfv = viewport[3]
        xi = window[0]
        yi = window[1]
        xf = window[2]
        yf = window[3]

        a = (xfv - xiv) / (xf - xi)
        b = (yfv - yiv) / (yf - yi)

        m = np.array(
            [
                [a, 0, xiv - a * xi],
                [0, b, yiv - b * yi],
                [0, 0, 1],
            ]
        )

        return self.apply_transformation(p, m)


class Cat:
    def __init__(
        self,
        game: Game,
        steps: int,
        window: tuple[int, int, int, int],
        viewport: tuple[int, int, int, int],
    ) -> None:
        self.game = game
        self.cat_texture = np.asarray(
            Image.open(os.path.join(cg_dir, "resources", "cat.png")),
        )
        self.cat_pol = TexturePolygon(
            [
                [210, 475, 0, 0],
                [210, 550, 0, 1],
                [290, 550, 1, 1],
                [290, 475, 1, 0],
            ]
        )
        self.steps = steps

        pol = self.game.map_window(self.cat_pol, window, viewport)
        self.game.scanline_with_texture(pol, self.cat_texture)

    def move_right(
        self,
        window: tuple[int, int, int, int],
        viewport: tuple[int, int],
    ):
        x_actual = self.cat_pol.points[3][0]
        if x_actual + self.steps >= viewport[2]:
            return

        pol = self.game.map_window(self.cat_pol, window, viewport)
        self.game.scanline_base(pol, Color((0, 0, 0)))

        m1 = self.game.create_transformation_matrix()
        m1 = self.game.compose_translation(m1, self.steps, 0)

        self.cat_pol = self.game.apply_transformation(self.cat_pol, m1)

        pol = self.game.map_window(self.cat_pol, window, viewport)
        self.game.scanline_with_texture(pol, self.cat_texture)

    def move_left(
        self,
        window: tuple[int, int, int, int],
        viewport: tuple[int, int],
    ):
        x_actual = self.cat_pol.points[1][0]
        if x_actual - self.steps <= 0:
            return

        pol = self.game.map_window(self.cat_pol, window, viewport)
        self.game.scanline_base(pol, Color((0, 0, 0)))

        m1 = self.game.create_transformation_matrix()
        m1 = self.game.compose_translation(m1, -self.steps, 0)

        self.cat_pol = self.game.apply_transformation(self.cat_pol, m1)

        pol = self.game.map_window(self.cat_pol, window, viewport)
        self.game.scanline_with_texture(pol, self.cat_texture)


class EnemyPolygons:
    def __init__(
        self,
        game: Game,
        window: tuple[int, int, int, int],
        viewport: tuple[int, int, int, int],
    ) -> None:
        self.game = game
        self.viewport = viewport
        self.window = window
        self.polygons: list[list[Polygon, str, np.ndarray | None, Color | None]] = []

    def create_random_polygon(self) -> None:
        colors = list(Color.get_default_colors().values())

        pol_width = random.randint(40, 90)
        pol_height = random.randint(40, 80)

        pol_xi = random.randint(0, self.viewport[2] - pol_width)
        pol_yi = random.randint(0, 30)

        pol_points = [
            [pol_xi, pol_yi],
            [pol_xi, pol_yi + pol_height],
            [pol_xi + pol_width, pol_yi + pol_height],
            [pol_xi + pol_width, pol_yi],
        ]

        polygon_type = random.choice(
            [
                "simple",
                "color_gradient",
                "texture",
                "color_gradient",
                "texture",
                "color_gradient",
                "texture",
                "texture",
            ],
        )

        if polygon_type == "color_gradient":
            for i in range(4):
                pol_points[i].append(random.choice(colors))

        elif polygon_type == "texture":
            pol_points[0] += [0, 0]
            pol_points[1] += [0, 1]
            pol_points[2] += [1, 1]
            pol_points[3] += [1, 0]

        pol = Polygon(points=pol_points)

        pol_aux = self.game.map_window(pol, self.window, self.viewport)

        if polygon_type == "simple":
            color = random.choice(colors)
            self.game.scanline_base(polygon=pol_aux, color=color)

        elif polygon_type == "color_gradient":
            self.game.scanline_with_color_gradient(polygon=pol_aux)

        else:
            image = random.choice(
                os.listdir(os.path.join(cg_dir, "resources", "enemys_textures"))
            )
            texture = np.asarray(
                Image.open(os.path.join(cg_dir, "resources", "enemys_textures", image)),
            )
            self.game.scanline_with_texture(polygon=pol_aux, texture=texture)

        self.polygons.append(
            [
                pol,
                polygon_type,
                texture if polygon_type == "texture" else None,
                color if polygon_type == "simple" else None,
            ]
        )

    def move_polygons(self) -> None:
        polygons_list = self.polygons.copy()

        for i in range(len(self.polygons)):
            polygon = self.polygons[i][0]
            pol_type = self.polygons[i][1]

            pol_aux = self.game.map_window(polygon, self.window, self.viewport)
            self.game.scanline_base(pol_aux, Color((0, 0, 0)))

            y_actual = polygon.points[2][1]
            if y_actual >= self.viewport[3]:
                polygons_list.remove(self.polygons[i])
                continue

            m1 = self.game.create_transformation_matrix()
            m1 = self.game.compose_translation(m1, 0, 3)

            polygon = self.game.apply_transformation(polygon, m1)
            self.polygons[i][0] = polygon

            pol_aux = self.game.map_window(polygon, self.window, self.viewport)

            if pol_type == "simple":
                self.game.scanline_base(polygon=pol_aux, color=self.polygons[i][3])

            elif pol_type == "color_gradient":
                self.game.scanline_with_color_gradient(polygon=pol_aux)

            else:
                self.game.scanline_with_texture(
                    polygon=pol_aux, texture=self.polygons[i][2]
                )

        self.polygons = polygons_list

    def check_for_colision(self, cat: Cat) -> bool:
        return any(
            cat.cat_pol.check_collision(polygon) for polygon, _, _, _ in self.polygons
        )
