import tkinter as tk
from hypercube_viewer.controls.custom_widgets import PlaceholderEntry
from hypercube_viewer.controls.custom_widgets import HoverButton
from hypercube_viewer.controls.custom_widgets import ScrollableFrame
from hypercube_viewer.controls.custom_widgets import RotationItem
from tkinter import messagebox
from math import radians

class RotationControls():
    def __init__(self, parent, options, axis_options, shape):

        self.shape = shape

        # Rotation Controls
        self.rotation_frame = tk.Frame(options, bg = "#333333")
        self.rotation_frame.grid(row = 2)

        self.rotation_label = tk.Label(self.rotation_frame, text = "Rotate", font = "Verdana 15", fg = "white", bg = "#333333")
        self.rotation_label.pack(padx = 6, pady = (10, 5), anchor = "w")

        self.axis1 = tk.StringVar()
        self.axis1.set("Axis")
        self.rotation_axis1 = tk.OptionMenu(self.rotation_frame, self.axis1, *axis_options)
        self.rotation_axis1.config(font = "Verdana 12", width = 4, indicatoron = False, bg = "#999999", activebackground = "#f8f8f8", highlightthickness = 0, relief = "sunken", bd = 0)
        self.rotation_axis1.pack(padx = (10, 0), pady = (0, 10), side = "left", fill = "y")

        self.axis2 = tk.StringVar()
        self.axis2.set("Axis")
        self.rotation_axis2 = tk.OptionMenu(self.rotation_frame, self.axis2, *axis_options)
        self.rotation_axis2.config(font = "Verdana 12", width = 4, indicatoron = False, bg = "#999999", activebackground = "#f8f8f8", highlightthickness = 0, relief = "sunken", bd = 0)
        self.rotation_axis2.pack(padx = (0, 9), pady = (0, 10), side = "left", fill = "y")

        self.rotation_entry = PlaceholderEntry(self.rotation_frame, "Speed", font = "Verdana 12", relief = "flat", width = 8)
        self.rotation_entry.add_placeholder(None)
        self.rotation_entry.pack(padx = (1, 0), pady = (0, 10), side = "left", fill = "y")

        self.rotation_button = HoverButton(self.rotation_frame, text = "Apply", font = "Verdana 12", relief = "flat", bg = "#999999", activebackground = "#f8f8f8")
        self.rotation_button.bind("<Button-1>", self.rotation_callback)
        self.rotation_button.pack(pady = (0, 10), padx = (0, 10))

        # Rotation View
        self.view_frame = tk.LabelFrame(parent, text = "Rotations", font = "Verdana 20", fg = "white", bg = "#333333", relief = "raised")
        self.view_frame.pack(padx = 10, pady = (5, 10), fill = "both", expand = "true")
        
        self.list_frame = ScrollableFrame(self.view_frame)
        self.list_frame.pack(pady = (14, 10), fill = "y", expand = True)
        self.update_list()
    
    def rotation_callback(self, e):
        axis1 = self.axis1.get()
        axis2 = self.axis2.get()
        speed = self.rotation_entry.get()
        if axis1 == "Axis" or axis2 == "Axis":
            messagebox.showerror("Couldn't add rotation!", "Please select two axes to rotate.")
            return "break"
        if axis1 == axis2:
            messagebox.showerror("Couldn't add rotation!", "Please select two different axes.")
            return "break"
        if not speed.isnumeric():
            messagebox.showerror("Couldn't add rotation!", "Please set speed to a positive integer.")
            return "break"
        if int(speed) > 180:
            confirm = messagebox.askokcancel("Are you sure?", f"Speed is measured in degrees per second. {speed} is more than half a revolution per second.", icon = "warning")
            if not confirm:
                return "break"
        radians_speed = radians(int(speed) / 50)
        for rotation in self.shape.rotations:
            if rotation[0][0] == int(axis1) and rotation[0][1] == int(axis2):
                self.shape.rotations.remove(rotation)
                break
        self.shape.rotations.append([(int(axis1), int(axis2)), radians_speed, speed])
        self.update_list()
        return "break"

    # Change axis options when dimension changed
    def update_options(self, dimension):
        self.rotation_axis1["menu"].delete(0, "end")
        self.rotation_axis2["menu"].delete(0, "end")
        for option in range(0, dimension):
            self.rotation_axis1["menu"].add_command(label = option, command = tk._setit(self.axis1, option))
            self.rotation_axis2["menu"].add_command(label = option, command = tk._setit(self.axis2, option))
        if self.axis1.get() != "Axis" and int(self.axis1.get()) >= dimension:
            self.axis1.set("Axis")
        if self.axis2.get() != "Axis" and int(self.axis2.get()) >= dimension:
            self.axis2.set("Axis")
    
    # Update rotation list
    def update_list(self):
        row = 0
        for widget in self.list_frame.frame.winfo_children():
            widget.destroy()
        for rotation in self.shape.rotations:
            new_item = RotationItem(self.list_frame.frame, rotation, self.shape.rotations, self)
            new_item.grid(row = row, padx = (3, 0), sticky = "w")
            row += 1