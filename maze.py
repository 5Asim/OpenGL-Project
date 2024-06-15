from OpenGL.GL import *
import glfw
from texture import *
LINE_WIDTH = 10
class line:
    def __init__(self, x1, y1, x2, y2):  # initialize line end points (x1,y1) & (x2,y2)
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.vertical = (x1 == x2)

    def get_vertices(self):
        return [[self.x1, self.y1], [self.x2, self.y2]]
    
    def draw_line(self):
        glColor3f(0, 1, 0)
        glLineWidth(3)
        glBegin(GL_LINES)
        glVertex3f(self.x1, self.y1, 0)
        glVertex3f(self.x2, self.y2, 0)
        glEnd()

    def draw_dashed_line(self):
        glColor3f(1, 1, 1)
        glLineWidth(3)
        glEnable(GL_LINE_STIPPLE)
        glLineStipple(30, 0xAAAA)  # Dash pattern
        glBegin(GL_LINES)
        glVertex3f(self.x1, self.y1, 0)
        glVertex3f(self.x2, self.y2, 0)
        glEnd()
        glDisable(GL_LINE_STIPPLE)

class box:
    def __init__(self, left, bottom, right, top, Type=0):
        self.left = left-5
        self.bottom = bottom-5
        self.right = right+5
        self.top = top+5
        self.type = Type
        self.collected = False  # if collected it will not be drawn, else it will be drawn

    def draw(self):
        if not self.collected:
            # Choosing texture of box based on its type
            if self.type == 3:
                glBindTexture(GL_TEXTURE_2D, FINISH_LINE)
            glBegin(GL_POLYGON)
            glTexCoord2f(0, 0)
            glVertex3f(self.left, self.bottom, 0)
            glTexCoord2f(1, 0)
            glVertex3f(self.right, self.bottom, 0)
            glTexCoord2f(1, 1)
            glVertex3f(self.right, self.top, 0)
            glTexCoord2f(0, 1)
            glVertex3f(self.left, self.top, 0)
            glEnd()
            glBindTexture(GL_TEXTURE_2D, -1)

    def get_vertices(self):
        vertices = [
            [self.left, self.top],
            [self.left, self.bottom],
            [self.right, self.bottom],
            [self.right, self.top],
        ]
        return vertices

# Maze walls
maze1 = [
    line(0, 100, 300, 100), line(150, 200, 150, 600),
    line(0, 600, 150, 600), line(300, 200, 300, 600),
    line(300, 200, 900, 200), line(450, 300, 900, 300),
    line(600, 400, 900, 400), line(0, 700, 0, 0),
    line(600, 500, 1200, 500), line(1050, 500, 1050, 200),
    line(600, 500, 600, 600), line(600, 600, 1050, 600),
    line(900, 400, 900, 300), line(450, 700, 450, 300),
    line(900, 200, 900, 100), line(450, 100, 1050, 100),
    line(450, 0, 450, 100), line(0, 0, 1200, 0),
    line(1200, 0, 1200, 700), line(1200, 700, 0, 700)
]

class FinishLine:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def get_vertices(self):
        return [(self.x1, self.y1), (self.x1, self.y2), (self.x2, self.y2), (self.x2, self.y1)]
# Finish line of maze
finish = [box(730, 507-0.5, 750, 593+0.5, 3)]

# Reset every box in the given list of boxes to its initial state
def reset(lst_of_box: list):
    for i in lst_of_box:
        if i.collected:
            i.collected = False

# Reset all boxes to the initial state to be able to play again
def reset_maze():
    pass  # No boxes to reset anymore

# Draw maze walls
def draw_map():
    for i in range(len(maze1)):
        maze1[i].draw_line()

# Draw finish line of the map
def draw_finish():
    glColor3f(1, 1, 1)
    for i in finish:
        i.draw()

# Draw a grid 1200 * 700, every cell in this grid is 150 * 100 so we have a 8 * 7 grid to make it easy to allocate everything in the world
def draw_grid():
    glLineWidth(1)
    glColor3f(1, 0, 0)
    glBegin(GL_LINES)
    for i in range(8):
        glVertex3f(-1500, i*100, 0)
        glVertex3f(1200, i*100, 0)
    for i in range(9):
        glVertex3f(i*150, -1500, 0)
        glVertex3f(i*150, 1500, 0)
    glEnd()

def draw_dashed_lines():
    for wall in maze1:
        if wall.vertical:
            # Draw a dashed line to the left of the vertical line
            if wall.x1 > 0:
                dashed_line = line(wall.x1 - LINE_WIDTH*15/2, wall.y1, wall.x2 - LINE_WIDTH*15/2, wall.y2)
                dashed_line.draw_dashed_line()
        else:
            # Draw a dashed line above the horizontal line
            if wall.y1 < 700:
                dashed_line = line(wall.x1, wall.y1 + LINE_WIDTH*10/2, wall.x2, wall.y2 + LINE_WIDTH*10/2)
                dashed_line.draw_dashed_line()

# Main display function
def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_TEXTURE_2D)

    draw_map()
    draw_finish()
    draw_dashed_lines()

    glDisable(GL_TEXTURE_2D)
    glfw.swap_buffers()
