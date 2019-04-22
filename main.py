import tkinter

class Project: # Model class
    pass

class View:
    pass

class Controller:
    pass

class MainWindow(tkinter.Tk):
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
    app = MainWindow()
    app.mainloop()
