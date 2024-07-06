import random

class Gym:
    def __init__(self, num_weights):
        # Each weight is identified by an index, and its designated spot is the same as its index for simplicity
        self.designated_spots = {i: i for i in range(num_weights)}
        self.current_spots = {i: i for i in range(num_weights)}  # Initially, all weights are in their designated spots

    def pick_up_weight(self, weight_id):
        # Simulate picking up a weight (this could be expanded with more logic)
        if weight_id in self.current_spots:
            del self.current_spots[weight_id]

    def return_weight(self, weight_id, spot_id):
        # Return a weight to a spot (which might not be its designated spot)
        self.current_spots[weight_id] = spot_id

    def chaos_report(self):
        # Calculate how many weights are not in their designated spots
        misplaced_weights = sum(
            1 for weight_id, spot_id in self.current_spots.items()
            if spot_id != self.designated_spots[weight_id]
        )
        print(f"Chaos Report: {misplaced_weights} weights are not in their designated spots.")

def simulate_gym_chaos(num_weights=10, num_interactions=50):
    gym = Gym(num_weights)
    for _ in range(num_interactions):
        weight_id = random.randint(0, num_weights - 1)
        gym.pick_up_weight(weight_id)
        # Simulate the chance of returning to the right or wrong spot
        if random.random() < 0.5:  # 50% chance to return to the right spot for simplicity
            gym.return_weight(weight_id, weight_id)
        else:
            wrong_spot_id = random.randint(0, num_weights - 1)
            gym.return_weight(weight_id, wrong_spot_id)
    gym.chaos_report()

simulate_gym_chaos(30, 100)
