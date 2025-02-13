import tkinter as tk
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import numpy as np
import io
import threading
config = None

def change_graph(parent_frame):
    # generate updated data
    x = np.linspace(0, 10, 100)
    return _update_graph(parent_frame, x, np.sin(x), "receiver frames", moving=True)
def create_graph(parent_frame,conf):
    global config
    config = conf
    # Generate an empty graph
    x = []
    y = []
    return _update_graph(parent_frame, x, y, "", moving=False)
maxdata=0
def _update_graph(parent_frame, x, y, title, moving=False):
    def animate():
        nonlocal y
        global maxdata
        # update the data to make the graph move
        # y = np.roll(y, -1)  # Shift data for animation
        # y[-1] = np.sin(np.pi * (np.random.rand()))  # Append a random value
        # create a new figure
        fig, ax = plt.subplots(figsize=(4, 3))  # Width = 2 inches, Height = 1.5 inches
        ax.plot(config.graphData)
        ax.set_title(title, fontsize=8)
        ax.set_xlabel("X-axis", fontsize=6)
        ax.set_ylabel("Y-axis", fontsize=6)
        ax.tick_params(axis='both', which='major', labelsize=6)
        maxdata= max(maxdata,np.max(config.graphData))
        ax.set_ylim(0, maxdata)
        # save the figure to an in-memory buffer
        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=100)
        buf.seek(0)
        plt.close(fig)  # close the figure to free resources

        # load the image from the buffer and update the Tkinter label
        img = Image.open(buf)
        img = ImageTk.PhotoImage(img)

        graph_label.configure(image=img)
        graph_label.image = img  # keep a reference to avoid garbage collection

        # schedule the next update
        if moving:
            parent_frame.after(20, animate)  # update every 500ms

    # initialize the graph
    fig, ax = plt.subplots(figsize=(4, 3))
    if len(x) > 0 and len(y) > 0:
        ax.plot(x, y)
    ax.set_title(title, fontsize=8)
    ax.set_xlabel("X-axis", fontsize=6)
    ax.set_ylabel("Y-axis", fontsize=6)
    ax.tick_params(axis='both', which='major', labelsize=6)

    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=100)
    buf.seek(0)
    plt.close(fig)

    img = Image.open(buf)
    img = ImageTk.PhotoImage(img)

    graph_label = tk.Label(parent_frame, image=img, bg="white")
    graph_label.image = img
    graph_label.place(relx=1.0, rely=0.5, anchor="e", x=-8, y=20)


    # start the animation if moving is enabled
    if moving:
        parent_frame.after(500, animate)

    return graph_label