# FRCStreamDeckClient

Client to use a stream deck on a FRC Robot. Uses NetworkTables4



In the future, i plan to add:

* UI for images

* Robot-side code for complete ease-of-use

* Multiple Stream decks

* Maybe make it look pretty

Expect a build soon (in the next 2 weeks)

  

### Help! Landen forgot about this project, what do i do?

If I happen to do this, and you're unable to use a build, you need to modify the wanted images in the assets folder with what you would like,  put the dll in the `DLL` folder with your python executable (weird i know, but it's not my library), and make robot code that intercepts the key number.



### Help! The code is ugly, what is the stack?

The stack is the [python-elgato-streamdeck](https://github.com/abcminiuser/python-elgato-streamdeck) library, which takes the images in the assets folder and assigns them. The code then reaches out over networktables, specifically on the `StreamDeckData` table, and publishes data to the `true` publisher. Key info starts at 1, not zero, as the easiest way for me to publish the key info was to have 0 be disabled. 

### I want to build the application myself

Great! Here's an install line for all the dependencies `pip3 install pyntcore streamdeck pillow`
