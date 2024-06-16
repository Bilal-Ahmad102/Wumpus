# KB Agent Visualization README

## Table of Contents
1. [Introduction](#introduction)
2. [Requirements](#requirements)
3. [Setup and Installation](#setup-and-installation)
4. [Usage](#usage)
5. [Project Structure](#project-structure)
6. [Key Components](#key-components)
7. [Generating a Valid Environment](#generating-a-valid-environment)
8. [Visualization with Pygame](#visualization-with-pygame)
9. [Screenshots](#screenshots)
10. [Conclusion](#conclusion)

## Introduction
This project implements a knowledge-based (KB) agent that explores a grid environment to find gold while avoiding pits and a Wumpus. The agent uses percepts like stench (near Wumpus), breeze (near pit), and glitter (gold) to update its knowledge base and make decisions. The environment and agent's movements are visualized using Pygame.

## Requirements
- Python 3.x
- Pygame library

## Setup and Installation

1. **Clone the Repository**
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2. **Install Dependencies**
    ```bash
    pip install pygame
    ```

3. **Ensure Required Images are in Place**
    Place the following images in the `Wumpus/src/` directory:
    - `wumpus.jpeg`
    - `agent.jpeg`
    - `G_S_B.jpeg`
    - `pit.jpeg`
    - `stench.jpeg`
    - `breeze.jpeg`
    - `b_s.jpeg`
    - `g_s.jpeg`
    - `g_b.jpeg`
    - `GOLD.jpeg`

## Usage
To run the KB Agent visualization, execute the following command:
```bash
python <script_name>.py
```

## Project Structure
- **main.py**: The main script containing the KB Agent logic and Pygame visualization.
- **Wumpus/src/**: Directory containing the image assets used for visualization.

## Key Components

### KB_Agent Class
- **`__init__(self, environment_size, environment)`**: Initializes the agent with the environment size and grid.
- **`update_percepts(self, percepts)`**: Updates the knowledge base based on percepts (stench, breeze, glitter).
- **`handle_stench(self)`**: Handles stench percepts by marking adjacent cells as possible Wumpus locations.
- **`handle_breeze(self)`**: Handles breeze percepts by marking adjacent cells as possible pit locations.
- **`handle_glitter(self)`**: Handles glitter percepts indicating gold is found.
- **`get_adjacent_positions(self, x, y)`**: Returns adjacent positions for a given cell.
- **`is_safe(self, x, y)`**: Checks if a cell is safe to move to.
- **`dfs(self, start_position)`**: Performs Depth-First Search (DFS) to explore the grid and find paths to gold.
- **`display_paths_to_gold(self)`**: Displays all valid paths to gold.

### Environment Generation
- **`generate_valid_environment(environment_size, agent_start_position)`**: Generates a random valid environment.
- **`generate_random_environment(environment_size)`**: Creates a random environment with pits, Wumpus, and gold.

### Pygame Visualization
- **`draw_grid(screen, agent, environment, cell_size, images)`**: Draws the grid environment using Pygame.
- **`main()`**: Main function to initialize Pygame, generate environment, and run the visualization loop.

## Generating a Valid Environment
The environment is generated with a given size and ensures the following:
- The agent's start position is safe (no pit or Wumpus).
- There is at least one gold in the environment.
- Cells may contain pits, Wumpus, and gold with specific probabilities.

## Visualization with Pygame
The grid environment and agent movements are visualized using Pygame. The agent navigates the grid, updating its knowledge base and displaying the path to gold.

## Screenshots
Here are some screenshots of the KB Agent in action:

### Environment 1:
!(https://github.com/Bilal-Ahmad102/Wumpus/blob/main/src/ScreenShots/Screenshot%20from%202024-06-16%2011-24-24.png)

###  Environment 2:
!(https://github.com/Bilal-Ahmad102/Wumpus/blob/main/src/ScreenShots/Screenshot%20from%202024-06-16%2011-24-37.png)

###  Environment 3:
!(https://github.com/Bilal-Ahmad102/Wumpus/blob/main/src/ScreenShots/Screenshot%20from%202024-06-16%2011-24-37.png)

## Conclusion
This project demonstrates a knowledge-based agent navigating a hazardous environment, making use of percepts to update its knowledge and make informed decisions. The Pygame visualization provides an intuitive view of the agent's exploration process.
