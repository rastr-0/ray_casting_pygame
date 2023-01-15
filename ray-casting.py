#packages
import pygame
import sys
import math

#global constants
SCREEN_HEIGHT = 480
SCREEN_WIDTH = SCREEN_HEIGHT * 2
MAP_SIZE = 8
TILE_SIZE = int((SCREEN_WIDTH / 2) / MAP_SIZE)
FOV = math.pi / 3
HALF_FOV = FOV / 2
CASTED_RAYS = 400
STEP_ANGLE = FOV / CASTED_RAYS
MAX_DEPTH = int(MAP_SIZE * TILE_SIZE)
#global variables
player_x = (SCREEN_WIDTH / 2) / 2
player_y = (SCREEN_WIDTH / 2) / 2
player_angle = math.pi

#map
MAP = (
    '########'
    '# #    #'
    '# #  ###'
    '#      #'
    '##     #'
    '#  ### #'
    '#   #  #'
    '########'
)

#init pygame
pygame.init()

#game window
win = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Ray-casting')

#init timer
clock = pygame.time.Clock()

def draw_map():
    #iterate over map
    for i in range(MAP_SIZE):
        for j in range(MAP_SIZE):
            #calculate square index
            square = i * MAP_SIZE + j

            #draw map
            pygame.draw.rect(
                win, (191, 191, 191) if MAP[square] == '#' else (65, 65, 65),
                (j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE - 1, TILE_SIZE - 1)
            )

    #draw player
    pygame.draw.circle(win, (162, 0, 255), (int(player_x), int(player_y)), 12)

    #player direction
    pygame.draw.line(win, (233, 166, 49), (player_x, player_y), 
                                (player_x - math.sin(player_angle) * 50, 
                                player_y + math.cos(player_angle) * 50), 3)
    
    #player FOV
    pygame.draw.line(win,(233, 166, 49), (player_x, player_y), 
                                (player_x - math.sin(player_angle - HALF_FOV) * 50, 
                                player_y + math.cos(player_angle - HALF_FOV) * 50), 3)

    pygame.draw.line(win, (233, 166, 49), (player_x, player_y), 
                                (player_x - math.sin(player_angle + HALF_FOV) * 50, 
                                player_y + math.cos(player_angle + HALF_FOV) * 50), 3)

#ray-casting algorithm
def ray_casting():
    #left angle of FOV
    start_angle = player_angle - HALF_FOV
    
    #iterate over casted rays
    for ray in range(CASTED_RAYS):
        for depth in range(MAX_DEPTH):
            #get ray target coordinates
            target_x = player_x - math.sin(start_angle) * depth
            target_y = player_y +  math.cos(start_angle) * depth

            #convert target 'x', 'y' coordinates to map col, row
            col = int(target_x / TILE_SIZE)
            row = int(target_y / TILE_SIZE)  

            #calculate map square index
            square = row * MAP_SIZE + col
            
            #print(square)

            if MAP[square] == '#':
                pygame.draw.rect(win, (195, 137, 38), (col * TILE_SIZE,
                                                                        row * TILE_SIZE,
                                                                        TILE_SIZE - 1,
                                                                        TILE_SIZE - 1))
                
                #draw casted ray
                pygame.draw.line(win, (233, 166, 49), (player_x, player_y), (target_x, target_y))
                
                break

        #increment angle by step
        start_angle += STEP_ANGLE

#game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
    
    #update background
    pygame.draw.rect(win, (0, 0, 0), (0, 0, SCREEN_HEIGHT, SCREEN_HEIGHT))

    draw_map()
    ray_casting()

    #get user input
    keys = pygame.key.get_pressed()

    #handle user input
    if keys[pygame.K_LEFT]:
        #working with radians, not degrees
        player_angle -= 0.1
    elif keys[pygame.K_RIGHT]:
        player_angle += 0.1
    elif keys[pygame.K_UP]:
        player_x += -1 * math.sin(player_angle) * 5
        player_y += math.cos(player_angle) * 5
    elif keys[pygame.K_DOWN]:
        player_x -= -1 * math.sin(player_angle) * 5
        player_y -= math.cos(player_angle) * 5

    #update display
    pygame.display.flip()

    #set FPS
    clock.tick(30)
