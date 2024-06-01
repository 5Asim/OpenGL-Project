import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from shapes import draw_cube, draw_sphere, draw_pyramid

# Initialize Pygame and OpenGL
pygame.init()
display = (800, 600)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
glOrtho(-5, 5, -5, 5, -5, 5)

# Parameters for transformations
initial_translate = [0, 0, 0]
initial_rotate = [0, 0, 0]
initial_scale = [1, 1, 1]

translate = initial_translate.copy()
rotate = initial_rotate.copy()
scale = initial_scale.copy()

shape_index = 0

shapes = [draw_cube, draw_sphere, draw_pyramid]

def handle_input():
    global translate, rotate, scale, shape_index
    keys = pygame.key.get_pressed()
    if keys[K_LEFT]:
        translate[0] -= 0.1
    if keys[K_RIGHT]:
        translate[0] += 0.1
    if keys[K_UP]:
        translate[1] += 0.1
    if keys[K_DOWN]:
        translate[1] -= 0.1
    if keys[K_q]:
        translate[2] -= 0.1
    if keys[K_e]:
        translate[2] += 0.1
    if keys[K_a]:
        rotate[1] -= 5
    if keys[K_d]:
        rotate[1] += 5
    if keys[K_w]:
        rotate[0] -= 5
    if keys[K_s]:
        rotate[0] += 5
    if keys[K_z]:
        scale[0] *= 0.9
        scale[1] *= 0.9
        scale[2] *= 0.9
    if keys[K_x]:
        scale[0] *= 1.1
        scale[1] *= 1.1
        scale[2] *= 1.1
    if keys[K_TAB]:
        shape_index = (shape_index + 1) % len(shapes)
    if keys[K_r]:
        reset_transformations()

def reset_transformations():
    global translate, rotate, scale
    translate = initial_translate.copy()
    rotate = initial_rotate.copy()
    scale = initial_scale.copy()

def main():
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        handle_input()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glPushMatrix()
        glTranslatef(*translate)
        glRotatef(rotate[0], 1, 0, 0)
        glRotatef(rotate[1], 0, 1, 0)
        glRotatef(rotate[2], 0, 0, 1)
        glScalef(*scale)
        shapes[shape_index]()
        glPopMatrix()

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()
