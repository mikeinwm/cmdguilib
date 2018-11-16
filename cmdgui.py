"""
Library for quickly converting a console application into a gui application.
"""

from tkinter import *
from tkinter import ttk
import sys


class Redirect:
    # Redirect class is the replacement for sys.stdout
    def __init__(self, target):
        self.output = target

    def write(self, txt):
        # Inserts captured output into text area on gui
        self.output.insert(END, str(txt))

    def flush(self):  # TODO: Handle stdout and stderr functions
        pass


class CmdGUI:
    # Class that handles gui creation and interactions
    def __init__(self, commands):
        # Takes commands argument as a dict of command: "code to execute" in the gui
        self.commands = commands

        # Create main window # TODO: Themes and Styles
        self.root = Tk()
        self.root.title("CmdGUI Window")  # TODO: Set title with argument
        self.root.grid()
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Create Frame covering entire window
        self.mainframe = ttk.Frame(self.root, padding=(5, 5, 5, 5), borderwidth=5, relief="groove")
        self.mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.mainframe.columnconfigure(0, weight=2)
        self.mainframe.rowconfigure(0, weight=2)

        # Create Frame containing output text area
        self.outframe = ttk.Frame(self.mainframe, padding=(3, 3, 3, 3))
        self.outframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.outframe.columnconfigure(0, weight=2)
        self.outframe.rowconfigure(0, weight=2)

        # Create Frame containing input text area
        self.inframe = ttk.Frame(self.mainframe, padding=(3, 3, 3, 3))
        self.inframe.grid(column=0, row=1, sticky=(N, W, E, S))
        self.inframe.columnconfigure(0, weight=2)
        self.inframe.rowconfigure(0, weight=2)

        # Create Text output widget
        self.txtoutput = Text(self.outframe, wrap="word")
        self.txtoutput.grid(column=0, row=0, sticky=(N, W, E, S))

        # Create Text input widget
        self.txtinput = Text(self.inframe, height=4, wrap="word")
        self.txtinput.grid(column=0, row=0, sticky=(N, W, E, S))

        # Create enter/submit button
        self.enterbutton = Button(self.inframe, text="Enter", command=self.onenter)
        self.enterbutton.grid(column=1, row=0, sticky=(N, W, E, S))

        # Redirect stdout to text output frame
        txtframe = Redirect(self.txtoutput)
        sys.stdout = txtframe

    def onenter(self):  # TODO: Run if Enter key pressed
        # Runs the code (value) of the given command (key)
        cmd = self.txtinput.get("1.0", "end -1c").strip().lower()
        if cmd in self.commands.keys():
            exec(self.commands[cmd]())  # TODO: Threading for looping commands
        else:
            print("Invalid Command")


if __name__ == "__main__":  # TODO: Create demo app here
    app = CmdGUI(commands={})
    app.root.mainloop()
