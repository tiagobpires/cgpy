from cgpy import Image, Polygon, Color

HEIGHT = 500
WIDTH = 500
red = Color((255, 0, 0))
green = Color((0, 255, 0))
blue = Color((0, 0, 255))


def main():
    img = Image(width=WIDTH, height=HEIGHT)

    pol1 = Polygon(points=[(10, 200), (200, 50), (100, 50), (50, 10)])

    img.draw_polygon(polygon=pol1, color=green)
    img.border_fill(51, 51, green)

    # img.line_DDAAA(400, 100, 300, 500, red)

    img.run()


if __name__ == "__main__":
    main()
