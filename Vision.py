from time import sleep, time
import cv2
import numpy as np
import win32gui
import win32ui
import win32con


class Vision:

    # Desktop hwnd
    hwnd = None

    # Window info
    title = 'Albion Online Client'
    width = 0
    height = 0
    pos_x = 0
    pos_y = 0

    # Images
    mount_img = None
    map_corner_img = None
    map_pointer_img = None
    inventory_img = None
    place_img = None
    t3_seed_img = None
    t4_seed_img = None
    teleporter = None

    # Cache
    map_route_contour_cache = None

    # Constructor
    def __init__(self):
        hwnd = win32gui.FindWindow(None, self.title)
        if not hwnd:
            raise Exception('Window not found: {}'.format(self.title))
        else:
            win32gui.SetForegroundWindow(hwnd)

        self.hwnd = win32gui.GetDesktopWindow()

        window_rect = win32gui.GetWindowRect(hwnd)
        self.width = window_rect[2] - window_rect[0]
        self.height = window_rect[3] - window_rect[1]

        border_pixels = 8    # Win 11
        titlebar_pixels = 31  # Win 11
        self.width = self.width - (border_pixels * 2)
        self.height = self.height - titlebar_pixels - border_pixels
        self.pos_x = window_rect[0] + border_pixels
        self.pos_y = window_rect[1] + titlebar_pixels

        self.mount_img = cv2.imread('img/mount.jpg', cv2.IMREAD_UNCHANGED)
        self.map_corner_img = cv2.imread(
            'img/map_corner.jpg', cv2.IMREAD_UNCHANGED)
        self.map_pointer_img = cv2.imread(
            'img/map_pointer.jpg', cv2.IMREAD_UNCHANGED)
        self.inventory_img = cv2.imread(
            'img/inventory.jpg', cv2.IMREAD_UNCHANGED)
        self.place_img = cv2.imread(
            'img/place.jpg', cv2.IMREAD_UNCHANGED)
        self.t3_seed_img = cv2.imread(
            'img/t3_seed.jpg', cv2.IMREAD_UNCHANGED)
        self.t4_seed_img = cv2.imread(
            'img/t4_seed.jpg', cv2.IMREAD_UNCHANGED)
        self.teleporter = cv2.imread(
            'img/teleporter.jpg', cv2.IMREAD_UNCHANGED)

    def imshow(self, data):
        cv2.imshow('Imshow', data)

    def waitForDestroy(self):
        cv2.waitKey()
        cv2.destroyAllWindows()

    def matchTemplateLocation(self, img, threshold, untilFound=False):
        result = cv2.matchTemplate(
            self.getScreenshot(), img, cv2.TM_CCOEFF_NORMED)

        locations = np.where(result >= threshold)
        locations = list(zip(*locations[::-1]))

        if len(locations) >= 1:
            return self.normalizePosition(locations[0], img.shape)
        else:
            if untilFound:
                return self.matchTemplateLocation(img, threshold-0.05, untilFound=True)
            else:
                return None

    def normalizePosition(self, tuple, shape):
        return (tuple[0] + self.pos_x + shape[1] / 2, tuple[1] + self.pos_y + shape[0] / 2)

    def getScreenshot(self, debugFileName=None):
        # Create a device context
        desktop_dc = win32gui.GetWindowDC(self.hwnd)
        img_dc = win32ui.CreateDCFromHandle(desktop_dc)

        # Create a memory device context
        mem_dc = img_dc.CreateCompatibleDC()

        # Create a bitmap object
        screenshot = win32ui.CreateBitmap()
        screenshot.CreateCompatibleBitmap(img_dc, self.width, self.height)
        mem_dc.SelectObject(screenshot)

        # Memory device context to the theme
        mem_dc.BitBlt((0, 0), (self.width, self.height), img_dc,
                      (self.pos_x, self.pos_y), win32con.SRCCOPY)

        # Convert the raw data into a format opencv can read
        if debugFileName:
            screenshot.SaveBitmapFile(mem_dc, debugFileName)
        signedIntsArray = screenshot.GetBitmapBits(True)
        img = np.fromstring(signedIntsArray, dtype='uint8')
        img.shape = (self.height, self.width, 4)

        # Memory release
        img_dc.DeleteDC()
        mem_dc.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, desktop_dc)
        win32gui.DeleteObject(screenshot.GetHandle())

        img = img[..., :3]

        img = np.ascontiguousarray(img)

        return img

    def mounted(self):
        location = self.matchTemplateLocation(self.mount_img, 0.8)
        return location != None

    def mapOpened(self):
        location = self.matchTemplateLocation(self.map_corner_img, 0.8)
        return location != None

    def inventoryOpened(self):
        location = self.matchTemplateLocation(self.inventory_img, 0.8)
        return location != None

    def locateSeed(self, seed):
        img = None
        if seed == 3:
            img = self.t3_seed_img
        elif seed == 4:
            img = self.t4_seed_img

        return self.matchTemplateLocation(img, 0.8, True)

    def locatePlaceButton(self):
        return self.matchTemplateLocation(self.place_img, 0.8, True)

    def locateTeleporter(self):
        return self.matchTemplateLocation(self.teleporter, 0.7, True)

    def locateMapPointer(self):
        image = self.getScreenshot()
        pointer_color = np.array([255, 179, 97])
        mask = cv2.inRange(image, pointer_color, pointer_color)

        cnt = cv2.findContours(mask, cv2.RETR_EXTERNAL,
                               cv2.CHAIN_APPROX_SIMPLE)
        cnt = cnt[0] if len(cnt) == 2 else cnt[1]
        largestCnt = None
        maxArea = -1
        for i in range(len(cnt)):
            area = cv2.contourArea(cnt[i])
            if area > maxArea:
                largestCnt = cnt[i]
                maxArea = area
        center = cv2.moments(largestCnt)
        cX = int(center["m10"] / center["m00"])
        cY = int(center["m01"] / center["m00"])

        # debugImg = cv2.circle(image.copy(), (cX, cY), radius=0,
        #                 color=(0, 0, 255), thickness=4)
        # self.imshow(debugImg)

        return (cX, cY)
