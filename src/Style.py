import ttkbootstrap as ttk
from ttkbootstrap.constants import INFO


def apply_custom_styles():
    # css color, border, and etc
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
    frame,
    first_button_action,
    second_button_action,
    first_butt_name="Select",
    second_butt_name="Start",
    slider_name1="Slider 1",
    slider_name2="Slider 2",
    slider_name3="Slider 3",
):
    apply_custom_styles()

    # create a parent frame (hold the container_frame and graph)
    parent_frame = ttk.Frame(frame)
    parent_frame.pack(pady=20, padx=20, fill="both", expand=True)
    parent_frame.config(width=200, height=500)  # Ensure the parent frame is large enough

    # place the container frame
    container_frame = ttk.Frame(parent_frame, padding=10, relief="solid")
    container_frame.place(x=0, y=0, width=300, height=300)

    # add a label inside the container frame (for visibility)
    ttk.Label(container_frame).pack()

    # first button
    ttk.Button(
        container_frame,
        text=first_butt_name,
        command=first_button_action,
        style="Blue.TButton",
        width=25,
    ).pack(pady=10, anchor="w", side="top")

    # second button
    ttk.Button(
        container_frame,
        text=second_butt_name,
        command=second_button_action,
        style="Blue.TButton",
        width=25,
    ).pack(pady=10, anchor="w", side="top")

    # update the displayed value of the sliders
    def update_slider_label(slider, label):
        value = slider.get()
        label.config(text=f"{value:.1f}")

    # sliders
    for i, (label_text, slider_range) in enumerate(
        [
            (slider_name1, (0, 100)),
            (slider_name2, (0, 50)),
            (slider_name3, (1, 10)),
        ]
    ):
        slider_frame = ttk.Frame(container_frame)
        slider_frame.pack(anchor="w", pady=5)

        ttk.Label(slider_frame, text=label_text).pack(side="left")
        slider_value = ttk.Label(slider_frame, text=str(slider_range[0]), width=5)
        slider_value.pack(side="left", padx=5)
        ttk.Label(slider_frame, text=str(slider_range[0])).pack(side="left")

        slider = ttk.Scale(
            slider_frame,
            from_=slider_range[0],
            to=slider_range[1],
            orient="horizontal",
            length=200,
        )
        slider.pack(side="left", padx=5)
        ttk.Label(slider_frame, text=str(slider_range[1])).pack(side="left")
        slider.config(command=lambda value, sv=slider_value: update_slider_label(slider, sv))
