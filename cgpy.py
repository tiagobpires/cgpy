import pygame
from pygame import gfxdraw
from math import sin, ceil, floor


class Color:
    def __init__(self, values: tuple[int]) -> None:
        self.r = values[0]
        self.g = values[1]
        self.b = values[2]
        self.a = values[3] if len(values) == 4 else 255

    def get_color(self):
        return (self.r, self.g, self.b, self.a)

    def with_alpha(self, a) -> "Color":
        return Color((self.r, self.g, self.b, a))

    def __eq__(self, color):
        return self.r == color.r and self.g == color.g and self.b == color.b

    def __ne__(self, color):
        return not (self.r == color.r and self.g == color.g and self.b == color.b)

    def __repr__(self) -> str:
        return f"({self.r}, {self.g}, {self.b}, {self.a})"


class Polygon:
    def __init__(self, points: list[tuple[int, int]] = []) -> None:
        self.points = points

    def insert_points(self, points: list[tuple[int, int]]) -> None:
        self.points += points

    def update_point(self, pos: int, point: tuple[int, int]) -> None:
        self.points[pos] = point

    def y_min(self) -> int:
        return min(row[1] for row in self.points)

    def y_max(self) -> int:
        return max(row[1] for row in self.points)


class Image:
    def __init__(self, height: int, width: int, caption: str = "Trabalho CG") -> None:
        self.height = height
        self.width = width

        pygame.init()
        pygame.display.set_caption(caption)

        self.surface = pygame.display.set_mode((width, height))

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            pygame.display.update()

    def set_pixel(self, x: int, y: int, color: Color) -> None:
        x = int(min(max(x, 0), self.width))
        y = int(min(max(y, 0), self.height))

        gfxdraw.pixel(self.surface, x, y, color.get_color())

    def get_pixel(self, x: int, y: int):
        color = self.surface.get_at((x, y))

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

        while y > x:
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

        while px < py:
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

    def flood_fill(self, x: int, y: int, color: Color) -> None:
        initial_color = Color(self.get_pixel(x, y))

        if color == initial_color:
            return

        stack = [(x, y)]

        while stack:
            x, y = stack.pop()

            if Color(self.get_pixel(x, y)) != initial_color:
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

    def draw_polygon(self, polygon: Polygon, color: Color) -> None:
        xi, yi = polygon.points[0]

        for i in range(1, len(polygon.points)):
            xf, yf = polygon.points[i]
            self.line_DDA(xi, yi, xf, yf, color)
            xi, yi = xf, yf

        xf, yf = polygon.points[0]
        self.line_DDA(xi, yi, xf, yf, color)

    def intersection(self, y: int, segment: list[list[int]]) -> int:
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

        return xi + t * (xf - xi) if t > 0 and t <= 1 else -1

    def scanline(self, polygon: Polygon, color: Color) -> None:
        y_min = polygon.y_min()
        y_max = polygon.y_max()

        for y in range(y_min, y_max):
            intersections = []

            pix = polygon.points[0][0]
            piy = polygon.points[0][1]

            for p in range(1, len(polygon.points)):
                pfx = polygon.points[p][0]
                pfy = polygon.points[p][1]

                xi = int(self.intersection(y, [[pix, piy], [pfx, pfy]]))

                if xi >= 0:
                    intersections.append(xi)

                pix = pfx
                piy = pfy

            pfx = polygon.points[0][0]
            pfy = polygon.points[0][1]

            xi = int(self.intersection(y, [[pix, piy], [pfx, pfy]]))

            if xi >= 0:
                intersections.append(xi)

            intersections.sort()
            for pi in range(0, len(intersections), 2):
                for pixel in range(intersections[pi], intersections[pi + 1]):
                    self.set_pixel(pixel, y, color)
