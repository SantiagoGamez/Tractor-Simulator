from flask import Flask, jsonify
import agentpy as ap
import numpy as np

app = Flask(__name__)
L = 2
field = np.zeros((L, L))

class Tractor(ap.Agent):
    def setup(self):
        self.x = np.random.randint(0, L)
        self.y = np.random.randint(0, L)
        self.area_to_cut = []
        self.direction = 1
        self.initial_position = (self.x, self.y)

    def move(self):
        if self.x == 0:
            self.direction = 1
        elif self.x == L - 1:
            self.direction = -1

        new_x = self.x + self.direction
        new_y = max(0, min(self.y + np.random.randint(-1, 2), L - 1))

        if field[new_x, new_y] == 1:
            not_cut = np.argwhere(field == 0)
            if len(not_cut) > 0:
                new_x, new_y = not_cut[np.random.randint(0, len(not_cut))]
                self.direction = np.sign(new_x - self.x)

        self.x, self.y = new_x, new_y
        self.area_to_cut.append((float(self.x), float(self.y)))
        field[self.x, self.y] = 1

class HarvestModel(ap.Model):
    def setup(self):
        self.tractors = ap.AgentList(self, self.p.tractors, Tractor)

    def step(self):
        for tractor in self.tractors:
            tractor.move()

@app.route("/")
def home():
    return "Test API V1.0"

@app.route("/simulation")
def run_simulation():


    parameters = {
        'tractors': 2,
        'steps': 1,
        'random_seed': 42,
    }

    model = HarvestModel(parameters)
    model.run()

    for _ in range(model.p.steps):
        model.step()

    tractor_info = {}

    for idx, tractor in enumerate(model.tractors, 1):
        coordinates = [
            {"X_COORDINATE": float(x), "Z_COORDINATE": float(y)} for x, y in tractor.area_to_cut
        ]
        # Add the initial position to the beginning of the list
        coordinates.insert(
            0, {"X_COORDINATE": float(tractor.initial_position[0]), "Z_COORDINATE": float(tractor.initial_position[1])}
        )
    
        tractor_info["harvester" + str(idx)] = coordinates

        data = {
            "data": tractor_info
        }

    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
