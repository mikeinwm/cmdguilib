import cmdgui as gui
from time import sleep

commands = {}
looprun = True


def appexit():
    print("This would exit the app.")


def looptest():
    global looprun
    looprun = True
    while looprun:
        print("This is a loop test!")
        sleep(4)


def loopstop():
    global looprun
    looprun = False


commands['exit'] = appexit
commands['loop'] = looptest
commands['stop'] = loopstop


if __name__ == "__main__":
    MyGUI = gui.CmdGUI(commands)
    MyGUI.root.mainloop()
