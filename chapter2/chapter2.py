# -*- coding: UTF-8 -*-
# 字典解析进行筛选
from collections import OrderedDict
from random import randint

data = {x: randint(20, 100) for x in xrange(1, 20)}
print {k: v for k, v in data.iteritems() if v > 60}

# 如何让字典保持有序性
ordered_dict = OrderedDict()
ordered_dict[0] = "root"
ordered_dict[1] = "hammer"
ordered_dict[2] = "AA"
ordered_dict[3] = "SS"
print(ordered_dict)


