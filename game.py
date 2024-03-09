import pygame as pg
from OpenGL.GL import *
import numpy as np
from OpenGL.GL.shaders import compileProgram, compileShader

class App:
        def __init__(self):
                # Initialize pygame and create a window
                pg.init()
                pg.display.set_mode((640, 480), pg.OPENGL|pg.DOUBLEBUF)
                self.clock = pg.time.Clock()
                
                # Initialize OpenGL
                glClearColor(0.1, 0.2, 0.2, 1)
                self.shader = self.createShader("shaders/vertex.txt", "shaders/fragment.txt")
                glUseProgram(self.shader)
                
                # Initialize shapes
                self.shapes = [Triangle(), Pyramid()]  # Add more shapes if needed
                self.current_shape_index = 0  # Start with the first shape
                
                self.mainLoop()
                
        # createShader method as before
        def createShader(self, vertexFilepath, fragmentFilepath):
        # Read vertex shader source
                with open(vertexFilepath, 'r') as file:
                        vertex_src = file.read()

                # Read fragment shader source
                with open(fragmentFilepath, 'r') as file:
                        fragment_src = file.read()

                # Compile shaders and link program
                vertex_shader = compileShader(vertex_src, GL_VERTEX_SHADER)
                fragment_shader = compileShader(fragment_src, GL_FRAGMENT_SHADER)
                shader = compileProgram(vertex_shader, fragment_shader)

                return shader


        def mainLoop(self):
                running = True
                while running:
                        for event in pg.event.get():
                                if event.type == pg.QUIT:
                                        running = False
                                elif event.type == pg.KEYDOWN:
                                        if event.key == pg.K_n:  # Press 'n' to switch to the next shape
                                                self.current_shape_index = (self.current_shape_index + 1) % len(self.shapes)
                
                        # Refresh Screen
                        glClear(GL_COLOR_BUFFER_BIT)
                        glUseProgram(self.shader)
                        
                        shape = self.shapes[self.current_shape_index]
                        glBindVertexArray(shape.vao)
                        if hasattr(shape, 'indices'):
                                glDrawElements(GL_TRIANGLES, shape.vertex_count, GL_UNSIGNED_INT, None)
                        else:
                                glDrawArrays(GL_TRIANGLES, 0, shape.vertex_count)
                        
                        pg.display.flip()
                        
                        # Timing
                        self.clock.tick(60)
                self.quit()
                
        def quit(self):
                for shape in self.shapes:
                        shape.destroy()
                glDeleteProgram(self.shader)
                pg.quit()

class Triangle:
        def __init__(self):
                self.vertices = np.array([
                -0.5, -0.5, 0, 1.0, 0.0, 0.0,  # Vertex 1
                0.5, -0.5, 0, 0.0, 1.0, 0.0,  # Vertex 2
                0.0,  0.5, 0, 0.0, 0.0, 1.0   # Vertex 3
                ], dtype=np.float32)
                
                self.vertex_count = 3
                
                self.vao = glGenVertexArrays(1)
                glBindVertexArray(self.vao)
                
                self.vbo = glGenBuffers(1)
                glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
                glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)
                
                # Position attribute
                glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
                glEnableVertexAttribArray(0)
                
                # Color attribute
                glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
                glEnableVertexAttribArray(1)
                
                glBindVertexArray(0)  # Unbind VAO
                
        def destroy(self):
                glDeleteVertexArrays(1, (self.vao,))
                glDeleteBuffers(1, (self.vbo,))

                
class Pyramid:
        def __init__(self):
                self.vertices = np.array([
                # Base
                -0.5, -0.5, -0.5,  1.0, 0.0, 0.0,
                0.5, -0.5, -0.5,  0.0, 1.0, 0.0,
                0.5, -0.5,  0.5,  0.0, 0.0, 1.0,
                -0.5, -0.5,  0.5,  1.0, 1.0, 0.0,
                # Apex
                0.0,  0.75, 0.0,  0.5, 0.5, 1.0
                ], dtype=np.float32)
                
                self.indices = np.array([
                0, 1, 2,  2, 3, 0,  # Base
                0, 1, 4,  1, 2, 4,  2, 3, 4,  3, 0, 4  # Sides
                ], dtype=np.uint32)
                
                self.vertex_count = len(self.indices)
                
                self.vao = glGenVertexArrays(1)
                glBindVertexArray(self.vao)
                
                self.vbo = glGenBuffers(1)
                glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
                glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)
                
                self.ebo = glGenBuffers(1)
                glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo)
                glBufferData(GL_ELEMENT_ARRAY_BUFFER, self.indices.nbytes, self.indices, GL_STATIC_DRAW)
                
                glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))
                glEnableVertexAttribArray(0)
                
                glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
                glEnableVertexAttribArray(1)
                
                glBindVertexArray(0)  # Unbind VAO
                
        def destroy(self):
                glDeleteVertexArrays(1, (self.vao,))
                glDeleteBuffers(1, (self.vbo,))
                glDeleteBuffers(1, (self.ebo,))

                
                
if __name__ == "__main__":
        myApp = App()