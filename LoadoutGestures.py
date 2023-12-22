#For Testing 
#can transfer to the loadout.py in the future

import numpy as np

GestureArr = [] # How many Gestures does the file have
KeyBoardArr = [] # How many Gestures does the file have
#gesture and keyboard array are linked 1:1 so if the array is inconsistant will have problem

min_detection_confidence = 0.5 #settings configs 
min_tracking_confidence  = 0.5 #settings configs 

#TotalList
GestureKeyBoardArr = []

#loadout Loading gestures
#to load the gestures
def Loadgestures(): 
        global GestureKeyBoardArr       

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
        KeyBoardArr.append("Release")
        #Add Loaded Gestures
        #GestureArr.append("")
        #KeyBoardArr.append("")

        #GestureArr.remove(Key)
        #KeyBoardArr.remove(Key)

        GestureKeyBoardArr= np.array([GestureArr,KeyBoardArr])
      
        print("Loadout Gestures Loaded")

#to save gesture to specfic Key
def SaveGesture(Num):
        GestureArr.append(Gesture)
        KeyBoardArr.append(Key)
        print("Gesture saved")
        
def DeleteGesture(Num):
        GestureArr.append(Gesture)
        KeyBoardArr.append(Key)
        print("Gesture deleted")
       
def SaveLoadoutFile(File_path):# to export/save import
        #file = open("Loadout/LoadOutTest.txt", "w") #w means create file, but will override if possible

        file = open(File_path, "w") #w means create file, but will override if possible

        file.write(str(min_detection_confidence)+"\n")
        file.write(str(min_tracking_confidence)+"\n")

        for x in range(len(GestureArr)): # writes "Gesture inputtrigger" on each line 
            file.write(GestureArr[x]+" ")
            file.write(KeyBoardArr[x]+"\n")

  
        file.close()
        print("LoadOut File saved")

def LoadLoadoutFile(File_path):#import/read file
        global GestureKeyBoardArr      

        #with open("Loadout/LoadOutTest.txt") as file:
        with open(File_path) as file:
            GestureArr.clear()
            KeyBoardArr.clear() 

            min_detection_confidence = float(file.readline())
            print(str(min_detection_confidence)+"\n")
            min_tracking_confidence = float(file.readline())
            print(str(min_tracking_confidence)+"\n")

            #read each line by line
            for each in file:
                #print (each)
                first_word = each.split()[0] #GestureArr
                sec_word = each.split()[1] #KeyBoardArr
            
                print(first_word+"\n")
                print(sec_word+"\n")
                GestureArr.append(first_word)
                KeyBoardArr.append(sec_word)

            GestureKeyBoardArr= np.array([GestureArr,KeyBoardArr])
        file.close()
        
        print("LoadOut File Loaded to gesture")
