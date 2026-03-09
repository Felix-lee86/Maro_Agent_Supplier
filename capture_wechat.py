import uiautomation as auto
import time
from PIL import ImageGrab

def capture_wechat():
    wechat_window = auto.WindowControl(searchDepth=1, ClassName='WeChatMainWndForPC')
    if wechat_window.Exists(0):
        print(f"Capturing Wechat window: {wechat_window.Name}")
        wechat_window.SetFocus()
        time.sleep(1) # Wait for focus
        
        rect = wechat_window.BoundingRectangle
        bbox = (rect.left, rect.top, rect.right, rect.bottom)
        print(f"Bounding Rectangle: {bbox}")
        
        screenshot = ImageGrab.grab(bbox)
        screenshot.save("wechat_snapshot.png")
        print("Screenshot saved to wechat_snapshot.png")
    else:
        print("WeChat window not found for capture.")

if __name__ == "__main__":
    capture_wechat()
