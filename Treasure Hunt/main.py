import random
from collections import deque

# Constants
GRID_SIZE = 7
NUM_TRAPS = 10  # 10 traps
NUM_POWERUPS = 10  # 10 power-ups
MAX_MOVES = 15 #maximum 15 moves to find the treasure

# Initializing the grid with numbers for coordinates
grid = [['.' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Game elements
traps = ['Pitfall', 'Poison Gas', 'Poisonous Plant']
power_ups = ['Shield', 'Health Potion']

# solving these riddles can help avoid traps
riddles = [
    {
        "question": "I can fly but have no wings. I can cry but I have no eyes. Wherever I go, darkness follows me. What am I?",
        "answer": "clouds"},
    {"question": "What is so delicate that saying its name breaks it?", "answer": "silence"},
    {"question": "What can you catch but never throw?", "answer": "a cold"},
    {"question": "If you have me, you will want to share me. If you share me, you will no longer have me. What am I?",
     "answer": "a secret"},
    {"question": "If you feed it, it lives; If you water it, it dies. What is it?", "answer": "fire"},
    {"question": "What is full of holes but can still hold water?", "answer": "a sponge"},
]
# Function to randomize treasure position and ensure it isn't at the starting position or on a trap/power-up
def randomize_treasure(grid, grid_size):
    while True:
        x, y = random.randint(0, grid_size - 1), random.randint(0, grid_size - 1)
        if (x, y) != (0, 0) and grid[x][y] == '.':  # Ensure treasure isn't at (0, 0) or overlapping with traps/power-ups
            return (x, y)


# Global treasure position
TREASURE_POSITION = randomize_treasure(grid, GRID_SIZE)


# Randomly place the treasure, traps, and power-ups
def place_game_elements():
    # Place the treasure
    grid[TREASURE_POSITION[0]][TREASURE_POSITION[1]] = 'T'

    # Place traps
    for _ in range(NUM_TRAPS):
        while True:
            trap_position = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
            # Ensure no traps on the starting position (0,0)
            if grid[trap_position[0]][trap_position[1]] == '.' and trap_position != (0, 0):
                grid[trap_position[0]][trap_position[1]] = '?'
                break

    # Place power-ups
    for _ in range(NUM_POWERUPS):
        while True:
            powerup_position = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
            # Ensure no power-ups on the starting position (0,0)
            if grid[powerup_position[0]][powerup_position[1]] == '.' and powerup_position != (0, 0):
                grid[powerup_position[0]][powerup_position[1]] = '?'
                break


# Display the grid (with the player visible and treasure hidden)
def display_grid(player_position):
    # Make a copy of the grid to hide elements
    visible_grid = [['.' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

    # Place the player's position as 'X'
    x, y = player_position
    visible_grid[x][y] = 'X'

    # Reveal treasure only when the player finds it
    treasure_x, treasure_y = TREASURE_POSITION
    if player_position == (treasure_x, treasure_y):
        visible_grid[treasure_x][treasure_y] = 'TX'  # Treasure found by the player

    # Hiding traps and power-ups using '?'
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if grid[i][j] == '?':
                visible_grid[i][j] = '?'

    # Print the grid with numbers for coordinates
    print("Currently on the Map:")
    print("  0 1 2 3 4 5 6")  # Column
    for i, row in enumerate(visible_grid):
        print(f"{i} " + " ".join(row))  # Row number followed by the row's content
    print()  # New line for better readability


# Player class
class Player:
    def __init__(self, name, health=100):
        self.name = name
        self.health = health
        self.position = (0, 0)  # Starting at top-left
        self.has_treasure = False
        self.shield_active = False  # No shield at the start
        self.saved_clues = []

    def move(self, direction):
        x, y = self.position
        if direction == 'up' and x > 0:
            self.position = (x - 1, y)
        elif direction == 'down' and x < GRID_SIZE - 1:
            self.position = (x + 1, y)
        elif direction == 'left' and y > 0:
            self.position = (x, y - 1)
        elif direction == 'right' and y < GRID_SIZE - 1:
            self.position = (x, y + 1)
        else:
            print("Error: You cannot move outside the grid! Please choose a valid direction.")

    def encounter(self):
        x, y = self.position
        item = grid[x][y]

        if (x, y) == TREASURE_POSITION:  # Checks if the player has reached the treasure position
            self.has_treasure = True
            print(
                f"{self.name} stumbles upon a large wooden chest! It's filled with gems, gold, and precious jewels! You've found the treasure!")
        elif item == '?':  # If it's a hidden item
            actual_item = random.choice(traps + power_ups)  # Randomly decides if it's a trap or power-up
            print(f"{self.name} discovers a hidden object!")
            if actual_item in traps:
                self.solve_riddle_to_avoid_trap(actual_item)  # Try to solve a riddle to avoid the trap
            elif actual_item in power_ups:
                print(f"Great! You found a {actual_item}.")
                if actual_item == 'Shield':
                    self.shield_active = True  # Activating the shield power-up
                elif actual_item == 'Health Potion':
                    self.health = min(100, self.health + 15)  # Max health is 100, increase by 15
                print(f"Your current health is now {self.health}%.")
        elif item == 'Shield' or item == 'Health Potion':
            if item == 'Shield':
                self.shield_active = True
            elif item == 'Health Potion':
                self.health = min(100, self.health + 15)
            print(f"You found a {item}. Your health is now {self.health}%.")
        grid[x][y] = '.'  # After encountering the item, it disappears

    def handle_trap(self, trap):
        if trap == 'Pitfall':
            return 25  # Pitfall causes 25% health loss
        elif trap == 'Poison Gas':
            return 20  # Poison Gas causes 20% health loss
        elif trap == 'Poisonous Plant':
            return 15  # Poisonous Plant causes 15% health loss

    def solve_riddle_to_avoid_trap(self, trap):
        riddle = random.choice(riddles)
        print(f"{self.name}, you stepped into a trap! It's a {trap}.")
        print(f"To avoid it, answer this riddle:")
        print(riddle["question"])
        attempts = 2

        while attempts > 0:
            answer = input("Your answer: ").strip().lower()
            if answer == riddle["answer"]:
                print(f"Correct! You cleverly avoid the {trap}.")
                return
            else:
                attempts -= 1
                print(f"Wrong answer! You have {attempts} attempt(s) left.")

        print(f"Sorry, you failed to solve the riddle. The {trap} takes its toll.")
        self.health -= self.handle_trap(trap)
        print(f"Your health is now {self.health}%.")
 #for BS
def find_quadrant(position):
    x, y = position
    if x < GRID_SIZE // 2:
        return "top-left" if y < GRID_SIZE // 2 else "top-right"
    else:
        return "bottom-left" if y < GRID_SIZE // 2 else "bottom-right"

#for BFS
def bfs_clue(start, treasure, grid):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, down, left, right
    queue = deque([(start, [])])  # (current position, path)
    visited = set()

    while queue:
        (x, y), path = queue.popleft()
        if (x, y) == treasure:
            return path
        if (x, y) in visited:
            continue
        visited.add((x, y))

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and grid[nx][ny] != '?' and (nx, ny) not in visited:
                queue.append(((nx, ny), path + [(nx, ny)]))
    return None  # No path found

def dfs_clue(start, treasure, grid):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, down, left, right
    stack = [(start, [])]
    visited = set()
    suggestions = []

    while stack:
        (x, y), path = stack.pop()
        if (x, y) == treasure:
            return suggestions
        if (x, y) in visited:
            continue
        visited.add((x, y))

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and grid[nx][ny] != '?' and (nx, ny) not in visited:
                stack.append(((nx, ny), path + [(nx, ny)]))
                if (nx, ny) not in suggestions:
                    suggestions.append((nx, ny))
    return suggestions


# Add a dictionary or flags to track clue usage
clue_used = {'b': False, 's': False, 'd': False}


# Main Game Loop for Single Player or Two Player Mode
def main():
    # Welcome message
    print("Welcome to the Treasure Hunt Game!")
    print("You are on a quest to find the hidden treasure on a dangerous forest.")
    print("Move around the grid, avoid traps, collect power-ups, and find the treasure before your health runs out!")
    print("Game Instructions:")
    print(" - Use 'up', 'down', 'left', 'right' to move.")
    print("the Grid is in the (x,y) where x is the row and y is the column")
    print(" - You will be given search clues that can only be used once in each game: \n   * BS - clue about the general quadrant\n   * BFS - clue about the shortest safe path towards the treasure \n   * DFS - alternative routes to the treasure")
    print(" - Traps and power-ups are hidden with a '?' take them at your own risk")
    print(" - Solve the riddles to avoid traps to preserve your health.")
    print(" - Collect power-ups to help you on your journey.")
    print(" - Find the treasure within 15 moves to win the game!")
    print("\nLet's begin!")

    # Seting up game elements
    place_game_elements()
    moves_left = MAX_MOVES

    # Player setup with option for two players
    player_count = input("How many players? (1 or 2): ").strip()
    players = []
    if player_count == '2':
        player1_name = input("Enter Player 1's name: ").strip()
        player2_name = input("Enter Player 2's name: ").strip()
        players.append(Player(player1_name))
        players.append(Player(player2_name))
    else:
        player_name = input("Enter your name: ").strip()
        players.append(Player(player_name))

    # Player loop
    turn = 0
    while True:
        current_player = players[turn % len(players)]  # To alternate turns between players
        print(f"\n{current_player.name}'s turn.")
        display_grid(current_player.position)

        move_choice = input(
            f"Your health is {current_player.health}%.\nMoves left: {moves_left}\nChoose a direction to move (up, down, left, right): ").lower()
        current_player.move(move_choice)
        current_player.encounter()

        # To allow the player to choose a search method for clues after each move
        if current_player.health > 0 and moves_left > 0:
            if not clue_used['b'] or not clue_used['s'] or not clue_used['d']:
                search_choice = input(
                    "Choose your search method: Binary Search (B), BFS (S), DFS (D) or Save for Later (L): ").strip().lower()

                # Binary Search Clue
                if search_choice == 'b' and not clue_used['b']:
                    quadrant = find_quadrant(TREASURE_POSITION)
                    print(f"Performing Binary Search for treasure...")
                    print(f"Clue: The treasure is in the {quadrant} quadrant of the grid.")
                    clue_used['b'] = True

                # BFS Clue
                elif search_choice == 's' and not clue_used['s']:
                    path = bfs_clue(current_player.position, TREASURE_POSITION, grid)
                    if path:
                        print("Performing BFS to find the shortest path to the treasure...")
                        print(f"Clue: Move towards {path[0]} to begin the safest path to the treasure.")
                    else:
                        print("No safe path to the treasure could be determined.")
                    clue_used['s'] = True

                # DFS Clue
                elif search_choice == 'd' and not clue_used['d']:
                    suggestions = dfs_clue(current_player.position, TREASURE_POSITION, grid)
                    print("Performing DFS to explore alternative routes...")
                    print(f"Clue: Consider exploring {', '.join(map(str, suggestions))}.")
                    clue_used['d'] = True

                elif search_choice == 'l':
                    print("You saved your clue for later use.")
                    current_player.saved_clues.append(search_choice)

                else:
                    print(
                        "You have already used this search method or it's not able to perform this search at this cell.")
            else:
                print("You have used all available search clues.")

        if current_player.has_treasure:
            print(f"{current_player.name} has successfully found the treasure! Congratulations!")
            break
        elif current_player.health <= 0:
            print(f"{current_player.name} has lost all their health. Game over.")
            break
        elif moves_left == 0:
            print(f"Sorry, {current_player.name}! You've run out of moves! Game Over!")
            break

        # Alternate turns between the players
        turn += 1
        moves_left -= 1


# To run the game
if __name__ == "__main__":
    main()

