from Actions import Actions
from Vision import Vision
from pynput import keyboard
import os

# Change the working directory to the folder this script is in.
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# initialize the WindowCapture class
vision = Vision()
actions = Actions(vision)
print('Window size x{} y{}'.format(vision.width, vision.height))
print('Window position x{} y{}'.format(vision.pos_x, vision.pos_y))


def prerequisite():
    actions.activateGameWindow()
    actions.ensureMaxView()
    actions.ensureMapSizeAndLocation()
    actions.ensureMounted()
    print("Prerequisite alignment actions done.")


def two_T3():
    prerequisite()

    # Starting from "Solacens's Island"
    actions.autoFarm(seed=3, water=False)
    actions.useTeleporter("SOLACEND'S ISLAND")
    actions.autoFarm(seed=3, water=False)
    actions.useTeleporter("SOLACENS'S ISLAND")


def two_T4_water():
    prerequisite()

    # Starting from "Solacens's Island"
    actions.useTeleporter("SOLACENE'S ISLAND")
    actions.autoFarm(seed=4, water=True)
    actions.useTeleporter("SOLACENO'S ISLAND")
    actions.autoFarm(seed=4, water=True)
    actions.useTeleporter("SOLACENS'S ISLAND")


def two_T4():
    prerequisite()

    # Starting from "Solacens's Island"
    actions.useTeleporter("SOLACENX'S ISLAND")
    actions.autoFarm(seed=4, water=False)
    actions.useTeleporter("SOLACENZ'S ISLAND")
    actions.autoFarm(seed=4, water=False)
    actions.useTeleporter("SOLACENS'S ISLAND")


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
        elif key.vk == 103:  # 7
            two_T3()
            return
        elif key.vk == 104:  # 8
            two_T4_water()
            return
        elif key.vk == 105:  # 9
            two_T4()
            return


# Action listener
listener = keyboard.Listener(
    on_press=on_press)
listener.start()

# Quit listener
listener_quit = keyboard.Listener(
    on_press=on_press_quit)
listener_quit.start()

print("""
# 0
actions.pointCharacterCursor()
# +
actions.recordCursorPosition()
# -
actions.moveToRecordedCursorPosition()
# .
actions.getOffsetToRecordedCursorPosition()
# 1
actions.takeOrWaterAction()
# 2
actions.farmAction()
# 3
actions.takeOrWaterAction(True)
# 4
prerequisite()
actions.autoFarm(seed=3, water=False)
# 5
prerequisite()
actions.autoFarm(seed=4, water=False)
# 6
prerequisite()
actions.autoWater()
# 7
two_T3()
# 8
two_T4_water()
# 9
two_T4()
""")

if True:
    listener_quit.join()
else:
    prerequisite()
    # Debug
