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
        GestureArr.append("Victory")
        KeyBoardArr.append("space")
        
        #Add Loaded Gestures
        GestureArr.append("Open_Palm")
        KeyBoardArr.append("w")

        #Add Loaded Gestures
        GestureArr.append("Thumb_Up")
        KeyBoardArr.append("a")

        #Add Loaded Gestures
        GestureArr.append("Thumb_Down")
        KeyBoardArr.append("d")

        #Add Loaded Gestures
        GestureArr.append("Pointing_Up")
        KeyBoardArr.append("s")
        
        #Add Loaded Gestures
        GestureArr.append("Closed_Fist")    #default handgesture to reset everything else
        #KeyBoardArr.append("space")

        #Add Loaded Gestures
        #GestureArr.append("")
        #KeyBoardArr.append("")

        #GestureArr.remove(Key)
        #KeyBoardArr.remove(Key)

#to save gesture to specfic Key
def SaveGesture(Num):
        GestureArr.append(Gesture)
        KeyBoardArr.append(Key)
        print("Gesture saved")
        
def DeleteGesture(Num):
        GestureArr.append(Gesture)
        KeyBoardArr.append(Key)
        print("Gesture deleted")
       
def SaveLoadoutFile():
        file = open("Loadout/LoadOutTest.txt", "w") #w means create file, but will override if possible

        for x in range(len(GestureArr)): # writes "Gesture inputtrigger" on each line 
            file.write(GestureArr[x]+" ")
            file.write(KeyBoardArr[x]+"\n")

        file.write(str(min_detection_confidence)+"\n")
        file.write(str(min_tracking_confidence)+"\n")
        file.close()
        print("LoadOut File saved")

def LoadLoadoutFile():
        file = open("Loadout/LoadOutTest.txt", "r") # Read file
        print("LoadOut File Loaded")
