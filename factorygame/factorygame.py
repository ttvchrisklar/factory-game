import pygame
import random

pygame.init()
# lists
rect_size = 50
row_spacing = 0
nextavalebelpress = 0
ore_pice_list = []
belt_list = []
drill_list = []
ore_list = []
key_timeout = {}
player_list = []
rectangles = []
unocupide_squers = []
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
width, height = 4000, 3000
screen_width, screen_height = 1800, 1000
visible_width = -0
visible_height = -0
go = False
bilding_selted = 1
nextactiontime = 1000


class gridclass:
    def __init__(self, x, y, height_width, is_ocupied, ocuide_by, id):
        self.rect = pygame.Rect(x, y, height_width, height_width)
        self.is_ocupied = is_ocupied
        self.ocuide_by = ocuide_by
        self.id = id
        self.has_bilding = False


class player:
    def __init__(self, pbox, speed):
        self.pbox = pbox  # box the player is in
        self.speed = speed


class ore:
    def __init__(self, location, oretype):
        self.location = location
        self.oretype = oretype
        self.dir = 0

class drill:
    def __init__(self, location, oretype, dir):
        self.location = location
        self.oretype = oretype
        self.dir = dir
        self.miningspeed = 1
        return
    
    def generateore(self,pos):
        if self.dir == 0:
            if rectangles[pos + grid_width].ocuide_by == "BELT": 
                createorepice(pos + grid_width, self.oretype)           
                return
        if self.dir == 90:
            if rectangles[pos + 1].ocuide_by == "BELT": 
                createorepice(pos + 1, self.oretype)           
                return
        if self.dir == 180:
            if rectangles[pos - grid_width].ocuide_by == "BELT": 
                createorepice(pos - grid_width, self.oretype)           
                return
        if self.dir == 270:
            if rectangles[pos - 1].ocuide_by == "BELT": 
                createorepice(pos - 1, self.oretype)           
                return
class belt:
    def __init__(self, location, dir):
        self.location = location
        self.carying = []
        self.dir = dir
    
    def pushitem(self,pos):
        for bs in belt_list:
            if bs.location == bs.direction(pos):
                print("print true")
    def direction(self,pos):
        if self.dir == 0:
            if rectangles[pos + grid_width].ocuide_by == "BELT":   
                return pos + grid_width
        if self.dir == 90:
            if rectangles[pos + 1].ocuide_by == "BELT":
                return pos + 1
        if self.dir == 180:
            if rectangles[pos - grid_width].ocuide_by == "BELT":
                return pos - grid_width
        if self.dir == 270:
            if rectangles[pos - 1].ocuide_by == "BELT":
                return pos - 1

class orepice:
    def __init__(self, location, type, dir):
        self.location = location
        self.type = type
        self.dir = dir


# Set up display
# screen = pygame.display.set_mode((screen_width, screen_height))
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
pygame.display.set_caption("Factory")
screensize = pygame.display.get_window_size()
print(screensize)
clock = pygame.time.Clock()


