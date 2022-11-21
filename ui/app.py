import tkinter as tk
import util.color as color
import util.font as font

title_text = "Finite Impulse Response Filter Design"
filters = ["High Pass", "Low Pass", "Band Pass", "Band Stop"]

def run_app(window):
    global root
    root = window

    tk.Label(root, text=title_text, bg=color.bg, fg=color.text, font=font.title, padx=10).grid(row=0, column=0)

    global filter_select
    filter_select = tk.StringVar(root)
    filter_select.set(filters[0])

    tk.OptionMenu(root, filter_select, *filters).grid(row=1, column=0)

    tk.Button(root, text='Select', command=select_filter, width=8, font=font.text, bg=color.accent, fg=color.text).grid(row=2, column=0, pady=5)

def select_filter():
    selected_filter = filter_select.get()
    print(f'Selected Filter: {selected_filter}')