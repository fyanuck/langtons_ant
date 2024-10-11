import pygame
import numpy as np
from pprint import pprint


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

# Ant's trace
trace_max_len = 128  # Let the max len be 256
trace_points = []
trace_base_color = (255, 0, 0)  # RED
trace_final_color = (255, 128, 128)   # The color of the last element of the trace

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (128, 128, 128)

trace_points_colors = []  # Starting with more intense, ending with white-ish


R_diff = trace_final_color[0] - trace_base_color[0]
G_diff = trace_final_color[1] - trace_base_color[1]
B_diff = trace_final_color[2] - trace_base_color[2]

# How much should each consecutive trace point color change
R_step = R_diff / trace_max_len
G_step = G_diff / trace_max_len
B_step = B_diff / trace_max_len

R_temp, G_temp, B_temp = trace_base_color
for p in range(trace_max_len-1, -1, -1):
        R_temp += R_step
        G_temp += G_step
        B_temp += B_step
        trace_points_colors.append((int(R_temp), int(G_temp), int(B_temp)))


# World
world = np.ones((width, height), dtype=int)

# Screen
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption(f"Langton's Ant: {width}x{height} cells")



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
    # 6. Update trace
    update_trace(ant_coords)


# Update trace
def update_trace(new_coords):
    new_x, new_y = new_coords
    global trace_points
    trace_points = [(new_x, new_y)] + trace_points[:trace_max_len]
    

# Draw
def draw_world(world):
    for x in range(width):
        for y in range(height):
            if not world[x, y]:
                pygame.draw.rect(screen, BLACK, (x * cell_size, y * cell_size, cell_size, cell_size))

# Draw trace
def draw_trace(world):
    for trace_point, point_color in zip(trace_points, trace_points_colors):
        x, y = trace_point
        pygame.draw.rect(screen, point_color, (x * cell_size, y * cell_size, cell_size, cell_size))


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
    draw_trace(world)
    pygame.display.flip()

    # Tick
    clock.tick(0)
    ticks += 1
    
    if ticks % 10 == 0:
        pygame.display.set_caption(f"Langton's Ant: {width}x{height} cells, {ticks} ticks")


# Quit
pygame.quit()

