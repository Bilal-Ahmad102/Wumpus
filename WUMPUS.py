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
            current_percepts = self.environment[y][x]
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

# Testing the implementation
environment = [
    [["stench"], ["    "],                     ["breeze"], ["PIT"]],
    [["wumpus"], ["stench", "breeze", "GOLD"], ["PIT"],    ["breeze"]],
    [["stench"], ["    "],                     ["breeze"], ["    "]],
    [["    "],   ["breeze"],                   ["PIT"],    ["breeze"]]
]

agent = KB_Agent(environment_size=(4, 4), environment=environment)
paths = agent.dfs((1, 3))  # Start from (0, 0)
print(paths)

# agent.display_paths_to_gold()
