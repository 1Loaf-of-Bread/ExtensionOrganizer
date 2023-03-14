from colorama import Fore, init
from time import sleep
import shutil
import os
init(autoreset=True)


def getSourcePath():
    userHelp = False
    
    while True:
        os.system("cls")
        
        print("~~~ Folder Path Entry ~~~")
        print()

        if userHelp == True:
            print(f"{Fore.CYAN}Example: {Fore.WHITE}C:\\Users\\computeruser1\\Desktop\\Folder to Organize")
            print()

        sourcePath = input("Enter Exact Path of The Folder: ")

        
        if os.path.isdir(sourcePath):
            break
        else:
            print()
            print(f"{Fore.RED}ERROR!: {Fore.WHITE}The Path '{sourcePath}' Does not Exist.")

            sleep(1)

            userHelp = True

    print()
    print(f"{Fore.GREEN}Found Folder.")
    sleep(1)
    print()

    return sourcePath


def createExtensionFolders(sourcePath):
    destPath = f"{os.path.basename(sourcePath)}_extOrg"

    if not os.path.isdir(destPath):
        os.mkdir(destPath)

    for path, dir, files in os.walk(sourcePath):
        for file in files:
            fileExt = os.path.splitext(file)[1]

            if not os.path.isdir(f"{destPath}\\{fileExt}"):
                os.mkdir(f"{destPath}\\{fileExt}")
                
                if os.path.isdir(f"{destPath}\\{fileExt}"):
                    print(f"{Fore.MAGENTA}Created Folder: {Fore.WHITE}{destPath}\\{fileExt}")
                else:
                    print(f"{Fore.RED}ERROR!: {Fore.WHITE}Failed to Create Folder \"{destPath}\\{fileExt}\"")
                    print()

                    input("Press ENTER to Exit...")
                    exit()

    sleep(1)
    print()

    return


def extensionOrganize(sourcePath, organize):
    renameCount = 0
    failCount = 0
    fileCount = 0

    for path, dir, files in os.walk(sourcePath):
        for file in files:
            fileName = os.path.splitext(file)[0]
            fileExt = os.path.splitext(file)[1]
            pathFile = f"{path}\\{file}"
            folderDest = f"{os.path.basename(sourcePath)}_extOrg\\{fileExt}"

            if file != __file__:
                if not os.path.isfile(f"{folderDest}\\{file}"):
                    try:
                        if organize == "move":
                            shutil.move(pathFile, f"{folderDest}\\{file}")
                        else:
                            shutil.copyfile(pathFile, f"{folderDest}\\{file}")
                    except:
                        pass
                
                    if os.path.isfile(f"{folderDest}\\{file}"):
                        fileCount += 1

                        if organize == "move":
                            print(f"{Fore.GREEN}Moved File: {Fore.WHITE}{file}")
                        else:
                            print(f"{Fore.GREEN}Copied File: {Fore.WHITE}{file}")

                        print(f"    {Fore.GREEN}To: {Fore.WHITE}{folderDest}")
                    else:
                        failCount += 1

                        if organize == "move":
                            print(f"{Fore.RED}Failed to Move File: {Fore.WHITE}{file}")
                        else:
                            print(f"{Fore.RED}Failed to Copy File: {Fore.WHITE}{file}")
                else:
                    renameCount += 1

                    fileRename = f"ren{renameCount}_{fileName}{fileExt}"

                    try:
                        if organize == "move":
                            shutil.move(pathFile, fileRename)
                        else:
                            shutil.copyfile(pathFile, fileRename)
                    except:
                        pass

                    if os.path.isfile(fileRename):
                        print(f"{Fore.YELLOW}Renamed File: {Fore.WHITE}{file}")
                        print(f"    {Fore.YELLOW}To: {Fore.WHITE}{fileRename}")

                        try:
                            shutil.move(fileRename, f"{folderDest}\\{fileRename}")
                        except:
                            pass

                        if os.path.isfile(f"{folderDest}\\{fileRename}"):
                            fileCount += 1

                            if organize == "move":
                                print(f"{Fore.GREEN}Moved File: {Fore.WHITE}{fileRename}")
                            else:
                                print(f"{Fore.GREEN}Copied File: {Fore.WHITE}{fileRename}")

                            print(f"    {Fore.GREEN}To: {Fore.WHITE}{folderDest}")
                        else:
                            failCount += 1

                            if organize == "move":
                                print(f"{Fore.RED}Failed to Move File: {Fore.WHITE}{fileRename}")
                            else:
                                print(f"{Fore.RED}Failed to Copy File: {Fore.WHITE}{fileRename}")

                            os.rename(fileRename, pathFile)

                            renameCount -= 1

                            print(f"    {Fore.MAGENTA}Reverted Changes Made to File.")
                    else:
                        failCount += 1
                        
                        print(f"{Fore.RED}Failed to Rename File: {Fore.WHITE}{pathFile}")

    return failCount, fileCount, renameCount


if __name__ == "__main__":
    while True:
        os.system("cls")

        print("~~~~~~~~ Main Menu ~~~~~~~~")
        print("|                         |")
        print("|    1. Move Files        |")
        print("|    2. Copy Files        |")
        print("|                         |")
        print("|    e. Exit              |")
        print("|                         |")
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        print()
        
        choice = input("--> ")

        if choice != "1" and choice != "2" and choice != "e":
            print()
            print(f"{Fore.RED}ERROR!: {Fore.WHITE}Please enter either 1, 2 or e.")
            sleep(1)
        else:
            if choice == "e":
                exit()

            sourcePath = getSourcePath()

            createExtensionFolders(sourcePath)

            if choice == "1":
                failCount, fileCount, renameCount = extensionOrganize(sourcePath, "move")

                print()
                print()
                print("~~~ Folder Orginization Complete ~~~")
                print("|                                  |")
                print(f"|     Files Moved: {fileCount}")
                print(f"|     Failed File Moves: {failCount}")
                print(f"|     Files Renamed: {renameCount}")
                print("|                                  |")
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                print()

                input("Press ENTER to Continue...")
            else:
                failCount, fileCount, renameCount = extensionOrganize(sourcePath, "copy")

                print()
                print()
                print("~~~ Folder Orginization Complete ~~~")
                print("|                                  |")
                print(f"|     Files Copied: {fileCount}")
                print(f"|     Failed File Copies: {failCount}")
                print(f"|     Files Renamed: {renameCount}")
                print("|                                  |")
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                print()

                input("Press ENTER to Continue...")
