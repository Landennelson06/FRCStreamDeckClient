from ntcore import NetworkTableInstance,_logutil
import yaml
from StreamDeck.DeviceManager import DeviceManager
from tkinter import *
from threading import Thread,Event
from tkinter import messagebox
import os
from StreamDeck.ImageHelpers import PILHelper
from PIL import Image, ImageDraw, ImageFont
import psutil 
ASSETS_PATH = os.path.join(os.path.dirname(__file__), "assets")
ICON_PATH = os.path.join(os.path.dirname(__file__), "ico")
VERSON_NO = "0.15a"
class updateVars(Thread):
    def __init__(self, event):
        Thread.__init__(self)
        self.stopped = event

    def run(self):
        while not self.stopped.wait(0.1):
            global deckConnect
            if(len(DeviceManager().enumerate()) != deckConnect):
                    loadStreamDeck()
                    deckConnect = len(DeviceManager().enumerate())    
            checkStreamDeck()
            if(inst.isConnected()):
                isConn.set("Connected to bot") 
            else:
                isConn.set("Disconnected from bot")   
            try:
                if(len(DeviceManager().enumerate()) >0):
                    isConnSD.set("Deck Connected")
                else:
                    isConnSD.set("No Deck Connected")
            except Exception as e:
                if "main thread is not in" not in str(e):
                    messagebox.showerror("Error!", "Uh Oh! An error occurred: \n" + str(e))
                    on_closing()
def checkStreamDeck():
    if("StreamDeck.exe" in (i.name() for i in psutil.process_iter())):
            messagebox.showerror("Error!", "Close StreamDeck Before Use")
def loadStreamDeck():
    streamdecks = DeviceManager().enumerate()
    for index, deck in enumerate(streamdecks):
        # This example only works with devices that have screens.
        if not deck.is_visual():
            continue

        deck.open()
        deck.reset()

        # print("Opened '{}' device (serial number: '{}', fw: '{}')".format(
        #     deck.deck_type(), deck.get_serial_number(), deck.get_firmware_version()
        # ))

        # Set initial screen brightness to 30%.
        deck.set_brightness(30)

        # Set initial key images.
        for key in range(deck.key_count()):
            update_key_image(deck, key, False)

        # Register callback function for when a key state changes.
        deck.set_key_callback(key_change_callback)

# Generates a custom tile with run-time generated text and custom image via the
# PIL module.
def render_key_image(deck, icon_filename, font_filename, label_text):
    # Resize the source image asset to best-fit the dimensions of a single key,
    # leaving a margin at the bottom so that we can draw the key title
    # afterwards.
    icon = Image.open(icon_filename)
    image = PILHelper.create_scaled_key_image(deck, icon, margins=[0, 0, 0, 0])

    # Load a custom TrueType font and use it to overlay the key index, draw key
    # label onto the image a few pixels from the bottom of the key.
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font_filename, 14)
    draw.text((image.width, image.height), text="", font=font, anchor="ms", fill="white")

    return PILHelper.to_native_key_format(deck, image)
def get_key_style(deck, key, state):
    # Last button in the example application is the exit button.
        name = "emoji"
        icon = "{}.png".format(key)
        font = "Roboto-Regular.ttf"
        label = "{}".format(key)

        return {
            "name": name,
            "icon": os.path.join(ASSETS_PATH, icon),
            "font": os.path.join(ASSETS_PATH, font),
            "label": label
    }
def update_key_image(deck, key, state):
    # Determine what icon and label to use on the generated key.
    key_style = get_key_style(deck, key, state)

    # Generate the custom key with the requested image and label.
    image = render_key_image(deck, key_style["icon"], key_style["font"], key_style["label"])

    # Use a scoped-with on the deck to ensure we're the only thread using it
    # right now.
    with deck:
        # Update requested key with the generated image.
        deck.set_key_image(key, image)
def key_change_callback(deck, key, state):
    # Print new key state
    if(state):
        truePublisher.set(key+1,0)
    else:
        truePublisher.set(0,0)
        

    # Update the key image based on the new key state.
    update_key_image(deck, key, state)

    # Check if the key is changing to the pressed state.
    if state:
        key_style = get_key_style(deck, key, state)
def on_closing():
    print("Closing")
    stopFlag.set()
    root.quit()
    root.destroy()
root = Tk()
root.protocol("WM_DELETE_WINDOW", on_closing)
if __name__ == '__main__':
    # When this module is run (not imported) then create the app, the
    # frame, show it, and start the event loop.
    global inst
    inst = NetworkTableInstance.getDefault()
    table = inst.getTable("StreamDeckData")
    global trueTopic
    trueTopic = table.getIntegerTopic("true")
    global truePublisher
    truePublisher = trueTopic.publish()
    inst.startClient4("StreamDeckClient")
    inst.startDSClient() # recommended if running on DS computer; this gets the robot IP from the DS    
    # root window title and dimension
    root.title("FRC Stream Deck Client")
    # Set geometry (widthxheight)
    root.geometry('350x200')
    root.iconbitmap(os.path.join(ICON_PATH, "FRCStreamDeckIcon.ico"))

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

    verLabel = Label(root, text=VERSON_NO)
    verLabel.place(x=350, y=200,anchor=SE)

    # all widgets will be here
    # Execute Tkinter
    stopFlag = Event()
    thread = updateVars(stopFlag)

    
    thread.start()
    root.mainloop()
