import tkinter

import customtkinter

from views.components.CanvasInGlowingButton import CanvasInGlowingButton
from views.components.CodeInput import CodeInput
from views.components.DragableFrameAdministrator import DraggableFrameAdministrator
from views.components.DraggableFrame import DraggableFrame
from views.components.Plot import Plot
from views.components.PoweredImage import PoweredImage
from views.components.ResponsibleLabel import ResponsiveLabel

app = customtkinter.CTk()
app.title('preview')

window_manager = DraggableFrameAdministrator(app)
window_manager.start_change_state_detection()

responsive_label = ResponsiveLabel(app, text="Imagine if you have a very long text, i could be a problem because in normal customtkinter it could rendered outside the window :/ [RESIZE DE WINDOW TO SEE ME IN ACTION]")
responsive_label.pack(padx=2, pady=2, fill="x")


base_frame = customtkinter.CTkFrame(app)
base_frame.pack(fill="both", expand=True)

interface_plot = Plot(base_frame, enable_capture_motion_callback=True, plot_drag_cursor='dot', camera_corner_align=True)
interface_plot.pack(fill="both", expand=True)

def bind_rendering():
    interface_plot.canvas.create_text(100, 80, text="Powered Image example", fill='white', anchor="nw")
    interface_plot.canvas.create_text(100, 310, text="Image picked from https://pixabay.com/users/betidraws-23986844/", fill='white', anchor="nw")

first_example_frame = customtkinter.CTkFrame(interface_plot.canvas, width=400, height=400)
first_example_frame.place(x=100, y=100)

powered_image = PoweredImage(first_example_frame, './resources/images/betidraws-halloween-9079096_1280.jpg')
powered_image.pack(fill="both", expand=True, padx=5, pady=5)

a_draggable_frame = DraggableFrame(app)
window_manager.register_window(a_draggable_frame)
a_draggable_frame.open_window()

make_python_label_window = customtkinter.CTkLabel(a_draggable_frame.content_frame, text="It time to make something cool using python")
make_python_label_window.pack(padx=2, pady=2)

code_editor = CodeInput(a_draggable_frame.content_frame, language="python")
code_editor.pack(padx=2, pady=2, fill="both", expand=True)
code_editor.register_code("""
def render():
    print("The beauty of love")
    
render()
""")

def print_code():
    print(code_editor.entry.get("1.0", tkinter.END))

canvas_in_glowing_button = CanvasInGlowingButton(a_draggable_frame.content_frame, text="this is a glowing button that prints the code in console", click_order=print_code)
canvas_in_glowing_button.draw_out_corners(5,5,5,5)
canvas_in_glowing_button.pack(padx=2, pady=2, fill="x")

interface_plot.register_dragging_callback(bind_rendering)

app.mainloop()
