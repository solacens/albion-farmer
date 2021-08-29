from time import sleep, time
import cv2 as cv
import numpy as np
import pyautogui
import math


class Actions:

    # Debug
    debug = True

    # Vision module
    vision = None

    # Recorded cursor
    recorded_position = {"x": 0, "y": 0}

    # Predefined offsets
    offset_takeOrWater = [(115, 112), (-43, 199), (-128, 1), (-214, -92),
                          (11, -126), (115, -168), (177, 8), (276, 104), (-128, 164)]
    offset_farm = [(109, 85), (215, 3), (105, -73), (14, -139),
                   (-94, -84), (-214, -21), (-129, 67), (-10, 156)]

    # Predefined paths
    # Teleporter (303, 703)
    # Farm 1 (451, 428)
    # Farm 2 (583, 474)
    # Farm 3 (648, 521)
    # Farm 4 (716, 478)
    # Farm 5 (782, 521)
    # Midway Middle (416, 618)
    # Midway Left (359, 570)
    # Midway Right (516, 684)
    path_teleporter_to_1 = [(416, 618), (359, 570), (451, 428)]
    path_1_to_2 = [(583, 474)]
    path_2_to_3 = [(648, 521)]
    path_3_to_4 = [(716, 478)]
    path_4_to_5 = [(781, 520)]
    path_5_to_teleporter = [(516, 684), (416, 618), (303, 703)]

    # Constructor
    def __init__(self, vision):
        self.vision = vision

    def activateGameWindow(self):
        pyautogui.moveTo(x=self.vision.pos_x + 40, y=self.vision.pos_y - 15)
        pyautogui.click()
        self.centerCursor()

    def centerCursor(self):
        x = self.vision.pos_x + self.vision.width / 2
        y = self.vision.pos_y + self.vision.height / 2
        pyautogui.moveTo(x, y)
        return (x, y)

    def pointCharacterCursor(self):
        x = self.vision.pos_x + self.vision.width / 2 + 4
        y = self.vision.pos_y + self.vision.height / 2 - 47
        pyautogui.moveTo(x, y)
        return (x, y)

    def recordCursorPosition(self):
        pos = pyautogui.position()
        self.recorded_position["x"] = pos.x
        self.recorded_position["y"] = pos.y
        print("Position recorded: {} {}".format(
            self.recorded_position["x"], self.recorded_position["y"]))

    def moveToRecordedCursorPosition(self):
        pyautogui.moveTo(
            x=self.recorded_position["x"], y=self.recorded_position["y"])
        print("Moving back to position: {} {}".format(
            self.recorded_position["x"], self.recorded_position["y"]))

    def getOffsetToRecordedCursorPosition(self):
        pos = pyautogui.position()
        x = pos.x - self.recorded_position["x"]
        y = pos.y - self.recorded_position["y"]
        print('Offset: {} {}'.format(x, y))

    def ensureMaxView(self):
        for _ in range(0, 10):
            pyautogui.scroll(-1)

    def ensureMapSizeAndLocation(self):
        if not self.vision.mapOpened():
            pyautogui.press('n')
        center = self.centerCursor()
        for _ in range(0, 25):
            pyautogui.scroll(-1)
        pyautogui.moveTo(center[0]+160, center[1])
        pyautogui.drag(-200, 160, 1, button='left')
        self.centerCursor()
        for _ in range(0, 16):
            pyautogui.scroll(1)
            sleep(0.25)
        pyautogui.press('n')

    def ensureMounted(self):
        if self.vision.mapOpened():
            pyautogui.press('n')
        if not self.vision.mounted():
            pyautogui.press('a')
            sleep(4)

    def pressTake(self, backToOriginal=False):
        pos = pyautogui.position()
        location = self.vision.locateTakeButton()
        if location is not None:
            pyautogui.click(x=location[0], y=location[1])
        else:
            pyautogui.press('esc')
            self.ensureMounted()
            raise Exception('Cannot take')
        if backToOriginal:
            pyautogui.moveTo(x=pos.x, y=pos.y)

    def pressWater(self, backToOriginal=False):
        pos = pyautogui.position()
        location = self.vision.locateWaterButton()
        if location is not None:
            pyautogui.click(x=location[0], y=location[1])
            sleep(1.5)
        else:
            location = self.vision.locateCantWaterButton()
            if location is None:
                pyautogui.press('esc')
                self.ensureMounted()
                raise Exception('Cannot water')
        if backToOriginal:
            pyautogui.moveTo(x=pos.x, y=pos.y)

    def farmAction(self):
        pos = pyautogui.position()
        pyautogui.click()
        sleep(1.5)
        pyautogui.moveTo(
            x=pos.x + self.offset_farm[0][0], y=pos.y + self.offset_farm[0][1])
        pyautogui.click()
        sleep(1.5)
        pyautogui.moveTo(
            x=pos.x + self.offset_farm[1][0], y=pos.y + self.offset_farm[1][1])
        pyautogui.click()
        sleep(1.5)
        pyautogui.moveTo(
            x=pos.x + self.offset_farm[2][0], y=pos.y + self.offset_farm[2][1])
        pyautogui.click()
        sleep(1.5)
        pyautogui.moveTo(
            x=pos.x + self.offset_farm[3][0], y=pos.y + self.offset_farm[3][1])
        pyautogui.click()
        sleep(1.5)
        pyautogui.moveTo(
            x=pos.x + self.offset_farm[4][0], y=pos.y + self.offset_farm[4][1])
        pyautogui.click()
        sleep(1.5)
        pyautogui.moveTo(
            x=pos.x + self.offset_farm[5][0], y=pos.y + self.offset_farm[5][1])
        pyautogui.click()
        sleep(1.5)
        pyautogui.moveTo(
            x=pos.x + self.offset_farm[6][0], y=pos.y + self.offset_farm[6][1])
        pyautogui.click()
        sleep(1.5)
        pyautogui.moveTo(
            x=pos.x + self.offset_farm[7][0], y=pos.y + self.offset_farm[7][1])
        pyautogui.click()
        sleep(1.5)
        self.ensureMounted()

    def takeOrWaterAction(self, water=False):
        delay = 0
        pos = pyautogui.position()
        pyautogui.click()
        sleep(1)
        if water:
            self.pressWater()
        else:
            self.pressTake()
        pyautogui.press('esc')
        pyautogui.click(
            x=pos.x + self.offset_takeOrWater[0][0], y=pos.y + self.offset_takeOrWater[0][1])
        sleep(1)
        if water:
            self.pressWater()
        else:
            self.pressTake()
        pyautogui.press('esc')
        pyautogui.click(
            x=pos.x + self.offset_takeOrWater[1][0], y=pos.y + self.offset_takeOrWater[1][1])
        sleep(1)
        if water:
            self.pressWater()
        else:
            self.pressTake()
        pyautogui.press('esc')
        pyautogui.click(
            x=pos.x + self.offset_takeOrWater[2][0], y=pos.y + self.offset_takeOrWater[2][1])
        sleep(1)
        if water:
            self.pressWater()
        else:
            self.pressTake()
        pyautogui.press('esc')
        pyautogui.click(
            x=pos.x + self.offset_takeOrWater[3][0], y=pos.y + self.offset_takeOrWater[3][1])
        sleep(1)
        if water:
            self.pressWater()
        else:
            self.pressTake()
        pyautogui.press('esc')
        pyautogui.click(
            x=pos.x + self.offset_takeOrWater[4][0], y=pos.y + self.offset_takeOrWater[4][1])
        sleep(1)
        if water:
            self.pressWater()
        else:
            self.pressTake()
        pyautogui.press('esc')
        pyautogui.click(
            x=pos.x + self.offset_takeOrWater[5][0], y=pos.y + self.offset_takeOrWater[5][1])
        sleep(1)
        if water:
            self.pressWater()
        else:
            self.pressTake()
        pyautogui.press('esc')
        pyautogui.click(
            x=pos.x + self.offset_takeOrWater[6][0], y=pos.y + self.offset_takeOrWater[6][1])
        sleep(1)
        if water:
            self.pressWater()
        else:
            self.pressTake()
        pyautogui.press('esc')
        pyautogui.click(
            x=pos.x + self.offset_takeOrWater[7][0], y=pos.y + self.offset_takeOrWater[7][1])
        sleep(1)
        if water:
            self.pressWater()
        else:
            self.pressTake()
        pyautogui.press('esc')
        pyautogui.click(
            x=pos.x + self.offset_takeOrWater[8][0], y=pos.y + self.offset_takeOrWater[8][1], button='right')
        sleep(2)
        self.ensureMounted()

    def useSeed(self, seed):
        pos = pyautogui.position()
        if not self.vision.inventoryOpened():
            pyautogui.press('b')
        location = self.vision.locateSeed(seed)
        pyautogui.click(x=location[0], y=location[1])
        location = self.vision.locatePlaceButton()
        pyautogui.click(x=location[0], y=location[1])
        pyautogui.press('b')
        pyautogui.moveTo(x=pos.x, y=pos.y)

    def integratedFarm(self, seed, water=False):
        # Take
        self.pointCharacterCursor()
        try:
            self.takeOrWaterAction()
        except:
            print("Error in farming")
            return

        # Farm
        self.pointCharacterCursor()
        pos = pyautogui.position()
        pyautogui.moveTo(x=pos.x, y=pos.y - 90)
        self.useSeed(seed)
        self.farmAction()
        pyautogui.press('esc')

        # Back to field center
        self.pointCharacterCursor()
        pos = pyautogui.position()
        pyautogui.click(x=pos.x - 5, y=pos.y - 76, button='right')
        sleep(1)
        self.pointCharacterCursor()

        # Water
        if water:
            self.takeOrWaterAction(water=True)

        print("Farmed")

    def locateMapPointer(self):
        if not self.vision.mapOpened():
            pyautogui.press('n')
        pos = self.vision.locateMapPointer()
        pyautogui.press('n')
        return pos

    def getRelativeDistance(self, p1, p2):
        return math.sqrt(((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2))

    # East is 0, North is 90, West is 180, South is 270
    def getRelativeDegree(self, p1, p2):
        degree = 180 - math.degrees(math.atan2(
            p1[1] - p2[1], p1[0] - p2[0]))
        return degree % 360

    # East is 0, North is 90, West is 180, South is 270
    def translatePosition(self, X, Y, angle, distance):
        dY = distance*math.cos(math.radians(angle + 90))
        dX = distance*math.sin(math.radians(angle + 90))
        Xfinal = X + dX
        Yfinal = Y + dY
        return (Xfinal, Yfinal)

    def determineStep(self, fromPlace, toPlace):
        sourcePath = getattr(self, "path_{}_to_{}".format(fromPlace, toPlace))
        # Pop will change source list if not copied
        path = sourcePath.copy()
        while len(path):
            charCenter = self.pointCharacterCursor()
            target = path.pop(0)
            while True:
                pyautogui.press('s')
                sleepTime = 0.45

                pos = self.locateMapPointer()
                dis = self.getRelativeDistance(pos, target)

                moveDis = 200
                if dis < 3:
                    if len(path) == 0:
                        print("Position {} reached".format(toPlace))
                    break
                elif dis < 30 and dis > 3:
                    moveDis = 60
                    sleepTime = 0

                degree = self.getRelativeDegree(pos, target)

                wayPos = self.translatePosition(
                    charCenter[0], charCenter[1], degree, moveDis)

                pyautogui.click(x=wayPos[0], y=wayPos[1], button='right')

                sleep(sleepTime)

            # Center again for further operation
            charCenter = self.pointCharacterCursor()

    def testPath(self):
        self.determineStep("teleporter", "1")
        self.determineStep("1", "2")
        self.determineStep("2", "3")
        self.determineStep("3", "4")
        self.determineStep("4", "5")
        self.determineStep("5", "teleporter")

    def autoFarm(self, seed, water=False):
        self.determineStep("teleporter", "1")
        self.integratedFarm(seed, water)
        self.determineStep("1", "2")
        self.integratedFarm(seed, water)
        self.determineStep("2", "3")
        self.integratedFarm(seed, water)
        self.determineStep("3", "4")
        self.integratedFarm(seed, water)
        self.determineStep("4", "5")
        self.integratedFarm(seed, water)
        self.determineStep("5", "teleporter")
        print("Auto farm completed")

    def autoWater(self):
        self.determineStep("teleporter", "1")
        self.takeOrWaterAction(True)
        self.determineStep("1", "2")
        self.takeOrWaterAction(True)
        self.determineStep("2", "3")
        self.takeOrWaterAction(True)
        self.determineStep("3", "4")
        self.takeOrWaterAction(True)
        self.determineStep("4", "5")
        self.takeOrWaterAction(True)
        self.determineStep("5", "teleporter")
        print("Auto water completed")

    def useTeleporter(self, islandName):
        location = self.vision.locateTeleporter()
        pyautogui.click(x=location[0], y=location[1])
        sleep(0.5)
        pyautogui.moveTo(x=self.vision.pos_x + 134, y=self.vision.pos_y + 150)
        pyautogui.mouseDown()
        sleep(0.5)
        pyautogui.mouseUp()
        pyautogui.write(islandName)
        pyautogui.press('enter')
        pyautogui.click(x=self.vision.pos_x + 259, y=self.vision.pos_y + 632)

        sleep(5)
        while not self.vision.mounted():
            sleep(1)
        sleep(4)

        print("Travelled to {}".format(islandName))
