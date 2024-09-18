import MetaTrader5 as mt5
from modules.components.customDialog import Dialog

def initConnect(userData):
    esto = [86330370,"Q+Jx2pSd", "MetaQuotes-Demo"]
    
    userLogin, userPassword, metaServer = userData
    
    response = mt5.initialize(
        login=int(userLogin),
        password=userPassword,
        server=metaServer
    )
    
    if response:
        print("Conexión exitosa")
        Dialog("Connected").exec_()
        return True
    else:
        print("Error initializing MT5")
        Dialog("Error 😂").exec_()
        return False
        
    # Me quedé por aquí


