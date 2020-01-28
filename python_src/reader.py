from smartcard.System import readers
from smartcard.util import toHexString, toBytes
from smartcard.ATR import ATR
from smartcard.CardType import ATRCardType, AnyCardType

from smartcard.CardRequest import CardRequest
from atr_cardtype import *


rfid = readers()
print(rfid)

cardtype = AnyCardType()

while(1):
	cardrequest = CardRequest( timeout=10, cardType=cardtype )
	cardservice = cardrequest.waitforcard()
	cardservice.connection.connect()

	detected_card = toHexString(cardservice.connection.getATR())
	#print(detected_card)
	#print(ATR_STUDENT_CARD)
	#print(cardservice.connection.getReader())

	if detected_card == ATR_STUDENT_CARD_HEX:
		print("STUDENT CARD INSERTED!")
	elif detected_card == ATR_RASPI_TAG_HEX:
		print("RASPBERY BOARD TAG DETECTED!")
	else:
		print("Warning. We don't know this card!")
