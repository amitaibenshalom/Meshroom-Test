import pygame
import datetime as dt
import time
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *
from pygame.constants import *
from objloader import *
from consts import *
from shutil import rmtree


def init_model(obj_file, render=True):
    """
    initialize the object model with the given obj file
    """
    global viewport, output_directory, rx, ry, rz, zpos, obj, state
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(*BACKGROUND_COLOR)
    glLoadIdentity()

    center_object(obj_file)
    obj = OBJ(obj_file, swapyz=True)
    obj.generate()
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    width, height = viewport
    gluPerspective(70.0, width/float(height), 1, 100.0)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_MODELVIEW)
    glTranslate(0,0,zpos)
    glRotatef(ry, 0.0, 1.0, 0.0)
    glRotatef(rx, 1.0, 0.0, 0.0)
    glRotatef(rz, 0.0, 0.0, 1.0)
    
    if render:
        obj.render()


def rotate_model(render=False):
    """
    rotate the object model on the screen by 1 degree (not rendering the object, just rotating)
    """
    global rx, ry, rz, obj, zpos
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(*BACKGROUND_COLOR)
    glLoadIdentity()
    ry += 1
    glTranslate(0,0,zpos)
    glRotatef(ry, 0.0, 1.0, 0.0)
    glRotatef(rx, 1.0, 0.0, 0.0)
    glRotatef(rz, 0.0, 0.0, 1.0)

    if render:
        obj.render()


def render_model():
    """
    render the object model on the screen
    """
    global rx, ry, rz, obj, zpos
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(*BACKGROUND_COLOR)
    glLoadIdentity()
    glTranslate(0,0,zpos)
    glRotatef(ry, 0.0, 1.0, 0.0)
    glRotatef(rx, 1.0, 0.0, 0.0)
    glRotatef(rz, 0.0, 0.0, 1.0)
    obj.render()


def show_error_screen(msg=1):
    """
    show the error screen on the screen
    """
    global screen
    font = pygame.font.Font(None, 36)  # Use default system font, size 36
    text = f'Cant find any 3D models in the given folder: "{photogrammetry_data_path}" - please check the data folder and try again! Press ESC to exit window'
    
    if msg == 2:
        text = f'Error in loading model: "{obj_file_path}" - object might be corrupted, try deleting it. Press ESC to exit window'

    text_surface = font.render(text, True, (0,0,0))  # Render the text
    screen.fill((255, 255, 255))  # Fill the screen with white
    screen.blit(text_surface, (0, 0))


def get_nth_obj_in_folder(folder_path, n):
    """
    get the nth obj file and texture file in the given folder path
    """
    items = os.listdir(folder_path)
    items = sorted(items)
    
    if len(items) == 0:
        raise FileNotFoundError(f"No files found in the given folder: {folder_path}")
    
    if n >= len(items):
        raise IndexError(f"Index out of range: {n} - the folder has only {len(items)} files")
    
    n += 1
    obj_file_path = os.path.join(folder_path, items[-n], obj_path)
    texture_file_path = os.path.join(folder_path, items[-n], texture_path)
    return obj_file_path, texture_file_path


pygame.init()
screen_info = pygame.display.Info()
viewport = (screen_info.current_w,screen_info.current_h)
width = screen_info.current_w
height = screen_info.current_h

screen = pygame.display.set_mode(viewport, OPENGL | DOUBLEBUF | pygame.FULLSCREEN)
gluPerspective(70.0, width/float(height), 1, 100.0)
glMatrixMode(GL_PROJECTION)
glEnable(GL_DEPTH_TEST)
glMatrixMode(GL_MODELVIEW)
# glLightfv(GL_LIGHT0, GL_POSITION,  (-40, 200, 100, 0.0))
# glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
# glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
# glEnable(GL_LIGHT0)
# glEnable(GL_LIGHTING)
# glEnable(GL_COLOR_MATERIAL)
glEnable(GL_DEPTH_TEST)
glShadeModel(GL_SMOOTH)
glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
glClearColor(*BACKGROUND_COLOR)

glViewport(0, 0, width, height)
glLoadIdentity()
glOrtho(0, width, height, 0, -1, 1)
glLoadIdentity()

