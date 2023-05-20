from cgpy import Image, Polygon, Color

HEIGHT = 500
WIDTH = 500
red = Color((255, 0, 0))
green = Color((0, 255, 0))
blue = Color((0, 0, 255))


def main():
    img = Image(width=WIDTH, height=HEIGHT)

    pol1 = Polygon(points=[(100, 300), (200, 10), (300, 300)])

    img.draw_polygon(polygon=pol1, color=green)

    img.scanline(polygon=pol1, color=green)
    pol1 = Polygon(points=[(100, 300), (200, 10), (300, 300)])

    img.draw_polygon(polygon=pol1, color=red)

    img.run()


if __name__ == "__main__":
    main()
