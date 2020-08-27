import tkinter as tk
from tkinter import messagebox
from hypercube_viewer.controls.custom_widgets import HoverButton
from hypercube_viewer.controls.custom_widgets import PlaceholderEntry

class ShapeControls():
    def __init__(self, parent, shape, display, rotation_controls):

        self.shape = shape
        self.display = display
        self.rotation_controls = rotation_controls
        self.auto_zoom = True

        # Dimensions controls
        self.dimension_frame = tk.Frame(parent, bg = "#333333")
        self.dimension_frame.grid(row = 0)

        self.dimension_label = tk.Label(self.dimension_frame, text = "Dimensions", font = "Verdana 15", fg = "white", bg = "#333333")
        self.dimension_label.pack(padx = 6, pady = (10, 5), anchor = "w")

        self.dimension_entry = PlaceholderEntry(self.dimension_frame, "Dimension", font = "Verdana 12", relief = "flat", width = 19)
        self.dimension_entry.insert(0, "3")
        self.dimension_entry.pack(padx = (10, 0), side = "left", fill = "y")

        self.dimension_button = HoverButton(self.dimension_frame, text = "Apply", font = "Verdana 12", relief = "flat", bg = "#999999", activebackground = "#f8f8f8")
        self.dimension_button.bind("<Button-1>", self.dimension_callback)
        self.dimension_button.pack(padx = (0, 10))

        # Zoom controls
        self.zoom_frame = tk.Frame(parent, bg = "#333333")
        self.zoom_frame.grid(row = 1)

        self.zoom_label_frame = tk.Frame(self.zoom_frame, bg = "#333333")
        self.zoom_label_frame.grid(row = 0)

        self.zoom_label = tk.Label(self.zoom_label_frame, text = "Zoom", font = "Verdana 15", fg = "white", bg = "#333333")
        self.zoom_label.pack(pady = (8, 2), side = "left")

        self.auto_checkbox = HoverButton(self.zoom_label_frame, text = "AUTO", width = 4, font = "Verdana 11", relief = "flat", bg = "#333333", activebackground = "#333333", activeforeground = "#f8f8f8",fg = "green")
        self.auto_checkbox.pack(padx = (2, 150), pady = (12, 2))
        self.auto_checkbox.bind("<Button-1>", self.auto_callback)

        self.zoom_control_frame = tk.Frame(self.zoom_frame, bg = "#333333")
        self.zoom_control_frame.grid(row = 1)

        self.zoom_entry = PlaceholderEntry(self.zoom_control_frame, "Zoom", font = "Verdana 12", relief = "flat", width = 19)
        self.zoom_entry.insert(0, "500")
        self.zoom_entry.pack(padx = (10, 0), side = "left", fill = "y")

        self.zoom_button = HoverButton(self.zoom_control_frame, text = "Apply", font = "Verdana 12", relief = "flat", bg = "#999999", activebackground = "#f8f8f8")
        self.zoom_button.bind("<Button-1>", self.zoom_callback)
        self.zoom_button.pack(padx = (0, 10))

    def dimension_callback(self, e):
            dimension = self.dimension_entry.get()
            if dimension.isnumeric() and int(dimension) > 0:
                if int(dimension) > 9:
                    confirm = messagebox.askokcancel("Are you sure?", "Dimensions 10 and above can take a long time to load, going too high could crash the program.", icon = "warning")
                    if not confirm:
                        return "break"
                bad_rotations = []
                for rotation in self.shape.rotations:
                    if rotation[0][0] >= int(dimension) or rotation[0][1] >= int(dimension):
                        bad_rotations.append(rotation)
                for rotation in bad_rotations:
                    self.shape.rotations.remove(rotation)
                self.shape.create_shape(int(dimension))
                self.rotation_controls.update_options(int(dimension))
                self.rotation_controls.update_list()
                if self.auto_zoom:
                    self.display.zoom = 125 * pow(2, int(dimension) - 1)
                    self.zoom_entry.delete(0, "end")
                    self.zoom_entry.insert(0, 125 * pow(2, int(dimension) - 1))
            else:
                messagebox.showerror("Couldn't set dimension!", "Please enter a positive integer.")
            return "break"
    
    def zoom_callback(self, e):
            zoom = self.zoom_entry.get()
            if zoom.isnumeric() and int(zoom) > 0:
                self.display.zoom = int(zoom)
            else:
                messagebox.showerror("Couldn't set zoom!", "Please enter a positive integer.")
            return "break"
    
    def auto_callback(self, e):
        if self.auto_zoom:
            self.auto_zoom = False
            self.auto_checkbox.foreground = "red"
        else:
            self.auto_zoom = True
            self.auto_checkbox.foreground = "green"
            self.display.zoom = 125 * pow(2, self.shape.dimensions - 1)
            self.zoom_entry.delete(0, "end")
            self.zoom_entry.insert(0, 125 * pow(2, self.shape.dimensions - 1))
        return "break"