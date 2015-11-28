from datetime import date
from decimal import Decimal

class NdaTransaction(object):
    "Contains data of single NDA transaction. Additional information is discarded."
    referenceNumber  = None #reference of transaction
    amount = None #amount of money in transaction
    timestamp = None #date transaction is registered
    eventType = None #type of transaction
    name = None #name of creditor / debitor
    

    def __init__(self, amount, timestamp):
        self.amount      = amount
        self.timestamp   = timestamp

    def __repr__(self):
        return "<ndaTransaction refNum:%s amt:%s time:%s type:%s name:%s>" % (self.referenceNumber, self.amount, self.timestamp, self.eventType, self.name)

def parseLine(line):
    "Parses one line of NDA file. Returns one transaction structure. Input must be an entire line of NDA file, invalid lines are discarded and null is returned"
    #Bypass lines not beginning "T10", "T10" is start of transaction
    if "T10" != line[0:3]:
        return None

    #extract date
    year      = 2000 + int(line[30:32])
    month     = int(line[32:34])
    day       = int(line[34:36])
    timestamp = date(year, month, day)

    #amount
    amount = int(line[87:106])
    amount = Decimal(amount)/100

    transaction = NdaTransaction(amount, timestamp)

    #Event type
    eventType = line[52:86]
    transaction.eventType = eventType.rstrip()

    #name
    name = line[108:142]
    transaction.name = name.rstrip();

    #reference
    reference = line[159:178]
    reference = reference.strip()
    transaction.referenceNumber = reference.lstrip("0")

    return transaction


