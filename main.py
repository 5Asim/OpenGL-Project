import os
import glfw
import pygame
from OpenGL.GL import *
from maze import *
from car import *
from collision import *
from Healthbar import *
from texture import *
from OpenGL.GLUT import GLUT_STROKE_MONO_ROMAN

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
PERIOD = 10
First_Start_Flag = True
Go_Drive_Flag = False
Go_Back_Flag = False
Break_Flag = False
On_button = False
Song_Flag = False
mouse_x, mouse_y = 0, 0
start_game = 0
game_over = 0
credits_sc = 0
you_win = 0
carModel = car()

pygame.init()
font = pygame.font.Font(None, 36)
sounds = [pygame.mixer.Sound("Sound/crash.wav"),
          pygame.mixer.Sound("Sound/coin.wav"),
          pygame.mixer.Sound("Sound/revive.wav"),
          pygame.mixer.Sound("Sound/car_horn.wav"),
          pygame.mixer.Sound("Sound/starting_game.wav"),
          pygame.mixer.Sound("Sound/lambo_drive.wav"),
          pygame.mixer.Sound("Sound/car_reverse.wav"),
          pygame.mixer.Sound("Sound/car_break.wav"),
          pygame.mixer.Sound("Sound/song.wav"),
          pygame.mixer.Sound("Sound/lobby_music.wav"),
          pygame.mixer.Sound("Sound/mouse_point.wav"),
          pygame.mixer.Sound("Sound/car_reverse1.wav"),
          pygame.mixer.Sound("Sound/bomb.wav"),
          pygame.mixer.Sound("Sound/bravo.wav")
          ]
sounds[8].set_volume(0.3)
sounds[10].set_volume(0.5)
sounds[11].set_volume(0.08)


