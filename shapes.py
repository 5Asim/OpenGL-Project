from OpenGL.GL import *
from OpenGL.GLU import *

def draw_cube():
    vertices = [
        [1, 1, -1], [1, -1, -1], [-1, -1, -1], [-1, 1, -1],
        [1, 1, 1], [1, -1, 1], [-1, -1, 1], [-1, 1, 1]
    ]
    edges = [
        [0, 1], [1, 2], [2, 3], [3, 0],
        [4, 5], [5, 6], [6, 7], [7, 4],
        [0, 4], [1, 5], [2, 6], [3, 7]
    ]
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(vertices[vertex])
    glEnd()

def draw_sphere():
    quad = gluNewQuadric()
    gluSphere(quad, 1, 32, 32)

def draw_pyramid():
    vertices = [
        [1, -1, -1], [-1, -1, -1], [-1, -1, 1], [1, -1, 1],
        [0, 1, 0]
    ]
    faces = [
        [0, 1, 4], [1, 2, 4], [2, 3, 4], [3, 0, 4],
        [0, 1, 2, 3]
    ]
    glBegin(GL_TRIANGLES)
    for face in faces[:-1]:
        for vertex in face:
            glVertex3fv(vertices[vertex])
    glEnd()
    glBegin(GL_QUADS)
    for vertex in faces[-1]:
        glVertex3fv(vertices[vertex])
    glEnd()
