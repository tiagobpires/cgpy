### Lines

## Bresenhan

Tests for bresenham:

```py
img.line_bresenham(250, 250, 500, 500, red)
img.line_bresenham(250, 250, 0, 0, red)
img.line_bresenham(250, 250, 0, 500, red)
img.line_bresenham(250, 250, 500, 0, red)
img.line_bresenham(250, 250, 250, 500, red)
img.line_bresenham(250, 250, 500, 250, red)
img.line_bresenham(250, 250, 250, 0, red)
img.line_bresenham(250, 250, 0, 250, red)
```

Base:

- https://github.com/encukou/bresenham/blob/master/bresenham.py
- https://en.wikipedia.org/wiki/Bresenham's_line_algorithm


## Circumference

Tests:

```py
img.circumference(250, 250, 200, red)
```

Base:

- https://www.geeksforgeeks.org/bresenhams-circle-drawing-algorithm/
- https://www.javatpoint.com/computer-graphics-bresenhams-circle-algorithm


## Ellipse

Tests:

```py
img.ellipse(250, 250, 200, 100, red)
img.ellipse(250, 250, 100, 200, red)
img.ellipse(250, 250, -100, 100, red)
```

## Flood Fill

Tests:

```py
img.ellipse(250, 250, -100, 100, blue)
img.circumference(250, 250, 50, green)
img.circumference(300, 280, 20, blue)

img.flood_fill(250, 250, red)
```

## Boundary Fill

Tests:

```py
img.ellipse(250, 250, -100, 100, blue)
img.circumference(250, 250, 50, green)
img.circumference(300, 280, 20, blue)

img.boundary_fill(250, 250, blue)
```

## Scanline with gradient colors

```py
pol1 = Polygon(
    points=[(20, 480, green), (250, 20, red), (480, 480, blue)],
)

pol1 = Polygon(
    points=[
        (20, 20, red),
        (20, 480, green),
        (480, 480, red),
        (480, 20, red),
        (250, 50, blue),
    ],
)

img.scanline_with_color_gradient(polygon=pol1)
img.draw_polygon(polygon=pol1, color=green)
```

## Class page

http://lia.ufc.br/~yuri/20231/cg/