from colorama import Fore, init
from time import sleep
import shutil
import os
init(autoreset=True)


def getPath(): # Function to get the user input for exact path, and check if the path exists.
    userHelp = False
    
    while True:
        os.system("cls") # Clears the terminal.

        print("Enter Exact URL of Folder.")
        print()

        if userHelp == True:
            print(f"{Fore.CYAN}Example: {Fore.WHITE}C:\\Users\\computer1\\Desktop\\Folder to Organize")
            print()

        sourcePath = input("--> ") # Gets user input.

        
        if os.path.isdir(sourcePath): # Checks if user input matches a directory on computer.
            break
        else:
            userHelp = True

    print()
    print(f"{Fore.GREEN}Folder Exists!")
    sleep(1)

    createExtensionFolders(sourcePath)


def createExtensionFolders(sourcePath): # Function to create extension folders for files in user input directory tree.
    for path, dir, files in os.walk(sourcePath): # Walks through all files in the directory tree of the user input path.
        for file in files:
            fileExt = os.path.splitext(file)[1]

            if not os.path.isdir(fileExt):
                os.makedirs(fileExt)
                
                if os.path.isdir(fileExt): # Checks if the extension folder exists for this extension, if not, create it.
                    print(f"{Fore.MAGENTA}Created Folder: {Fore.WHITE}{fileExt}")
                else:
                    print(f"{Fore.RED}ERROR!: {Fore.WHITE}Failed to Create Folder '{fileExt}'")
                    print()

                    input("Press ENTER to Exit...")
                    exit()

    moveFiles(sourcePath)


def moveFiles(sourcePath): # Function to move files to designated extension folders.
    renameCount = 0
    failCount = 0
    moveCount = 0

    for path, dir, files in os.walk(sourcePath):
        for file in files:
            fileName = os.path.splitext(file)[0]
            fileExt = os.path.splitext(file)[1]
            pathFile = f"{path}\\{file}"

            if not os.path.isfile(f"{fileExt}\\{file}"): # Checks if the file already exists in the designated extension folder, is it does, rename the file.
                shutil.move(pathFile, fileExt)
            
                if os.path.isfile(f"{fileExt}\\{file}"): # Check if the file was successfully moved.
                    print(f"{Fore.GREEN}Moved File: {Fore.WHITE}{file}")
                    moveCount += 1
                else:
                    print(f"{Fore.RED}Failed to Move File: {Fore.WHITE}{file}")
                    failCount += 1
            else:
                renameCount += 1

                os.rename(pathFile, f"{path}\\{fileName} ~rename{renameCount}~{fileExt}") # Rename the file.
                shutil.move(f"{path}\\{fileName} ~rename{renameCount}~{fileExt}", fileExt) # Move the file to the designated extension folder.
            
                if os.path.isfile(f"{fileExt}\\{fileName} ~rename{renameCount}~{fileExt}"): # Check if the file was successfully moved.
                    print(f"{Fore.CYAN}Renamed File '{Fore.WHITE}{file}{Fore.CYAN}' to '{Fore.WHITE}{fileName} ~rename{renameCount}~{fileExt}{Fore.CYAN}'")
                    print(f"{Fore.GREEN}Moved File: {Fore.WHITE}{fileName} ~rename{renameCount}~{fileExt}")

                    moveCount += 1
                else:
                    print(f"{Fore.CYAN}Renamed File '{Fore.WHITE}{file}{Fore.CYAN}' to '{Fore.WHITE}{fileName} ~rename{renameCount}~{fileExt}{Fore.CYAN}'")
                    print(f"{Fore.RED}Failed to Move File: {Fore.WHITE}{fileName} ~rename{renameCount}~{fileExt}")

                    failCount += 1

    complete(failCount, moveCount, renameCount)


def complete(failCount, moveCount, renameCount):
    os.system("cls")

    print("~~~ Folder Orginization Complete ~~~")
    print()
    print(f"     Files Moved: {moveCount}")
    print(f"     Failed File Moves: {failCount}")
    print(f"     Files Renamed: {renameCount}")
    print()
    input("Press ENTER to Exit...")
    
    exit()



getPath()