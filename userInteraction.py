from pynput.mouse import Listener

def on_move(x, y):
    print('Pointer moved to {0}'.format((x, y)))

def on_click(x, y, button, pressed):
    global clickPos
    print('{0} at {1}'.format('Pressed' if pressed else 'Released',(x, y)))
        
    if not pressed:
        clickPos = (x,y)
        # Stop listener
        return False

def on_scroll(x, y, dx, dy):
    print('Scrolled {0}'.format((x, y)))

# Collect events until released
def getNextClickPos():
    with Listener(on_click=on_click) as listener:
        listener.join()
        return clickPos

    

