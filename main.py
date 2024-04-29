import math
import numpy as np
import matplotlib.pyplot as plt

class crt_raster:
    field = None
    adjustments = {"shift_x": 0, 
                     "shift_y": 0, 
                     "scale_x": 1,
                     "scale_y": 1,
                     "keystone_balance": 0,
                     "keystone": 0}
    divisions = None
    starting_width = None
    starting_height = None
    
    # Generates the normal CRT Raster
    def __init__(self, width=20, height=20, divisions=10000):
        self.divisions = divisions
        self.starting_width = width
        self.starting_height = height

    # Takes modifications and applies vector field
    def generate_field(self,):
        # Define the parameter t
        t = np.linspace(-self.starting_width/2, self.starting_width/2 + 1, self.divisions)

        # Define x(t) and y(t)
        x = np.floor(t)
        y = self.starting_height * (t - np.floor(t)) - self.starting_height/2

        # Apply Keystone balance


        # Apply Shift and Scale
        x = np.multiply(x, self.adjustments["scale_x"]) + self.adjustments["shift_x"]
        y = np.multiply(y, self.adjustments["scale_y"]) + self.adjustments["shift_y"]

        # Identify discontinuities and insert NaNs
        discontinuities = np.where(np.diff(np.floor(t)) != 0)[0]
        y[discontinuities] = np.nan  # Insert NaNs where the discontinuities occur
        self.field = [x, y]

    def shift(self, x=None, y=None):
        if x is not None:
            self.adjustments["shift_x"] = x
        if y is not None:
            self.adjustments["shift_y"] = y

    def scale(self, x=None, y=None):
        if x is not None:
            self.adjustments["scale_x"] = x
        if y is not None:
            self.adjustments["scale_y"] = y

    def plot_field(self,grid=False):
        # Generate Field
        self.generate_field()
        # Create the plot
        plt.xlim(-self.starting_width/2 * 1.1, self.starting_width/2 * 1.1)
        plt.ylim(-self.starting_height/2 * 1.1, self.starting_height/2 * 1.1)
        plt.plot(self.field[0], self.field[1])
        plt.title("Modified Parametric Function with Vector Field")
        plt.xlabel("x = cos(t)")
        plt.ylabel("y = 20 * (t - floor(t)) - 10")
        if grid:
            plt.grid(True)
        plt.show()

if __name__ == "__main__":
    output_raster = crt_raster()
    output_raster.scale(1)
    output_raster.plot_field()