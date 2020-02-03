from smartcard.System import readers
from smartcard.util import toHexString, toBytes
from smartcard.ATR import ATR
from smartcard.CardType import ATRCardType, AnyCardType
from smartcard.CardMonitoring import CardMonitor, CardObserver


from smartcard.CardRequest import CardRequest
from atr_cardtype import *

READER = "ACS ACR122U PICC Interface 00 00"
	
		
def get_cardtype(atr):
	if atr == ATR_STUDENT_CARD_HEX:
		print("This is a student card")
		return StudentCard()
		
	elif atr == ATR_RASPI_TAG_HEX:
		print("This is a Raspi board")
		return RaspiTag()
		
	else:
		return None



def read_student_card(card):
	pass
	

def read_raspitag(card):
	pass
		

class DetectionObserver(CardObserver):
	"""A card observer that is notified
	when cards are inserted/removed from the system and
	detects the type of the card based on ATR
	"""
    
	def update(self, observable, actions):
		(addedcards, removedcards) = actions
		for card in addedcards:
			atr = toHexString(card.atr)
			print("+Inserted: ", atr)
			added_card = get_cardtype(atr)
			#print(type(detected_card))
			if isinstance(added_card, StudentCard):
				read_student_card(added_card)
				
			elif isinstance(added_card, RaspiTag):
				read_raspitag(added_card)
			
			elif inserted_card is None:
				print("Insert valid student card or scan a Raspberry Board RFID Tag")
				
		for card in removedcards:
			atr = toHexString(card.atr)
			print("-Removed: ", atr)
			removed_card = get_cardtype(atr)
			#print(type(detected_card))
			if isinstance(removed_card, StudentCard):
				read_student_card(removed_card)
				
			elif isinstance(removed_card, RaspiTag):
				read_raspitag(removed_card)
			
			elif removed_card is None:
				print("Goog bye stranger")


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
	


def request_any_card(cardtype):
	cardrequest = CardRequest(timeout=10, cardType=cardtype)
	cardservice = cardrequest.waitforcard()
	
	cardservice.connection.connect()

	atr = ATR(cardservice.connection.getATR())
	atr_hex = toHexString(cardservice.connection.getATR())
	
	#print_atr_info(atr)
	return atr_hex, atr



"""
MAIN PART OF THE SCRIPT 
"""

cardtype = AnyCardType()

cardmonitor = CardMonitor()
print_readers_info(readers())

cardobserver = DetectionObserver()

cardmonitor.addObserver(cardobserver)


while(1):
	"""
	"""

