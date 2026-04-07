import random 

class GridEnvironment:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        # Grid holds None or a single Agent object per cell
        self.grid = [[None for _ in range(width)] for _ in range(height)]
        # Dictionary to quickly find agent objects by ID
        self.agents = {}
        self._next_agent_id = 0

    def _get_next_id(self):
        self._next_agent_id += 1
        return self._next_agent_id

    def add_agent(self, agent):
        """Adds an existing agent object to an empty cell."""
        x, y = agent.position
        if 0 <= x < self.width and 0 <= y < self.height:
            # Check if cell is empty before placing
            if self.grid[y][x] is None:
                self.grid[y][x] = agent
                self.agents[agent.agent_id] = agent
            
            

    def add_new_agent(self, agent_class, initial_energy, position):
        """Creates and adds a new agent if the target cell is empty."""
        x, y = position
        # Check bounds and if cell is empty
        if not (0 <= x < self.width and 0 <= y < self.height and self.grid[y][x] is None):
             
             return None  # Don't place in occupied or invalid cell

        agent_id = self._get_next_id()
        new_agent = agent_class(agent_id, self, initial_energy, position)
        self.grid[y][x] = new_agent # Place on grid
        self.agents[agent_id] = new_agent 
        
        return new_agent

    def remove_agent(self, agent):
        """Removes an agent from the grid and agent list."""
        
        x, y = agent.position
        if 0 <= x < self.width and 0 <= y < self.height:
             # Check if the agent we are removing is actually the one on the grid
            if self.grid[y][x] == agent:
                self.grid[y][x] = None
        
        
        removed_agent = self.agents.pop(agent.agent_id, None)
        

    def move_agent(self, agent, new_position):
        """Moves an agent if the target cell is valid and empty."""
        new_x, new_y = new_position
        # Check bounds
        if not (0 <= new_x < self.width and 0 <= new_y < self.height):
            
            return False 

        # Check if target cell is occupied *by another agent*
        target_cell_content = self.grid[new_y][new_x]
        if target_cell_content is not None and target_cell_content != agent:
            
            return False # Indicate move failed

        # Proceed with move
        old_x, old_y = agent.position
        

        # Vacate old cell only if agent was actually there
        if self.grid[old_y][old_x] == agent:
             self.grid[old_y][old_x] = None
        


        # Occupy new cell
        self.grid[new_y][new_x] = agent
        # Update agent's internal state
        agent.position = new_position
        return True # Indicate move succeeded

    def get_agent_at(self, position):
        """Returns the agent object at a position, or None if empty/invalid."""
        x, y = position
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.grid[y][x]
        return None

    def get_valid_neighboring_positions(self, position):
        """Gets valid (within bounds) and *empty* neighboring grid cell coordinates."""
        x, y = position
        neighbors = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue # Skip self
                nx, ny = x + dx, y + dy
                # Check bounds AND if the cell is empty (None)
                if 0 <= nx < self.width and 0 <= ny < self.height and self.grid[ny][nx] is None:
                    neighbors.append((nx, ny))
        return neighbors

    # --- ADDED METHOD needed for Wolf.hunt_nearby ---
    def get_neighboring_positions_all(self, position, include_self=False):
         """Gets coordinates of valid neighboring cells, regardless of occupancy."""
         x, y = position
         neighbors = []
         for dx in [-1, 0, 1]:
             for dy in [-1, 0, 1]:
                 if not include_self and dx == 0 and dy == 0:
                     continue # Skip self unless requested
                 nx, ny = x + dx, y + dy
                 # Check bounds only
                 if 0 <= nx < self.width and 0 <= ny < self.height:
                     neighbors.append((nx, ny))
         return neighbors
    #-------------------------------------------------

    def get_all_agents(self):
        """Returns a list of all active agent objects."""
        # Important: Return a copy of the list of values
        return list(self.agents.values())

    def get_all_agents_of_type(self, agent_type):
        """Returns a list of active agents matching the specified type string."""
        return [agent for agent in self.agents.values() if agent.type == agent_type]

    def display(self):
        """Prints a text representation of the grid."""
        print("-" * (self.width + 2)) # Top border
        for y in range(self.height):
            row = "|" # Left border
            for x in range(self.width):
                agent = self.grid[y][x]
                if agent is None:
                    row += "."
                elif agent.type == 'wolf':
                    row += "W"
                elif agent.type == 'sheep': 
                    row += "S"
                else:
                     row += "?" 
            row += "|" # Right border
            print(row)
        print("-" * (self.width + 2)) # Bottom border