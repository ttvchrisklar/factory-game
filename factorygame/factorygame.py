import pygame
import random

pygame.init()
# lists
rect_size = 50
row_spacing = 0
nextavalebelpress = 0
beltlist = []
drilllist = []
orelist = []
wallplacelist = []
key_timeout = {}
playerlist = []
rectangles = []
foodlist = []
walllist = []
unocupidesquers = []
portallist = []
white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)
width, height = 4000, 3000
screenwidth, screenheight = 1800, 1000
visible_width = -0
visible_height = -0
go = False
bildingselted = 1


class gridclass:
    def __init__(self, x, y, heightwidth, isocupied, ocuideby, id):
        self.rect = pygame.Rect(x, y, heightwidth, heightwidth)
        self.isocupied = isocupied
        self.ocuideby = ocuideby
        self.id = id
        self.has_bilding = False


class player:
    def __init__(self, pbox, speed):
        self.pbox = pbox  # box the player is in
        self.speed = speed


class ore:
    def __init__(self, location, oretype, amaount, nextto):
        self.location = location
        self.oretype = oretype
        self.amaount = amaount
        self.nextto = nextto
        self.dir = 0

class drill:
    def __init__(self, location, oretype, dir):
        self.location = location
        self.oretype = oretype
        self.dir = dir
        self.miningspeed = 1
class belt:
    def __init__(self, location, dir):
        self.location = location
        self.carying = []
        self.dir = dir



# Set up display
screen = pygame.display.set_mode((screenwidth, screenheight))
# screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
pygame.display.set_caption("Factory")
screensize = pygame.display.get_window_size()
print(screensize)
clock = pygame.time.Clock()


