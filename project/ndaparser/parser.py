#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import date
from decimal import Decimal


class NdaTransaction(object):
    "Contains data of single NDA transaction. Additional information is discarded."
    # Data field positions, lengths. some are omitted for brevity.
    # Refer to https://www.fkl.fi/materiaalipankki/ohjeet/Dokumentit/Konekielinen_tiliote_palvelukuvaus.pdf for details.
    STRUCT_IDENTIFIER_START = 0
    STRUCT_IDENTIFIER_LENGTH = 3
    EVENT_COUNTER_START = 6
    EVENT_COUNTER_LENGTH = 6
    ARCHIVE_IDENTIFIER_START = 12
    ARCHIVE_IDENTIFIER_LENGTH = 18
    # notary date is the date money becomes / stops being available
    NOTARY_DATE_START = 30
    NOTARY_DATE_LENGTH = 6

    # Payment date is date of transaction initiation.
    PAYMENT_DATE_START = 42
    PAYMENT_DATE_LENGTH = 6
    EVENT_TYPE_START = 52
    EVENT_TYPE_LENGTH = 35
    AMOUNT_START = 87
    AMOUNT_LENGTH = 19
    NAME_START = 108
    NAME_LENGTH = 35
    REFERENCE_START = 159
    REFERENCE_LENGTH = 20
    # Transactions can be split onto many levels.
    # Level 0 or ' ' (empty) means actual transaction, 1-9
    # is different levels of split. Level 0 always contains
    # the total sum.
    LEVEL_START = 187
    LEVEL_LENGTH = 1

    referenceNumber = None  # reference of transaction
    amount = None  # amount of money in transaction
    timestamp = None  # date transaction is registered
    eventType = None  # type of transaction
    name = None  # name of creditor / debitor
    arhiveID = None  # Archive ID of transaction.

    def __init__(self, amount, timestamp, archiveID):
        self.amount = amount
        self.timestamp = timestamp
        self.archiveID = archiveID

    def __repr__(self):
        return "<ndaTransaction refNum:%s amt:%s time:%s type:%s name:%s ID:%s>" % (self.referenceNumber, self.amount, self.timestamp, self.eventType, self.name, self.archiveID)


def parseLine(line):
    "Parses one line of NDA file. Returns one transaction structure. Input must be an entire line of NDA file, invalid lines are discarded and null is returned"
    # Bypass lines not beginning "T10", "T10" is start of transaction
    if "T10" != line[NdaTransaction.STRUCT_IDENTIFIER_START:
                     NdaTransaction.STRUCT_IDENTIFIER_START +
                     NdaTransaction.STRUCT_IDENTIFIER_LENGTH]:
        return None

    # Bypass lines with level not empty or greater than 0
    level = line[NdaTransaction.LEVEL_START:
                 NdaTransaction.LEVEL_START +
                 NdaTransaction.LEVEL_LENGTH]
    if level.isdigit():
        level = int(level)
        if level > 0:
            return None

    # extract date
    year = int(line[NdaTransaction.NOTARY_DATE_START:
                    NdaTransaction.NOTARY_DATE_START + 2]) + 2000
    month = int(line[NdaTransaction.NOTARY_DATE_START + 2:
                     NdaTransaction.NOTARY_DATE_START + 4])
    day = int(line[NdaTransaction.NOTARY_DATE_START + 4:
                   NdaTransaction.NOTARY_DATE_START + 6])
    timestamp = date(year, month, day)

    # amount
    amount = int(line[NdaTransaction.AMOUNT_START:
                      NdaTransaction.AMOUNT_START +
                      NdaTransaction.AMOUNT_LENGTH])
    amount = Decimal(amount) / 100

    # Archive ID
    archiveID = line[NdaTransaction.ARCHIVE_IDENTIFIER_START:
                     NdaTransaction.ARCHIVE_IDENTIFIER_START +
                     NdaTransaction.ARCHIVE_IDENTIFIER_LENGTH]

    transaction = NdaTransaction(amount, timestamp, archiveID)

    # Event type
    eventType = line[NdaTransaction.EVENT_TYPE_START:
                     NdaTransaction.EVENT_TYPE_START +
                     NdaTransaction.EVENT_TYPE_LENGTH]
    transaction.eventType = eventType.rstrip()

    # name
    name = line[NdaTransaction.NAME_START:
                NdaTransaction.NAME_START +
                NdaTransaction.NAME_LENGTH]
    name = name.rstrip()
    transaction.name = ascii2scandic(name)

    # reference
    reference = line[NdaTransaction.REFERENCE_START:
                     NdaTransaction.REFERENCE_START +
                     NdaTransaction.REFERENCE_LENGTH]
    reference = reference.strip()
    transaction.referenceNumber = reference.lstrip("0")

    return transaction


def ascii2scandic(string):
    "Replaces []\\{}| with ÄÅÖäåö, respectively"
    string = string.replace('[', 'Ä')
    string = string.replace(']', 'Å')
    string = string.replace('\\', 'Ö')
    string = string.replace('{', 'ä')
    string = string.replace('}', 'å')
    string = string.replace('|', 'ö')
    return string


if __name__ == "__main__":
    transactions = []
    with open("./testdata.nda") as f:
        for line in f:
            transaction = parseLine(line)
            if transaction is not None:
                transactions.append(transaction)
    for transaction in transactions:
        print(transaction)
