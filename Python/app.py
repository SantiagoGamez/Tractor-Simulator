# Recuerda instalar primero flask
# pip install Flask agentpy numpy matplotlib

from flask import Flask, jsonify
import json
import agentpy as ap
import numpy as np
import matplotlib.pyplot as plt

app = Flask(__name__)


@app.route("/")
def home():
    return "La API está corriendo exitosamente."

@app.route("/steps")
def steps_simulation():
    # Lista en donde guardaremos toda la información
    steps_info = []

    for step in range(model.p.steps):
        model.step()

        # Info de cada paso
        step_info = {
            "step": step + 1,
            "tractors": [
                {
                    "position": [int(tractor.x), int(tractor.y)],
                    "cutting_areas": [[int(x), int(y)] for x, y in tractor.area_to_cut]
                }
                for tractor in model.tractors
            ]
        }

        steps_info.append(step_info)

    # Regresa la info de todos los pasos en formato JSON
    return json.dumps(steps_info)


from flask import jsonify

@app.route("/tractors")
def tractors_simulation():
    # Lista en donde guardaremos toda la información
    tractors_info_list = []

    for step in range(model.p.steps):
        model.step()

        # Info de cada paso
        step_tractors_info = {
            "tractors": [
                {
                    "position": {"x": int(tractor.x), "z": int(tractor.y)}
                }
                for tractor in model.tractors
            ]
        }

        tractors_info_list.append(step_tractors_info)

    # Regresa la info de todos los pasos en formato JSON
    return jsonify(tractors_info_list)


L = 10
field = np.zeros((L, L))

class Tractor(ap.Agent):
    
    def setup(self):
        self.x = np.random.randint(0, L)
        self.y = np.random.randint(0, L)
        self.area_to_cut = []
        self.direction = 1

    def move(self):
        if self.x == 0:
            self.direction = 1
        elif self.x == L - 1:
            self.direction = -1

        # Update x coordinate
        new_x = self.x + self.direction

        # Update y coordinate within valid range
        new_y = max(0, min(self.y + np.random.randint(-1, 2), L - 1))

        # Check if the target location has already been cut
        if field[new_x, new_y] == 1:
            not_cut = np.argwhere(field == 0)

            # Check if there are available positions to cut
            if len(not_cut) > 0:
                new_x, new_y = not_cut[np.random.randint(0, len(not_cut))]
                self.direction = np.sign(new_x - self.x)

        # Update the coordinates and mark the field as cut
        self.x, self.y = new_x, new_y
        self.area_to_cut.append((self.x, self.y))
        field[self.x, self.y] = 1


class HarvestModel(ap.Model):
    def setup(self):
        self.tractors = ap.AgentList(self, self.p.tractors, Tractor)

    def step(self):
        for tractor in self.tractors:
            tractor.move()

#Parametros parala simulación que utilizará el modelo
parameters = {
    'tractors': 2,
    'steps': 49,
    'random_seed': 42,
}
model = HarvestModel(parameters)
model.run()
