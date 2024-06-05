from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 1020

'''
To draw the health bar we have to do 3 steps:
1- We draw the white bar which represents full health.
2- We need to calculate the length of the green bar which represnts health.
3- We change the color of the health bar.
4- We draw the green bar.
'''


def draw_white_bar(center):
    glColor3f(1, 1, 1)
    glBegin(GL_POLYGON)
    # Adjusted vertices for a vertical bar, moved down by 170 units
    glVertex3f(center[0] - 10 - 230 - 10, center[1] + 60 + 165 - 170, 0)
    glVertex3f(center[0] + 10 - 230 - 10, center[1] + 60 + 165 - 170, 0)
    glVertex3f(center[0] + 10 - 230 - 10, center[1] - 60 + 165 - 170, 0)
    glVertex3f(center[0] - 10 - 230 - 10, center[1] - 60 + 165 - 170, 0)
    glEnd()

def draw_health_bar(health, center):
    # As health decreases, the green decreases and the red increases.
    glColor3f(1 - health / 100, health / 100, 0)
    # Calculating the height of the green section based on health
    Green_Section = (health * (116 / 100))
    glBegin(GL_POLYGON)
    # Fixing the bottom side of the health bar to decrease only from the top, moved down by 170 units
    glVertex3f(center[0] - 10 - 230 - 10, center[1] - 59 + 165 - 170, 0)
    glVertex3f(center[0] + 10 - 230 - 10, center[1] - 59 + 165 - 170, 0)
    glVertex3f(center[0] + 10 - 230 - 10, center[1] - 59 + Green_Section + 165 - 170, 0)
    glVertex3f(center[0] - 10 - 230 - 10, center[1] - 59 + Green_Section + 165 - 170, 0)
    glEnd()



def draw_health(health, center):
    glPushMatrix()
    draw_health_bar(health, center)
    draw_white_bar(center)
    glPopMatrix()
