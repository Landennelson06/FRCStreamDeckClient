from StreamDeck.DeviceManager import DeviceManager
from StreamDeck.ImageHelpers import PILHelper
from PIL import Image, ImageDraw, ImageFont
import os
import constants
import networkTables
def loadStreamDeck():
    streamdecks = DeviceManager().enumerate()
    for index, deck in enumerate(streamdecks):

        if not deck.is_visual():
            continue

        deck.open()
        deck.reset()

        # Set initial screen brightness to 30%.
        deck.set_brightness(30)

        # Set initial key images.
        for key in range(deck.key_count()):
            notPressed(deck, key)

        # Register callback function for when a key state changes.
        deck.set_key_callback(key_change_callback)

# Generates a custom tile with run-time generated text and custom image via the
# PIL module.
def render_key_image(deck, icon_filename, margins=[0, 0, 0, 0]):
    # Resize the source image asset to best-fit the dimensions of a single key,
    # leaving a margin at the bottom so that we can draw the key title
    # afterwards.
    icon = Image.open(icon_filename)
    image = PILHelper.create_scaled_key_image(deck, icon, margins)

    return PILHelper.to_native_key_format(deck, image)

def key_change_callback(deck, key, state):
    if(state):
        isPressed(deck,key)
        networkTables.set(key+1)
    else:
        notPressed(deck,key)
        networkTables.set(0)
        
def isPressed(deck,key):
    icon = "{}.png".format(key)
    iconPath = os.path.join(constants.ASSETS_PATH, icon)
    exists = os.path.exists(iconPath)
    if(exists):
        with deck:
            deck.set_key_image(key, render_key_image(deck, iconPath, margins=[10,10,10,10]))
def notPressed(deck,key):
    icon = "{}.png".format(key)
    iconPath = os.path.join(constants.ASSETS_PATH, icon)
    exists = os.path.exists(iconPath)
    if(exists):
        with deck:
            deck.set_key_image(key, render_key_image(deck, iconPath ))

def getDeckNum():
     return int(len(DeviceManager().enumerate()))