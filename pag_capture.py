import os
import pyautogui
import pygetwindow as gw
import numpy as np
import cv2
from typing import Optional, Tuple

class WindowCapture:
    @staticmethod
    def find_window_from_executable_name(name: str) -> Optional[gw.Window]:
        try:
            # Lọc các cửa sổ theo tiêu đề chứa tên executable
            windows = [w for w in gw.getAllWindows() if name.lower() in w.title.lower()]
            
            # Trả về cửa sổ đầu tiên nếu có
            return windows[0] if windows else None
        except Exception as e:
            print(f"Lỗi khi tìm cửa sổ: {e}")
            return None

class CaptureWindow:
    def __init__(self, window: Optional[gw.Window]):
        """
        Khởi tạo đối tượng chụp cửa sổ
        
        Args:
            window (Optional[gw.Window]): Cửa sổ cần chụp
        """
        self.window = window
        self.bitmap_handle = None

    def __enter__(self) -> Optional[np.ndarray]:
        if not self.window:
            return None

        try:
            screenshot = pyautogui.screenshot(
                region=(
                    self.window.left, 
                    self.window.top, 
                    self.window.width, 
                    self.window.height
                )
            )

            # Chuyển đổi sang numpy array
            screenshot_np = np.array(screenshot)
            
            # Chuyển từ RGB sang RGBA
            screenshot_bgra = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGRA)
            
            return screenshot_bgra

        except Exception as e:
            print(f"Lỗi khi chụp ảnh: {e}")
            return None

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Dọn dẹp khi kết thúc chụp ảnh
        """
        # Không cần giải phóng bộ nhớ trong phiên bản này
        pass

def find_window_from_executable_name(name: str) -> Optional[gw.Window]:

    return WindowCapture.find_window_from_executable_name(name)
