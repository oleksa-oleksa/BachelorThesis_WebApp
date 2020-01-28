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

STUDENT_CARD = ATR([0x3B, 0x9E, 0x95, 0x80, 0x1F, 0xC3, 0x80, 0x31, 0xA0, 0x73,
           0xBE, 0x21, 0x13, 0x67, 0x29, 0x02, 0x01, 0x01, 0x81,
           0xCD, 0xB9])
