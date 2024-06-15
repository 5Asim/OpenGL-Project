import os
import glfw
import pygame
from OpenGL.GL import *
from maze import *
from car import *
from collision import *
from texture import *
from maze import finish

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
          pygame.mixer.Sound("Sound/win.wav"),
          pygame.mixer.Sound("Sound/bravo.wav"),
          ]
sounds[8].set_volume(0.3)


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
        
    if you_win == 1:
        sounds[9].stop()
        glClearColor(0, 0, 0, 0)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT, 0, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        draw_texture(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, YOU_WIN)
        
    elif game_over == 1:
        glClearColor(0, 0, 0, 0)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT, 0, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        draw_texture(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, TRY_AGAIN_RED)

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

        glPushMatrix()
        glPopMatrix()

        draw_map()
        draw_finish()

        glPushMatrix()
        carModel.animation()
        carModel.draw()
        glPopMatrix()
        
        draw_dashed_lines()
        check_collision_with_finish()

    glfw.swap_buffers(window)


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
    

# main.py
def check_collision_with_finish():
    global you_win, start_game, finish  # Add 'finish' to the global variables
    car_vertices = carModel.get_vertices()
    for f in finish:
        box_vertices = f.get_vertices()
        if (box_vertices[0][0] <= car_vertices[0][0] <= box_vertices[2][0]) and (box_vertices[1][1] <= car_vertices[1][1] <= box_vertices[0][1]):
            you_win = 1
            start_game = 0  # Stop the game
            sounds[9].play(0)  # Play the "bravo" sound effect
            break  # Exit the loop after the first collision with the finish line




def handle_keys(window, key, scancode, action, mods):
    global carModel, Go_Drive_Flag, Go_Back_Flag, Break_Flag, Song_Flag, start_game, you_win, game_over

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
        
        
        elif key == glfw.KEY_R:
            carModel.reset_position()
            carModel.health = 100
            you_win = 0
            start_game = 1 
            game_over = 0 
           

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
    window = glfw.create_window(WINDOW_WIDTH, WINDOW_HEIGHT, "Maze Runner", None, None)
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
