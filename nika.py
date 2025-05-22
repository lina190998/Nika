import tkinter as tk
import customtkinter
from tkinter import PhotoImage
import cv2
import numpy as np
import os
import pyautogui
import requests
import base64
from PIL import Image, ImageTk
import asyncio
import threading
import random
from time import perf_counter
import psutil
import pygetwindow
import win32gui
from pynput.keyboard import Key, Controller as KeyboardController, Listener
from pynput.mouse import Controller as MouseController
from configparser import ConfigParser
import time
import re
import git
mouse = MouseController()
keyboard = KeyboardController()
class TkinterBot(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.repo_url = "https://github.com/lina190998/Nika.git"
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.local_repo_path = os.path.join(self.BASE_DIR, "Nika")
        self.check_and_update_source()
        self.config = ConfigParser()
        self.config.read(os.path.join(self.BASE_DIR, 'settings.ini'))
        self.dawnkey = self.config.get('main', 'dawnkey')
        self.api_key = self.config.get('main', 'api_key')
        self.count_dawn = self.config.get('main', 'countdawn')
        self.dawn_timer = self.config.get('main', 'dawntimer')
        self.init_tkinter()
        self.init_maple_windows()
        self.start_button = customtkinter.CTkButton(self, text="Start", command=self.togglepause, fg_color='tomato', text_color='black', font=('Helvetica', 16), width=130, hover=False)
        self.start_button.pack(pady=20)
        self.countdawn_label = customtkinter.CTkLabel(self, text="Count Dawn : ", text_color='black', font=('Helvetica', 14), width=20)
        self.countdawn_label.pack(pady=20)
        self.countdawn_label.place(x=5,y=60)
        self.combobox_dawn = customtkinter.CTkComboBox(self, values=[str(i) for i in [1, 2, 3]], font=('Helvetica', 14), state="readonly",command=self.on_select, width=20)
        self.combobox_dawn.place(x=100,y=60)
        self.combobox_dawn.set(self.count_dawn)
        self.dawntimer_label = customtkinter.CTkLabel(self, text="Dawn Timer : ", text_color='black', font=('Helvetica', 14), width=20)
        self.dawntimer_label.pack(pady=20)
        self.dawntimer_label.place(x=5,y=100)
        self.combobox_dawn_timer = customtkinter.CTkComboBox(self, values=[str(i) for i in [90, 95, 100, 105, 110, 115, 120]], font=('Helvetica', 14), state="readonly",command=self.on_select_dawn, width=70)
        self.combobox_dawn_timer.place(x=100,y=100)
        self.combobox_dawn_timer.set(self.dawn_timer)
        self.label_start_button = customtkinter.CTkLabel(self, text='F1 : Stop/Start', text_color='black', font=('Helvetica', 10), width=20)
        self.label_start_button.pack(pady=20)
        self.label_start_button.place(x=10, y=self.window_height - 40)
        self.pause = True
        self.loop1 = asyncio.new_event_loop()
        self.loop2 = asyncio.new_event_loop()
        self.thread1 = threading.Thread(target=self.run_thread1)
        self.thread2 = threading.Thread(target=self.run_thread2)
        self.stop_event = asyncio.Event()
        self.asyncfunction1_event = asyncio.Event()
        self.asyncfunction1_event.set()
        self.asyncfunction2_event = asyncio.Event()
        self.asyncfunction2_event.set()
        self.dawntimer0=0
        self.dawntimer=0
        self.dawn=True
        self.now=0
        self.counterld=0
        self.listener = Listener(on_press=self.on_press)
        self.listener.start()

    def check_and_update_source(self):
        if not os.path.exists(self.local_repo_path):
            print("Repository không tồn tại. Đang clone từ GitHub...")
            git.Repo.clone_from(self.repo_url, self.local_repo_path)
            print("Clone thành công!")
            print("Clone thành công!")
        else:
            print("Đang kiểm tra cập nhật từ GitHub...")
            repo = git.Repo(self.local_repo_path)
            origin = repo.remotes.origin

            # Lấy thông tin cập nhật
            origin.fetch()
            if repo.head.commit != origin.refs.main.commit:
                print("Có bản cập nhật mới. Đang cập nhật...")
                repo.git.pull()
                print("Cập nhật thành công!")
            else:
                print("Không có bản cập nhật mới.")

    def on_select(self, event):
        self.setdawn = self.combobox_dawn.get()
        print(f"Current Dawn is set to {self.setdawn}")

    def on_select_dawn(self, event):
        self.setdawn_timer = self.combobox_dawn_timer.get()
        print(f"Current Dawn Timer is set to {self.setdawn_timer}")
        

    def on_press(self, key):
        try:
            if key == Key.f1:
                self.togglepause()
        except Exception as e:
            print(f"Error in on_press: {e}")

    def run_thread1(self):
        print("Thread 1 Is On")
        asyncio.set_event_loop(self.loop1)
        self.loop1.run_until_complete(self.async_function1()) # Thread Botting

    def run_thread2(self):
        print("Thread 2 Is On")
        asyncio.set_event_loop(self.loop2)
        self.loop2.run_until_complete(self.async_function2()) # Thread solving LD

    def start_threads(self):
        self.thread1.start()
        self.thread2.start()

    async def process_timer(self):
        self.setdawn_timer = self.combobox_dawn_timer.get()
        self.dawntimer = self.now - self.dawntimer0
        if self.dawntimer > int(self.setdawn_timer):
            self.dawn = True

    async def pressdawn(self):
        self.setdawn = self.combobox_dawn.get()
        print(f'Press Dawn : {self.setdawn}')
        if int(self.setdawn) == 1:
            await asyncio.sleep(0.5)
            keyboard.press(self.dawnkey)
            await asyncio.sleep(0.1)
            keyboard.release(self.dawnkey)
            await asyncio.sleep(0.5)
        elif int(self.setdawn) == 2:
            for _ in range(2):
                await asyncio.sleep(0.5)
                keyboard.press(self.dawnkey)
                await asyncio.sleep(0.1)
                keyboard.release(self.dawnkey)
                await asyncio.sleep(0.5)
        elif int(self.setdawn) == 3:
            for _ in range(3):
                await asyncio.sleep(0.5)
                keyboard.press(self.dawnkey)
                await asyncio.sleep(0.1)
                keyboard.release(self.dawnkey)
                await asyncio.sleep(0.5)
        self.dawn = False
        self.dawntimer0=perf_counter()

    async def move_to_and_click(self, x, y):
        pyautogui.moveTo(x, y, duration=0.5)
        pyautogui.click()
        await asyncio.sleep(.01)

    async def level_rebirth_pt(self):
        rb ="rb"
        luk ="luk 2000"
        keyboard.press(self.dawnkey)
        keyboard.release(self.dawnkey)
        await asyncio.sleep(1.)
        keyboard.press(Key.enter)
        await asyncio.sleep(0.1)
        keyboard.release(Key.enter)
        keyboard.press(Key.shift)
        keyboard.press('2')
        keyboard.release('2')
        keyboard.release(Key.shift)
        for i in luk:
            keyboard.press(i)
            keyboard.release(i)
            await asyncio.sleep(0.1)
        await asyncio.sleep(1.)
        keyboard.press(Key.enter)
        await asyncio.sleep(0.1)
        keyboard.release(Key.enter)
        await asyncio.sleep(1.)
        keyboard.press(Key.shift)
        keyboard.press('2')
        keyboard.release('2')
        keyboard.release(Key.shift)
        await asyncio.sleep(0.1)
        for i in rb:
            keyboard.press(i)
            keyboard.release(i)
            await asyncio.sleep(0.1)
        keyboard.press(Key.enter)
        await asyncio.sleep(0.1)
        keyboard.release(Key.enter)
        await asyncio.sleep(15.)
        keyboard.press(Key.enter)
        await asyncio.sleep(0.1)
        keyboard.release(Key.enter)
        await asyncio.sleep(1.)

    async def async_function1(self):
        while True:
            while self.pause or not self.asyncfunction1_event.is_set():
                await asyncio.sleep(1)
                if self.stop_event.is_set():
                    return  
            try:
                rb, hottime = self.detect_all_image()
                if rb:
                    await self.level_rebirth_pt()
                elif self.dawn:
                    await asyncio.sleep(.5)               
                    await self.pressdawn()
                    await asyncio.sleep(.5)
                elif hottime:
                    print("Got Hot Time...")
                    await asyncio.sleep(.5)
                    await self.move_to_and_click(772, 443)
                    await asyncio.sleep(.5)
                    print("Click Ok Done...")
                else:
                    await asyncio.sleep(.3)
                self.now = perf_counter()
                await self.process_timer()
            except Exception as e:
                print(f'function1 error {e}')
            await asyncio.sleep(0.333)

    async def async_function2(self):
        while True:
            while self.pause or not self.asyncfunction2_event.is_set():
                await asyncio.sleep(1)
                if self.stop_event.is_set():
                    return  
            try:
                botcheck = self.run_once_detect_img_cookbot()
                if botcheck:
                    print(f'Got LD : {botcheck}')
                    self.asyncfunction1_event.clear()
                    while True:
                        self.counterld+=1
                        if self.counterld == 1:
                            num_clicks = random.randint(2, 3)
                            for _ in range(num_clicks):
                                await self.move_to_and_click(800, 400)
                                await asyncio.sleep(.1)
                            screenshot_path = os.path.join(self.BASE_DIR, 'image', 'img_ld.png')
                            screenshot = self.capture_screenshot()
                            cv2.imwrite(screenshot_path, screenshot)
                            screenshot_bgr = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
                            image = np.array(screenshot_bgr)
                            print("Solving Captcha Ranmelle...")
                            cropped_image = self.find_and_crop_image(image)
                            # base64_image = self.image_to_base64(cropped_image)
                            # result = self.ocr_vision_base64(base64_image)
                            result = self.ocr_space_file(cropped_image)
                            result = self.filter_result(result)
                            print(result)
                        else:
                            count_IL = self.count_IL(result)
                            result = self.replace_IL(result, count_IL)
                            base = 2
                            idx = self.counterld - base
                            if 0 <= idx < len(result):
                                result = result[idx]
                            else:
                                result = None
                                self.close_maplestory()
                            print(f"Result {self.counterld} =", result)
                            
                        await self.move_to_and_click(750, 434)
                        await asyncio.sleep(.5) 
                        for _ in range(30):
                            keyboard.press(Key.backspace)
                            keyboard.release(Key.backspace)
                            await asyncio.sleep(0.1)
                        await asyncio.sleep(.5)
                        for char in result:
                            if char.isupper():
                                keyboard.press(Key.shift)
                                keyboard.press(char.lower())
                                keyboard.release(char.lower())
                                keyboard.release(Key.shift)
                                await asyncio.sleep(0.1)
                            else:
                                keyboard.press(char)
                                keyboard.release(char)
                                await asyncio.sleep(0.1)
                        await asyncio.sleep(1.)
                        await self.move_to_and_click(926, 488)
                        await asyncio.sleep(1.5)
                        num_clicks = random.randint(2, 3)
                        for _ in range(num_clicks):
                            await self.move_to_and_click(865, 435)
                            await asyncio.sleep(.2)
                        await asyncio.sleep(3.)
                        print("Looking for Failed and Passed")
                        img_failed = self.run_once_detect_img_failed()
                        img_passed = self.run_once_detect_img_passed()
                        await asyncio.sleep(.5)
                        if img_failed:
                            print("Failed try again")
                            await self.move_to_and_click(924, 496)
                            continue
                        elif img_passed:
                            print("Passed !! Congratulations !!")
                            await self.move_to_and_click(924, 496)
                            self.counterld=0
                            self.asyncfunction1_event.set()
                            break
                        else:
                            print("Both images not found... Try again...")
                            await self.move_to_and_click(924, 496)
                            self.counterld=0
                            self.asyncfunction1_event.set()
                            break
            except Exception as e:
                print(f'function1 error {e}')
            await asyncio.sleep(0.333)

    def init_tkinter(self):
        self.title("Nika")
        self.iconpath = ImageTk.PhotoImage(file=os.path.join(self.BASE_DIR, "nika.ico"))
        self.wm_iconbitmap()
        self.iconphoto(False, self.iconpath)
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.window_width = 200
        self.window_height = 170
        self.window_x = self.screen_width - self.window_width
        self.window_y = 0
        self.geometry(f"{self.window_width}x{self.window_height}+{self.window_x-10}+{self.window_y}")
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.tkinter_started=True
    
    def init_maple_windows(self):
        windows=[]
        winlist=[]
        winlist = pygetwindow.getWindowsWithTitle('Ranmelle')
        for w in winlist:
            windows.append(w._hWnd)
        for windowhwnd in windows:
            position = win32gui.GetWindowRect(windowhwnd)
            x, y, w, h = position
            if w-x == 410:
                self.chathwnd=windowhwnd
            elif w-x == 1936 or w-x == 1382 or w-x == 1296 or w-x == 1040 or w-x == 816:
                self.maplehwnd=windowhwnd
            elif w-x == 1938 or w-x == 1384 or w-x == 1298 or w-x == 1042 or w-x == 818:
                self.maplehwnd=windowhwnd
            elif w-x == 1388 or w-x == 1300 or w-x == 824 or w-x == 1374 or w-x == 2592:
                self.maplehwnd=windowhwnd
        if self.maplehwnd:
            current_position = win32gui.GetWindowRect(self.maplehwnd)
            current_x, current_y, _, _ = current_position
            if current_x != 2 or current_y != 2:
                new_position = (2, 2, w - x, h - y)
                win32gui.SetWindowPos(self.maplehwnd, 0, *new_position, 0)
                print("Moved MapleStory window to the position (2, 2).")
        if not self.maplehwnd:
            print(f'is your maple on?')

    def togglepause(self):
        self.pause = not self.pause
        print(f'Start Button Pressed .. {self.pause}')
        if self.pause:
            self.start_button.configure(text='Start', fg_color='tomato', hover=False)
        else:
            self.start_button.configure(text='Stop', fg_color='lime', hover=False)
    
    def capture_screenshot(self):
        img = pyautogui.screenshot()
        screenshot = np.array(img)
        result = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
        return result
    
    def detect_all_image(self):
        img = self.capture_screenshot()
        img_path = cv2.imread(os.path.join(self.BASE_DIR, 'image', 'img_level_300.png'))
        img_path2 = cv2.imread(os.path.join(self.BASE_DIR, 'image', 'img_hottime.png'))
        location = self.mini_checker_img_function_2(img, img_path)
        location2 = self.mini_checker_img_function(img, img_path2)
        return (location, location2)

    def run_once_detect_img_cookbot(self):
        img = self.capture_screenshot()
        img_path1 = cv2.imread(os.path.join(self.BASE_DIR, 'image', 'img_cookbot.png'))
        location1 = self.mini_checker_img_function(img,img_path1)
        return (location1)

    def run_once_detect_img_failed(self):
        img = self.capture_screenshot()
        img_path1 = cv2.imread(os.path.join(self.BASE_DIR, 'image', 'img_failed.png'))
        location1 = self.mini_checker_img_function(img,img_path1)
        return (location1)
    
    def run_once_detect_img_passed(self):
        img = self.capture_screenshot()
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
    
    # def image_to_base64(self, image_path):
    #     with open(image_path, 'rb') as image_file:
    #         return base64.b64encode(image_file.read()).decode('utf-8')
    
    def filter_result(self, result):
        filtered_result = re.sub(r'\r?\n+', '', result)
        return filtered_result
    
    def find_and_crop_image(self, image):
        if image is None:
            return None
        try:
            output_path = (os.path.join(self.BASE_DIR, 'image', 'processed_image.png'))
            result = self.run_once_detect_img_cookbot()
            x, y = result[0]
            x = int(x)
            y = int(y)
            x1 = x + 290
            y1 = y + 4
            cropped_image = image[y-27:y1, x+65:x1]
            width = int(cropped_image.shape[1] * 1100 / 100)
            height = int(cropped_image.shape[0] * 1100 / 100)
            dim = (width, height)
            resized_image = cv2.resize(cropped_image, dim, interpolation=cv2.INTER_CUBIC)
            gray = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray, 225, 255, cv2.THRESH_BINARY)

            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            cv2.imwrite(output_path, thresh)
            return output_path
        except Exception as e:
            print(f"Lỗi khi cắt ảnh: {e}")
            return None
    
    # def ocr_vision_base64(self, base64_image):
    #     url = f"https://vision.googleapis.com/v1/images:annotate?key={self.api_key}"
    #     request_body = {"requests": [{"image": {"content": base64_image},"features": [{"type": "TEXT_DETECTION","maxResults": 10}]}]}
    #     response = requests.post(url, json=request_body)
    #     if response.status_code == 200:
    #         result = response.json()
    #         texts = result['responses'][0].get('textAnnotations', [])
    #         return texts[0]['description'] if texts else "Không có văn bản"
    #     else:
    #         return f"Lỗi: {response.status_code}"
        
    def ocr_space_file(self, filename, language='eng'):
        payload = {'isOverlayRequired': False,'apikey': self.api_key,'language': language,'OCREngine': 1}
        with open(filename, 'rb') as f:
            r = requests.post('https://api.ocr.space/parse/image',files={filename: f},data=payload)
        result = r.json()
        if result['IsErroredOnProcessing']:
            return f"Lỗi: {result['ErrorMessage']}"
        else:
            return result['ParsedResults'][0]['ParsedText'] if result['ParsedResults'] else "Không có văn bản"
    
    def close_maplestory(self):
        print("[-] Đang đóng tiến trình chứa 'MapleStory' và 'Ranmelle'...")
        for proc in psutil.process_iter(['name']):
            try:
                if 'MapleStory' in proc.info['name'] or 'Ranmelle' in proc.info['name']:
                    proc.terminate()
                    print(f"[+] Đã gửi lệnh terminate cho tiến trình {proc.info['name']}")
                    time.sleep(1.)
                    if proc.is_running():
                        proc.kill()
                        print(f"[!] Đã buộc dừng tiến trình {proc.info['name']}")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
    
    def count_IL(self, input_string):
        return sum(1 for c in input_string if c == 'I' or c == 'l')
    
    def replace_IL(self, input_string, count_IL):
        if count_IL == 0:
            print("Không có ký tự 'I' hoặc 'l' để thay thế")
            self.close_maplestory()
            return [input_string]
        IL_positions = [i for i, c in enumerate(input_string) if c == 'I' or c == 'l']
        def swap_char(c):
            return 'l' if c == 'I' else 'I'
        if count_IL == 1:
            pos = IL_positions[0]
            lst = list(input_string)
            lst[pos] = swap_char(lst[pos])
            result = ''.join(lst)
            print(f"Chuỗi ban đầu: {input_string}")
            print(f"Số lượng 'I' + 'l': {count_IL}")
            print(f"Chuỗi sau khi thay thế: {result}")
            return [result]
        results = []
        for replace_count in range(1, count_IL + 1):
            for i in range(replace_count):
                lst = list(input_string)
                pos = IL_positions[i]
                lst[pos] = swap_char(lst[pos])
            results.append(''.join(lst))
        lst_all = list(input_string)
        for pos in IL_positions:
            lst_all[pos] = swap_char(lst_all[pos])
        results.append(''.join(lst_all))
        print(f"Chuỗi ban đầu: {input_string}")
        for idx, s in enumerate(results, 1):
            print(f"Chuỗi thay thế {idx}: {s}")
        return results
    
    def on_close(self):
        self.listener.stop()
        self.pause = True
        self.stop_event.set()
        self.asyncfunction1_event.clear()
        self.asyncfunction2_event.clear()

        self.setdawn = self.combobox_dawn.get()
        self.setdawn_timer = self.combobox_dawn_timer.get()

        # Save configuration
        self.config.set('main', 'countdawn', str(self.setdawn))
        self.config.set('main', 'dawntimer', str(self.setdawn_timer))

        with open('settings.ini', 'w') as f:
            self.config.write(f)

        try:
            self.quit()
            self.destroy()
            threads = [self.thread1, self.thread2]
            for thread in threads:
                if thread and thread.is_alive():
                    thread.join(timeout=5)
        except Exception as e:
            print(f"Error while stopping threads: {e}")

        # Instead of closing the event loop directly, set a flag to stop tasks
        if asyncio.get_event_loop().is_running():
            print("Stopping asyncio tasks...")
            for task in asyncio.all_tasks(asyncio.get_event_loop()):
                task.cancel()

            # Allow tasks to finish
            try:
                asyncio.gather(*asyncio.all_tasks(asyncio.get_event_loop()), return_exceptions=True)
            except Exception as e:
                print(f"Error while gathering tasks: {e}")

        print("All threads and tasks have been stopped.")
        os._exit(0)


async def main2():
    mytkinter = TkinterBot()
    mytkinter.start_threads()
    mytkinter.mainloop()

if __name__ == "__main__":
    asyncio.run(main2())
    pass
