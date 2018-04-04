DEBUG = False

def log(s):
    if DEBUG:
        print ("DEBUG: " + s)

def setDebug():
    DEBUG = True
