import tkinter as tk
from hypercube_viewer.display.projection import project_2D

class Display():
    def __init__(self, parent, zoom):
        
        self.zoom = zoom

        # Create canvas
        self.canvas = tk.Canvas(parent, bg = "#1E1E1E", highlightthickness = 0)
        self.canvas.pack(fill = "both", expand = True)
    
    def draw_shape(self, shape):

        projected_points = project_2D(shape.points)

        # Draw edges
        self.canvas.delete("all")
        for edge in shape.edges:
            self.canvas.create_line(projected_points[edge[0]][0] * self.zoom, projected_points[edge[0]][1] * self.zoom,
                                    projected_points[edge[1]][0] * self.zoom, projected_points[edge[1]][1] * self.zoom,
                                    fill = "white")
        self.canvas.move("all", self.canvas.winfo_width() / 2, self.canvas.winfo_height() / 2)