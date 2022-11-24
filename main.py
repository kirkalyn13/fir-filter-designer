import tkinter as tk
import util.color as color
import ui.app as ui

APP_TITLE = "Finite Impulse Response Filter Design"
ICON_PATH = "assets/waveform_icon.png"
SIZE = "600x500"

def main():
    ## App Setup
    root = tk.Tk()
    root.title(APP_TITLE)
    root.geometry(SIZE)
    app_icon = tk.PhotoImage(file=ICON_PATH)
    root.configure(bg=color.bg, padx=20, pady=20)
    root.iconphoto(False, app_icon)

    ## Render App
    ui.run_app(root, SIZE)
    root.mainloop()

if __name__ == '__main__':
    main()