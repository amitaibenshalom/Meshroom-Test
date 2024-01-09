#!/usr/bin/env python
# Basic OBJ file viewer. needs objloader from:
#  http://www.pygame.org/wiki/OBJFileLoader
# LMB + move: rotate
# RMB + move: pan
# Scroll wheel: zoom in/out
import sys, pygame
from pygame.locals import *
from pygame.constants import *
from OpenGL.GL import *
from OpenGL.GLU import *
import time

# IMPORT OBJECT LOADER
from objloader import *

pygame.init()
screen_info = pygame.display.Info()
viewport = (screen_info.current_w,screen_info.current_h)

# open a window in fullscreen mode with opengl enabled and pink background
pygame.display.set_caption("Photogrammetry")
screen = pygame.display.set_mode(viewport, OPENGL | DOUBLEBUF | pygame.FULLSCREEN)
screen.fill((200, 0, 100))
pygame.display.flip()
time.sleep(5)


glLightfv(GL_LIGHT0, GL_POSITION,  (-40, 200, 100, 0.0))
glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
glEnable(GL_LIGHT0)
glEnable(GL_LIGHTING)
glEnable(GL_COLOR_MATERIAL)
glEnable(GL_DEPTH_TEST)
glShadeModel(GL_SMOOTH)           # most obj files expect to be smooth-shaded

# LOAD OBJECT AFTER PYGAME INIT
obj_file_path = r"C:\Users\mada\Documents\photogrammetry\photogrammetry_data\2024-01-01-10-35-52-0016\output\texturedMesh.obj"
obj = OBJ(obj_file_path, swapyz=True)
obj.generate()

clock = pygame.time.Clock()

glMatrixMode(GL_PROJECTION)
glLoadIdentity()
width, height = viewport
gluPerspective(90, width/float(height), 1, 100.0)
glEnable(GL_DEPTH_TEST)
glMatrixMode(GL_MODELVIEW)

rx, ry, rz = (-90,90,0)
tx, ty, tz = (0,-5,-5)

rotate = move = False

# glTranslatef(tx, ty, tz)

stopwatch = time.time()
MAX_TIME = 10
while 1:
    if time.time() - stopwatch > MAX_TIME:
        break
    clock.tick(30)
    for e in pygame.event.get():
        if e.type == QUIT:
            sys.exit()
        elif e.type == KEYDOWN and e.key == K_ESCAPE:
            sys.exit()
        # elif e.type == MOUSEBUTTONDOWN:
        #     if e.button == 4: zpos = max(1, zpos-1)
        #     elif e.button == 5: zpos += 1
        #     elif e.button == 1: rotate = True
        #     elif e.button == 3: move = True
        # elif e.type == MOUSEBUTTONUP:
        #     if e.button == 1: rotate = False
        #     elif e.button == 3: move = False
        # elif e.type == MOUSEMOTION:
        #     i, j = e.rel
        #     if rotate:
        #         rx += i
        #         ry += j
        #     if move:
        #         tx += i
        #         ty -= j
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(1,1,1,1)
    # glLoadIdentity()

    ry += 1
    # rz += 1
    # rx += 1


    glRotatef(ry, 0, 1.0, 0)
    glRotatef(rz, 0, 0, 1.0)
    glRotatef(rx, 1.0, 0, 0)
    glPushMatrix()
    glTranslatef(tx, ty, tz)
    obj.render()
    glPopMatrix()


    # glPushMatrix()
    # glTranslatef(tx, ty, tz)
    # glRotatef(ry, 0, 1.0, 0)
    # glRotatef(rz, 0, 0, 1.0)
    # glRotatef(rx, 1.0, 0, 0)
    # glTranslatef(-tx, -ty, -tz)
    # obj.render()
    # glPopMatrix()


    # glPushMatrix()
    # glTranslate(-tx, -ty, -tz)
    # glRotate(ry, 0, 1, 0)
    # glTranslate(tx, ty, tz)
    # obj.render()
    # glPopMatrix()


    # RENDER OBJECT
    # glTranslate(0, 0, 0)
    # glTranslate(tx/20.0, ty/20.0, - zpos)
    # glRotate(ry, 1, 0, 0)
    # glRotate(rx, 0, 1, 0)
    # glRotate(rz, 0, 0, 1)
    # glTranslate(tx/20., ty/20., - zpos)


    pygame.display.flip()