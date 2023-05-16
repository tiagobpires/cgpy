import pygame
from pygame import gfxdraw
from math import sin


ColorType = tuple[int, int, int]


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

    def set_pixel(self, x: int, y: int, color: ColorType) -> None:
        x = round(min(max(x, 0), self.width))
        y = round(min(max(y, 0), self.height))

        gfxdraw.pixel(self.surface, x, y, color)

    def get_pixel(self, x: int, y: int):
        color = self.surface.get_at((x, y))

        return (color[0], color[1], color[2])

    def sin(self) -> None:
        for x in range(self.width):
            y = int((self.height / 2) + 25 * sin(x * 0.05))

            self.set_pixel(x, y, (255, 0, 0))

    def line(self, xi: int, yi: int, xf: int, yf: int, color: ColorType) -> None:
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

    def line_DDA(self, xi: int, yi: int, xf: int, yf: int, color: ColorType) -> None:
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

    def line_bresenham(
        self, xi: int, yi: int, xf: int, yf: int, color: ColorType
    ) -> None:
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

    def circumference(self, xc: int, yc: int, r: int, color: ColorType) -> None:
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

    def ellipse(self, xc: int, yc: int, rx: int, ry: int, color: ColorType) -> None:
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

    def flood_fill(self, x: int, y: int, color: ColorType) -> None:
        initial_color = self.get_pixel(x, y)

        stack = [(x, y)]

        while stack:
            x, y = stack.pop()

            if self.get_pixel(x, y) != initial_color:
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

    def border_fill(
        self, x: int, y: int, color: ColorType, border_color: ColorType = None
    ) -> None:
        stack = [(x, y)]

        if not border_color:
            border_color = color

        while stack:
            x, y = stack.pop()

            if self.get_pixel(x, y) in [border_color, color]:
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

            print(".")
