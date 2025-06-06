import tkinter as tk
import customtkinter
from tkinter import PhotoImage
import cv2
import numpy as np
import os
import pyautogui
from PIL import Image, ImageTk
import asyncio
import threading
import random
from time import perf_counter
import psutil
import pygetwindow as gw
import win32gui
from pynput.keyboard import Key, Controller as KeyboardController, Listener
from pynput.mouse import Controller as MouseController
from configparser import ConfigParser
import time
from game import Game
from anticaptchaofficial.imagecaptcha import *
import requests
mouse = MouseController()
keyboard = KeyboardController()
class TkinterBot(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.g = Game((8, 103, 230, 170))
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
        await asyncio.sleep(0.1)
        keyboard.press(self.dawnkey)
        await asyncio.sleep(0.1)
        keyboard.release(self.dawnkey)
        await asyncio.sleep(0.1)

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
                self.g.generate_newest_screenshot()
                rb, hottime = self.g.detect_all_image()
                if rb:
                    await self.level_rebirth_pt()
                elif hottime:
                    print("Got Hot Time...")
                    await asyncio.sleep(.5)
                    await self.move_to_and_click(772, 443)
                    await asyncio.sleep(.5)
                    print("Click Ok Done...")
                else:
                    await asyncio.sleep(.5)               
                    await self.pressdawn()
                    await asyncio.sleep(.5)
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
                self.g.generate_newest_screenshot()
                botcheck = self.g.run_once_detect_img_cookbot()
                if botcheck:
                    print(f'Got LD : {botcheck}')
                    self.asyncfunction1_event.clear()
                    while True:
                        self.counterld+=1
                        if self.counterld <= 8:
                            num_clicks = random.randint(2, 3)
                            for _ in range(num_clicks):
                                await self.move_to_and_click(800, 400)
                                await asyncio.sleep(.1)
                            screenshot_path = os.path.join(self.BASE_DIR, 'image', 'img_ld.png')
                            screenshot = self.g.capture_screenshot()
                            cv2.imwrite(screenshot_path, screenshot)
                            screenshot_bgr = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
                            image = np.array(screenshot_bgr)
                            print("Solving Captcha Ranmelle...")
                            cropped_image = self.find_and_crop_image(image)
                            result = self.ocr_imagecaptcha(cropped_image)
                            print(result)
                        else:
                            await self.close_maplestory()
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
                        self.g.generate_newest_screenshot()
                        img_failed = self.g.run_once_detect_img_failed()
                        img_passed = self.g.run_once_detect_img_passed()
                        await asyncio.sleep(.5)
                        if img_failed is not None:
                            print("Failed try again")
                            await self.move_to_and_click(924, 496)
                            self.counterld+1
                            continue
                        elif img_passed is not None:
                            print("Passed !! Congratulations !!")
                            await self.move_to_and_click(924, 496)
                            self.counterld=0
                            self.asyncfunction1_event.set()
                            break
                        else:
                            print("Both images not found... Try again...")
                            await self.move_to_and_click(924, 496)
                            self.counterld+1
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
        winlist = gw.getWindowsWithTitle('Ranmelle')
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
    
    def find_and_crop_image(self, image):
        if image is None:
            return None
        try:
            output_path = (os.path.join(self.BASE_DIR, 'image', 'processed_image.png'))
            self.g.generate_newest_screenshot()
            result = self.g.run_once_detect_img_cookbot()
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
    
    def ocr_imagecaptcha(self, image):
        try:
            solver = imagecaptcha()
            solver.set_verbose(1)
            solver.set_key(self.api_key)
            solver.set_soft_id(0)
            solver.set_case(True)
            solver.set_language_pool("en")
            captcha_text = solver.solve_and_return_solution(image)
            if captcha_text != 0:
                return captcha_text
            else:
                print("Task finished with error "+solver.error_code)
                return None
        except Exception as e:
            print(f"Lỗi Anti-Catpcha: {e}")
            return None
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
