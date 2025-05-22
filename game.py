import pag_capture
import numpy as np
import cv2
import os
import pyautogui
import numpy as np

class Game:
    def __init__(self, region):
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.hwnd = pag_capture.find_window_from_executable_name("Ranmelle")
        self.top, self.left, self.bottom, self.right = region[0], region[1], region[2], region[3]  
        self.newest_screenshot = None
        self.height, self.width = 769,1367
        with pag_capture.CaptureWindow(self.hwnd) as img:
            if img is None:
                return None
            self.height, self.width = img.shape[0], img.shape[1]
            self.newest_screenshot = img.copy()

    def get_screenshot(self):
        with pag_capture.CaptureWindow(self.hwnd) as img:
            if img is None:
                return None
            return img.copy()

    def generate_newest_screenshot(self):
        self.newest_screenshot = self.get_screenshot()        
    
    def capture_screenshot(self):
        screenshot_all = pyautogui.screenshot()
        screenshot = cv2.cvtColor(np.array(screenshot_all), cv2.COLOR_RGB2BGR)
        return screenshot
    
    def detect_all_image(self):
        img = self.newest_screenshot
        img_path = cv2.imread(os.path.join(self.BASE_DIR, 'image', 'img_level_300.png'))
        img_path2 = cv2.imread(os.path.join(self.BASE_DIR, 'image', 'img_hottime.png'))
        location = self.mini_checker_img_function_2(img, img_path)
        location2 = self.mini_checker_img_function(img, img_path2)
        return (location, location2)

    def run_once_detect_img_cookbot(self):
        img = self.newest_screenshot
        img_path1 = cv2.imread(os.path.join(self.BASE_DIR, 'image', 'img_cookbot.png'))
        location1 = self.mini_checker_img_function(img,img_path1)
        return (location1)

    def run_once_detect_img_failed(self):
        img = self.newest_screenshot
        img_path1 = cv2.imread(os.path.join(self.BASE_DIR, 'image', 'img_failed.png'))
        location1 = self.mini_checker_img_function(img,img_path1)
        return (location1)
    
    def run_once_detect_img_passed(self):
        img = self.newest_screenshot
        img_path1 = cv2.imread(os.path.join(self.BASE_DIR, 'image', 'img_passed.png'))
        location1 = self.mini_checker_img_function(img,img_path1)
        return (location1)
    
    def mini_checker_img_function(self, img, template_img):
        locations = []
        if template_img is None or template_img.size == 0:
            return None

        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        template_img = cv2.cvtColor(template_img, cv2.COLOR_RGB2BGR)

        result = cv2.matchTemplate(img, template_img, cv2.TM_CCOEFF_NORMED)
        locations = np.where(result >= 0.8)
        match_centers = [(loc[0] + template_img.shape[1] / 2, loc[1] + template_img.shape[0] / 2) for loc in zip(*locations[::-1])]
        
        return match_centers if match_centers else None
    
    def mini_checker_img_function_2(self, img, template_img):
        locations = []
        if template_img is None or template_img.size == 0:
            return None

        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        template_img = cv2.cvtColor(template_img, cv2.COLOR_RGB2BGR)

        result = cv2.matchTemplate(img, template_img, cv2.TM_CCOEFF_NORMED)
        locations = np.where(result >= 0.99)
        match_centers = [(loc[0] + template_img.shape[1] / 2, loc[1] + template_img.shape[0] / 2) for loc in zip(*locations[::-1])]
        
        return match_centers if match_centers else None

