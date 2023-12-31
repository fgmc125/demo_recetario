import tkinter as tk

import ui
import datos
import config

def main():
    # crear db y tabla si no existe
    datos.create_if_not_exists()

    root = tk.Tk()
    root.iconbitmap(default=config.icono)
    root.title("TODO")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    ui.Principal(root).grid(sticky=tk.NSEW)
    root.mainloop()

if __name__ == "__main__":
    main()