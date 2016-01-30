# -*- coding: utf-8 -*-
import datetime
import hashlib

import pytz
from creditor.handlers import AbstractTransaction

from asylum.utils import get_handler_instance

from .parser import parseLine

# It's highly unlikely you would use Nordea transaction files in any other timesozone
HELSINKI = pytz.timezone('Europe/Helsinki')


class NDAImporter(object):

    def __init__(self, stream):
        self.stream = stream

    def import_transactions(self, transactions_handler=None):
        if transactions_handler is None:
            transactions_handler = get_handler_instance('TRANSACTION_CALLBACKS_HANDLER')
        transactions = []
        for line in self.stream:
            nt = parseLine(line)
            if nt is not None:
                if transactions_handler:
                    at = AbstractTransaction()
                    at.name = str(nt.name)
                    at.reference = str(nt.referenceNumber)
                    at.amount = nt.amount  # We know this is Decimal instance
                    at.stamp = HELSINKI.fromutc(datetime.datetime.combine(nt.timestamp, datetime.datetime.min.time()))
                    # DO NOT EVER CHANGE THIS, it must always and forever yield same unique_id for same transaction.
                    at.unique_id = hashlib.sha1(str(nt.archiveID).encode('utf-8') + nt.timestamp.isoformat().encode('utf-8') + str(nt.referenceNumber).encode('utf-8')).hexdigest()
                    ret = transactions_handler.import_transaction(at)
                    if ret is not None:
                        transactions.append(ret)
                else:
                    transactions.append(nt)
            else:
                # Raise error ? AFAIK there should be no unparseable lines
                pass
        return transactions
