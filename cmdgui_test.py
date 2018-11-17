import cmdgui as gui
from time import sleep

commands = {}


def appexit():
    print("This would exit the app.")

@gui.ThreadedLoop
def looptest():
    while True:
        print("This is a loop test!")
        sleep(4)


commands['exit'] = appexit
commands['loop'] = looptest


if __name__ == "__main__":
    MyGUI = gui.CmdGUI(commands)
    MyGUI.root.mainloop()
