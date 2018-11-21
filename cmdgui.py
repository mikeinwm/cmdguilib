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
    """
    Modified ScrolledText widget to include queue, methods to redirect stdout, and auto-disable editing.
    """
    def __init__(self, master, **options):
        scrolledtext.ScrolledText.__init__(self, master, **options)
        self.text_queue = queue.Queue()
        self.update_me()

    def write(self, line):
        """
        This replaces stdout.write
        """
        self.text_queue.put(line)

    def clear(self):
        self.config(state="normal")
        self.delete(1.0, END)
        self.config(state="disabled")

    def flush(self):
        """
        This replaces stdout.flush
        Unused by queue
        """
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
        self.commands = {"help": self.help_menu, "themes": self.list_themes}  # Commands to run when nothing is running
        self.defaults = {}  # Commands always available (during loops)
        self.loop_in_progress = False
        self.wintitle = "CmdGUI Window"

        # Create main window # TODO: Custom Themes
        self.root = Tk()
        self.root.title(self.wintitle)
        self.root.grid()
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.minsize(width=472, height=348)

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
        self.commands['clear'] = self.txtoutput.clear

        # Create label for user messages
        self.usermsg = StringVar()
        self.usermsg.set("Please enter a command. (type help for a list)")
        self.usermsg_traceid = self.usermsg.trace("w", self.reset_msg)
        self.msglabel = Label(self.inframe, textvariable=self.usermsg)
        self.msglabel.grid(column=0, row=0, sticky=(W, N, E))

        # Create Text input widget
        self.txtinput = Text(self.inframe, height=4, wrap="word")
        self.txtinput.grid(column=0, row=1, sticky=(W, E, S))
        self.txtinput.bind("<Return>", self.onenter)  # Send command when pressing enter

        # Create enter/submit button
        self.enterbutton = Button(self.inframe, text="Enter", command=self.onenter)
        self.enterbutton.grid(column=1, row=1, sticky=(N, W, E, S))

        # Redirect stdout to gui
        sys.stdout = self.txtoutput
        sys.stderr = sys.stdout

        self.txtinput.focus_set()

        self.theme = ttk.Style()
        self.theme.theme_use('alt')

    def onenter(self, event=None):  # TODO: Explore creating commands using a class
        """
        Sends the value (function) of key (command) to be run by proc_exec.
        """
        cmd = self.txtinput.get("1.0", "1.0 wordend").strip().lower()
        cmd_arg = self.txtinput.get("1.0 wordend +1c", "end -1c")
        if cmd in self.commands.keys() and not self.loop_in_progress:
            self.proc_exec(self.commands[cmd], arg=cmd_arg)
        elif cmd in self.defaults.keys():
            self.proc_exec(self.defaults[cmd], arg=cmd_arg)
        else:
            self.usermsg.set("Invalid Command")
        self.txtinput.delete(1.0, END)
        return 'break'

    def proc_exec(self, task, arg=None):
        """
        Runs designated function with threading
        """
        if arg is None or arg is "":
            tp = threading.Thread(target=task)
        else:
            tp = threading.Thread(target=task, args=(arg,))
        tp.start()

    def reset_msg(self, *args):
        """
        Changes msglabel for 3 seconds, then back.
        """
        self.usermsg.trace_vdelete("w", self.usermsg_traceid)
        t_msg = threading.Timer(3.0, self.reset_msg2)
        t_msg.start()

    def reset_msg2(self):
        self.usermsg.set("Please enter a command. (type help for a list)")
        self.usermsg_traceid = self.usermsg.trace("w", self.reset_msg)

    def help_menu(self):
        self.txtoutput.clear()
        print("Regular commands list:")
        print(list(self.commands.keys()))
        print("Special commands list:")
        print(list(self.defaults.keys()))

    def list_themes(self):
        print(self.theme.theme_names())


"""
The below code is included as a demo of the library.
"""
if __name__ == "__main__":
    from time import strftime

    demo = CmdGUI()
    demo.wintitle = "CmdGUI Demo"  # Sets the main window title
    stop = False

    def infloop_test():
        """
        An example of running a looping function with tkinter
        Sets the initial time display.
        With infloop_test2
        """
        demo.txtoutput.clear()
        print(strftime("%a - %b %d, %Y  %H:%M:%S"))
        demo.usermsg.set("Type stop and press enter to stop the loop.")
        infloop_test2()

    def infloop_test2():
        """
        Updates the time display every 500ms until stop command is given.
        """
        global stop
        demo.loop_in_progress = True

        if not stop:
            curtime = strftime("%a - %b %d, %Y  %H:%M:%S")
            time_display = demo.txtoutput.get(1.0, 1.28)  # Read all characters on the first line
            curtime = list(curtime)
            time_display = list(time_display)
            for index, char in enumerate(time_display):
                if curtime[index] != time_display[index]:
                    cursor = "1.{0}".format(index)  # Use number of current character as column index
                    demo.txtoutput.config(state="normal")
                    demo.txtoutput.delete(cursor)  # Delete char at cursor
                    demo.txtoutput.insert(cursor, curtime[index])  # Insert new char, if changed at cursor
                    demo.txtoutput.config(state="disabled")
            demo.txtoutput.after(500, infloop_test2)  # Calls infloop_test2 over again after 500ms
        else:
            demo.usermsg.set("Time loop has been stopped.")
            demo.loop_in_progress = False
            stop = False

    def end_loop():
        """
        Used to change global variable stop to True for stopping loops.
        """
        global stop
        stop = True

    def forloop_test():
        for i in range(10):
            print("This is step " + str(i) + ".")

    def say(*args):  # Very basic attempt at using arguments with commands, treats anything after say as text

        print(*args)


    # Create commands to be typed to run each function
    demo.commands['infloop'] = infloop_test
    demo.defaults["stop"] = end_loop
    demo.commands['forloop'] = forloop_test
    demo.commands['say'] = say

    demo.root.mainloop()
