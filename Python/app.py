from flask import Flask, jsonify
import agentpy as ap
import numpy as np
import tkinter as tk
import time

app = Flask(__name__)


@app.route("/")
def home():
    return "Test API V1.0"


@app.route("/simulation")
def run_simulation():

    L = 10
    field = np.zeros((L, L))
    np.random.seed(42)

    class Tractor(ap.Agent):
        def setup(self):
            self.x = np.random.randint(0, L)
            self.y = np.random.randint(0, L)
            self.area_to_cut = []
            self.direction = 1
            self.alpha = 0.1  # Learning rate
            self.gamma = 0.9  # Discount factor
            self.Q = {}

        def move(self, field, all_tractors):
            state = (self.x, self.y)

            # Calculate distances to uncut areas
            not_cut = np.argwhere(field == 0)
            distances = np.abs(not_cut - np.array([self.x, self.y]))
            total_distances = np.sum(distances, axis=1)

            # Sort uncut areas by distance
            sorted_indices = np.argsort(total_distances)
            sorted_not_cut = not_cut[sorted_indices]

            # Move to the closest uncut area
            target_x, target_y = sorted_not_cut[0]
            new_x = (self.x + np.sign(target_x - self.x)) % L
            new_y = max(0, min(self.y + np.sign(target_y - self.y), L - 1))

            
            new_x = self.x
            new_y = self.y
            if field[new_x, new_y] == 1:
                not_cut = np.argwhere(field == 0) 
                if len(not_cut) > 0:
                    # Calculate distances to uncut areas
                    distances = np.abs(not_cut - np.array([self.x, self.y]))
                    total_distances = np.sum(distances, axis=1)
                    # Find the index of the nearest uncut cell
                    nearest_index = np.argmin(total_distances)
                    # Get the coordinates of the nearest uncut cell
                    new_x, new_y = not_cut[nearest_index]
                    # Update the direction
                    self.direction = np.sign(new_x - self.x)
            self.x, self.y = new_x, new_y

            # Collision detection
            if (new_x, new_y) in [(tractor.x, tractor.y) for tractor in all_tractors if tractor != self]:
                # If the new position is already occupied by another harvester, stay in the current position
                new_x, new_y = self.x, self.y

            reward = field[new_x, new_y] == 1  # 1 if the cell was cut, 0 otherwise

            # Update Q-value
            next_state = (new_x, new_y)
            if state not in self.Q:
                self.Q[state] = 0
            if next_state not in self.Q:
                self.Q[next_state] = 0

            self.Q[state] = (1 - self.alpha) * self.Q[state] + self.alpha * (reward + self.gamma * self.Q[next_state])

            # Update the direction
            self.direction = np.sign(new_x - self.x)
            self.x, self.y = new_x, new_y

            # Update the field and record the harvested area
            field[self.x, self.y] = 1
            self.area_to_cut.append((self.x, self.y))

    class HarvestModel(ap.Model):
        def setup(self):
            self.tractors = ap.AgentList(self, self.p.tractors, Tractor)

        def step(self):
            for tractor in self.tractors:
                tractor.move(field, self.tractors)


    # Define parameters
    parameters = {
        'tractors': 2,
        'steps': 50,
        'random_seed': 42,
    }

    # Create and run the model
    model = HarvestModel(parameters)
    model.run(parameters['steps'])

    tractor_info = {}

    for idx, tractor in enumerate(model.tractors, 1):
        coordinates = [
            {"X_COORDINATE": float(x), "Z_COORDINATE": float(y)} for x, y in tractor.area_to_cut
        ]
        # Add the initial position to the beginning of the list
        coordinates.insert(
            0, {"X_COORDINATE": float(tractor.x), "Z_COORDINATE": float(tractor.y)}
        )

        tractor_info["harvester" + str(idx)] = coordinates

    data = {
        "data": tractor_info
    }

    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
