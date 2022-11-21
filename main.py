import tkinter as tk
import util.color as color
import ui.app as ui

app_title = "Finite Impulse Response Filter Design"
icon_path = "assets/waveform_icon.png"
size = "500x200"

def main():
    ## App Setup
    root = tk.Tk()
    root.title(app_title)
    root.geometry(size)
    app_icon = tk.PhotoImage(file=icon_path)
    root.configure(bg=color.bg, padx=20, pady=20)
    root.iconphoto(False, app_icon)

    ui.run_app(root)
    
    root.mainloop()

if __name__ == '__main__':
    main()