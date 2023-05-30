import os
import time

import numpy as np
import pygame
from PIL import Image

from cgpy import Cat, Color, Game, Polygon, TexturePolygon, EnemyPolygons

clock = pygame.time.Clock()


red = Color((255, 0, 0))
green = Color((0, 255, 0))
green_pastel1 = Color((181, 255, 172))
green_pastel2 = Color((72, 181, 163))
blue = Color((0, 0, 255))
blue_pastel = Color((111, 183, 214))
purple_pastel = Color((165, 137, 193))
red_pastel = Color((255, 150, 129))
blank = Color((255, 255, 255))
black = Color((0, 0, 0))

cg_dir = os.getcwd()
viewport = [0, 0, 500, 550]
window = [0, 0, 500, 550]


FPS = 60
ADD_POLYGON_INTERVAL = 3000
MOVE_POLYGON_INTERVAL = 30


def home_screen(game: Game):
    sky_falling_logo_pol = TexturePolygon(
        [
            [0, 0, 0, 0],
            [0, 95, 0, 1],
            [500, 95, 1, 1],
            [500, 0, 1, 0],
        ]
    )

    sky_falling_logo_texture = np.asarray(
        Image.open(os.path.join(cg_dir, "resources", "sky_falling_logo.png"))
    )

    game.scanline_with_texture(sky_falling_logo_pol, sky_falling_logo_texture)

    game.line_bresenham(0, 145, 40, 195, blank)
    game.circumference(60, 195, 20, green_pastel1)
    game.line_bresenham(80, 195, 120, 165, blank)
    game.ellipse(145, 165, 25, 40, purple_pastel)

    game.line_bresenham(170, 165, 250, 215, blank)

    # Rectangle
    game.line_bresenham(250, 165, 250, 245, blue_pastel)
    game.line_bresenham(250, 245, 300, 245, blue_pastel)
    game.line_bresenham(300, 245, 300, 165, blue_pastel)
    game.line_bresenham(300, 165, 250, 165, blue_pastel)

    game.line_bresenham(300, 205, 350, 165, blank)
    game.circumference(375, 165, 25, red_pastel)
    game.line_bresenham(400, 165, 440, 190, blank)
    game.circumference(460, 190, 20, green_pastel2)
    game.line_bresenham(480, 190, 500, 195, blank)

    pygame.display.update()

    game.flood_fill(60, 195, green_pastel1, animation=True)
    game.check_for_quit()

    game.flood_fill(145, 165, purple_pastel, animation=True)
    game.check_for_quit()

    game.flood_fill(270, 175, blue_pastel, animation=True)
    game.check_for_quit()

    game.flood_fill(375, 165, red_pastel, animation=True)
    game.check_for_quit()

    game.flood_fill(460, 190, green_pastel2, animation=True)
    game.check_for_quit()

    instructions_pol = TexturePolygon(
        [
            [80, 284, 0, 0],
            [80, 524, 0, 1],
            [420, 524, 1, 1],
            [420, 284, 1, 0],
        ]
    )

    instructions_texture = np.asarray(
        Image.open(os.path.join(cg_dir, "resources", "instructions.png"))
    )

    game.scanline_with_texture(instructions_pol, instructions_texture)

    pygame.display.update()

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    print("Jogo iniciado!")
                    running = False
                    pygame.display.update()

    # Remove lines "securing" the figures
    game.line_bresenham(0, 145, 40, 195, black)
    game.line_bresenham(80, 195, 120, 165, black)
    game.line_bresenham(170, 165, 250, 215, black)
    game.line_bresenham(300, 205, 350, 165, black)
    game.line_bresenham(400, 165, 440, 190, black)
    game.line_bresenham(480, 190, 500, 195, black)

    pygame.display.update()

    time.sleep(0.5)

    game.surface.fill((0, 0, 0))
    game.scanline_with_texture(sky_falling_logo_pol, sky_falling_logo_texture)

    # Setting all figures as polygons to apply transformations

    circumference_green_1_pol = TexturePolygon(
        [
            [40, 175, 0, 0],
            [40, 215, 0, 1],
            [80, 215, 1, 1],
            [80, 175, 1, 0],
        ]
    )

    circumference_green_1_tex = np.asarray(
        Image.open(os.path.join(cg_dir, "resources", "green_1_circumference.png"))
    )
    game.scanline_with_texture(
        circumference_green_1_pol,
        circumference_green_1_tex,
    )

    purple_ellipse_1_pol = TexturePolygon(
        [
            [118, 125, 0, 0],
            [118, 205, 0, 1],
            [170, 205, 1, 1],
            [170, 125, 1, 0],
        ]
    )

    purple_ellipse_1_tex = np.asarray(
        Image.open(os.path.join(cg_dir, "resources", "purple_ellipse.png"))
    )
    game.scanline_with_texture(
        purple_ellipse_1_pol,
        purple_ellipse_1_tex,
    )

    red_circumference_pol = TexturePolygon(
        [
            [350, 140, 0, 0],
            [350, 190, 0, 1],
            [400, 190, 1, 1],
            [400, 140, 1, 0],
        ]
    )

    red_circumference_tex = np.asarray(
        Image.open(os.path.join(cg_dir, "resources", "red_circumference.png"))
    )
    game.scanline_with_texture(
        red_circumference_pol,
        red_circumference_tex,
    )

    green_2_circumference_pol = TexturePolygon(
        [
            [440, 170, 0, 0],
            [440, 210, 0, 1],
            [480, 210, 1, 1],
            [480, 170, 1, 0],
        ]
    )

    green_2_circumference_tex = np.asarray(
        Image.open(os.path.join(cg_dir, "resources", "green_2_circumference.png"))
    )
    game.scanline_with_texture(
        green_2_circumference_pol,
        green_2_circumference_tex,
    )

    rectangle_pol = Polygon(
        [
            [250, 165],
            [250, 245],
            [300, 245],
            [300, 165],
        ]
    )
    game.scanline_base(rectangle_pol, blue_pastel)

    pygame.display.update()

    m1 = game.create_transformation_matrix()
    m2 = game.create_transformation_matrix()
    m3 = game.create_transformation_matrix()
    m4 = game.create_transformation_matrix()
    m5 = game.create_transformation_matrix()

    # Scale rectangle
    m5 = game.compose_translation(m5, -250, -165)
    m5 = game.compose_scale(m5, 1.8, 1.3)
    m5 = game.compose_translation(m5, 250, 165)
    game.apply_transformation(rectangle_pol, m5)

    m5 = game.create_transformation_matrix()

    time.sleep(0.2)

    pygame.display.update()

    game.scanline_base(rectangle_pol, blue_pastel)

    # Figures falling animation
    for _ in range(5):
        m1 = game.compose_translation(m1, 0, 100)
        game.scanline_base(circumference_green_1_pol, black)
        game.apply_transformation(circumference_green_1_pol, m1)
        game.scanline_with_texture(circumference_green_1_pol, circumference_green_1_tex)

        m2 = game.compose_rotation(m2, -3)
        m2 = game.compose_translation(m2, 0, 50)
        game.scanline_base(purple_ellipse_1_pol, black)
        game.apply_transformation(purple_ellipse_1_pol, m2)
        game.scanline_with_texture(purple_ellipse_1_pol, purple_ellipse_1_tex)

        m3 = game.compose_translation(m3, 0, 80)
        game.scanline_base(red_circumference_pol, black)
        game.apply_transformation(red_circumference_pol, m2)
        game.scanline_with_texture(red_circumference_pol, red_circumference_tex)

        m4 = game.compose_translation(m4, 0, 45)
        game.scanline_base(green_2_circumference_pol, black)
        game.apply_transformation(green_2_circumference_pol, m4)
        game.scanline_with_texture(green_2_circumference_pol, green_2_circumference_tex)

        m4 = game.compose_translation(m5, 0, 30)
        game.scanline_base(rectangle_pol, black)
        game.apply_transformation(rectangle_pol, m4)
        game.scanline_base(rectangle_pol, blue_pastel)

        time.sleep(0.25)

        pygame.display.update()

    time.sleep(0.5)
    game.surface.fill((0, 0, 0))

    pygame.display.update()


