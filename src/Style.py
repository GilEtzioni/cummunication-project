import ttkbootstrap as ttk
from ttkbootstrap.constants import INFO

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
    slider_name1="Binary Slider",
    slider_name2="Frequency Slider",
    slider_name3="BitRate Slider",
):
    apply_custom_styles()

    # store current slider values
    slider_values = {
        "num_slider1": MIN_SLIDER_1,
        "num_slider2": SECOND_SLIDER_VALUES[0] if SECOND_SLIDER_VALUES else None,
        "num_slider3": THIRD_SLIDER_VALUES[0] if THIRD_SLIDER_VALUES else None,
    }

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
        # if "num_slider1" in slider_values and slider_values["num_slider1"] is not None:
        #     conf.set_volume(slider_values["num_slider1"])
        if "num_slider2" in slider_values and slider_values["num_slider2"] is not None:
            conf.set_frequency(slider_values["num_slider2"])  
        if "num_slider3" in slider_values and slider_values["num_slider3"] is not None:
            conf.set_bitrate(slider_values["num_slider3"])  


    # button
    ttk.Button(
        container_frame,
        text=second_butt_name,
        command=lambda: [set_config(), second_button_action()],
        style="Blue.TButton",
        width=25,
    ).pack(pady=10, anchor="w", side="top")

    def update_slider_label(value, label, var_name, discrete_values=None):
        if discrete_values:
            index = round(float(value))
            slider_values[var_name] = discrete_values[index]
            value = discrete_values[index]
        else:
            value = round(float(value))
            slider_values[var_name] = value
        label.config(text=f"{value}")

    sliders_config = [
        (slider_name1, (MIN_SLIDER_1, MAX_SLIDER_1), "num_slider1", None, None),
        (slider_name2, SECOND_SLIDER_VALUES, "num_slider2", None, SECOND_SLIDER_VALUES),
        (slider_name3, THIRD_SLIDER_VALUES, "num_slider3", None, THIRD_SLIDER_VALUES),
    ]

    for slider in sliders_config:
        if slider[0] is None:  # Skip rendering this slider if its name is None
            continue

        label_text, slider_range, var_name, step, discrete_values = slider
        slider_frame = ttk.Frame(container_frame)
        slider_frame.pack(anchor="w", pady=5)

        ttk.Label(slider_frame, text=label_text).pack(side="left", padx=5)

        slider_value_label = ttk.Label(slider_frame, text=str(slider_range[0] if isinstance(slider_range, tuple) else slider_range[0]), width=10)
        slider_value_label.pack(side="left", padx=5)

        if discrete_values is None:
            slider = ttk.Scale(
                slider_frame,
                from_=slider_range[0],
                to=slider_range[1],
                orient="horizontal",
                length=200,
                command=lambda value, sv=slider_value_label, vn=var_name: update_slider_label(value, sv, vn),
            )
        else:
            slider = ttk.Scale(
                slider_frame,
                from_=0,
                to=len(discrete_values) - 1,
                orient="horizontal",
                length=200,
                command=lambda value, sv=slider_value_label, vn=var_name, dv=discrete_values: update_slider_label(
                    value, sv, vn, dv
                ),
            )
        slider.pack(side="left", padx=5)
