from smartcard.System import readers
from smartcard.util import toHexString, toBytes
from smartcard.ATR import ATR
from smartcard.CardType import ATRCardType
from smartcard.CardRequest import CardRequest
from .atr_cardtype import *


rfid = readers()
print(rfid)
