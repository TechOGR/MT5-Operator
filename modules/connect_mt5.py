import MetaTrader5 as mt5
from modules.components.customDialog import Dialog

def initConnect(userData):
    esto = [86330370,"Q+Jx2pSd", "MetaQuotes-Demo"]
    userLogin, userPassword, metaServer = userData

    if response := mt5.initialize(
        login=int(userLogin), password=userPassword, server=metaServer
    ):
        return _openDialog("Conexión exitosa", "Connected", True)
    else:
        return _openDialog("Error initializing MT5", "Error 😂", False)


def _openDialog(arg0, msg, value):
    print(arg0)
    Dialog(msg).exec_()
    return value