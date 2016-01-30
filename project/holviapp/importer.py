# -*- coding: utf-8 -*-
import datetime
import hashlib
from decimal import Decimal

import dateutil.parser
import holviapi
import pytz
from creditor.handlers import AbstractTransaction

from asylum.utils import get_handler_instance


class HolviImporter(object):

    def __init__(self, stream):
        """The stream is iterator which contains Invoices or Orders"""
        self.stream = stream

    def import_transactions(self, transactions_handler=None):
        if transactions_handler is None:
            transactions_handler = get_handler_instance('TRANSACTION_CALLBACKS_HANDLER')
        transactions = []
        for obj in self.stream:
            atlist = None
            #print("DEBUG: processing %s with code %s" % (obj.__class__.__name__, obj.code))
            if type(obj) is holviapi.Invoice:
                atlist = self.invoice2atlist(obj)
            if type(obj) is holviapi.Order:
                atlist = self.order2atlist(obj)

            if atlist is None:
                continue

            if transactions_handler:
                for at in atlist:
                    ret = transactions_handler.import_transaction(at)
                    if ret is not None:
                        transactions.append(ret)
            else:
                transactions += atlist
        return transactions

    def invoice2atlist(self, i):
        if not i.payments:
            return None
        atlist = []
        for pline in i.payments:
            at = AbstractTransaction()
            at.holvi_invoice = i  # nonstandard field, but ought to be helpful
            at.name = str(i.receiver.name)
            at.email = str(i.receiver.email)
            at.amount = Decimal(pline['amount'])
            at.reference = str(i.rf_reference)
            at.stamp = dateutil.parser.parse(pline['time'])
            # DO NOT EVER CHANGE THIS, it must always and forever yield same unique_id for same transaction.
            at.unique_id = hashlib.sha1(str(i.code).encode('utf-8') + at.stamp.isoformat().encode('utf-8')).hexdigest()
            atlist.append(at)
        return atlist

    def order2atlist(self, o):
        if not o.paid:
            return None
        at = AbstractTransaction()
        at.holvi_order = o  # nonstandard field, but ought to be helpful
        at.name = "%s, %s" % (o.buyer.lastname, o.buyer.firstname)
        at.email = str(o.buyer.email)
        at.stamp = o.paid_time  # this is already parsed by holviapi
        at.amount = o.net
        at.reference = "holvi:%s" % o.code
        # DO NOT EVER CHANGE THIS, it must always and forever yield same unique_id for same transaction.
        at.unique_id = hashlib.sha1(str(o.code).encode('utf-8') + at.stamp.isoformat().encode('utf-8')).hexdigest()
        return [at]  # We must return a list since invoice might have multiple payments
