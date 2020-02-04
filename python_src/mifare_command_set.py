from smartcard.util import toHexString, toBytes

"""
A step in an application protocol consists of sending a command, processing it in the receiving entity and sending back the response. 
Therefore a spcecific response corresponds to a specific command, referred to as a command-response pair.
An application protocol data unit (APDU) contains either a command message or a response message, sent from the interface device to the card or conversely.
In a command-response pair, the command message and the response message may contain data, thus inducing four cases 
"""
SELECT = [0xA0, 0xA4, 0x00, 0x00, 0x02]
DF_TELECOM = [0x7F, 0x10]


INS_ERASE_BINARY = 0x0E
INS_VERIFY = 0x20
INS_MANAGE_CHANNEL = 0x70
INS_EXTERNAL_AUTHENTICATE = 0x82 
INS_GET_CHALLENGE = 0x84 
INS_INTERNAL_AUTHENTICATE = 0x88 
INS_SELECT_FILE = 0xA4
INS_READ_BINARY = 0xB0
INS_READ_RECORDS = 0xB2 
INS_GET_RESPONSE = 0xC0
INS_ENVELOPE = 0xC2
INS_GET_DATA = 0xCA
INS_WRITE_BINARY = 0xD0
INS_WRITE_RECORD = 0xD2
INS_UPDATE_BINARY = 0xD6
INS_PUT_DATA = 0xDA
INS_UPDATE_DATA = 0xDC
INS_APPEND_RECORD = 0xE2 
