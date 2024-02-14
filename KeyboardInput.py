import keyboard

#https://stackabuse.com/guide-to-pythons-keyboard-module/
#https://www.geeksforgeeks.org/keyboard-module-in-python/

def PressKey(Key):
		keyboard.press(Key)	  #press a key.
		print(Key+" is pressed")

def ReleaseKey(Key):
		keyboard.release(Key) #releases a key.
		
def PressNrelease(Key):
		keyboard.press_and_release(Key) # presses and releases a key.
		print(Key+" is pressed and released")

def ReleaseAllKeys(KeyBoardLoad):	#for default hand gesture to reset 
		for k in KeyBoardLoad:
			if k != "Release":
				ReleaseKey(k)

		print("All Keys are released")

def GetKey(Key):		     # to keys bind with specfic gesture
		keyboard.record(Key) # records keyboard activity until key is pressed


# detect key pressed and return the pressed key name
def detect_key():
    return keyboard.read_event(suppress=True).name		
	
