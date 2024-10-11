import pygame
import numpy as np


pygame.init()

width, height = 400, 300
cell_size = 3
window_size = (width * cell_size, height * cell_size)

# Ant movement and rotation
directional_shifts = {
    'n': (0, -1),
    's': (0, 1),
    'w': (-1, 0),
    'e': (1, 0)
}
l_rots = {
    'n': 'w',
    'w': 's',
    's': 'e',
    'e': 'n'
}
r_rots = {
    'n': 'e',
    'e': 's',
    's': 'w',
    'w': 'n'
}
rot_dirs = {
    1: r_rots,
    0: l_rots
}

# Ant state
ant_direction = 'n'
ant_coords = [width // 2, height // 2]

# World
# world = [[1 for x in range(width)] for y in range(height)]
world = np.ones((width, height), dtype=int)

# Screen
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption(f"Langton's Ant: {width}x{height} cells")
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)


# Update
def update_world():
    global ant_direction, ant_coords, world
    # 1. Given the color of ant's current cell - find rotation direction
    ant_x = ant_coords[0]
    ant_y = ant_coords[1]
    ants_cell_val = world[ant_x, ant_y]
    rotation = rot_dirs[ants_cell_val]
    # 2. Rotate
    ant_direction = rotation[ant_direction]
    # 3. Change color of current cell
    world[ant_x, ant_y] = 1 - ants_cell_val
    # 4. Take a step in the direction
    ant_shift = directional_shifts[ant_direction]
    ant_coords[0] += ant_shift[0]
    ant_coords[1] += ant_shift[1]
    # 5. (optional) Prevent out of bounds: %
    ant_coords[0] %= width
    ant_coords[1] %= height
    

# Draw
def draw_world(world):
    for x in range(width):
        for y in range(height):
            if not world[x, y]:
                pygame.draw.rect(screen, BLACK, (x * cell_size, y * cell_size, cell_size, cell_size))

# Main loop
running = True
clock = pygame.time.Clock()
ticks = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            continue
    
    # Update
    update_world()

    # Draw
    screen.fill(WHITE)
    draw_world(world)
    pygame.display.flip()

    # Tick
    clock.tick(0)
    ticks += 1
    
    if ticks % 10 == 0:
        pygame.display.set_caption(f"Langton's Ant: {width}x{height} cells, {ticks} ticks")


# Quit
pygame.quit()

