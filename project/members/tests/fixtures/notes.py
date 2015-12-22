# -*- coding: utf-8 -*-
import datetime, pytz
import factory.django, factory.fuzzy
import loremipsum
import random
import re
from members.models import Member, MemberNote


class FuzzyLoremipsum(factory.fuzzy.BaseFuzzyAttribute):
    fixer = re.compile("[bB]'(.*?)'")
    fixto = "\g<1>"

    def fuzz(self):
        ret = ""
        for outer in range(random.randint(1, 5)):
            ret += "\n\n"
            for inner in range(random.randint(3, 10)):
                ret += self.fixer.sub(self.fixto, loremipsum.get_sentence()).capitalize() + " "
        return ret.strip()


class MemberNoteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MemberNote
        django_get_or_create = ('stamp', 'member')
    stamp = factory.fuzzy.FuzzyDateTime(datetime.datetime.now(pytz.utc)-datetime.timedelta(days=180))
    member = factory.fuzzy.FuzzyChoice(Member.objects.all())
    notes = FuzzyLoremipsum()
