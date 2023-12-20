import keyboard

#https://stackabuse.com/guide-to-pythons-keyboard-module/
#https://www.geeksforgeeks.org/keyboard-module-in-python/
#
key_states = {}  # Dictionary to store the state of each key

def PressKey(Key):
		if Key == "Release":         #change to whatever default handgesture is to to reset keys
			ReleaseAllKeys()
			return		

		keyboard.press(Key)	  #press a key.
		print(Key+" is pressed")
		key_states[Key] = True  # Update key state to pressed

def ReleaseKey(Key):
		if Key == "Release":         #change to whatever default handgesture is to to reset keys
			ReleaseAllKeys()
			return	

		keyboard.release(Key) #releases a key.
		print(Key+" is released")
		key_states[Key] = False  # Update key state to released
		
def PressNrelease(Key):
		if Key == "Release":         #change to whatever default handgesture is to to reset keys
			ReleaseAllKeys()
			return

		ReleaseKey(Key)
		keyboard.press_and_release(Key) # presses and releases a key.
		print(Key+" is pressed and released")

def ReleaseAllKeys():	#for default hand gesture to reset 
		for key in keyboard._pressed_events:
			keyboard.release(key.name)

		print("All Keys are released")


def GetKey(Key):		     # to keys bind with specfic gesture
		keyboard.record(Key) # records keyboard activity until key is pressed

		
	

#need to press key once and not press again unless a diff gesture is detected
#if not the system will keep pressing the key over and over again
