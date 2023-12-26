from tkinter import filedialog

def writeToFile(content):
    # ask the user to choose a file location
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        print(f"Selected export location: {file_path}")
        with open(file_path, 'w') as file:
            file.write(content)
        
def readFromFile():
    # ask the user to choose a file location
    file_path = filedialog.askopenfilename(title="Select a file", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        print(f"Selected file: {file_path}")
        with open(file_path, 'r') as file:
            content = file.read()
            return content