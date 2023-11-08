#----------------- Import Dependencies -----------------
import mouse
import keyboard
import time

#--------------Simulate Move with mouse-----------------
def go_left():
    #swipe left
    mouse.drag(0, 0, -400, 0, absolute=False, duration= 0.2)
    #replace mouse on the center
    mouse.move(400, 0, absolute=False, duration=0.2)

def go_right():
    #swipe right
    mouse.drag(0, 0 , 400, 0 , absolute=False, duration=0.2)
    #replace mouse on the center
    mouse.move(400,0, absolute=False, duration = 0.2)

def go_top():
    #swipe top
    mouse.drag(0, 0, 0, -400, absolute=False, duration=0.2)
    #replace mouse on the center
    mouse.move(0,400, absolute=False, duration = 0.2)

def go_bottom():
    #swipe bottom
    mouse.drag(0, 0, 0, 400, absolute=False, duration=0.2)
    #replace mouse on the center
    mouse.move(0,400, absolute=False, duration = 0.2)


#-----------------Simulate Move with keyboard-----------------
def go_top_arrow():
    if not keyboard.is_pressed('up'):
        keyboard.press('up')
    time.sleep(0.01)
    keyboard.release('up')

def go_bot_arrow():
    if not keyboard.is_pressed('down'):
        keyboard.press('down')
    time.sleep(0.01)
    keyboard.release('down')

def go_right_arrow():
    if not keyboard.is_pressed('right'):
        keyboard.press('right')
    time.sleep(0.01)
    keyboard.release('right')

def go_left_arrow():
    if not keyboard.is_pressed('left'):
        keyboard.press('left')
    time.sleep(0.01)
    keyboard.release('left')


#--------------- test : listen to keyboard input ---------------- 
def main():
    while True:
        if keyboard.is_pressed('q'):
            break
        
        # Start prog macro
        if keyboard.is_pressed('e') and keyboard.is_pressed('z'):
            print("ooook")
        
        if keyboard.is_pressed('f'):
            if not keyboard.is_pressed('left'):
                keyboard.press('left')
            time.sleep(0.1)  # Add a small delay to control how long the key is pressed
            keyboard.release('left')
        
        if keyboard.is_pressed('h'):
            if not keyboard.is_pressed('right'):
                keyboard.press('right')
            time.sleep(0.1)
            keyboard.release('right')
        
        if keyboard.is_pressed('g'):
            if not keyboard.is_pressed('down'):
                keyboard.press('down')
            time.sleep(0.1)
            keyboard.release('down')
        
        if keyboard.is_pressed('t'):
            if not keyboard.is_pressed('up'):
                keyboard.press('up')
            time.sleep(0.1)
            keyboard.release('up')

if __name__ == "__main__":
    main()