def cube_printer():
    io = False
    o = "GRASS"
    for row in range(height // (rect_size + row_spacing)):
        for col in range(width // (rect_size + row_spacing)):
            x = col * (rect_size + row_spacing)
            y = row * (rect_size + row_spacing)
            new_rec = gridclass(x, y, rect_size, io, o, len(rectangles))
            rectangles.append(new_rec)



def player_class_crator():
    new_player = player(find_center_square(), 250)
    player_list.append(new_player)
    bord_ocupation_updater("PLAYER", find_center_square())


def create_ore_block(pos,type):
    new_ore = ore(pos, type)
    ore_list.append(new_ore)
    bord_ocupation_updater(type.upper(), pos)

def createdrill(pos, oretype):
    newdrill = drill(pos,oretype,0)
    drill_list.append(newdrill)
    bord_ocupation_updater("DRILL", pos)

def createbelt(pos):
    newbelt = belt(pos,0)
    belt_list.append(newbelt)
    bord_ocupation_updater("BELT", pos)

def createorepice(pos,type):
    for belt in belt_list:
        if len(belt.carying) == 1:
            break
        if belt.location == pos:
            neworepice = orepice(pos,type,180)
            neworepice.dir = belt.dir
            pice = (type,len(ore_pice_list)+1)
            belt.carying.append(pice)
            ore_pice_list.append(neworepice)
            break


def getPressed(keys, key, timeout):
    global key_timeout

    if keys[key] == False:
        return False

    current_time = pygame.time.get_ticks()

    if key in key_timeout and key_timeout[key] > current_time:
        return False

    key_timeout[key] = current_time + timeout
    return True


def key_detection():
    global visible_width, visible_height, grid_width
    speed, ptomove, keys = player_list[0].speed, player_list[0].pbox, pygame.key.get_pressed()
    bilding_selector(keys)
    if keys[pygame.K_ESCAPE]:
        pygame.quit()
        quit()
    grid_width = len(rectangles) // (height // (rect_size + row_spacing))
    if getPressed(keys, pygame.K_w, speed):
        if rectangles[ptomove].rect.y == rectangles[0].rect.y:
            print("hit wall")
            # gameover()
            return
        if rectangles[ptomove - grid_width].ocuide_by == "GRASS":
            bord_ocupation_updater("GRASS", ptomove)
            player_list[0].pbox -= grid_width
            visible_height += rect_size + row_spacing
            ptomove = player_list[0].pbox
            bord_ocupation_updater("PLAYER", ptomove)

    if getPressed(keys, pygame.K_a, speed):
        if rectangles[ptomove].rect.x == rectangles[0].rect.x:
            print("hit wall")
            # gameover()
            return
        if rectangles[ptomove - 1].ocuide_by == "GRASS":
            bord_ocupation_updater("GRASS", ptomove)
            player_list[0].pbox -= 1
            visible_width += rect_size + row_spacing
            ptomove = player_list[0].pbox
            bord_ocupation_updater("PLAYER", ptomove)

    if getPressed(keys, pygame.K_s, speed):
        if rectangles[ptomove].rect.y == rectangles[len(rectangles) - 1].rect.y:
            print("hit wall")
            # gameover()
            return
        if rectangles[ptomove + grid_width].ocuide_by == "GRASS":
            bord_ocupation_updater("GRASS", ptomove)
            player_list[0].pbox += grid_width
            visible_height -= rect_size + row_spacing
            ptomove = player_list[0].pbox
            bord_ocupation_updater("PLAYER", ptomove)

    if getPressed(keys, pygame.K_d, speed):
        if rectangles[ptomove].rect.x == rectangles[len(rectangles) - 1].rect.x:
            print("hit wall")
            return
        if rectangles[ptomove + 1].ocuide_by == "GRASS":
            bord_ocupation_updater("GRASS", ptomove)
            player_list[0].pbox += 1
            visible_width -= rect_size + row_spacing
            ptomove = player_list[0].pbox
            bord_ocupation_updater("PLAYER", ptomove)

def squer_ocupation_checer():
    global unocupide_squers
    unocupide_squers = []
    for i in range(len(rectangles)):
        if rectangles[i].ocuide_by == "GRASS":
            unocupide_squers.append(i)

def bord_ocupation_updater(type, location):
    rectangles[int(location)].is_ocupied = True
    rectangles[int(location)].ocuide_by = type
    squer_ocupation_checer()

def painter(image_name,type,scale):
    image_path = "C:/Users/chris/Desktop/all_files/coding/python/factorygame/images/"
    image = pygame.image.load(image_path + image_name)
    if type == rectangles:
        for im in type:
            image = pygame.transform.scale(image, (im.rect.width, im.rect.height))
            screen.blit(image, (im.rect.x + visible_width, im.rect.y + visible_height))
        return
    elif type != player_list and type != ore_pice_list:
        for im in type:
            if im.location is not None:
                im_rect = rectangles[im.location].rect
                scaled_image = pygame.transform.scale(image, (im_rect.width // scale, im_rect.height // scale))
                rotated_image = pygame.transform.rotate(scaled_image,im.dir)
                screen.blit(rotated_image, (im_rect.x + visible_width, im_rect.y + visible_height))
        return
    if type == player_list:
        for im in type:
            image = pygame.transform.scale(image, (rectangles[im.pbox].rect.width, rectangles[im.pbox].rect.height))
            screen.blit(image, (rectangles[im.pbox].rect.x + visible_width, rectangles[im.pbox].rect.y + visible_height))
        return
    if type == ore_pice_list:
        for im in type:
            if im.location is not None:
                im_rect = rectangles[im.location].rect
                scaled_image = pygame.transform.scale(image, (im_rect.width // scale, im_rect.height // scale))
                rotated_image = pygame.transform.rotate(scaled_image,im.dir)
                screen.blit(rotated_image, (im_rect.x + visible_width + (im_rect.width // scale)/3, im_rect.y + visible_height + (im_rect.height // scale)/3))
        return

def bord_painter():
    painter("grass.png",rectangles,1)
    painter("player.png",player_list,1)
    painter("copper.png",ore_list,1)
    painter("drill.png",drill_list,1)
    painter("belt.png",belt_list,1)
    painter("copper_ore.png",ore_pice_list,1.5)

def randomsquer():
    if not unocupide_squers:
        print("Error: No unoccupied squares available")
        return -1  # or any other value indicating error
    else:
        return random.choice(unocupide_squers)

def find_center_square():
    screen_center_x = screensize[0] // 2
    screen_center_y = screensize[1] // 2
    for square in rectangles:
        if square.rect.collidepoint(screen_center_x, screen_center_y):
            return square.id-1
    return None

def bilding_selector(keys):
    global bilding_selted
    if keys[pygame.K_1]:
        bilding_selted = 1
        return
    if keys[pygame.K_2]:
        bilding_selted = 2
        return

def set_camra():
    global visible_width, visible_height
    visible_width = 0
    visible_height = 0

def game_start():
    global player_list, rectangles, go
    go = False
    player_list = []
    rectangles = []
    cube_printer()
    squer_ocupation_checer()
    player_class_crator()
    create_ore_block(731,"COPPER_ORE_BLOCK")
    set_camra()
    squer_ocupation_checer()

def rotate_building(square, type):
    for ro in type:
        if ro.location == square.id:
            ro.dir += 90
            if ro.dir == 360:
                ro.dir = 0
                return
            break
def mouse_click_ditector(ev):
    # Adjust mouse position for visible_width and visible_height
    mouse_adjusted = (ev.pos[0] - visible_width, ev.pos[1] - visible_height)
    bildeblepos, rotateteble = ["COPPER_ORE_BLOCK","GRASS"], ["DRILL","BELT"]
    if ev.button == 1:
        for square in rectangles:
            if square.rect.collidepoint(mouse_adjusted) and square.ocuide_by in bildeblepos:
                square.has_bilding = True
                if bilding_selted == 1 and square.ocuide_by != "GRASS":
                    createdrill(square.id,"COPPER_ORE_BLOCK")
                    break
                if bilding_selted == 2 and square.ocuide_by == "GRASS":
                    createbelt(square.id)
                    break
            if square.rect.collidepoint(mouse_adjusted) and square.ocuide_by in rotateteble:
                if square.ocuide_by == "DRILL":
                    rotate_building(square, drill_list)
                    break
                if square.ocuide_by == "BELT":
                    rotate_building(square, belt_list)
                    break

    if ev.button == 2:
        for square in rectangles:
            if square.rect.collidepoint(mouse_adjusted):
                print(square.id)
                create_ore_block(square.id)
    if ev.button == 3:
        for square in rectangles:
            if square.rect.collidepoint(mouse_adjusted) and square.ocuide_by in rotateteble:
                square.has_bilding = False
                if square.ocuide_by == "DRILL":
                    i=0
                    for i in range(len(drill_list)):
                        if drill_list[i-1].location == square.id:
                            bord_ocupation_updater("COPPER_ORE_BLOCK", square.id)
                            drill_list.pop(i-1)
                if square.ocuide_by == "BELT":
                    i=0
                    for i in range(len(belt_list)):
                        if belt_list[i-1].location == square.id:
                            bord_ocupation_updater("GRASS", square.id)
                            belt_list.pop(i-1)

def bilding_action():
    global nextactiontime
    current_time = pygame.time.get_ticks()  # Get the current time
    if current_time >= nextactiontime:
        nextactiontime += 1000  # Increment next action time by 1000 milliseconds
        for drill in drill_list:
            drill.generateore(drill.location)
        for belt in belt_list:
            belt.pushitem(belt.location)

# Main game loop
def game_loop():
    game_start()
    while True:
        global ev, mouse, time
        time = pygame.time.get_ticks()
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                quit()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                mouse_click_ditector(ev)
                            
        # Clear the screen
        screen.fill((30, 30, 30))

        bilding_action()
        key_detection()
        bord_painter()
        # Draw rectangles from the list
        # Update the display
        pygame.display.flip()

game_loop()

