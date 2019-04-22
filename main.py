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

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
