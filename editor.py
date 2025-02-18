import pygame
import pickle
import threading

# Load grid data
def load_data():
    name = input("Please enter file path: ")
    try:
        with open(name, "rb") as f:
            return pickle.load(f), name
    except Exception as e:
        print("file not found: ", e)
        return None, None

data, name = load_data()
if data is None:
    exit()

GRID_SIZE = (len(data), len(data[0])) 
CELL_SIZE = 50
# Grid settings
def resize(CELL_SIZE):
    return round(CELL_SIZE // 2.5), (min(800, GRID_SIZE[0] * CELL_SIZE), min(600, GRID_SIZE[1] * CELL_SIZE))

FONT_SIZE, SCREEN_SIZE = resize(CELL_SIZE)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE, pygame.DOUBLEBUF | pygame.HWSURFACE)
font = pygame.font.Font(None, FONT_SIZE)
running = True
selected = [0, 0]  # Currently selected cell
clock = pygame.time.Clock()

# Camera settings
offset_x, offset_y = 0, 0
zoom = 1.0

def get_scaled_value(value):
    return int(value * zoom)

def get_scaled_rect(x, y, size):
    return pygame.Rect(get_scaled_value(x) + offset_x, get_scaled_value(y) + offset_y, get_scaled_value(size), get_scaled_value(size))

# Cache loaded sprites
sprite_cache = {}

def get_sprite(path):
    if path and path not in sprite_cache:
        sprite_cache[path] = pygame.image.load(path).convert_alpha()
    return sprite_cache.get(path)

# Input prompt state
input_active = False
input_text = ""
prompt_type = None  # 'name' or 'sprite'

# Threaded input handling
def handle_input():
    global running, selected, input_active, input_text, prompt_type, offset_x, offset_y, zoom
    while running:
        event = pygame.event.wait()
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if input_active:
                if event.key == pygame.K_RETURN:
                    if prompt_type == 'name':
                        data[selected[1]][selected[0]][0] = input_text
                    elif prompt_type == 'sprite':
                        data[selected[1]][selected[0]][2] = input_text if input_text else None
                    input_active = False
                    input_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode
            else:
                if event.key == pygame.K_LEFT:
                    selected[0] = max(0, selected[0] - 1)
                elif event.key == pygame.K_RIGHT:
                    selected[0] = min(GRID_SIZE[0] - 1, selected[0] + 1)
                elif event.key == pygame.K_UP:
                    selected[1] = max(0, selected[1] - 1)
                elif event.key == pygame.K_DOWN:
                    selected[1] = min(GRID_SIZE[1] - 1, selected[1] + 1)
                elif event.key == pygame.K_e:
                    input_active = True
                    input_text = ""
                    prompt_type = 'name'
                elif event.key == pygame.K_r:
                    data[selected[1]][selected[0]] = ["Air", 2, None, 0, True, False]
                elif event.key == pygame.K_s:
                    input_active = True
                    input_text = ""
                    prompt_type = 'sprite'
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                mx, my = pygame.mouse.get_pos()
                selected[0] = (mx - offset_x) // get_scaled_value(CELL_SIZE)
                selected[1] = (my - offset_y) // get_scaled_value(CELL_SIZE)
            elif event.button == 4:  # Scroll up
                zoom *= 1.1
            elif event.button == 5:  # Scroll down
                zoom *= 0.9
        elif event.type == pygame.MOUSEMOTION:
            if pygame.mouse.get_pressed()[2]:  # Right click and drag
                offset_x += event.rel[0]
                offset_y += event.rel[1]

# Start input handling thread
input_thread = threading.Thread(target=handle_input, daemon=True)
input_thread.start()

# Main loop
while running:
    screen.fill(WHITE)
    
    for y in range(GRID_SIZE[1]):
        for x in range(GRID_SIZE[0]):
            rect = get_scaled_rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, BLACK, rect, 2)
            
            if data[y][x][2] is not None:
                sprite = get_sprite(data[y][x][2])
                if sprite:
                    sprite = pygame.transform.scale(sprite, (get_scaled_value(CELL_SIZE - 10), get_scaled_value(CELL_SIZE - 10)))
                    screen.blit(sprite, (rect.x + 5, rect.y + 5))
            else:
                text = font.render(data[y][x][0], True, BLACK)
                screen.blit(text, (rect.x + 5, rect.y + 5))
    
    pygame.draw.rect(screen, BLUE, get_scaled_rect(selected[0] * CELL_SIZE, selected[1] * CELL_SIZE, CELL_SIZE), 3)
    
    if input_active:
        prompt_surface = pygame.Surface((SCREEN_SIZE[0], 30))
        prompt_surface.fill(GRAY)
        prompt_text = font.render(f"Enter {prompt_type}: {input_text}", True, BLACK)
        prompt_surface.blit(prompt_text, (5, 5))
        screen.blit(prompt_surface, (0, SCREEN_SIZE[1] - 30))
    
    pygame.display.flip()
    clock.tick(60)  # Cap the frame rate

with open(name, "wb") as f:
    pickle.dump(data, f)

pygame.quit()
