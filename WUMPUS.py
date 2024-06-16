import pygame
import sys
import random

class KB_Agent:
    def __init__(self, environment_size, environment):
        self.environment_size = environment_size
        self.current_position = (0, 0)  # Starting position
        self.knowledge_base = {}  # Initialize an empty knowledge base
        self.gold_found = False
        self.environment = environment
        self.paths_to_gold = []
    
    def update_percepts(self, percepts):
        for percept in percepts:
            if percept == "stench":
                self.handle_stench()
            elif percept == "breeze":
                self.handle_breeze()
            elif percept == "GOLD":
                self.handle_glitter()

    def handle_stench(self):
        x, y = self.current_position
        adjacent_positions = self.get_adjacent_positions(x, y)
        for pos in adjacent_positions:
            if pos not in self.knowledge_base:
                self.knowledge_base[pos] = set()
            self.knowledge_base[pos].add("possible_wumpus")

    def handle_breeze(self):
        x, y = self.current_position
        adjacent_positions = self.get_adjacent_positions(x, y)
        for pos in adjacent_positions:
            if pos not in self.knowledge_base:
                self.knowledge_base[pos] = set()
            self.knowledge_base[pos].add("possible_pit")

    def handle_glitter(self):
        self.gold_found = True

    def get_adjacent_positions(self, x, y):
        positions = []
        if x > 0:
            positions.append((x - 1, y))
        if x < self.environment_size[0] - 1:
            positions.append((x + 1, y))
        if y > 0:
            positions.append((x, y - 1))
        if y < self.environment_size[1] - 1:
            positions.append((x, y + 1))
        return positions

    def is_safe(self, x, y):
        return "possible_wumpus" not in self.knowledge_base.get((x, y), set()) and "possible_pit" not in self.knowledge_base.get((x, y), set())

    def dfs(self, start_position):
        stack = [(start_position, [])]  # Each item in the stack is a tuple containing the position and the path taken so far
        visited = set()

        while stack:
            (x, y), path = stack.pop()  # Get the current position and path from the top of the stack
            self.current_position = (x, y)
            current_percepts = self.environment[x][y]
            self.update_percepts(current_percepts)
            
            if "GOLD" in current_percepts:
                self.handle_glitter()
                self.paths_to_gold.append(path + [(x, y)])  # Save the path to gold

            if (x, y) not in path:  # Avoid revisiting the same node in the current path
                new_path = path + [(x, y)]
                for direction, (dx, dy) in [("up", (0, 1)), ("down", (0, -1)), ("left", (-1, 0)), ("right", (1, 0))]:
                    next_position = (x + dx, y + dy)
                    if (
                        0 <= next_position[0] < self.environment_size[0] and
                        0 <= next_position[1] < self.environment_size[1] and
                        next_position not in new_path
                    ):
                        stack.append((next_position, new_path))
        # Filter out paths that pass through cells with "PIT" or "wumpus"
        valid_paths = []
        for path in self.paths_to_gold:
            valid = True
            for cell in path:
                if "PIT" in self.environment[cell[0]][cell[1]] or "wumpus" in self.environment[cell[0]][cell[1]]:
                    valid = False
                    break
            if valid:
                valid_paths.append(path)

        self.paths_to_gold = valid_paths
        return valid_paths

    def display_paths_to_gold(self):
        if not self.paths_to_gold:
            print("Gold not found!")
            return
        print("All Paths to Gold:")
        for path in self.paths_to_gold:
            print(" -> ".join(map(str, path)))
def generate_valid_environment(environment_size, agent_start_position):
    def is_valid(environment, agent_start_position):
        for x in range(environment_size[0]):
            for y in range(environment_size[1]):
                if (x, y) == agent_start_position:
                    if "PIT" in environment[x][y] or "wumpus" in environment[x][y]:
                        return False
                if "GOLD" in environment[x][y] and (x, y) == agent_start_position:
                    return False
                if "PIT" in environment[x][y] and "GOLD" in environment[x][y]:
                        return False
                if "GOLD" in environment[x][y] and "wumpus" in environment[x][y]:
                        return False
        return True
    
    while True:
        environment = generate_random_environment(environment_size)
        if is_valid(environment, agent_start_position):
            return environment

def generate_random_environment(environment_size):
    width, height = environment_size
    environment = [[[] for _ in range(width)] for _ in range(height)]
    
    # Define probabilities for elements
    pit_prob = 0.15
    wumpus_prob = 0.15
    gold_prob = 0.02
    
    # Place elements in the environment
    for y in range(height): 
        for x in range(width):
            if random.random() < pit_prob:
                environment[y][x] = ["PIT"]
            elif random.random() < wumpus_prob:
                environment[y][x] = ["wumpus"]
            elif random.random() < gold_prob:
                environment[y][x].append("GOLD")
    
    # Ensure there is at least one gold in the environment
    gold_positions = [(y, x) for y in range(height) for x in range(width) if "GOLD" in environment[y][x]]
    if not gold_positions:
        gold_x, gold_y = random.randint(0, width - 1), random.randint(0, height - 1)
        environment[gold_y][gold_x].append("GOLD")

    # Add percepts based on the elements
    for y in range(height):
        for x in range(width):
            if "wumpus" in environment[y][x]:
                for adj_y, adj_x in get_adjacent_positions(x, y, environment_size):
                    environment[adj_y][adj_x].append("stench")
            if "PIT" in environment[y][x]:
                for adj_y, adj_x in get_adjacent_positions(x, y, environment_size):
                    environment[adj_y][adj_x].append("breeze")
    return environment