clock = pygame.time.Clock()
rx, ry, rz = (-90,180,0)
obj = None
last_touch = time.time()
idle = False
obj_file_path, texture_file_path = None, None

try:
    obj_file_path, texture_file_path = get_nth_obj_in_folder(photogrammetry_data_path, model_number)

except:
    print("No obj file found in the given folder")
    screen = pygame.display.set_mode(viewport, pygame.FULLSCREEN)
    show_error_screen()
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
        pygame.display.flip()
    exit()

files_in_data_folder = len(os.listdir(photogrammetry_data_path))

try:
    init_model(obj_file_path)

except:
    print("No obj file found in the given folder")
    screen = pygame.display.set_mode(viewport, pygame.FULLSCREEN)
    show_error_screen(msg=2)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
        pygame.display.flip()
    exit()

print(f"model path: {obj_file_path}")
print(f"texture path: {texture_file_path}")


running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
            break

        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
                break

            if event.key == K_r:
                model_number += 1
                if model_number >= MAX_MODEL_NUMBER or model_number >= len(os.listdir(photogrammetry_data_path)):
                    model_number = 0
                obj_file_path, texture_file_path = get_nth_obj_in_folder(photogrammetry_data_path, model_number)
                print(f"model path: {obj_file_path}")
                try:
                    init_model(obj_file_path)
                except:
                    print(f"Error in loading model {obj_file_path}")
                    # # the obj file is probably corrupted, remove it's parent folder
                    # # get two directories up and remove the folder
                    # parent_folder = os.path.dirname(os.path.dirname(obj_file_path))
                    # print(f"Removing folder: {parent_folder}")
                    # # delete the folder (and all it's contents)
                    # # rmtree(parent_folder)


            if event.key == K_l:
                model_number -= 1
                if model_number < 0:
                    model_number = min(MAX_MODEL_NUMBER-1, len(os.listdir(photogrammetry_data_path)) - 1)
                obj_file_path, texture_file_path = get_nth_obj_in_folder(photogrammetry_data_path, model_number)
                print(f"model path: {obj_file_path}")
                try:
                    init_model(obj_file_path)
                except:
                    print(f"Error in loading model {obj_file_path}")
                    # # the obj file is probably corrupted, remove it's parent folder
                    # # get two directories up and remove the folder
                    # parent_folder = os.path.dirname(os.path.dirname(obj_file_path))
                    # print(f"Removing folder: {parent_folder}")
                    # # rmtree(parent_folder)

        elif event.type == MOUSEBUTTONDOWN:  # if mouse is dragged then rotate the model accordingly (not used because of the touch screen)
            last_touch = time.time()
            idle = False
            if event.button == 4:
                # zpos = max(zpos - 1, -30)
                pass
            elif event.button == 5:
                # zpos = min(zpos + 1, -1)
                pass
            elif event.button == 1:
                # x, y = event.pos
                # rx += (y - ry)
                # ry += (x - rx)
                pass

        elif event.type == MOUSEMOTION:  # if mouse is moved then rotate the model accordingly (good for touch screen)
            last_touch = time.time()
            idle = False
            if event.buttons[0]:
                x, y = event.rel
                if borders[0] * width < event.pos[0] < (1 - borders[0]) * width and borders[1] * height < event.pos[1] < (1 - borders[1]) * height: 
                    rx -= y * 0.3
                    ry += x * 0.3
                    
        elif event.type == MOUSEWHEEL:
            # zpos += event.y
            pass

    if files_in_data_folder != len(os.listdir(photogrammetry_data_path)):
        files_in_data_folder = len(os.listdir(photogrammetry_data_path))
        model_number = 0
        time.sleep(TIME_TO_WAIT_FOR_NEW_MODEL)  # wait for the new model to be fully written
        obj_file_path, texture_file_path = get_nth_obj_in_folder(photogrammetry_data_path, model_number)
        init_model(obj_file_path)
    
    if time.time() - last_touch > time_to_idle:
        idle = True
    if idle:
        rotate_model()
        rx = -90
    
    render_model()
    pygame.display.flip()
    clock.tick(60)


