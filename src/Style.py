import ttkbootstrap as ttk
from ttkbootstrap.constants import INFO
from tkinter import DoubleVar
# first Slider (binary)
MIN_SLIDER_1 = 0
MAX_SLIDER_1 = 1

# second slider values - 1000, 3000, 8000, 15000
SECOND_SLIDER_VALUES = [1000, 3000, 8000, 15000]

# Third slider values - 2, 5, 20, 50
THIRD_SLIDER_VALUES = [2, 5, 20, 50]

# css
def apply_custom_styles():
    style = ttk.Style()
    style.configure(
        "Blue.TButton",
        background="#87CEEB",  # blue color
        foreground="white",
        font=("Arial", 14, "bold"),
        padding=10,
        relief="flat",  # no border
        borderwidth=0,  # no border
    )
    style.map("Blue.TButton", background=[("active", "#B0E0E6")])  # lighter blue when active

    style.configure("GreyFrame.TFrame", background="#D3D3D3")  # grey background


def create_ui(
    # the function paramaters
    frame,
    first_button_action,
    second_button_action,
    conf,
    first_butt_name="Select",
    second_butt_name="Start",
    has_volume = True,
):
    apply_custom_styles()


    parent_frame = ttk.Frame(frame)
    parent_frame.pack(pady=20, padx=20, fill="both", expand=True)
    parent_frame.config(width=200, height=500)

    container_frame = ttk.Frame(parent_frame, padding=10, relief="solid")
    container_frame.place(x=0, y=0, width=300, height=300)

    # first button
    ttk.Button(
        container_frame,
        text=first_butt_name,
        command=first_button_action,
        style="Blue.TButton",
        width=25,
    ).pack(pady=10, anchor="w", side="top")
    
    # use the set methods from AudioConfig.py
    def set_config():
        if has_volume:
            conf.set_volume(volume.get())
        conf.set_bitrate(int(bitrate.get()))
        conf.set_frequency(int(frequency.get()))



    # button
    ttk.Button(
        container_frame,
        text=second_butt_name,
        command=lambda: [set_config(), second_button_action()],
        style="Blue.TButton",
        width=25,
    ).pack(pady=10, anchor="w", side="top")
    def add_dropdown(name:str, options:list, default:float|int):
        drop_frame = ttk.Frame(container_frame)
        drop_frame.pack( anchor="w", side="top",fill="both")
        label = ttk.Label( drop_frame , text = name ) 
        label.pack(pady=10, anchor="w", side="left")
        var = DoubleVar()
        var.set(default)
        drop = ttk.OptionMenu(drop_frame, var ,var.get(),*options)
        drop.pack(pady=10, anchor="w", side="right")
        return var
    if has_volume:
        volume = add_dropdown("Volume:", [x/10.0 for x in range(0,11)], 0.5)
    bitrate = add_dropdown("Bitrate (Bps):", [2, 5, 10], 5)
    frequency = add_dropdown("Start Frequency (Hz):", [300,1000,2000,10000], 2000)
    set_config()
   