"""
This is the main file for Animation creator.

Animation creator is a simple tools for create the
2D skeleton animation and export it to GIF or atlas.
"""

import tkinter

#class Project:
#    """Model in our MVC framework"""

#class View:
#    pass

#class Controller:
#    pass

class MainWindow(tkinter.Tk):
    """This is main window of the aplication. It contains static UI."""
    def __init__(self):
        tkinter.Tk.__init__(self)
        self.title("Animation creator")
        self._init_menu()

    def _init_menu(self):
        self.main_menu = tkinter.Menu(self)
        self.config(menu=self.main_menu)

        file_menu = tkinter.Menu(self.main_menu)
        file_menu.add_command(label="Open Project")
        file_menu.add_command(label="Save Project")
        file_menu.add_command(label="Exit", command=self.quit)
        self.main_menu.add_cascade(label="File", menu=file_menu)

if __name__ == "__main__":
    APP = MainWindow()
    APP.mainloop()
