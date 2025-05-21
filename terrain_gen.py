import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import noise
import numpy as np

cols, rows = 0, 0
scl = 20
w = 1400
h = 1000
flying = 0

terrain = []


def setup():
    global cols, rows, terrain
    cols = int(w / scl)
    rows = int(h / scl)
    terrain = np.zeros((cols, rows))


def generate_terrain():
    global flying, terrain
    flying += 0.1
    yoff = flying

    for y in range(rows):
        xoff = 0
        for x in range(cols):
            terrain[x][y] = noise.pnoise2(xoff, yoff, octaves=4) * 200 - 100
            xoff += 0.2
        yoff += 0.2


def draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glPushMatrix()

    glTranslatef(0, -50, -400)  # Adjust to move terrain down
    glRotatef(-60, 1, 0, 0)     # Flip terrain by changing the rotation angle
    glTranslatef(-w / 2, -h / 2, 0)

    glColor3f(1, 1, 1)
    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)  # Set to wireframe mode

    for y in range(rows - 1):
        glBegin(GL_TRIANGLE_STRIP)
        for x in range(cols):
            glVertex3f(x * scl, y * scl, terrain[x][y])
            glVertex3f(x * scl, (y + 1) * scl, terrain[x][y + 1])
        glEnd()

    glPopMatrix()
    pygame.display.flip()


def main():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    gluPerspective(45, (display[0] / display[1]), 0.1, 1000.0)
    glTranslatef(0.0, 0.0, -500)

    setup()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        generate_terrain()
        draw()
        pygame.time.wait(10)

    pygame.quit()


if __name__ == "__main__":
    main()
