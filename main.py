from cgpy import Image

HEIGHT = 500
WIDTH = 500
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)


def main():
    img = Image(width=WIDTH, height=HEIGHT)

    img.ellipse(250, 250, -100, 100, blue)

    img.circumference(250, 250, 50, green)
    img.circumference(300, 280, 20, blue)

    img.flood_fill(250, 250, red)
    img.border_fill(250, 250, color=blue)

    img.run()


if __name__ == "__main__":
    main()
