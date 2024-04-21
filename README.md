# FRCStreamDeckClient

Client to use a stream deck on a FRC Robot. Uses NetworkTables4

In the future, i plan to add:

* [ ] UI for images

* [ ] Multiple Stream decks

 

### Help! The code is ugly, what is the stack?

The stack is the [python-elgato-streamdeck](https://github.com/abcminiuser/python-elgato-streamdeck) library, which takes the images in the assets folder and assigns them. The code then reaches out over networktables, specifically on the `StreamDeckData` table, and publishes data to the `true` publisher. Key info starts at 1, not zero, as the easiest way for me to publish the key info was to have 0 be disabled. 

### I want to build the application myself

Great! Here's an install line for all the dependencies `pip3 install pyntcore streamdeck pillow psutil pyinstaller`, and run `pyinstaller mainWindow.spec`, and your build will be in the `dist` folder. 

### How do I use this?

    Download the latest build from the releases tab on Github. Extract and open. Change assets using the `Open Assets Folder` button on the UI as needed. In your RobotContainer, add this method:

```java  
private void configureStreamDeck(){
    NetworkTableInstance inst = NetworkTableInstance.getDefault();
    NetworkTable table = inst.getTable("StreamDeckData");
    IntegerSubscriber data = table.getIntegerTopic("true").subscribe(0);
    new Trigger(()->Math.toIntExact(data.get()) == 1)
      .onTrue(intakeout);
    new Trigger(()->Math.toIntExact(data.get()) == 7)
      .onTrue(handoff);
  }
```

Change the triggers as needed, and run this method on RobotContainer construction. 



### I want to use a Stream Deck XL/Mini/etc

Check the [python-elgato-streamdeck](https://github.com/abcminiuser/python-elgato-streamdeck) library. If it supports it, the only thing this application will need is more/less assets with the correct index name.  
