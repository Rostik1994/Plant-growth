import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

class LSystem:
    def __init__(self, axiom, rules, iterations, light_intensity, water_availability):
        self.axiom = axiom
        self.rules = rules
        self.iterations = iterations
        self.light_intensity = light_intensity
        self.water_availability = water_availability
        self.sentence = self.generate()

    def generate(self):
        current = self.axiom
        for _ in range(self.iterations):
            next_sentence = ""
            for char in current:
                next_sentence += self.rules.get(char, char)
            current = next_sentence
        return current

    def interpret(self, sentence, angle):
        stack = []
        positions = []
        x, y = 0, 0
        direction = np.pi / 2  # Start facing upwards
        length = self.calculate_length()
        for char in sentence:
            if char == 'F':
                new_x = x + length * np.cos(direction)
                new_y = y + length * np.sin(direction)
                positions.append(((x, y), (new_x, new_y)))
                x, y = new_x, new_y
            elif char == '+':
                direction += angle
            elif char == '-':
                direction -= angle
            elif char == '[':
                stack.append((x, y, direction))
            elif char == ']':
                x, y, direction = stack.pop()
        return positions

    def calculate_length(self):
        # Simple model: length increases with light and water
        return self.light_intensity * self.water_availability * 2

# Example usage
axiom = "F"
rules = {"F": "F[+F]F[-F]F"}
iterations = 5
angle = np.pi / 6  # 30 degrees
light_intensity = 0.1  # Example light intensity (0 to 1)
water_availability = 0.6  # Example water availability (0 to 1)

lsystem = LSystem(axiom, rules, iterations, light_intensity, water_availability)
positions = lsystem.interpret(lsystem.sentence, angle)

# Animation
fig, ax = plt.subplots()
ax.set_xlim(-10, 10)
ax.set_ylim(0, 20)
lines = []

def init():
    for pos in positions:
        line, = ax.plot([], [], lw=2)
        lines.append(line)
    return lines

def update(frame):
    for i, pos in enumerate(positions[:frame]):
        (x0, y0), (x1, y1) = pos
        lines[i].set_data([x0, x1], [y0, y1])
    return lines

ani = animation.FuncAnimation(fig, update, frames=len(positions), init_func=init, blit=True)
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Procedural Plant Growth with L-System and Photosynthesis')
plt.show()