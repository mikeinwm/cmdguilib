"""
Library for quickly converting a console application into a gui application.
Includes threading and queues, custom commands, and redirecting stdout.
"""

import queue
import threading
from tkinter import *
from tkinter import ttk
from tkinter import scrolledtext


class TScrolledText(scrolledtext.ScrolledText):
    def __init__(self, master, **options):
        scrolledtext.ScrolledText.__init__(self, master, **options)
        self.text_queue = queue.Queue()
        self.update_me()

    def write(self, line):
        self.text_queue.put(line)

    def clear(self):
        self.config(state="normal")
        self.delete(1.0, END)
        self.config(state="disabled")

    def flush(self):
        pass

    def update_me(self):
        if not self.text_queue.empty():
            line = self.text_queue.get_nowait()
            self["state"] = "normal"
            self.insert(END, str(line))
            self["state"] = "disabled"
            self.see(END)
            self.update_idletasks()
        else:
            pass
        self.after(100, self.update_me)


class CmdGUI:
    """
    Handles gui creation and interactions
    """
    def __init__(self):
        self.commands = {}  # TODO: Disable most commands option for running a loop
        self.defaults = {}
        self.wintitle = "CmdGUI Window"

        # Create main window # TODO: Themes and Styles, minimize to tray?
        self.root = Tk()
        self.root.title(self.wintitle)
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
        self.txtoutput = TScrolledText(self.outframe, wrap="word", state="disabled")
        self.txtoutput.grid(column=0, row=0, sticky=(N, W, E, S))

        # Create Text input widget
        self.txtinput = Text(self.inframe, height=4, wrap="word")
        self.txtinput.grid(column=0, row=0, sticky=(N, W, E, S))

        # Create enter/submit button
        self.enterbutton = Button(self.inframe, text="Enter", command=self.onenter)
        self.enterbutton.grid(column=1, row=0, sticky=(N, W, E, S))

        # Redirect stdout to gui
        sys.stdout = self.txtoutput

    def onenter(self):  # TODO: Run if Enter key pressed, cmd params, default commands, cmd creation
        """
        Sends the value (function) of key (command) to be run by proc_exec.
        """
        cmd = self.txtinput.get("1.0", "end -1c").strip().lower()
        if cmd in self.commands.keys():
            self.proc_exec(self.commands[cmd])
        elif cmd in self.defaults.keys():
            self.proc_exec(self.defaults[cmd])
        else:
            print("Invalid Command")  # TODO: Secondary error display using label

    def proc_exec(self, task):
        """
        Runs designated function with threading
        """
        tp = threading.Thread(target=task)
        tp.start()


if __name__ == "__main__":
    from time import strftime

    demo = CmdGUI()
    demo.wintitle = "CmdGUI Demo"
    stop = False

    def infloop_test():  # TODO: Only delete and update changed values
        global stop
        if not stop:
            demo.txtoutput.clear()
            print(strftime("%c",))
            print("Type stop and press enter to stop the loop.")
            demo.txtoutput.after(1000, infloop_test)
        else:
            print("Time loop has been stopped.")
            stop = False

    def end_loop():
        global stop
        stop = True

    def forloop_test():
        for i in range(10):
            print("This is step " + str(i) + ".")

    def single_test():
        print("This is a single line of text.")

    demo.commands['infloop'] = infloop_test
    demo.commands["stop"] = end_loop
    demo.commands['forloop'] = forloop_test
    demo.commands['single'] = single_test

    demo.root.mainloop()
