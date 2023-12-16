import keyboard

#https://stackabuse.com/guide-to-pythons-keyboard-module/

def PressKey(Key)
		keyboard.press(key)	  #press a key.


def ReleaseKey(Key)
		keyboard.release(key) #releases a key.

		
def PressNrelease(Key)
		keyboard.send(key) # presses and releases a key.

def GetKey(Key)				 # to link keys with specfic gesture
		keyboard.record(key) # records keyboard activity until key is pressed