def get_adjacent_positions(x, y, environment_size):
    width, height = environment_size
    positions = []
    if x > 0:
        positions.append((y, x - 1))
    if x < width - 1:
        positions.append((y, x + 1))
    if y > 0:
        positions.append((y - 1, x))
    if y < height - 1:
        positions.append((y + 1, x))
    return positions

def min_path(paths):
    if len(paths) == 0: return []
    min_index = 0
    for i,ele in enumerate(paths):
        if len(ele) < len(paths[min_index]):
            min_index = i
    return paths[min_index]

# Pygame visualization
def draw_grid(screen, agent, environment, cell_size, images):
    for y in range(len(environment)):
        for x in range(len(environment[y])):
            rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, (255, 255, 255), rect)  # White for empty cell
            pygame.draw.rect(screen, (0, 0, 0), rect, 1)  # Black border
            
            # Draw percepts
            percepts = environment[y][x]
            if "PIT" in percepts :  # Only show pit if not visited by agent
                pit_rect = images["pit"].get_rect(center=rect.center)
                screen.blit(images["pit"], pit_rect.topleft)
            elif "wumpus" in percepts :  # Only show wumpus if not visited by agent
                wumpus_rect = images["wumpus"].get_rect(center=rect.center)
                screen.blit(images["wumpus"], wumpus_rect.topleft)

            elif "GOLD" in percepts and "breeze" in percepts and "stench" in percepts:
                screen.blit(images["g_s_b"], rect.topleft)

            elif "stench" in percepts and "breeze" in percepts:
                screen.blit(images["b_s"], rect.topleft)
            elif "stench" in percepts and "GOLD" in percepts:
                screen.blit(images["g_s"], rect.topleft)
            elif "GOLD" in percepts and "breeze" in percepts:
                screen.blit(images["g_b"], rect.topleft)
            elif "GOLD" in percepts :
                screen.blit(images["GOLD"], rect.topleft)

            elif "stench" in percepts:
                screen.blit(images["stench"], rect.topleft)
            elif "stench" in percepts:
                screen.blit(images["stench"], rect.topleft)
            elif "breeze" in percepts:
                screen.blit(images["breeze"], rect.topleft)
            elif "agent" in percepts:
                agent_rect = images["agent"].get_rect(center=rect.center)
                screen.blit(images["agent"], agent_rect.topleft)

def main():
    pygame.init()
    cell_size = 100
    environment_size = (4, 4)
    agent_position = (0,0)
    screen_size = (environment_size[0] * cell_size, environment_size[1] * cell_size)
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("KB Agent Visualization")

    # Load and scale images
    wumpus_img = pygame.image.load("Wumpus/src/wumpus.jpeg")
    agent_img = pygame.image.load("Wumpus/src/agent.jpeg")
    g_s_b_img = pygame.image.load("Wumpus/src/G_S_B.jpeg")
    pit_img = pygame.image.load("Wumpus/src/pit.jpeg")
    stench_img = pygame.image.load("Wumpus/src/stench.jpeg")
    breeze_img = pygame.image.load("Wumpus/src/breeze.jpeg")
    b_s_img = pygame.image.load("Wumpus/src/b_s.jpeg")
    g_s_img = pygame.image.load("Wumpus/src/g_s.jpeg")
    g_b_img = pygame.image.load("Wumpus/src/g_b.jpeg")
    gold_img = pygame.image.load("Wumpus/src/GOLD.jpeg")

    images = {
        "wumpus": pygame.transform.scale(wumpus_img, (cell_size // 2, cell_size // 2)),  # Smaller Wumpus image
        "agent": pygame.transform.scale(agent_img, (cell_size // 2, cell_size // 2)),
        "g_s_b": pygame.transform.scale(g_s_b_img, (cell_size, cell_size)),
        "pit": pygame.transform.scale(pit_img, (cell_size // 2, cell_size // 2)),  # Smaller pit image
        "stench": pygame.transform.scale(stench_img, (cell_size, cell_size)),
        "breeze": pygame.transform.scale(breeze_img, (cell_size, cell_size)),
        "b_s": pygame.transform.scale(b_s_img, (cell_size, cell_size)),
        "g_s": pygame.transform.scale(g_s_img, (cell_size, cell_size)),
        "g_b": pygame.transform.scale(g_b_img, (cell_size, cell_size)),
        "GOLD": pygame.transform.scale(gold_img, (cell_size, cell_size))

    }

    environment = [
        [["stench"], ["    "],                     ["breeze"], ["PIT"]],
        [["wumpus"], ["stench", "breeze", "GOLD"], ["PIT"],    ["breeze"]],
        [["stench"], ["    "],                     ["breeze"], ["    "]],
        [["    "],   ["breeze"],                   ["PIT"],    ["breeze"]]
    ]
    # environment[agent_position[0]][agent_position[1]] = ["agent"]
    environment = generate_valid_environment(environment_size,agent_position)
    agent = KB_Agent(environment_size=environment_size, environment=environment)

    running = True
    clock = pygame.time.Clock()
    paths = agent.dfs(agent_position)
    path = min_path(paths)
    print(path)
    for ele in environment:
        print(ele)
    prev = []
    i = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        if i < len(path):
            
            print(f"path i : {path[i]} , {environment[path[i][0]][path[i][1]]}")
            if i>=1:
                environment[path[i-1][0]][path[i-1][1]] = prev
                pass
            prev = environment[path[i][0]][path[i][1]]
            environment[path[i][0]][path[i][1]] = ["agent"]  # Corrected the indexing
            i += 1
        
        screen.fill((255, 255, 255))
        draw_grid(screen, agent, environment, cell_size, images)
        pygame.display.flip()
        clock.tick(1)  # Slow down the updates for visibility

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
