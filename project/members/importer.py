# -*- coding: utf-8 -*-
import csv
import logging

from .models import Member

logger = logging.getLogger('members.importer')


class importer(object):

    def __init__(self, fp):
        self.reader = csv.reader(fp, delimiter=';', quotechar='"')
        headers = next(self.reader)
        self.header_map = {}
        for x in range(len(headers)):
            prop = headers[x]
            m = Member()
            if not hasattr(m, prop):
                msg = "%s not matched to member fields" % prop
                logger.warning(msg)
                print(msg)
                continue
            self.header_map[prop] = x

    def import_members(self):
        for row in self.reader:
            # Incomplete row
            if len(row) < max(self.header_map.values()):
                continue
            m = Member()
            for prop in self.header_map:
                v = row[self.header_map[prop]]
                if prop == 'member_id':
                    if v:
                        m.member_id = int(v)
                elif prop == 'anonymized_id':
                    if v:
                        m.anonymized_id = v
                else:
                    setattr(m, prop, v)
            try:
                m.save()
                msg = "Member %s (#%d) added" % (m, m.pk)
                logger.info(msg)
                print(msg)
            except Exception as err:
                msg = "Got error %s when adding member" % err
                logger.error(msg)
                print(msg)
