"""
Library for quickly converting a console application into a gui application.
Includes threading and queues, custom commands, and redirecting stdout.
All non-looping processes wait for printing to complete.
"""

import queue
import threading
from tkinter import *
from tkinter import ttk

# Create queue which holds items to be printed to gui textbox
print_queue = queue.Queue()

# Create queue which holds code to be processed
process_queue = queue.Queue()


class Redirect:
    """
    Redirects the text output from print statements, and places them in print queue
    """
    def __init__(self, target):

        self.output = target

    @staticmethod
    def write(txt):
        """
        Inserts captured output into text area on gui
        """
        global print_queue
        print_queue.put(str(txt))
        # self.output.insert(END, str(txt)) # print to gui without threading or queue

    def flush(self):  # TODO: Handle stdout and stderr functions
        pass


class CmdGUI:
    """
    Handles gui creation and interactions
    Arg: commands = dictionary of text command : code to run
    """
    def __init__(self, commands):

        self.commands = commands

        # Create main window # TODO: Themes and Styles
        self.root = Tk()
        self.root.title("CmdGUI Window")  # TODO: Set title with argument
        self.root.grid()
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Create Frame covering entire window (for styling, no practical use)
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
        self.txtframe = Redirect(self.txtoutput)
        sys.stdout = self.txtframe

    def onenter(self):  # TODO: Run if Enter key pressed, loop manager, cmd params, clear box, default commands
        """
        Places the code (value) of the given command (key) into the process queue
        """
        global process_queue
        cmd = self.txtinput.get("1.0", "end -1c").strip().lower()
        if cmd in self.commands.keys():
            process_queue.put(self.commands[cmd]())
        else:
            print("Invalid Command")  # TODO: Secondary error display using label

    def print_manager(self):
        """
        Prints all lines in the print queue, then calls the process manager via process thread
        """
        global print_queue

        try:
            for line in iter(print_queue.get, None):
                self.txtframe.output.insert(END, str(line))
            self.root.after(1000, self.printer_thread())
        except print_queue.empty():
            self.root.after(1000, self.process_thread())

    def process_manager(self):
        """
        Executes a single process in the process queue then waits for print manager to be done
        """
        global process_queue

        try:
            proc = process_queue.get()
            exec(proc)
            proc.task_done()
            self.root.after(1000, self.printer_thread())
        except process_queue.empty():
            pass

    def printer_thread(self):
        """
        Starts a thread for print_manager
        """
        t = threading.Thread(target=self.print_manager)
        t.start()

    def process_thread(self):
        """
        Starts a thread for process_manager
        """
        t = threading.Thread(target=self.process_manager)
        t.start()


if __name__ == "__main__":  # TODO: Create demo app here
    app = CmdGUI(commands={})
    app.root.mainloop()
