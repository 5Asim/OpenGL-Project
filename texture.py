import pygame
from OpenGL.GL import *

# creating a list of texture names that will be used to identify each texture.
texture_names = [0, 1, 2]

# assigning a unique integer identifier to each texture using global constants, which makes it easier to refer to textures throughout the code.
CAR = 0
FINISH_LINE = 1
YOU_WIN = 2

#Enables 2D texture mapping for OpenGL, loads all the texture images, and stores them as a list of texture binary data.
#generates a unique texture name for each image and sets up the texture parameters for each texture using the setup_texture() function.
def load_texture():

    glEnable(GL_TEXTURE_2D)

    images = []

    # Load images from files
    images.append(pygame.image.load("texture/redcar_ku.png"))
    images.append(pygame.image.load("texture/finish_line.jpg"))
    images.append(pygame.image.load("texture/youwin.png"))

    # Convert the images to raw binary image data
    textures = [pygame.image.tostring(img, "RGBA", 1) for img in images]

    # Generate texture IDs
    glGenTextures(len(images), texture_names)

    # Bind each texture and set texture parameters
    for i in range(len(images)):
        setup_texture(textures[i],
                      texture_names[i],
                      images[i].get_width(),
                      images[i].get_height())

def setup_texture(binary_img, texture_iden, width, height):
    """
    Binds the texture to the texture identifier, sets texture parameters, and then loads the texture binary data.
    """
    glBindTexture(GL_TEXTURE_2D, texture_iden)

    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width,
                 height, 0, GL_RGBA, GL_UNSIGNED_BYTE, binary_img)
