from smartcard.System import readers
from smartcard.util import toHexString, toBytes
from smartcard.ATR import ATR
from smartcard.CardType import ATRCardType, AnyCardType
from smartcard.CardMonitoring import CardMonitor, CardObserver
from smartcard.CardRequest import CardRequest
from smartcard.scard import *
import smartcard.util

from atr_cardtype import *
from scard_command_set import *

READER = "ACS ACR122U PICC Interface 00 00"


def read_uid(cardtype):
    """
    So to read the UID we need to send a GET DATA command APDU using the SCardTransmit function.
    The GET DATA command APDU has the following format:
    Command		Class	INS		P1			P2		Lc	DataIn	Le
    Get Data	0xFF	0xCA	0x00 0x01	0x00	–	–		xx

    The options for P1 & P2 are:
    P1		P2
    0x00	0x00	UID is returned
    0x01	0x00	all historical bytes from the ATS of a ISO 14443 A card without CRC are returned



    cardrequest = CardRequest(timeout=1, cardType=cardtype)
    #cardservice = cardrequest.waitforcard()
    cardservice.connection.connect()
    trace_command(apdu)
    response, sw1, sw2 = cardservice.connection.transmit(apdu)
    trace_response(response, sw1, sw2)
    """
    apdu = GET_UID
    trace_command(apdu)
    hresult, hcontext = SCardEstablishContext(SCARD_SCOPE_USER)

    if hresult == SCARD_S_SUCCESS:

        hresult, readers = SCardListReaders(hcontext, [])

        if len(readers) > 0:

            reader = readers[0]

            hresult, hcard, dwActiveProtocol = SCardConnect(
                hcontext,
                reader,
                SCARD_SHARE_SHARED,
                SCARD_PROTOCOL_T0 | SCARD_PROTOCOL_T1)

            if hresult == SCARD_S_SUCCESS:

                hresult, response = SCardTransmit(hcard, dwActiveProtocol, apdu)
                res = response[0:-2]
                sw1 = response[-2]
                sw2 = response[-1]

                trace_response(res, sw1, sw2)
                print(smartcard.util.toHexString(response))

                # Addind detected UID to the instance
                cardtype.uid = toHexString(res)
            else:
                print("NO_CARD")
        else:
            print("NO_READER")
    else:
        print("FAILED")


def trace_command(apdu):
    print("sending " + toHexString(apdu))


def trace_response(response, sw1, sw2):
    if None == response: response = []
    print("response: ", toHexString(response), " status words: ", "%x %x" % (sw1, sw2))


def get_cardtype(atr, action):
    if atr == ATR_STUDENT_CARD_HEX:
        print("Student card", action)
        return StudentCard()

    elif atr == ATR_RASPI_TAG_HEX:
        print("Raspi board", action)
        return RaspiTag()

    else:
        return None


def read_student_card(cardtype):
    read_uid(cardtype)
    print("uid", cardtype.uid)


def read_raspitag(cardtype):
    read_uid(cardtype)


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
            added_card = get_cardtype(atr, "added")
            if isinstance(added_card, StudentCard):
                read_student_card(added_card)

            elif isinstance(added_card, RaspiTag):
                read_raspitag(added_card)

            elif added_card is None:
                print("Insert valid student card or scan a Raspberry Board RFID Tag")

        for card in removedcards:
            atr = toHexString(card.atr)
            print("-Removed: ", atr)
            removed_card = get_cardtype(atr, "removed")
            if isinstance(removed_card, StudentCard):
                pass

            elif isinstance(removed_card, RaspiTag):
                pass

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

    # print_atr_info(atr)
    return atr_hex, atr


"""
MAIN PART OF THE SCRIPT 
"""

cardmonitor = CardMonitor()

print_readers_info(readers())

cardobserver = DetectionObserver()

cardmonitor.addObserver(cardobserver)

while (1):
    """
    """

