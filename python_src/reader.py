from smartcard.System import readers
from smartcard.util import toHexString, toBytes
from smartcard.ATR import ATR
from smartcard.CardType import ATRCardType, AnyCardType

from smartcard.CardRequest import CardRequest
from atr_cardtype import *

READER = "ACS ACR122U PICC Interface 00 00"

def print_atr_info(atr):
	print('historical bytes: ', toHexString(atr.getHistoricalBytes()))
	print('checksum: ', "0x%X" % atr.getChecksum())
	print('checksum OK: ', atr.checksumOK)
	print('T0  supported: ', atr.isT0Supported())
	print('T1  supported: ', atr.isT1Supported())
	print('T15 supported: ', atr.isT15Supported())
	

def print_readers_info(r):
	if r != None:
		print("Connected readers:", r)
	else:
		print("No connected readers found.")


def check_reader(readers):
	if READER in readers:
		print("Reader found: ", READER)
		return readers.index(READER)
	else:
		print("Reader not found. Please connect ", READER")

def connect_card_reader():
	"""
	The list of available readers is retrieved with the readers() function. 
	We create a connection with the first reader (index 0 for reader 1, 1 for reader 2, ...) 
	with the r[0].createConnection() call and connect to the card with the connect() method of the connection. 
	We can then send APDU commands to the card with the transmit() method.
	"""
	r = readers()
	print_readers_info(r)
	
	# check if the proper reader exists in list of avaliable readers
	


connect_card_reader()

cardtype = AnyCardType()

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
