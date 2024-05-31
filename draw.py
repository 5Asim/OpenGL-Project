from OpenGL.GL import *
from OpenGL.GLU import *

def draw_ball(position):
    glPushMatrix()
    glTranslatef(position[0], position[1], position[2])
    glColor3f(1, 0, 0)
    quad = gluNewQuadric()
    gluSphere(quad, 0.5, 32, 32)
    glPopMatrix()

def draw_player(position):
    glPushMatrix()
    glTranslatef(position[0], position[1], position[2])
    glColor3f(0, 1, 0)
    glBegin(GL_QUADS)
    for vertex in cube_vertices():
        glVertex3fv(vertex)
    glEnd()
    glPopMatrix()

def cube_vertices():
    return [
        [1, 1, -1],
        [1, -1, -1],
        [-1, -1, -1],
        [-1, 1, -1],
        [1, 1, 1],
        [1, -1, 1],
        [-1, -1, 1],
        [-1, 1, 1]
    ]

def draw_goal(position, size):
    glPushMatrix()
    glTranslatef(position[0], position[1], position[2])
    glColor3f(1, 1, 0)
    glBegin(GL_LINES)
    glVertex3f(-size / 2, -0.5, 0)
    glVertex3f(size / 2, -0.5, 0)
    glVertex3f(-size / 2, 0.5, 0)
    glVertex3f(size / 2, 0.5, 0)
    glVertex3f(-size / 2, -0.5, 0)
    glVertex3f(-size / 2, 0.5, 0)
    glVertex3f(size / 2, -0.5, 0)
    glVertex3f(size / 2, 0.5, 0)
    glEnd()
    glPopMatrix()
