from smartcard.System import readers
from smartcard.util import toHexString, toBytes
from smartcard.ATR import ATR
from smartcard.CardType import ATRCardType, AnyCardType
from smartcard.CardMonitoring import CardMonitor, CardObserver


from smartcard.CardRequest import CardRequest
from atr_cardtype import *

READER = "ACS ACR122U PICC Interface 00 00"

class PrintObserver(CardObserver):
    """A simple card observer that is notified
    when cards are inserted/removed from the system and
    prints the list of cards
    """

    def update(self, observable, actions):
        (addedcards, removedcards) = actions
        for card in addedcards:
            print("+Inserted: ", toHexString(card.atr))
        for card in removedcards:
            print("-Removed: ", toHexString(card.atr))

def print_atr_info(atr):
	print('historical bytes: ', toHexString(atr.getHistoricalBytes()))
	print('checksum: ', "0x%X" % atr.getChecksum())
	print('checksum OK: ', atr.checksumOK)
	# T = 0 is a byte oriented protocol
	print('T0  supported: ', atr.isT0Supported())
	# T = 1 is a block-of-bytes oriented protocol
	print('T1  supported: ', atr.isT1Supported())
	print('T15 supported: ', atr.isT15Supported())
	

def print_readers_info(r):
	if r is None:
		print("No connected readers found.")
		raise TypeError
		
	print("Found readers:", r)
	

# not in use right now	
def connect_card_reader():
	"""
	The list of available readers is retrieved with the readers() function. 
	and connect to the card with the connect() method of the connection. 
	We can then send APDU commands to the card with the transmit() method.
	"""
	r = readers()
	print_readers_info(r)
	
	"""
	We create a connection with the first reader (index 0 for reader 1, 1 for reader 2, ...) 
	with the r[0].createConnection() call
	"""
	connection = r[0].createConnection()
	connection.connect()

	
	print(r[0], "connected.")


def get_cardtype(atr_hex):
	if atr_hex == ATR_STUDENT_CARD_HEX:
		print("STUDENT CARD INSERTED!")
		return StudentCard()
		
	elif atr_hex == ATR_RASPI_TAG_HEX:
		print("RASPBERY BOARD TAG DETECTED!")
		return RaspiTag()
		
	else:
		return None


def request_any_card(cardtype):
	cardrequest = CardRequest(timeout=10, cardType=cardtype)
	cardservice = cardrequest.waitforcard()
	
	cardservice.connection.connect()

	atr = ATR(cardservice.connection.getATR())
	atr_hex = toHexString(cardservice.connection.getATR())
	
	#print_atr_info(atr)
	return atr_hex, atr


cardtype = AnyCardType()

cardmonitor = CardMonitor()
cardobserver = PrintObserver()
cardmonitor.addObserver(cardobserver)

#connect_card_reader()

while(1):
	atr_hex, atr = request_any_card(cardtype)
	
	# creates a new object of a detected card type
	detected_card = get_cardtype(atr_hex)
	if detected_card is None:
		print("Please insert valid card.")
	print("Detected card:", detected_card)

"""

while(1):
	cardrequest = CardRequest( timeout=10, cardType=cardtype )
	cardservice = cardrequest.waitforcard()
	cardservice.connection.connect()
	
	atr = ATR(cardservice.connection.getATR())
	print_atr_info(atr)
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
"""
