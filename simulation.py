
import random
import time
from environment import GridEnvironment
from agent import Wolf, Sheep # Keep imports



class Simulation:
    def __init__(self, width, height, initial_sheep, initial_wolves):
        self.environment = GridEnvironment(width, height)
        self.populate_initial_agents(initial_sheep, initial_wolves)

    def populate_initial_agents(self, num_sheep, num_wolves):
        """Places initial agents in unique random empty cells."""
        # Create list of all possible coordinates
        empty_cells = [(x, y) for x in range(self.environment.width) for y in range(self.environment.height)]
        random.shuffle(empty_cells) # Shuffle coordinates

        # Place sheep
        for _ in range(num_sheep):
            if not empty_cells: break # Stop if no more empty cells
            pos = empty_cells.pop()
            energy = random.randint(6, 12)
            self.environment.add_new_agent(Sheep, energy, pos)

        # Place wolves
        for _ in range(num_wolves):
            if not empty_cells: break # Stop if no more empty cells
            pos = empty_cells.pop()
            energy = random.randint(15, 25)
            self.environment.add_new_agent(Wolf, energy, pos)

    def run_step(self):
        """Runs a single step of the simulation."""
        current_agents = self.environment.get_all_agents()
        random.shuffle(current_agents)

        # Agent action phase
        for agent in current_agents:
            # Check if agent is still alive (might have been eaten this step)
            if agent.agent_id in self.environment.agents:
                # The check for MAX_TOTAL_AGENTS before step is optional,
                # as reproduce methods already check it.
                # if len(self.environment.agents) < MAX_TOTAL_AGENTS:
                agent.step() # Polymorphism in action!

    def run(self, num_steps, display_interval=1, delay=0.1):
        """Runs the text-based simulation for a given number of steps."""
        for step in range(num_steps):
            print(f"--- Step {step + 1} ---")

            self.run_step() # Run one simulation step

            # Display and statistics
            
            num_sheep = len(self.environment.get_all_agents_of_type('sheep'))
            num_wolves = len(self.environment.get_all_agents_of_type('wolf'))
            

            print(f"Sheep: {num_sheep}, Wolves: {num_wolves}")

            if display_interval > 0 and (step + 1) % display_interval == 0:
                self.environment.display()

            # Stop if populations die out
            if num_sheep == 0 or num_wolves == 0:
                print("Simulation ended: One species died out.")
                break

            if delay > 0:
                time.sleep(delay) # Slow down for visualization

        print("--- Simulation Finished ---")
        num_sheep = len(self.environment.get_all_agents_of_type('sheep'))
        num_wolves = len(self.environment.get_all_agents_of_type('wolf'))
        print(f"Final populations - Sheep: {num_sheep}, Wolves: {num_wolves}")