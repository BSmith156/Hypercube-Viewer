import tkinter as tk
from hypercube_viewer.display.display import Display
from hypercube_viewer.display.shape import Shape
from hypercube_viewer.controls.shape_controls import ShapeControls
from hypercube_viewer.controls.rotation_controls import RotationControls

def run():
    window = tk.Tk()
    window.title("Hypercube Viewer")

    # Try is a 'fix' for no file found error while I look for a proper fix
    try:
        icon = tk.PhotoImage(file = "hypercube_viewer\\resources\\icons\\hypercube_viewer_icon.png")
        window.iconphoto(False, icon)
    except:
        pass

    # Window geometry
    width = round(window.winfo_screenwidth() / 1.25)
    height = round(window.winfo_screenheight() / 1.25)
    window.geometry(f"{width}x{height}")

    # Grid config
    window.rowconfigure(0, weight = 1)
    window.columnconfigure(1, weight = 1)

    # Create frames
    controls_frame = tk.Frame(window, bg = "#333333")
    controls_frame.grid(row = 0, column = 0, sticky = "nsew")
    options_frame = tk.LabelFrame(controls_frame, text = "Options", font = "Verdana 20", fg = "white", bg = "#333333", relief = "raised")
    options_frame.pack(padx = 10, pady = (10, 0))

    display_frame = tk.Frame(window)
    display_frame.grid(row = 0, column = 1, sticky = "nsew")

    # Create display and default cube
    display = Display(display_frame, 500)
    shape = Shape(3, [[(0, 2), 0.01047, 30]])

    # Create controls
    rotation_controls = RotationControls(controls_frame, options_frame, [0, 1, 2], shape)
    ShapeControls(options_frame, shape, display, rotation_controls)

    # Display loop
    def loop():
        shape.rotate()
        display.draw_shape(shape)
        window.after(20, loop)
    window.after(20, loop)

    window.mainloop()