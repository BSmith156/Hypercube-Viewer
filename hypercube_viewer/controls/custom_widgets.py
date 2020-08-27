import tkinter as tk

# Set button to activebackground when hovered over
class HoverButton(tk.Button):
    def __init__(self, master, **kwargs):
        tk.Button.__init__(self, master = master, **kwargs)
        self.background = self["bg"]
        self.foreground = self["fg"]
        self.bind("<Enter>", self.mouse_enter)
        self.bind("<Leave>", self.mouse_leave)
    
    def mouse_enter(self, e):
        self["bg"] = self["activebackground"]
        self["fg"] = self["activeforeground"]
    
    def mouse_leave(self, e):
        self["bg"] = self.background
        self["fg"] = self.foreground

# Entry box with placeholder text
class PlaceholderEntry(tk.Entry):
    def __init__(self, master, placeholder, **kwargs):
        tk.Entry.__init__(self, master = master, **kwargs)
        self.placeholder = placeholder
        self.is_placeholder = False
        self.bind("<FocusIn>", self.remove_placeholder)
        self.bind("<FocusOut>", self.add_placeholder)
    
    def remove_placeholder(self, e):
        if self.is_placeholder:
            self.delete(0, "end")
            self["fg"] = "black"
            self.is_placeholder = False
    
    def add_placeholder(self, e):
        if self.get() == "":
            self.insert(0, self.placeholder)
            self["fg"] = "grey"
            self.is_placeholder = True

class ScrollableFrame(tk.Frame):
    def __init__(self, master, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)
        self.canvas = tk.Canvas(self, bd = 0, bg = "#333333", width = 233, highlightthickness = 0)
        self.frame = tk.Frame(self.canvas, bg = "#333333")
        self.scroll = tk.Scrollbar(self, orient = "vertical", command = self.canvas.yview, relief = "flat", bg = "#333333")

        self.canvas.configure(yscrollcommand = self.scroll.set)

        self.scroll.pack(side = "left", fill = "y")
        self.canvas.pack(side = "left", fill = "both", expand = True)
        self.canvas.create_window((0, 0), window = self.frame, anchor = "nw", tags = "self.frame")

        self.frame.bind("<Configure>", self.configure_callback)

    def configure_callback(self, e):
        self.canvas.configure(scrollregion = self.canvas.bbox("all"))

# Hover button for rotation list
class RotationItem(HoverButton):
    def __init__(self, master, rotation, rotation_list, view):
        HoverButton.__init__(self, master, text = f"Axes: {rotation[0][0]},{rotation[0][1]} - Speed: {rotation[2]}", font = "Verdana 12", fg = "white", activeforeground = "red", activebackground = "#333333", bg = "#333333", relief = "flat")
        self.rotation = rotation
        self.rotation_list = rotation_list
        self.view = view
        self.bind("<Button-1>", self.delete)
    
    def delete(self, e):
        self.rotation_list.remove(self.rotation)
        self.view.update_list()