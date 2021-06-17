import tkinter as tk
import matplotlib.pyplot as plt
import matplotlib
import math
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Gui(object):
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("some application")

        # menu left
        self.menu_left = tk.Frame(self.root, width=150, bg="#ababab")
        self.menu_left_upper = tk.Frame(self.menu_left, width=150, height=150, bg="red")
        self.menu_left_lower = tk.Frame(self.menu_left, width=150, bg="blue")

        self.test = tk.Label(self.menu_left_upper, text="test")
        self.test.pack()

        self.menu_left_upper.pack(side="top", fill="both", expand=True)
        self.menu_left_lower.pack(side="top", fill="both", expand=True)

        # right area
        self.some_title_frame = tk.Frame(self.root, bg="#dfdfdf")

        self.some_title = tk.Label(self.some_title_frame, text="some title", bg="#dfdfdf")
        self.some_title.pack()

        self.canvas_area = tk.Canvas(self.root, width=500, height=400, background="#ffffff")
        self.canvas_area.grid(row=1, column=1)

        # status bar
        self.status_frame = tk.Frame(self.root)
        self.status = tk.Label(self.status_frame, text="this is the status bar")
        self.status.pack(fill="both", expand=True)

        self.menu_left.grid(row=0, column=0, rowspan=2, sticky="nsew")
        self.some_title_frame.grid(row=0, column=1, sticky="ew")
        self.canvas_area.grid(row=1, column=1, sticky="nsew")
        self.status_frame.grid(row=2, column=0, columnspan=2, sticky="ew")

        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        self.root.mainloop()


def updateGraph():
    """Example function triggered by Tkinter GUI to change matplotlib graphs."""
    global currentGraph
    # Clear all graphs drawn in figure
    plt.clf()
    y = []
    if currentGraph == "sin":
        for i in x:
            y.append(math.cos(i))
        currentGraph = "cos"
    else:
        for i in x:
            y.append(math.sin(i))
        currentGraph = "sin"
    plt.plot(x, y)
    fig.canvas.draw()


if __name__ == "__main__":

    # This defines the Python GUI backend to use for matplotlib
    matplotlib.use('TkAgg')

    # Initialize an instance of Tk
    root = tk.Tk()

    # Initialize matplotlib figure for graphing purposes
    fig = plt.figure(1)

    # Special type of "canvas" to allow for matplotlib graphing
    canvas = FigureCanvasTkAgg(fig, master=root)
    plot_widget = canvas.get_tk_widget()

    # Example data (note: default calculations for angles are in radians)
    x = []
    for i in range(0, 500):
        x.append(i / 10)
    y = []
    for i in x:
        y.append(math.sin(i))
    plt.plot(x, y)

    currentGraph = "sin"

    # Add the plot to the tkinter widget
    plot_widget.grid(row=0, column=0)
    # Create a tkinter button at the bottom of the window and link it with the updateGraph function
    tk.Button(root, text="Update", command=updateGraph).grid(row=1, column=0)

    root.mainloop()
