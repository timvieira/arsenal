import win32gui, win32con

def win_enum_callback(hwnd, results):
    if win32gui.IsWindowVisible(hwnd) and win32gui.GetWindowText(hwnd) != '':
        results.append(hwnd)

def print_list():
    handles = []
    win32gui.EnumWindows(win_enum_callback, handles)
    print '\n'.join(['%d\t%s' % (h, win32gui.GetWindowText(h)) for h in handles])

##import time
##def cycle_foreground():
##    handles = []
##    win32gui.EnumWindows(win_enum_callback, handles)
##    for handle in handles:
##        print handle, win32gui.GetWindowText(handle)
##        win32gui.SetForegroundWindow(handle)    
##        time.sleep(1.0)

def move_window():
    handle = win32gui.GetForegroundWindow()
    if handle == 0:
        print "Can't move window 0."
        return
    
    win32gui.SetWindowPos(handle, win32con.HWND_TOP, 480-50, 0, 850, 770, 0)    # window_id, z-index, left, top, width, height, options

if __name__ == '__main__':
    
    #cycle_foreground()
    print_list()

    move_window()
