"""
Library for quickly converting a console application to a gui application.
A frame for console output, and a frame for input.
"""

from tkinter import *
from tkinter import ttk
import sys


class Redirect:
    def __init__(self, target):
        self.output = target

    def write(self, txt):
        self.output.insert(END, str(txt))

    def flush(self):
        pass


class CmdGUI:
    def __init__(self, commands):

        self.commands = commands

        self.root = Tk()
        self.root.title("CmdGUI Window")
        self.root.grid()
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.mainframe = ttk.Frame(self.root, padding=(5, 5, 5, 5), borderwidth=5, relief="groove")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.mainframe.columnconfigure(0, weight=2)
        self.mainframe.rowconfigure(0, weight=2)

        self.outframe = ttk.Frame(self.mainframe, padding=(3, 3, 3, 3))
        self.outframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.outframe.columnconfigure(0, weight=2)
        self.outframe.rowconfigure(0, weight=2)

        self.inframe = ttk.Frame(self.mainframe, padding=(3, 3, 3, 3))
        self.inframe.grid(column=0, row=1, sticky=(N, W, E, S))
        self.inframe.columnconfigure(0, weight=2)
        self.inframe.rowconfigure(0, weight=2)

        self.txtoutput = Text(self.outframe, wrap="word")
        self.txtoutput.grid(column=0, row=0, sticky=(N, W, E, S))

        self.txtinput = Text(self.inframe, height=4, wrap="word")
        self.txtinput.grid(column=0, row=0, sticky=(N, W, E, S))

        self.enterbutton = Button(self.inframe, text="Enter", command=self.onenter)
        self.enterbutton.grid(column=1, row=0, sticky=(N, W, E, S))

        txtframe = Redirect(self.txtoutput)
        sys.stdout = txtframe


    def onenter(self):
        cmd = self.txtinput.get("1.0", "end -1c").strip().lower()
        if cmd in self.commands.keys():
            exec(self.commands[cmd]())
        else:
            print("Invalid Command")



if __name__ == "__main__":
    app = CmdGUI(commands={})
    app.root.mainloop()
