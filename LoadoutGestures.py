#For Testing 
#can transfer to the loadout.py in the future

GestureArr = [] # How many Gestures does the file have
KeyBoardArr = [] # How many Gestures does the file have

 min_detection_confidence = 0.5 #settings configs 
 min_tracking_confidence  = 0.5 #settings configs 

#TotalList
#GestureKeyBoardArr =[TotalList][,GestureArr,KeyBoardArr] # test if better to use 2d

#loadout Loading gestures
#to load the gestures
def Loadgestures(): 

        #Clear Loaded Gestures 
        GestureArr.clear()
        KeyBoardArr.clear() 
       
        #Add Loaded Gestures
        GestureArr.append("Closed_Fist")
        KeyBoardArr.append("space")

        #Add Loaded Gestures
        #GestureArr.append("")
        #KeyBoardArr.append("")

        #GestureArr.remove(Key)
        #KeyBoardArr.remove(Key)

#to save gesture to specfic Key
def SaveGesture(Num):
        GestureArr.append(Gesture)
        KeyBoardArr.append(Key)
        
def DeleteGesture(Num):
        GestureArr.append(Gesture)
        KeyBoardArr.append(Key)
        