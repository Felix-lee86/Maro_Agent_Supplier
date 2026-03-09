import uiautomation as auto
import time

def find_weixin():
    print("Searching for Weixin (WeChat) window...")
    # Based on tasklist, the process name is Weixin.exe
    # We'll search for the window with common ClassNames for WeChat
    # Weixin.exe often produces windows with several names.
    
    # Method 1: Search by ClassName
    wechat_window = auto.WindowControl(searchDepth=1, ClassName='WeChatMainWndForPC')
    if not wechat_window.Exists(0):
        # Method 2: Search by partial name (Korean/Chinese/English)
        for w in auto.GetRootControl().GetChildren():
            if "WeChat" in w.Name or "微信" in w.Name:
                wechat_window = w
                break
                
    if wechat_window and wechat_window.Exists(0):
        print(f"Success: Weixin window found: '{wechat_window.Name}'")
        wechat_window.SetFocus()
        return wechat_window
    else:
        print("Error: Could not find Weixin window. Please ensure it's not minimized to tray.")
        return None

def read_messages(window):
    print("Attempting to read last message...")
    # This is a sample structure. Real WeChat UI tree might differ.
    # We look for a List or Pane containing messages.
    msg_list = window.ListControl(Name="消息") # "Messages" in Korean/Chinese often titled 消息
    if msg_list.Exists(0):
        items = msg_list.GetChildren()
        if items:
            last_msg = items[-1].Name
            print(f"Last message: {last_msg}")
    else:
        print("Could not find message list. Investigating UI tree...")
        # Print first few children of the window to find the right control
        for i, child in enumerate(window.GetChildren()):
            print(f"Child {i}: Name='{child.Name}', Class='{child.ClassName}', Type='{child.ControlTypeName}'")

if __name__ == "__main__":
    win = find_weixin()
    if win:
        read_messages(win)
