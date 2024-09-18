import json
from os import (
    getcwd,
    mkdir
)
from os.path import (
    join,
    exists
)
from modules.components.customDialog import Dialog

pathFolder = join(getcwd(), "config")
pathFile = join(pathFolder, "userData.json")

# Creating folder Config for file config
def createConfigFolder():
    print(pathFolder)
    try:
        mkdir(pathFolder)
        with open(pathFile, "w") as f:
            json.dump(
                {
                    "User": "First you",
                    "Pass": "must save",
                    "Server": "any data :)"
                },f
            )
    except:
        print("ERROR while we try create the folder")

# Convert to integer the user mt5
def convertInt(user):
    try:
        int(user)
        return True
    except:
        return False

# Save the UserData in the file 
def toSave(user, passwd, server) -> None:
    
    values = {
        "User": user,
        "Pass": passwd,
        "Server": server
    }
    
    try:
        with open(pathFile, "w") as f:
            json.dump(values, f)
            f.close()
            print("File Saved")
            Dialog("Data Saved !").exec_()
    except:
        print("ERROR while we saving your file")

# First Check for save the userData
def saveData(path_, dataUser_) -> None:
    MIN_CHAR = 8
    MAX_CHAR = 15

    user, password, server = dataUser_

    if not exists(pathFolder):
        createConfigFolder()
    else:
        if len(user) < MIN_CHAR or len(user) > MAX_CHAR and len(password) < MIN_CHAR or len(password) > MAX_CHAR:
            print("User and Password does not meet the minimum requirements")
        elif len(user) < MIN_CHAR or len(user) > MAX_CHAR:
            print("User does meet the minimum requirements")
        elif len(password) < MIN_CHAR or len(password) > MAX_CHAR:
            print("Password does not meet the minimum requirements")
        elif len(server) == 0:
            print("Please select one Server from the Server List")
        elif not convertInt(user):
            print("Please check your USER must be number")
        else:
            print(path_, user, password, server)
            toSave(
                int(user),
                password,
                server
            )    

# Load userData from ConfigFile
def loadData():
    if not exists(pathFolder):
        print("ERROR any data has been saved !")
        return False
    else:
        try:
            with open(pathFile, "r") as rF:
                data = json.load(rF)
                rF.close()
                print("File loaded: ", data)
                return data
        except:
            print("ERROR loading data from config file")
            return False