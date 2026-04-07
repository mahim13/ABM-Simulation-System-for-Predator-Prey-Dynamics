import pygame
from simulation import Simulation 
from agent import Sheep, Wolf  


GRID_WIDTH = 60
GRID_HEIGHT = 40
INITIAL_SHEEP = 100 # Increased sheep count for visual density
INITIAL_WOLVES = 20
CELL_SIZE = 15      # Smaller cells for larger grid
FPS = 15            

WINDOW_WIDTH = GRID_WIDTH * CELL_SIZE
WINDOW_HEIGHT = GRID_HEIGHT * CELL_SIZE


COLOR_BACKGROUND = (240, 240, 240) # Light grey
COLOR_SHEEP = (50, 200, 50)       
COLOR_WOLF = (200, 50, 50)        
COLOR_EMPTY = (200, 200, 200)     


def draw_simulation(screen, environment):
    """Draws the current state of the simulation environment."""
    screen.fill(COLOR_BACKGROUND)

    
    # Draw agents
    for agent in environment.get_all_agents():
        x, y = agent.position
        # Calculate center of the cell for the circle
        center_x = x * CELL_SIZE + CELL_SIZE // 2
        center_y = y * CELL_SIZE + CELL_SIZE // 2
        radius = CELL_SIZE // 2 - 1 # Leave a small gap

        # Determine color based on agent type
        if agent.type == 'sheep': 
            color = COLOR_SHEEP
        elif agent.type == 'wolf': # Use type attribute
            color = COLOR_WOLF
        else:
            color = (0, 0, 0) 

        pygame.draw.circle(screen, color, (center_x, center_y), radius)


def run_visual_simulation():
    """Initializes Pygame and runs the visual simulation loop."""
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Predator-Prey Simulation")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24) # Font for displaying stats

    # Create the simulation instance
    sim = Simulation(GRID_WIDTH, GRID_HEIGHT, INITIAL_SHEEP, INITIAL_WOLVES)

    running = True
    sim_running = True  # Flag to pause/resume simulation steps

    step_count = 0 # Keep track of steps

    # --- Main Game Loop ---
    while running:
        # --- Event Handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE: # Pause/Resume on Spacebar
                    sim_running = not sim_running
                if event.key == pygame.K_ESCAPE: # Quit on Escape
                     running = False

        # --- Simulation Step ---
        if sim_running:
            sim.run_step() # Execute one step using the method from Simulation class
            step_count += 1

            # Check for extinction
            num_sheep = len(sim.environment.get_all_agents_of_type('sheep'))
            num_wolves = len(sim.environment.get_all_agents_of_type('wolf'))
            if num_sheep == 0 or num_wolves == 0:
                sim_running = False # Stop simulation logic
                print("--- Simulation Ended (Extinction) ---")
                print(f"Final after {step_count} steps: Sheep = {num_sheep}, Wolves = {num_wolves}")

        
        draw_simulation(screen, sim.environment) # Draw agents

        # Display stats on screen
        num_sheep = len(sim.environment.get_all_agents_of_type('sheep'))
        num_wolves = len(sim.environment.get_all_agents_of_type('wolf'))
        stats_text = f"Step: {step_count} | Sheep: {num_sheep} | Wolves: {num_wolves} | {'RUNNING' if sim_running else 'PAUSED/ENDED'}"
        stats_surface = font.render(stats_text, True, (10, 10, 10)) # Dark text color
        screen.blit(stats_surface, (5, 5)) # Position stats at top-left

        
        pygame.display.flip()

        
        clock.tick(FPS) 

    # --- End of Loop ---
    pygame.quit()
    print("Pygame window closed.")


if __name__ == "__main__":
    try:
        run_visual_simulation()
    except Exception as e:
        print("\n--- SIMULATION CRASHED ---")
        print("Error:", e)
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...") # Keep window open to see error