import random
from abc import ABC, abstractmethod

MAX_TOTAL_AGENTS = 500 # Global agent limit

class Agent(ABC):
    def __init__(self, agent_id, environment, initial_energy, position):
        self.agent_id = agent_id
        self.environment = environment
        self.energy = initial_energy
        self.position = position # Should always be accurate after move_agent call

    @abstractmethod
    def step(self):
        """Defines the agent's actions during one simulation step."""
        pass

    def _lose_energy(self, amount=1):
        """Common energy loss per step."""
        self.energy -= amount

    def is_alive(self):
        """Check if the agent has enough energy to live."""
        return self.energy > 0

    def die(self):
        """Signal the environment to remove this agent."""
        # print(f"{self.type} {self.agent_id} died at {self.position}") # Debugging
        self.environment.remove_agent(self)

    def _move_randomly(self):
        """Moves to a random valid neighboring empty cell."""
        # Uses environment method that finds EMPTY neighbors
        moves = self.environment.get_valid_neighboring_positions(self.position)
        if moves:
            new_pos = random.choice(moves)
            self.environment.move_agent(self, new_pos) # move_agent handles grid update & self.position update


class Sheep(Agent):
    REPRODUCTION_THRESHOLD = 10
    ENERGY_GAIN_PER_STEP = 5  
    ENERGY_COST_PER_STEP = 1  

    def __init__(self, agent_id, environment, initial_energy, position):
        super().__init__(agent_id, environment, initial_energy, position)
        self.type = 'sheep'

    def step(self):
        self._lose_energy(self.ENERGY_COST_PER_STEP)
        if not self.is_alive():
            self.die()
            return

        self.energy += self.ENERGY_GAIN_PER_STEP # Passive gain

        # Reproduce with a certain probability if energy is sufficient
        if self.energy >= self.REPRODUCTION_THRESHOLD and random.random() < 0.08: 
             self.reproduce()

        self._move_randomly()

    def reproduce(self):
        # Check global agent limit
        if len(self.environment.agents) >= MAX_TOTAL_AGENTS:
            return

        # Find an empty neighboring cell to place offspring
        # Uses environment method that finds EMPTY neighbors
        empty_neighbor_positions = self.environment.get_valid_neighboring_positions(self.position)

        if empty_neighbor_positions:
            birth_pos = random.choice(empty_neighbor_positions) # Choose one random empty spot
            # Cost of reproduction
            repro_cost = self.energy // 2 # Example cost
            self.energy -= repro_cost
            # print(f"Sheep {self.agent_id} reproducing at {self.position}, offspring at {birth_pos}") # Debugging
            # Add the new agent via environment
            self.environment.add_new_agent(Sheep, repro_cost, birth_pos) # Give offspring the energy cost


class Wolf(Agent):
    REPRODUCTION_THRESHOLD = 25
    ENERGY_GAIN_FROM_EATING = 20 # Slightly reduced gain
    ENERGY_COST_PER_STEP = 2     # Higher cost for predator

    def __init__(self, agent_id, environment, initial_energy, position):
        super().__init__(agent_id, environment, initial_energy, position)
        self.type = 'wolf'

    def step(self):
        self._lose_energy(self.ENERGY_COST_PER_STEP)
        if not self.is_alive():
            self.die()
            return

        
        hunt_success = self.hunt_nearby()

        
        if not hunt_success:
            self._move_randomly()

        # Reproduce with a certain probability if energy is sufficient
        if self.energy >= self.REPRODUCTION_THRESHOLD and random.random() < 0.1: # Lowered probability
            self.reproduce()


    def hunt_nearby(self):
        """Checks neighboring cells for sheep, moves to eat one if found."""
        # Use the environment method that returns ALL neighbors (occupied or not)
        neighbor_positions = self.environment.get_neighboring_positions_all(self.position, include_self=False)
        random.shuffle(neighbor_positions) # Check neighbors in random order

        for pos in neighbor_positions:
            potential_prey = self.environment.get_agent_at(pos)
            # Check if there is an agent AND if it's a sheep
            if potential_prey is not None and potential_prey.type == 'sheep':
                # print(f"Wolf {self.agent_id} found sheep {potential_prey.agent_id} at {pos}") # Debugging
                # Try to move onto the sheep's square
                move_successful = self.environment.move_agent(self, pos)

                # If move was successful (meaning we are now on the sheep's square)
                # Note: move_agent now only moves if cell is empty or contains self, so this logic needs adjustment.
                # Let's revise: Wolf kills sheep in neighbor cell, THEN moves there.

                # Revised Hunt Logic:
                # 1. Kill the sheep first
                # print(f"Wolf {self.agent_id} eating sheep {potential_prey.agent_id} at {pos}") # Debugging
                potential_prey.die() # Environment removes the sheep
                self.energy += self.ENERGY_GAIN_FROM_EATING

                # 2. Now try to move into the (now potentially empty) cell
                move_successful = self.environment.move_agent(self, pos)
                # if not move_successful: print(f"Wolf {self.agent_id} ate but couldn't move to {pos}")

                return True # Indicate hunt occurred (even if move failed)

        return False # No sheep found nearby


    def reproduce(self):
         # Check global agent limit
        if len(self.environment.agents) >= MAX_TOTAL_AGENTS:
            return

        # Find an empty neighboring cell to place offspring
        empty_neighbor_positions = self.environment.get_valid_neighboring_positions(self.position)

        if empty_neighbor_positions:
            birth_pos = random.choice(empty_neighbor_positions) # Choose one random empty spot
            # Cost of reproduction
            repro_cost = self.energy // 2
            self.energy -= repro_cost
            # print(f"Wolf {self.agent_id} reproducing at {self.position}, offspring at {birth_pos}") # Debugging
            # Add the new agent via environment
            self.environment.add_new_agent(Wolf, repro_cost, birth_pos)