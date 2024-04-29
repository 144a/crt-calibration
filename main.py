import math
import numpy as np
import matplotlib.pyplot as plt

class crt_raster:
    field = None
    adjustments = None
    divisions = None
    starting_width = None
    starting_height = None
    
    # Generates the normal CRT Raster
    def __init__(self, width=20, height=20, divisions=10000):
        self.divisions = divisions
        self.starting_width = width
        self.starting_height = height
        self.adjustments = {"shift_x": 0, 
                     "shift_y": 0, 
                     "scale_x": 1,
                     "scale_y": 1,
                     "keystone_balance": 0,
                     "keystone": 1,
                     "pincushion_balance": 0,
                     "pincushion": 0}

    # Takes modifications and applies vector field
    def generate_field(self,):
        # Define the parameter t
        t = np.linspace(-self.starting_width/2, self.starting_width/2 + 1, self.divisions)

        # Define x(t) and y(t)
        x = np.floor(t)
        y = self.starting_height * (t - np.floor(t)) - self.starting_height/2

        # Apply Pincushion Balance adjustment
        x += (-np.abs(np.power(y, 2)) + (self.starting_height/2)**2) * self.adjustments["pincushion_balance"]/(100 * self.starting_width/2)

        # Apply Pincushion adjustment
        x += np.sign(x)*(-np.abs(np.power(y, 2) * x) + (self.starting_height/2)**2) * self.adjustments["pincushion"]/(1000 * self.starting_width/2)
        
        #(sgn(x) y² x + 16) * 0.1

        # Apply Keystone adjustment
        x = x * (1 + (self.adjustments["keystone"]/(200 * self.starting_width/2)) * y)

        # Apply Keystone Balance adjustment
        x += self.starting_width * (self.adjustments["keystone_balance"]/(200 * self.starting_width/2)) * y

        # Apply Shift and Scale adjustment
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

    # Reasonable values are around -20 to 20
    def keystone(self, val=None, bal = False):
        if bal:
            self.adjustments["keystone_balance"] = val
        else:
            self.adjustments["keystone"] = val
    
    def pincushion(self, val=None, bal = False):
        if bal:
            self.adjustments["pincushion_balance"] = val
        else:
            self.adjustments["pincushion"] = val        

    def plot_field(self,grid=False, title=None, path=None):
        plt.clf()
        # Generate Field
        self.generate_field()
        # Create the plot
        plt.xlim(-self.starting_width/2 * 1.2, self.starting_width/2 * 1.2)
        plt.ylim(-self.starting_height/2 * 1.2, self.starting_height/2 * 1.2)
        plt.plot(self.field[0], self.field[1])
        if title is None:
            plt.title("Modified Parametric Function with Vector Field Applied")
        else:
            plt.title(title)
        plt.xlabel("x(t) = cos(t)")
        plt.ylabel("y(t) = 20 * (t - floor(t)) - 10")
        if grid:
            plt.grid(True)
        if path is not None:
            plt.savefig(path)
        else:
            plt.show()

if __name__ == "__main__":
    normal_raster = crt_raster()
    normal_raster.plot_field(True, None, "Normal_raster.png")

    scale_shift_raster = crt_raster()
    scale_shift_raster.shift(x=1)
    scale_shift_raster.scale(y=0.75)
    scale_shift_raster.plot_field(True, "Shifted and Scaled Raster", "Shift_Scale_raster.png")

    keystone_raster = crt_raster()
    keystone_raster.keystone(8)
    keystone_raster.plot_field(True, "Keystone Raster", "Keystone_raster.png")
    keystone_raster.keystone(0)
    keystone_raster.keystone(8, True)
    keystone_raster.plot_field(True, "Keystone Balance Raster", "Keystone_Balance_raster.png")
    #output_raster.pincushion(-7)
    #output_raster.keystone(8, True)