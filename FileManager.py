from tkinter import filedialog
import os

def writeToFile(content, file_path=None):
    if file_path is None:
        # ask the user to choose a file location
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    else:
        # convert the string to compatitle file path depending on os
        file_path = os.path.normpath(file_path)
    if file_path:
        print(f"Selected export location: {file_path}")
        with open(file_path, 'w') as file:
            file.write(content)
        
def readFromFile(file_path=None):
    if file_path is None:
        # ask the user to choose a file location
        file_path = filedialog.askopenfilename(title="Select a file", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    else:
        # convert the string to compatitle file path depending on os
        file_path = os.path.normpath(file_path)
    # start reading from file
    if file_path:
        print(f"Selected file: {file_path}")
        with open(file_path, 'r') as file:
            content = file.read()
            return content, file.name
    else: return None, ""
        
def readFromFolder(folder_name):
        # get the folder directory
        folder_path = os.path.join(os.getcwd(), folder_name)
        print(f"cwd: {folder_path}")
        
        # get all files within that folder
        files = os.listdir(folder_path)
        contents = []
        fnames = []
        # loop through each file
        for file_name in files:
            file_path = os.path.join(folder_path, file_name)
            # read from the file and extract its data
            if os.path.isfile(file_path):
                with open(file_path, 'r') as file:
                    content = file.read()
                    contents.append(content)
                fnames.append(file_name)
                    
        return contents, fnames
    
def deleteFile(file_path):
    try:
        # convert the string to compatitle file path depending on os
        file_path = os.path.normpath(file_path)
        # Attempt to delete the file
        os.remove(file_path)
        print(f"The file {file_path} has been deleted successfully.")
    except FileNotFoundError:
        print(f"The file {file_path} does not exist.")
    except Exception as e:
        print(f"An error occurred: {e}")