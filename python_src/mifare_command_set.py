from smartcard.util import toHexString, toBytes

"""
A step in an application protocol consists of sending a command, processing it in the receiving entity and sending back the response. 
Therefore a spcecific response corresponds to a specific command, referred to as a command-response pair.
An application protocol data unit (APDU) contains either a command message or a response message, sent from the interface device to the card or conversely.
In a command-response pair, the command message and the response message may contain data, thus inducing four cases 
"""


INS_SELECT = 0xA4
INS_READ_BINARY = 0xB0
INS_UPDATE_BINARY = 0xD6 
INS_READ_RECORDS = 0xB2 
INS_APPEND_RECORD = 0xE2 
INS_GET_CHALLENGE = 0x84 
INS_INTERNAL_AUTHENTICATE = 0x88 
INS_EXTERNAL_AUTHENTICATE = 0x82 
