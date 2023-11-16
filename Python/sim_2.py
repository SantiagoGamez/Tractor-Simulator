import agentpy as ap
import numpy as np
import tkinter as tk
import time

L = 10
field = np.zeros((L, L))

class Tractor(ap.Agent):
    def setup(self):
        self.x = np.random.randint(0, L)
        self.y = np.random.randint(0, L)
        # self.x = 0
        # self.y = 0
        self.area_to_cut = []
        self.direction = 1

    def move(self, field):
        # Calculate distances to uncut areas
        not_cut = np.argwhere(field == 0)
        distances = np.abs(not_cut - np.array([self.x, self.y]))
        total_distances = np.sum(distances, axis=1)

        # Sort uncut areas by distance
        sorted_indices = np.argsort(total_distances)
        sorted_not_cut = not_cut[sorted_indices]

        # Move to the closest uncut area
        target_x, target_y = sorted_not_cut[0]
        self.x = (self.x + np.sign(target_x - self.x)) % L
        self.y = max(0, min(self.y + np.sign(target_y - self.y), L - 1))

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

        # Update the field and record the harvested area
        field[self.x, self.y] = 1
        self.area_to_cut.append((self.x, self.y))

class HarvestModel(ap.Model):
    def setup(self):
        self.tractors = ap.AgentList(self, self.p.tractors, Tractor)

    def step(self):
        for tractor in self.tractors:
            tractor.move(field)


# Define parameters
parameters = {
    'tractors': 2,
    'steps': 50,
    'random_seed': 42,
}

# Create and run the model
model = HarvestModel(parameters)
model.run(parameters['steps'])


# Verify the cutting areas of each tractor
for tractor in model.tractors:
    print(f"The tractor at position ({tractor.x}, {tractor.y}) cuts the following areas: {tractor.area_to_cut}")

# Create a Tkinter window
window = tk.Tk()
window.title("Harvest Simulation")

# Create a canvas to draw the field
canvas = tk.Canvas(window, width=200, height=200)
canvas.pack()


# mark the borders of the field with tkinter ovals
for x in range(0, 400, 20):
    for y in range(0, 400, 20):
        # canvas.create_oval(x, y, x + 20, y + 20, fill="green")
        canvas.create_rectangle(x, y, x + 20, y + 20, fill="green")


# draw the path of each tractor with tkinter ovals with sleep time
# a different color for a different tractor
colors = ["yellow", "blue", "pink"]
tractor_paths = []

# Collect tractor paths
for tractor in model.tractors:
    # color = colors[np.random.randint(0, len(colors))]
    color = colors[tractor.id]
    tractor_path = [(x, y, color) for x, y in tractor.area_to_cut]
    tractor_paths.append(tractor_path)

# Draw all tractor paths simultaneously
for step in range(len(max(tractor_paths, key=len))):
    for tractor_path in tractor_paths:
        if step < len(tractor_path):
            x, y, color = tractor_path[step]
            canvas.create_oval(x *20, y *20, x *20 +20, y *20 +20, fill=color)

    window.update()
    time.sleep(0.2)

# Run the Tkinter window
window.mainloop()