def init_proj():
    glClearColor(0, 0, 0, 0)
    glMatrixMode(GL_PROJECTION)
    glOrtho(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT, 0, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    load_texture()


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    global start_game, game_over, you_win, mouse_x, mouse_y
    start_game = 1
    game_over
    you_win
    mouse_x
    mouse_y

    # if carModel.health <= 0:
    #     start_game = 2
    #     game_over = 1

    if credits_sc == 1:
        if 260 <= mouse_x <= 460 and 600 <= mouse_y <= 680:
            draw_texture(260, 20, 460, 100, BACK_RED)
        draw_texture(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, CREDIT_SCREEN)

    elif start_game == 0:
        glLoadIdentity()
        if 280 <= mouse_x <= 520 and 280 <= mouse_y <= 360:
            draw_texture(280, 340, 520, 420, START_RED)
        else:
            draw_texture(280, 340, 520, 420, START_RED)

        if 280 <= mouse_x <= 520 and 380 <= mouse_y <= 460:
            draw_texture(280, 240, 520, 320, CREDIT_RED)
        else:
            draw_texture(280, 240, 520, 320, CREDIT_RED)

        if 280 <= mouse_x <= 520 and 480 <= mouse_y <= 560:
            draw_texture(280, 140, 520, 220, EXIT_RED)
        else:
            draw_texture(280, 140, 520, 220, EXIT_RED)
        draw_texture(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, START_SCREEN)

    elif start_game == 1:
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        cen = carModel.center()
        glOrtho(cen[0] - 300, cen[0] + 300, cen[1] - 175, cen[1] + 175, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glClearColor(0, 0, 0, 0)

        if test_car_walls(carModel, maze1):
            carModel.collosion = True
            sounds[0].set_volume(0.2)
            sounds[0].play(0)
            sounds[5].stop()
            sounds[6].stop()

        draw_health(carModel.health, cen)
        glPushMatrix()
        # s = "stars : " + str(carModel.coins)
        # print_text(s,cen[0]-285,cen[1] + 140)
        glPopMatrix()

        draw_map()
        # draw_coins()
        # draw_healthkit()
        # draw_bombs()
        draw_finish()

        glPushMatrix()
        carModel.animation()
        carModel.draw()
        glPopMatrix()
        
        draw_dashed_lines()

    elif game_over == 1:
        sounds[8].stop()
        glClearColor(0, 0, 0, 0)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT, 0, 1)
        glMatrixMode(GL_MODELVIEW)

        if 480 <= mouse_x <= 720 and 450 <= mouse_y <= 550:  # TRY AGAIN button area
            draw_texture(480, 150, 720, 250, TRY_AGAIN_RED)  # Highlighted texture
        else:
            draw_texture(480, 150, 720, 250, TRY_AGAIN_RED)

        if 480 <= mouse_x <= 720 and 570 <= mouse_y <= 670:  # EXIT button area
            draw_texture(480, 30, 720, 130, EXIT2_RED)  # Highlighted texture
        else:
            draw_texture(480, 30, 720, 130, EXIT2_RED)

        draw_texture(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, PLAY_AGAIN)

    elif you_win == 1:
        sounds[8].stop()
        glClearColor(0, 0, 0, 0)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT, 0, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        # Draw the "You Win" texture
        draw_texture(480, 570, 720, 670, HOME_RED)
        draw_texture(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, YOU_WIN)

        # Draw Play Again and Exit buttons
        if 480 <= mouse_x <= 720 and 450 <= mouse_y <= 550:  # Play Again button area
            draw_texture(480, 150, 720, 250, HOME_RED)  # Highlighted texture
        else:
            draw_texture(480, 150, 720, 250, HOME_RED)

        if 480 <= mouse_x <= 720 and 570 <= mouse_y <= 670:  # Exit button area
            draw_texture(480, 30, 720, 130, EXIT2_RED)  # Highlighted texture
        else:
            draw_texture(480, 30, 720, 130, EXIT2_RED)

        draw_texture(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, YOU_WIN)

    glfw.swap_buffers(window)

def print_text(text_string, x, y):
    font = pygame.font.Font(None, 64)
    text_surface = font.render(text_string, True, (255, 255, 0, 255))
    text_data = pygame.image.tostring(text_surface, "RGBA", True)
    
    glRasterPos2d(x, y)
    glDrawPixels(text_surface.get_width(), text_surface.get_height(), GL_RGBA, GL_UNSIGNED_BYTE, text_data)


def draw_texture(left, bottom, right, top, tex_iden):
    glBindTexture(GL_TEXTURE_2D, tex_iden)
    glColor3f(1, 1, 1)
    glBegin(GL_POLYGON)
    glTexCoord2f(0, 0)
    glVertex2f(left, bottom)
    glTexCoord2f(1, 0)
    glVertex2f(right, bottom)
    glTexCoord2f(1, 1)
    glVertex2f(right, top)
    glTexCoord2f(0, 1)
    glVertex2f(left, top)
    glEnd()
    glBindTexture(GL_TEXTURE_2D, -1)


def handle_keys(window, key, scancode, action, mods):
    global carModel, Go_Drive_Flag, Go_Back_Flag, Break_Flag, Song_Flag

    if action == glfw.PRESS or action == glfw.REPEAT:
        if key == glfw.KEY_W:
            carModel.speed = 2.5
            if not Go_Drive_Flag and start_game == 1:
                sounds[5].set_volume(0.1)
                sounds[5].play(-1)
                Go_Drive_Flag = True

        elif key == glfw.KEY_S:
            carModel.speed = -2
            if not Go_Back_Flag and start_game == 1:
                sounds[6].set_volume(0.5)
                sounds[6].play(-1)
                Go_Back_Flag = True

        elif key == glfw.KEY_A:
            carModel.rot = 1

        elif key == glfw.KEY_D:
            carModel.rot = -1

        elif key == glfw.KEY_SPACE:
            carModel.speed = 0
            if not Break_Flag and start_game == 1:
                sounds[7].set_volume(0.2)
                sounds[7].play(0)
                Break_Flag = True

    elif action == glfw.RELEASE:
        if key == glfw.KEY_W:
            carModel.speed = 0
            sounds[5].stop()
            Go_Drive_Flag = False

        elif key == glfw.KEY_S:
            carModel.speed = 0
            sounds[6].stop()
            Go_Back_Flag = False

        elif key == glfw.KEY_A:
            carModel.rot = 0  # Reset rotation when 'A' is released

        elif key == glfw.KEY_D:
            carModel.rot = 0  # Reset rotation when 'D' is released

        elif key == glfw.KEY_SPACE:
            Break_Flag = False


def main():
    if not glfw.init():
        return

    global window
    window = glfw.create_window(WINDOW_WIDTH, WINDOW_HEIGHT, "Car Game", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_key_callback(window, handle_keys)
    glfw.swap_interval(1)
    init_proj()

    while not glfw.window_should_close(window):
        display()
        glfw.poll_events()

    glfw.terminate()


if __name__ == "__main__":
    main()
