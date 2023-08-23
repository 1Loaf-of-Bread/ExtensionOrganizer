import customtkinter
import threading
import shutil
import os

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("350x225")
        self.resizable(False, False)
        self.title("Extension Organizer v3.0.0")

        self.fileOptions = customtkinter.IntVar()
        self.failCount = 0
        self.fileCount = 0
        self.renameCount = 0
        self.organizeMethod = ""
        self.inputPath = ""
        
        self.fileCountLabel = customtkinter.CTkLabel(self, text=f"File {self.organizeMethod.title()} Count: {self.fileCount}")
        self.renameCountLabel = customtkinter.CTkLabel(self, text=f"Rename Count: {self.fileCount}")
        self.failCountLabel = customtkinter.CTkLabel(self, text=f"Fail Count: {self.fileCount}")
        self.organizeProgressBar = customtkinter.CTkProgressBar(self, orientation=customtkinter.HORIZONTAL, mode='determinate')
        self.completeLabel = customtkinter.CTkLabel(self, text="Organizing Complete.", font=('Helvatical bold',20))
        self.returnButton = customtkinter.CTkButton(self, text="Return", command=self.changeWindowMain)

        self.inputPathButton = customtkinter.CTkButton(self, text="Select Directory to Organize", command=self.getInputPath)
        self.inputPathButton.pack(pady=10)

        self.inputPathTextbox = customtkinter.CTkTextbox(self, width=330, height=50)
        self.inputPathTextbox.configure(state="disabled")
        self.inputPathTextbox.pack(pady=10)

        self.copyFilesRadioButton = customtkinter.CTkRadioButton(self, text="Copy Files", variable=self.fileOptions, value=1)
        self.copyFilesRadioButton.pack(pady=5)
        self.moveFilesRadioButton = customtkinter.CTkRadioButton(self, text="Move Files", variable=self.fileOptions, value=2)
        self.moveFilesRadioButton.pack(pady=5)

        self.organizeFilesButton = customtkinter.CTkButton(self, text="Organize Files", command=self.initOrganizeFiles)
        self.organizeFilesButton.pack(pady=10)


    def getInputPath(self):
        self.inputPath = customtkinter.filedialog.askdirectory(initialdir = "%homepath%\Desktop", title = "Select Directory to Organize")

        self.inputPathTextbox.configure(state="normal")
        self.inputPathTextbox.delete("0.0", customtkinter.END)
        self.inputPathTextbox.insert("0.0", self.inputPath)
        self.inputPathTextbox.configure(state="disabled")

        return
    

    def initOrganizeFiles(self):
        self.checkVariables()
        self.changeWindowOrganize()
        
        threading.Thread(target=self.organizeFiles).start()

        return
    

    def checkVariables(self):
        self.failCount = 0
        self.fileCount = 0
        self.renameCount = 0
        totalFileCount = 0

        for path, dirs, files in os.walk(self.inputPath):
            for file in files:
                totalFileCount += 1
        
        self.organizeProgressBar.set(0)
        self.iterStep = 1/totalFileCount
        self.progressIter = self.iterStep

        if self.fileOptions.get() != 1 and self.fileOptions.get() != 2 or self.inputPath == "":
            return

        if self.fileOptions.get() == 1:
            self.organizeMethod = "copy"
        elif self.fileOptions.get() == 2:
            self.organizeMethod = "move"

        return
    

    def changeWindowOrganize(self):
        self.inputPathButton.pack_forget()
        self.inputPathTextbox.pack_forget()
        self.copyFilesRadioButton.pack_forget()
        self.moveFilesRadioButton.pack_forget()
        self.organizeFilesButton.pack_forget()

        self.fileCountLabel.configure(text=f"File {self.organizeMethod.title()} Count: 0")
        self.fileCountLabel.pack(pady=5)

        self.renameCountLabel.configure(text=f"Rename Count: 0")
        self.renameCountLabel.pack(pady=5)

        self.failCountLabel.configure(text=f"Fail Count: 0")
        self.failCountLabel.pack(pady=5)

        self.organizeProgressBar.pack(pady=5)

        return
    

    def changeWindowMain(self):
        self.fileCountLabel.pack_forget()
        self.renameCountLabel.pack_forget()
        self.failCountLabel.pack_forget()
        self.organizeProgressBar.pack_forget()
        self.completeLabel.pack_forget()
        self.returnButton.pack_forget()

        self.inputPathButton.pack(pady=10)
        self.inputPathTextbox.pack(pady=10)
        self.copyFilesRadioButton.pack(pady=5)
        self.moveFilesRadioButton.pack(pady=5)
        self.organizeFilesButton.pack(pady=10)

        return
    

    def organizeFiles(self):
        extensionPath = f"{os.path.basename(self.inputPath)}_ExtOrg"

        for path, dirs, files in os.walk(self.inputPath):
            for file in files:
                folderExt = f"{extensionPath}\\{os.path.splitext(file)[1][1:]}"

                if not os.path.isdir(folderExt):
                    os.makedirs(folderExt)

        for path, dirs, files in os.walk(self.inputPath):
            for file in files:
                fileName = os.path.splitext(file)[0]
                fileExt = os.path.splitext(file)[1]
                folderExt = fileExt[1:]

                if os.path.isfile(f"{extensionPath}\\{folderExt}\\{file}"):
                    self.renameCount += 1

                    if self.organizeMethod == "copy":
                        try:
                            shutil.copyfile(f"{path}\\{file}", f"{extensionPath}\\{folderExt}\\ren{self.renameCount}_{file}")
                        except:
                            pass
                    else:
                        try:
                            shutil.move(f"{path}\\{file}", f"{extensionPath}\\{folderExt}\\ren{self.renameCount}_{file}")
                        except:
                            pass

                    if os.path.isfile(f"{extensionPath}\\{folderExt}\\ren{self.renameCount}_{file}"):
                        self.fileCount += 1

                        self.fileCountLabel.configure(text=f"File {self.organizeMethod.title()} Count: {self.fileCount}")
                        self.renameCountLabel.configure(text=f"Rename Count: {self.renameCount}")
                    else:
                        self.failCount += 1
                        self.renameCount -= 1

                        self.failCountLabel.configure(text=f"Fail Count: {self.failCount}")
                    
                else:
                    if self.organizeMethod == "copy":
                        try:
                            shutil.copyfile(f"{path}\\{file}", f"{extensionPath}\\{folderExt}\\{file}")
                        except:
                            pass
                    else:
                        try:
                            shutil.move(f"{path}\\{file}", f"{extensionPath}\\{folderExt}\\{file}")
                        except:
                            pass

                    if os.path.isfile(f"{extensionPath}\\{folderExt}\\{file}"):
                        self.fileCount += 1

                        self.fileCountLabel.configure(text=f"File {self.organizeMethod.title()} Count: {self.fileCount}")
                    else:
                        self.failCount += 1

                        self.failCountLabel.configure(text=f"Fail Count: {self.failCount}")

                self.progressIter += self.iterStep
                self.organizeProgressBar.set(self.progressIter)

                self.update_idletasks()

        self.completeLabel.pack(pady=10)
        self.returnButton.pack(pady=10)

        return


if __name__ == "__main__":
    app = App()
    app.mainloop()
