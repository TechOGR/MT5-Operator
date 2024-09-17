import json
from os import (
    getcwd
)
from os.path import (
    join
)

pathFile = join(getcwd(), "config", "userData.json")

def convertInt(user):
    try:
        int(user)
        return True
    except:
        return False

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
    except:
        print("ERROR while we saving your file")

def saveData(path_, dataUser_) -> None:
    MIN_CHAR = 8
    MAX_CHAR = 15

    user, password, server = dataUser_

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
    
def loadData():
    try:
        with open(pathFile, "r") as rF:
            data = json.load(rF)
            rF.close()
            print("File loaded: ", data)
            return data
    except:
        print("ERROR loading data from config file")
        return False