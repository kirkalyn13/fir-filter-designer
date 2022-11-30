import tkinter as tk
import util.color as color
import util.constants as constants
import ui.app as ui


def main():
    ## App Setup
    root = tk.Tk()
    root.title(constants.APP_TITLE)
    root.geometry(constants.ORIGINAL_SIZE)
    app_icon = tk.PhotoImage(file=constants.LOGO_PATH)
    root.configure(bg=color.bg, padx=20, pady=20)
    root.iconphoto(False, app_icon)

    ## Render App
    ui.run_app(root)
    root.mainloop()

if __name__ == '__main__':
    main()