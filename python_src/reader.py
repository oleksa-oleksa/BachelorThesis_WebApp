from smartcard.System import readers
from smartcard.util import toHexString, toBytes
from smartcard.ATR import ATR
from smartcard.CardType import ATRCardType, AnyCardType

from smartcard.CardRequest import CardRequest
from atr_cardtype import *


rfid = readers()
print(rfid)

cardtype = AnyCardType()
cardrequest = CardRequest( timeout=10, cardType=cardtype )
cardservice = cardrequest.waitforcard()
cardservice.connection.connect()

detected_card = toHexString(cardservice.connection.getATR())
print(cardservice.connection.getReader())
