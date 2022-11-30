import tkinter as tk
from PIL import ImageTk, Image
import util.color as color
import util.font as font
import util.error as error
import filter.fir as fir

TITLE_TEXT = "Finite Impulse Response\nFilter Design"
LOGO_PATH = "./assets/waveform_logo.png"
EXPANDED_SIZE = "800x500"

FILTERS = fir.FILTERS
WINDOW_TYPES = fir.WINDOW_TYPES

## Render App UI
def run_app(window, size):
    ## Setup UI
    global root
    global original_size
    root = window
    original_size = size

    ## Setup Filters
    global filter_select
    filter_select = tk.StringVar(root)
    filter_select.set(FILTERS[0])
    filter_select.trace("w", adjust_by_filter)

    ## Setup window types
    global window_select
    window_select = tk.StringVar(root)
    window_select.set(WINDOW_TYPES[0])

    ## Setup inputs
    global input_sampling_freq
    global input_filter_taps
    global input_lower_cutoff
    global input_higher_cutoff

    ## Title
    app_logo = ImageTk.PhotoImage(Image.open(LOGO_PATH))
    tk.Label(root, text=TITLE_TEXT, bg=color.bg, fg=color.text_light, font=font.title, padx=10).grid(row=0, column=0, pady=5)
    logo = tk.Label(root, image=app_logo, bg=color.bg, pady=5)
    logo.image_names = [app_logo]
    logo.grid(row=0, column=1, sticky="E")

    ## Filter Type
    tk.Label(root, text="Filter Type:", bg=color.bg, fg=color.text_light, font=font.text, padx=10).grid(row=1, column=0, sticky="W", pady=5)
    tk.OptionMenu(root, filter_select, *FILTERS).grid(row=1, column=1, sticky="E")

    ## Window Type
    tk.Label(root, text="Window Type:", bg=color.bg, fg=color.text_light, font=font.text, padx=10).grid(row=2, column=0, sticky="W", pady=5)
    tk.OptionMenu(root, window_select, *WINDOW_TYPES).grid(row=2, column=1, sticky="E")

    ## Sampling Frequency
    tk.Label(root, text="Sampling Frequency (Hz):", bg=color.bg, fg=color.text_light, font=font.text, padx=10).grid(row=3, column=0, sticky="W", pady=5)
    input_sampling_freq = tk.Entry(root)
    input_sampling_freq.grid(row=3, column=1, sticky="E")

    ## Filter Taps
    tk.Label(root, text="Filter Taps:", bg=color.bg, fg=color.text_light, font=font.text, padx=10).grid(row=4, column=0, sticky="W", pady=5)
    input_filter_taps = tk.Entry(root)
    input_filter_taps.grid(row=4, column=1, sticky="E")

    ## Lower Cutoff
    tk.Label(root, text="Lower Cutoff (Hz):", bg=color.bg, fg=color.text_light, font=font.text, padx=10).grid(row=5, column=0, sticky="W", pady=5)
    input_lower_cutoff = tk.Entry(root)
    input_lower_cutoff.grid(row=5, column=1, sticky="E")

    ## Higher Cutoff
    tk.Label(root, text="Higher Cutoff (Hz):", bg=color.bg, fg=color.text_light, font=font.text, padx=10).grid(row=6, column=0, sticky="W", pady=5)
    input_higher_cutoff = tk.Entry(root)
    input_higher_cutoff.grid(row=6, column=1, sticky="E")

    ## Buttons
    tk.Button(root, text='DESIGN', command=design_filter, width=10, font=font.text, bg=color.accent, fg=color.text_dark).grid(row=7, column=0, padx=20, pady=10)
    tk.Button(root, text='RESET', command=reset, width=10,  font=font.text, bg=color.accent, fg=color.text_dark).grid(row=7, column=1, padx=20, pady=10)

## Design Filter
def design_filter():
    ## Validate Inputs
    is_invalid = validate_input()
    if is_invalid:
        return

    ## Get Input Values
    filter_type = filter_select.get()
    window_type = window_select.get()
    sampling_freq = int(input_sampling_freq.get())
    filter_taps = int(input_filter_taps.get())
    lower_cutoff = int(input_lower_cutoff.get())
    higher_cutoff = int(input_higher_cutoff.get())

    filter_coefficients = fir.window_method(filter_type, window_type, sampling_freq, filter_taps, lower_cutoff, higher_cutoff)
    show_coefficients(filter_coefficients)

## Display Coefficients on Listbox
def show_coefficients(coefficients):
    root.geometry(EXPANDED_SIZE)

    global coefficients_label
    global coefficients_list
    
    coefficients_label = tk.Label(root, text="Design Filter\nCoefficients:", bg=color.bg, fg=color.text_light, font=font.text, padx=10)
    coefficients_label.grid(row=0, column=2)
    coefficients_list = tk.Listbox(root, width=30)
    coefficients_list.grid(row=1, column=2, rowspan=7, sticky="NS", padx=50)

    for c in coefficients:
        coefficients_list.insert(tk.END, str('{:0.5e}'.format(c)))

## ===== INPUT VALIDATION ===== ##
## Validate Input
def validate_input():
    is_invalid = check_empty_inputs()
    if is_invalid == False:
        is_invalid = check_integer_inputs()
    if is_invalid == False:
        is_invalid = check_filter_taps()
    return is_invalid

## Check for Empty Inputs 
def check_empty_inputs():
    if input_sampling_freq.get() == "" or input_filter_taps.get() == "" or input_lower_cutoff.get() == "" or input_higher_cutoff.get() == "":
        error.warning("Incomplete Input", "Please make sure all fields are complete.")
        return True
    return False

## Check for Non-Integer Inputs 
def check_integer_inputs():
    if input_sampling_freq.get().isnumeric() == False or input_filter_taps.get().isnumeric() == False \
         or input_lower_cutoff.get().isnumeric() == False or input_higher_cutoff.get().isnumeric() == False :
        error.warning("Invalid Input", "Input must be numeric values.")
        return True
    return False

## Check if filter taps is odd 
def check_filter_taps():
    if int(input_filter_taps.get()) % 2 == 0 :
        error.warning("Invalid Input", "Filter taps must be odd.")
        return True
    if int(input_filter_taps.get()) < 3 :
        error.warning("Invalid Input", "Minimum value of 3 for filter taps.")
        return True
    return False

## ===== ADJUST CUTOFF BY FILTER TYPE ===== ##
## Adjust by Filter Type
def adjust_by_filter(*args):
    if filter_select.get() == "Low Pass":
        set_entry(0, input_higher_cutoff)
    elif filter_select.get() == "High Pass":
        set_entry(0, input_lower_cutoff)

## ===== RESET APP UI ===== ##
## Reset Fields
def reset():
    hide_coefficients()
    filter_select.set(FILTERS[0])
    window_select.set(WINDOW_TYPES[0])
    set_entry("", input_sampling_freq)
    set_entry("", input_filter_taps)
    set_entry("", input_lower_cutoff)
    set_entry("", input_higher_cutoff)

## Hide Coefficient Gridbox
def hide_coefficients():
    coefficients_label.grid_forget()
    coefficients_list.grid_forget()
    root.geometry(original_size)

## ===== HELPER FUNCTIONS ===== ##
## Set Entry
def set_entry(text, entry):
    entry.delete(0,tk.END)
    entry.insert(0,text)
    