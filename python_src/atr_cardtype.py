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
from smartcard.ATR import ATR

STUDENT_CARD = ATR([0x3B, 0x81, 0x80, 0x01, 0x80, 0x80])
RASPI_TAG_SQUARE = ART([0x3B, 0x8F, 0x80, 0x01, 0x80, 0x4F, 0x0C, 0xA0, 0x00, 0x00, 0x03, 0x06, 0x03, 0x00, 0x03, 0x00, 0x00, 0x00, 0x00, 0x68])
RASPI_TAG_ROUND = ART([0x3B, 0x8F, 0x80, 0x01, 0x80, 0x4F, 0x0C, 0xA0, 0x00, 0x00, 0x03, 0x06, 0x03, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x6A])

