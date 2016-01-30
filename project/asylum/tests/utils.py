# -*- coding: utf-8 -*-
import random
import re

import factory.django
import factory.fuzzy
import loremipsum


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
