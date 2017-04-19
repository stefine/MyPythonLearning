# -*- coding: UTF-8 -*-
from random import uniform

def oddNumber1(number):
    """
    yield an odd number.
    :param number:
    :return: boolean
    """
    for x in number:
        if x % 2 == 0:
            uniform1 = uniform(0, 1)
            if uniform1 > 0.5:
                y = str(x) + " is an odd number"
                yield y
            else:
                yield x


def oddNumber2(number):
    """
    judge if a odd number.
    :param number:
    :return: boolean
    """
    return (x for x in number if x % 2 == 0)

for x in oddNumber1(range(1, 100)):
    print x

for x in oddNumber2(range(1, 100)):
    print str(x) + " is an odd number!"
