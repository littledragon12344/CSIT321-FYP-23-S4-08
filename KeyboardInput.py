import keyboard

#https://stackabuse.com/guide-to-pythons-keyboard-module/
#https://www.geeksforgeeks.org/keyboard-module-in-python/
#

def PressKey(Key):
		keyboard.press(key)	  #press a key.
		print(Key+" is pressed")

def ReleaseKey(Key):
		keyboard.release(key) #releases a key.
		print(Key+" is released")
		
def PressNrelease(Key):
		keyboard.press_and_release(Key) # presses and releases a key.
		print(Key+" is pressed and released")

def GetKey(Key):		     # to keys bind with specfic gesture
		keyboard.record(key) # records keyboard activity until key is pressed


	

#need to press key once and not press again unless a diff gesture is detected
#if not the system will keep pressing the key over and over again
