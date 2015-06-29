from tkinter import *
import main


class Application(Frame):

    def create_widgets(self):
        self.QUIT = Button(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"] = "red"
        self.QUIT["command"] = self.quit

        self.QUIT.pack({"side": "left"})

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.create_widgets()

        liste = main.run('The Blacklist')
        self.list_to_gui(liste, 44)

    def list_to_gui(self, liste, episodes):
        l = Listbox(root, height=episodes)
        for x in liste:
            if not 'Title' in x:
                l.insert(END, x)
                l.pack()


root = Tk()
app = Application(master=root)
app.mainloop()
root.destroy()
