#For Testing 
#can transfer to the loadout.py in the future

GestureArr = [] # How many Gestures does the file have
KeyBoardArr = [] # How many Gestures does the file have

#TotalList
#GestureKeyBoardArr =[TotalList][,GestureArr,KeyBoardArr] # test if better to use 2d

#loadout Loading gestures
def Loadgestures(): #to load the gestures

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

        # min_detection_confidence #settings configs 
        # min_tracking_confidence= #settings configs 
