import yaml
from tkinter import *
from threading import Thread,Event
from tkinter import messagebox
import os
import psutil 
import streamDeck
import constants
import networkTables
def checkStreamDeck():
    if("StreamDeck.exe" in (i.name() for i in psutil.process_iter())):
            messagebox.showerror("Error!", "Close StreamDeck Application Before Use")
class updateVars(Thread):
    def __init__(self, event):
        Thread.__init__(self)
        self.stopped = event

    def run(self):
        while not self.stopped.wait(0.1):
            global deckConnect
            deckNum = streamDeck.getDeckNum()
            if(deckNum != deckConnect):
                    streamDeck.loadStreamDeck()
                    deckConnect = deckNum    
            checkStreamDeck()
            if(networkTables.isConn()):
                isConn.set("Connected to bot") 
            else:
                isConn.set("Disconnected from bot")   
            try:
                if(deckNum > 0):
                    isConnSD.set("Deck Connected")
                else:
                    isConnSD.set("No Deck Connected")
            except Exception as e:
                if "main thread is not in" not in str(e):
                    messagebox.showerror("Error!", "Uh Oh! An error occurred: \n" + str(e))
                    on_closing()


def on_closing():
    print("Closing")
    root.withdraw()
    stopFlag.set()
    root.quit()
def openAssets():
    os.startfile(constants.ASSETS_PATH)
root = Tk()
root.protocol("WM_DELETE_WINDOW", on_closing)
if __name__ == '__main__':
    # When this module is run (not imported) then create the app, the
    # frame, show it, and start the event loop.
    networkTables.startNT()
    # root window title and dimension
    root.title("FRC Stream Deck Client")
    # Set geometry (widthxheight)
    root.geometry('350x200')
    root.iconbitmap(os.path.join(constants.ICON_PATH, "FRCStreamDeckIcon.ico"))

    global deckConnect
    deckConnect = 0
    global isConn
    isConn = StringVar(root, "Loading...")
 
    isConnLabel = Label(root, textvariable=isConn)
    isConnLabel.pack()
    
    global isConnSD
    isConnSD = StringVar(root, "Loading...")
 
    isConnSDLabel = Label(root, textvariable=isConnSD)
    isConnSDLabel.pack()

    verLabel = Label(root, text=constants.VERSON_NO)
    verLabel.place(x=350, y=200,anchor=SE)

    fileLocation = Button(root, text="Open Assets Folder", command= openAssets  )
    reloadAssets = Button(root, text="Reload assets", command=streamDeck.loadStreamDeck)

    # fileLocation.place(x=50, y=150,anchor=NW)
    # reloadAssets.place(x=300, y=150,anchor=NW)
    fileLocation.pack()
    reloadAssets.pack()
    # all widgets will be here
    # Execute Tkinter
    stopFlag = Event()
    thread = updateVars(stopFlag)

    
    thread.start()
    root.mainloop()