def cubeprinter():
    io = False
    o = "GRASS"
    for row in range(height // (rect_size + row_spacing)):
        for col in range(width // (rect_size + row_spacing)):
            x = col * (rect_size + row_spacing)
            y = row * (rect_size + row_spacing)
            wh = rect_size
            i = len(rectangles)
            newrec = gridclass(x, y, wh, io, o, i)
            rectangles.append(newrec)
    bordpaternmaker()


def playerclasscrator():
    posision = find_center_square()
    speed = 250
    newplayer = player(posision, speed)
    playerlist.append(newplayer)
    bordocupationupdater("PLAYER", posision)


def createoreblock(pos):
    newore = ore(pos, "Copper", random.randint(100, 1000), [])
    orelist.append(newore)
    bordocupationupdater("COPPER", pos)

def createdrill(pos, oretype):
    newdrill = drill(pos,oretype,0)
    drilllist.append(newdrill)
    bordocupationupdater("DRILL", pos)

def createbelt(pos):
    newbelt = belt(pos,0)
    beltlist.append(newbelt)
    bordocupationupdater("BELT", pos)


def getPressed(keys, key, timeout):
    global key_timeout

    if keys[key] == False:
        return False

    current_time = pygame.time.get_ticks()

    if key in key_timeout and key_timeout[key] > current_time:
        return False

    key_timeout[key] = current_time + timeout
    return True


def keydetection():
    global visible_width, visible_height
    speed, ptomove, keys = playerlist[0].speed, playerlist[0].pbox, pygame.key.get_pressed()
    bildingselector(keys)
    if keys[pygame.K_ESCAPE]:
        pygame.quit()
        quit()
    grid_width = len(rectangles) // (height // (rect_size + row_spacing))
    if getPressed(keys, pygame.K_w, speed):
        if rectangles[ptomove].rect.y == rectangles[0].rect.y:
            print("hit wall")
            # gameover()
            return
        if rectangles[ptomove - grid_width].ocuideby == "GRASS":
            bordocupationupdater("GRASS", ptomove)
            playerlist[0].pbox -= grid_width
            visible_height += rect_size + row_spacing
            ptomove = playerlist[0].pbox
            bordocupationupdater("PLAYER", ptomove)

    if getPressed(keys, pygame.K_a, speed):
        if rectangles[ptomove].rect.x == rectangles[0].rect.x:
            print("hit wall")
            # gameover()
            return
        if rectangles[ptomove - 1].ocuideby == "GRASS":
            bordocupationupdater("GRASS", ptomove)
            playerlist[0].pbox -= 1
            visible_width += rect_size + row_spacing
            ptomove = playerlist[0].pbox
            bordocupationupdater("PLAYER", ptomove)

    if getPressed(keys, pygame.K_s, speed):
        if rectangles[ptomove].rect.y == rectangles[len(rectangles) - 1].rect.y:
            print("hit wall")
            # gameover()
            return
        if rectangles[ptomove + grid_width].ocuideby == "GRASS":
            bordocupationupdater("GRASS", ptomove)
            playerlist[0].pbox += grid_width
            visible_height -= rect_size + row_spacing
            ptomove = playerlist[0].pbox
            bordocupationupdater("PLAYER", ptomove)

    if getPressed(keys, pygame.K_d, speed):
        if rectangles[ptomove].rect.x == rectangles[len(rectangles) - 1].rect.x:
            print("hit wall")
            return
        if rectangles[ptomove + 1].ocuideby == "GRASS":
            bordocupationupdater("GRASS", ptomove)
            playerlist[0].pbox += 1
            visible_width -= rect_size + row_spacing
            ptomove = playerlist[0].pbox
            bordocupationupdater("PLAYER", ptomove)




def squerdocupationchecer():
    global unocupidesquers
    unocupidesquers = []
    for i in range(len(rectangles)):
        if rectangles[i].ocuideby == "GRASS":
            unocupidesquers.append(i)


def bordocupationupdater(type, location):
    rectangles[int(location)].isocupied = True
    rectangles[int(location)].ocuideby = type
    squerdocupationchecer()


def bordpaternmaker():
    patern = 0
    for i in range(len(rectangles)):
        if patern == 0:
            rectangles[i].color = (25, 100, 0)
            patern = 1
        else:
            rectangles[i].color = (50, 100, 0)
            patern = 0

def painter(image_name,type,scale):
    image_path = "C:/Users/chris/Desktop/all_files/coding/python/factorygame/images/"
    image = pygame.image.load(image_path + image_name)
    if type == rectangles:
        for im in type:
            image = pygame.transform.scale(image, (im.rect.width, im.rect.height))
            screen.blit(image, (im.rect.x + visible_width, im.rect.y + visible_height))
        return
    if type == playerlist:
        for im in type:
            image = pygame.transform.scale(image, (rectangles[im.pbox].rect.width, rectangles[im.pbox].rect.height))
            screen.blit(image, (rectangles[im.pbox].rect.x + visible_width, rectangles[im.pbox].rect.y + visible_height))
        return
    elif type != playerlist:
        for im in type:
            if im.location is not None:
                im_rect = rectangles[im.location].rect
                scaled_image = pygame.transform.scale(image, (im_rect.width // scale, im_rect.height // scale))
                rotated_image = pygame.transform.rotate(scaled_image,im.dir)
                screen.blit(rotated_image, (im_rect.x + visible_width, im_rect.y + visible_height))
        return

def bordpainter():
    painter("grass.png",rectangles,1)
    painter("player.png",playerlist,1)
    painter("copper.png",orelist,1)
    painter("drill.png",drilllist,1)
    painter("belt.png",beltlist,1)


def randomsquer():
    if not unocupidesquers:
        print("Error: No unoccupied squares available")
        return -1  # or any other value indicating error
    else:
        return random.choice(unocupidesquers)


def find_center_square():
    screen_center_x = screensize[0] // 2
    screen_center_y = screensize[1] // 2
    for square in rectangles:
        if square.rect.collidepoint(screen_center_x, screen_center_y):
            return square.id-1
    return None

def bildingselector(keys):
    global bildingselted
    if keys[pygame.K_1]:
        bildingselted = 1
        return
    if keys[pygame.K_2]:
        bildingselted = 2
        return

def setcamra():
    global visible_width, visible_height
    visible_width = 0
    visible_height = 0


def gamestart():
    global playerlist, rectangles, portallist, walllist, go
    go = False
    playerlist = []
    rectangles = []
    portallist = []
    walllist = []
    cubeprinter()
    squerdocupationchecer()
    playerclasscrator()
    createoreblock(731)
    setcamra()
    squerdocupationchecer()

def rotatebuilding(square, type):
    for ro in type:
        if ro.location == square.id:
            ro.dir += 90
            break



def mouseclickditector(ev):
    # Adjust mouse position for visible_width and visible_height
    mouse_adjusted = (ev.pos[0] - visible_width, ev.pos[1] - visible_height)
    bildeblepos, rotateteble = ["COPPER","GRASS"], ["DRILL","BELT"]
    if ev.button == 1:
        for square in rectangles:
            if square.rect.collidepoint(mouse_adjusted) and square.ocuideby in bildeblepos:
                square.has_bilding = True
                if bildingselted == 1 and square.ocuideby != "GRASS":
                    createdrill(square.id,"COPPER")
                    break
                if bildingselted == 2 and square.ocuideby == "GRASS":
                    createbelt(square.id)
                    break
            if square.rect.collidepoint(mouse_adjusted) and square.ocuideby in rotateteble:
                if square.ocuideby == "DRILL":
                    rotatebuilding(square, drilllist)
                    break
                if square.ocuideby == "BELT":
                    rotatebuilding(square, beltlist)
                    break

    if ev.button == 2:
        for square in rectangles:
            if square.rect.collidepoint(mouse_adjusted):
                print(square.id)
                createoreblock(square.id)
    if ev.button == 3:
        for square in rectangles:
            if square.rect.collidepoint(mouse_adjusted) and square.ocuideby in rotateteble:
                square.has_bilding = False
                if square.ocuideby == "DRILL":
                    i=0
                    for i in range(len(drilllist)):
                        if drilllist[i-1].location == square.id:
                            bordocupationupdater("COPPER", square.id)
                            drilllist.pop(i-1)
                if square.ocuideby == "BELT":
                    i=0
                    for i in range(len(beltlist)):
                        if beltlist[i-1].location == square.id:
                            bordocupationupdater("GRASS", square.id)
                            beltlist.pop(i-1)
# Main game loop
def gameloop():
    gamestart()
    while True:
        global ev, mouse
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                quit()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                mouseclickditector(ev)
                            
        # Clear the screen
        screen.fill((30, 30, 30))
        # superimposing the text onto our button
        if go:
            mouse = pygame.mouse.get_pos()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                if screenwidth / 2 <= mouse[0] <= screenwidth / 2 + 140 and screenheight / 2 <= mouse[1] <= screenheight / 2 + 40:
                    gamestart()
            keydetection()
        else:
            keydetection()
            bordpainter()
        # Draw rectangles from the list
        # Update the display
        pygame.display.flip()

gameloop()

