from simulation import Simulation

GRID_WIDTH = 20
GRID_HEIGHT = 15
INITIAL_SHEEP = 15
INITIAL_WOLVES = 30
SIMULATION_STEPS = 150
DISPLAY_EVERY_N_STEPS = 5
STEP_DELAY_SECONDS = 0.5


if __name__ == "__main__":
    print("Starting Predator-Prey Simulation...")
    sim = Simulation(
        width=GRID_WIDTH,
        height=GRID_HEIGHT,
        initial_sheep=INITIAL_SHEEP,
        initial_wolves=INITIAL_WOLVES
    )
    sim.run(
        num_steps=SIMULATION_STEPS,
        display_interval=DISPLAY_EVERY_N_STEPS,
        delay=STEP_DELAY_SECONDS
    )
