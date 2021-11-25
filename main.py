from Actions import Actions
from pynput import keyboard
import os

# Change the working directory to the folder this script is in.
os.chdir(os.path.dirname(os.path.abspath(__file__)))

print('Ready.')
print('----------------------------------------')

def prerequisite(actions):
    actions.activateGameWindow()
    actions.ensureMaxView()
    actions.ensureMapSizeAndLocation()
    actions.ensureMounted()
    # print("Prerequisite alignment actions done.")

def solacens():
    try:
        actions = Actions()
    except Exception as e:
        print(e)
        return

    prerequisite(actions)

    # Starting from "Solacens's Island"
    actions.useTeleporter("SOLACENO'S ISLAND")
    actions.autoFarm(seed=4, water=True)
    actions.useTeleporter("SOLACENX'S ISLAND")
    actions.autoFarm(seed=4, water=True)
    actions.useTeleporter("SOLACENZ'S ISLAND")
    actions.autoFarm(seed=4, water=False)
    actions.useTeleporter("SOLACENS'S ISLAND")

    print('----------------------------------------')

def solacenz():
    try:
        actions = Actions()
    except Exception as e:
        print(e)
        return

    prerequisite(actions)

    # Starting from "Solacens's Island"
    actions.autoFarm(seed=3, water=True)
    actions.useTeleporter("SOLACEND'S ISLAND")
    actions.autoFarm(seed=3, water=True)
    actions.useTeleporter("SOLACENE'S ISLAND")
    actions.autoFarm(seed=3, water=False)
    actions.useTeleporter("SOLACENS'S ISLAND")

    print('----------------------------------------')

def on_press_quit(key):
    if hasattr(key, 'vk'):
        if key.vk == 81:
            exit()


def on_press(key):
    if hasattr(key, 'vk'):
        if key.vk == 96:  # 0
            actions.pointCharacterCursor()
            return
        elif key.vk == 107:  # +
            actions.recordCursorPosition()
            return
        elif key.vk == 109:  # -
            actions.moveToRecordedCursorPosition()
            return
        elif key.vk == 110:  # .
            actions.getOffsetToRecordedCursorPosition()
            return
        elif key.vk == 97:  # 1
            actions.takeOrWaterAction()
            return
        elif key.vk == 98:  # 2
            actions.farmAction()
            return
        elif key.vk == 99:  # 3
            actions.takeOrWaterAction(True)
            return
        elif key.vk == 100:  # 4
            prerequisite()
            actions.autoFarm(seed=3, water=False)
            return
        elif key.vk == 101:  # 5
            prerequisite()
            actions.autoFarm(seed=4, water=False)
            return
        elif key.vk == 102:  # 6
            prerequisite()
            actions.autoWater()
            return
        elif key.vk == 103 or key.vk == 55:  # 7
            solacens()
            return
        elif key.vk == 104 or key.vk == 56:  # 8
            solacenz()
            return
        elif key.vk == 105 or key.vk == 57:  # 9
            return


# Action listener
listener = keyboard.Listener(
    on_press=on_press)
listener.start()

# Quit listener
listener_quit = keyboard.Listener(
    on_press=on_press_quit)
listener_quit.start()

if True:
    listener_quit.join()
else:
    prerequisite()
    # Debug
