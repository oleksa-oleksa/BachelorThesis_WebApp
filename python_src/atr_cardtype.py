"""
Constant values for ATR ot student card and RFID tags on the Raspberry Pi

The purpose of the ATR is to describe the supported communication parameters. 
The smart card reader, smart card reader driver, and operating system will use these parameters to establish a communication with the card. 
The ATR is described in the ISO7816-3 standard. The first bytes of the ATR describe the voltage convention (direct or inverse), 
followed by bytes describing the available communication interfaces and their respective parameters. 
These interface bytes are then followed by Historical Bytes which are not standardized, and are useful for transmitting proprietary i
nformation such as the card type, the version of the embedded software, or the card state. 
Finally these historical bytes are eventually followed by a checksum byte.
"""
from smartcard.CardType import ATRCardType
from smartcard.util import toBytes

ATR_STUDENT_CARD = "3B 81 80 01 80 80"
ATR_RASPI_TAG = "3B 8F 80 01 80 4F 0C A0 00 00 03 06 03 00 01 00 00 00 00 6A"
ATR_RASPI_TAG_RECTANGLE = "3B 8F 80 01 80 4F 0C A0 00 00 03 06 03 00 03 00 00 00 00 68"

ATR_CARD_TYPES = ATRCardType(toBytes(ATR_STUDENT_CARD), toBytes(ATR_RASPI_TAG))