def sky_falling_game(game: Game):
    cat = Cat(game=game, window=window, viewport=viewport, steps=8)

    enemy_polygons = EnemyPolygons(game=game, window=window, viewport=viewport)

    running = True
    move_right = False
    move_left = False

    polygon_spawn_timer = pygame.time.get_ticks()
    polygon_move_timer = pygame.time.get_ticks()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    move_right = True

                elif event.key == pygame.K_LEFT:
                    move_left = True

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    move_right = False
                elif event.key == pygame.K_LEFT:
                    move_left = False

        if move_right:
            cat.move_right(window=window, viewport=viewport)

        if move_left:
            cat.move_left(window=window, viewport=viewport)

        current_time = pygame.time.get_ticks()

        if current_time - polygon_spawn_timer >= ADD_POLYGON_INTERVAL:
            enemy_polygons.create_random_polygon()
            polygon_spawn_timer = current_time

        if current_time - polygon_move_timer >= MOVE_POLYGON_INTERVAL:
            enemy_polygons.move_polygons()
            if enemy_polygons.check_for_colision(cat):
                break

            polygon_move_timer = current_time

        clock.tick(FPS)
        pygame.display.update()


def main():
    game = Game(width=500, height=550)

    # home_screen(game)
    sky_falling_game(game)

    # viewport1 = [0, 0, 250, 250]
    # window1 = [0, 0, 500, 500]

    # viewport2 = [250, 250, 500, 500]
    # window2 = [0, 0, 250, 250]

    # instructions_pol = TexturePolygon(
    #     [
    #         [80, 240, 0, 0],
    #         [80, 480, 0, 1],
    #         [420, 480, 1, 1],
    #         [420, 240, 1, 0],
    #     ]
    # )

    # instructions_texture = np.asarray(
    #     Image.open(os.path.join(cg_dir, "resources", "instructions.png"))
    # )

    # # print(instructions_pol.points)
    # pol1 = game.map_window(instructions_pol, window1, viewport2)
    # print(type(pol1))

    # # print(instructions_pol.points)

    # print(pol1)
    # game.scanline_with_texture(pol1, instructions_texture)

    # pol2 = game.map_window(instructions_pol, window1, viewport1)
    # game.scanline_with_texture(pol2, instructions_texture)

    # game.run()


if __name__ == "__main__":
    main()
