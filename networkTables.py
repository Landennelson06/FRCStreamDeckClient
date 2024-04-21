from ntcore import NetworkTableInstance,_logutil
def startNT():
    global inst
    inst = NetworkTableInstance.getDefault()
    table = inst.getTable("StreamDeckData")
    global trueTopic
    trueTopic = table.getIntegerTopic("true")
    global truePublisher
    truePublisher = trueTopic.publish()
    inst.startClient4("StreamDeckClient")
    inst.startDSClient() # recommended if running on DS computer; this gets the robot IP from the DS
def set(key):
    truePublisher.set(key,0)
def isConn():
    global inst
    return bool(inst.isConnected())