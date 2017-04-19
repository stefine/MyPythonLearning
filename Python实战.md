# python 问题实战 #
**说明**
python实际是一个非常好用的脚本语言，实际生活中的很多问题没必要用 Java等语言来书写冗长繁重的代码，针对现实生活中的一些小问题，python 足以。以下章节总结了一些抽象问题的python 解决方案。注意：如果标题后有章节号标记的，代表在demo里提供了代码实现，因为这些问题特别实用或是具有特别容易忘记的一些python特性。

##  第二章 

- 在列表、字典和集合中如何筛选数据？

**列表解析进行筛选**

	from random import randint	
	# 随机生成列表数字
	data = [randint(-10, 10) for _ in xrange(10)]
	data

	# 使用列表解析更好
	[x for x in data if x >= 0]


** 字典解析进行筛选（chapter2）**

	# 随机生成字典
	d = {x:randint(60, 100) for x in xrange(1, 21)}
	{k:v for k, v in d.iteritems() if v > 90}

**set 解析进行筛选**

	data
	s = set(data)
	s
	# set解析
	{x for x in s if x % 3 == 0}


- 如何为元组中的每个元素命名，提高程序可读性？

**定义枚举类型**

	NAME, AGE, SEX, EMAIL = xrange(4)

- 如何统计序列中元素的出现频度？


	from random import randint
	data = [randint(0, 20) for _ in xrange(30)]
	# 初始化字典
	# 这边为何定义c？
	c = dict.fromkeys(data, 0)
	# 使用collection 下的counter 会更简洁
	from collections import Counter
	
	c2 = Counter(data)
	# 直接能求出访问频度最高的
	c2.most_common(3)
	
	import re
	
	txt = open('xx.txt').read()
	c3 = Counter(re.split('\W+',txt))

当然，也可以直接将 Counter 转化为 dict 的形式，可以说这个技巧太方便了！
	
	dict(c2)

- 根据字典中值的大小对字典进行排序


	# 随机生成字典（这边写法熟悉下）
	d = {x:randint(60,100) for x in 'xyzabc'}
	
	# 方法一：
	sorted(zip(d.itervalues(), d.iterkeys()))
	
	# 方法二：
	sorted(d.items(), key=lambda x: x[1])

- 如何快速找到多个字典的公共键


	from random import randint,sample
	# 随机取样3-6个
	sample('abcdefg', randint(3,6))
	s1 = {x:randint(1,4) for x in sample('abcdefg', randint(3, 6))}
	s2 = {x:randint(1,4) for x in sample('abcdefg', randint(3, 6))}
	s3 = {x:randint(1,4) for x in sample('abcdefg', randint(3, 6))}

	# dict.viewkeys 得到set集合，最后以集合的方式解决这个问题
	# map 运行结果是list集合，其实就是对list里的每个元素做相应的操作
	map(dict.viewkeys, [s1, s2, s3])
	reduce(lambda a,b: a&b, map(dict.viewkeys, [s1, s2, s3]))


- 如何让字典保持有序性
可以利用 collections 的 OrderedDict 类解决这个问题。


	from time import time
	from random import randint
	from collections import OrderedDict
	
	d = OrderedDict()
	player = list('ABCDEFG')
	start = time()
	
	for i in xrange(8):
	    raw_input()
	    p = player.pop(randint(0, 7-i))
	    end = time()
	    print i+1, p, end - start
	    d[p] = (i+1, end-start)
	
	print
	print '-' * 20
	
	for k in d:
	    print k, d[k]
	

- 如何实现用户的历史记录功能（最多n条）


	from collections import deque
	
	q = deque([], 5)
	q.append(1)
	q.append(2)
	q.append(3)
	q.append(4)
	q.append(5)
	print list(q)
	q.append(6)
	print list(q)
	
	import pickle
	
	pickle.dump(q, open('history', 'w'))
	q2 = pickle.load(open('history'))

## 第三章 可迭代对象 ##
可迭代对象和迭代器对象，可迭代对象*产生*迭代器对象。生成器和生成对象从通俗的角度来解释下：就是可迭代对象一般是一次性放置在内存中，但是有时候我们希望它生成一个就给后续环节处理一个。 所以，其实我们要改造的是 for x in ITERABLE 里的 ITERABLE 变量。一般来说，有两种处理方法（**chapter3**）：
1. 将 ITERABLE 变量继承 iterable 对象。
2. 轻量级处理方法：运用 yield 或是 生成器给迭代对象做一个轻包装。
从好理解的角度来看，生成器和迭代对象长相上只有 [] 和（）的区别，所以你完全可以就当做迭代对象使用； yield 可以这么理解：就是生成一个待对象返回一个。

- 如何实现可迭代对象和迭代器对象

**可迭代对象**(Iterable)：实现 __iter__ 方法，**可迭代对象和 yield 一般一起使用**，它的好处是十分明显的：一般对象只能运行完然后存放在内存里，**yield 产生的生成对象，是能够及时消费的，即生产一个消费一个**。这样很多可能需要延迟的对象就可以延迟使用，而不用苦苦等待着。 
**迭代器对象**(Iterator)：实现 next 方法 

先看一个获取城市气温的函数：

	# 获取一个城市的气温函数
	import requests
	def getWeather(city):
		r = requests.get(u'http://wthrcdn.etouch.cn/weather_mini?city='+city)
		data = r.json()['data']['forecast'][0]
		return '%s %s %s' %(city, data['low'], data['high'])
	# [u'北京', u'上海', u'广州', u'长春']
	print getWeather(u'北京')
	print getWeather(u'长春')


如果考虑实时性，一个城市就去一个响应：

	from collections import Iterable, Iterator
	import requests
	
	# 定义一个迭代器对象
	class WeatherIterator(Iterator):
	    def __init__(self, cities):
	        self.cities = cities
	        self.index = 0
	
	    def getWeather(self, city):
	        r = requests.get(u'http://wthrcdn.etouch.cn/weather_mini?city='+city)
	        data = r.json()['data']['forecast'][0]
	        return '%s %s %s' %(city, data['low'], data['high'])
	
	    def next(self):
	        if self.index == len(self.cities):
	            raise StopIteration
	        city = self.cities[self.index]
	        self.index += 1
	        return self.getWeather(city)
	
	# 定义一个可迭代对象
	class WeatherIterable(Iterable):
	    def __init__(self, cities):
	        self.cities = cities
	
	    def __iter__(self):
	        return WeatherIterator(self.cities)
	
	for x in WeatherIterable([u'北京', u'上海', u'广州', u'长春']):
	    print x

**Note：** 因为迭代器对象和生成器对象其实没有什么区别，***我们推荐使用 Iterable 接口实现***，将该类的 __iter__ 方法实现成生成器函数，每次yield返回一个素数。所以，可以有更简单的处理方式：

案例一：上述问题重写

	from collections import Iterable, Iterator
	import requests
	
	# 定义一个可迭代对象
	class WeatherIterable(Iterable):
	
	    def getWeather(self, city):
			r = requests.get(u'http://wthrcdn.etouch.cn/weather_mini?city='+city)
			data = r.json()['data']['forecast'][0]
			return '%s %s %s' %(city, data['low'], data['high'])
	
	    def __init__(self, cities):
	        self.cities = cities
	
	    def __iter__(self):
	        for city in self.cities:
	            yield self.getWeather(city)
	        # 以下也可以用生成器的方法
	        # return (self.getWeather(city) for city in self.cities)
	
	for x in WeatherIterable([u'北京', u'上海', u'广州', u'长春']):
	    print x

案例二：素数问题

	class PrimeNumbers(Iterable):
		def __init__(self, start, end):
			self.start = start
			self.end = end
		def isPrimeNum(self, k):
			if k<2:
				return False
			for i in xrange(2, k):
				if k % i == 0:
					return False
			return True
		
		def __iter__(self):
			for k in xrange(self.start, self.end + 1):
				if self.isPrimeNum(k):
					yield k
	
	for x in PrimeNumbers(1, 100):
		print x


- 如何进行和实现反向迭代

正向迭代实现__iter__ 方法和反向迭代实现__reversed__ 方法

	from collections import Iterable, Iterator
	import requests
	
	class FloatRange:
	    def __init__(self, start, end, step=0.1):
	        self.start = start
	        self.end = end
	        self.step = step
	
	    def __iter__(self):
	        t = self.start
	        while t <= self.end:
	            yield t
	            t += self.step
	
	    def __reversed__(self):
	        t = self.end
	        while t >= self.start:
	            yield t
	            t -= self.step
	
	for x in reversed(FloatRange(1.0, 4.0, 0.5)):
	    print x
	
	for x in iter(FloatRange(1.0, 4.0, 0.5)):
	    print x
	

- 如何对迭代器做切片操作
itertools 里的 islice 可以解决这个问题。


	#readlines()方法会一次性把数据读入内存中。
	f = open('')
	from itertools import islice
	
	# 返回生成器对象，返回100行到500行, step = 1
	islice(f, 100, 500, 1)
	# 100行到文件末尾
	islice(f, 100, None, 1)
	
	for x in islice(f, 100, 500, 1):
		print x
	
	l = range(20)
	t = iter(l)
	
	# 可以省略 step = 1
	for x in islice(t, 5, 10):
		print x
		
	# 只要是iter对象和list对象都可以
	for x in islice(l, 5, 10):
		print x	

# 第四章 字符串 #

- 如何拆分含有多种分隔符的字符串？


	import re
	# 可以是方括号中出现的任意字符进行切割
	# '+' 代表连续出现多次
	s = "++suu;su,55\t9su|"
	re.split(r'[,;\t|]+', s)
	print [x for x in re.split(r'[,;\t|+]+', s) if x != '']

- 如何去掉字符串不需要的字符？

**python 中的 strip, sub 方法不仅是去空格符那种，而且还能去掉任意字符你不想要的（你仔细想想原理就应该推理出来）**
	
	# 方法一：
	# strip(), lstrip(),rstrip() 方法去掉所要求的字符，注意这种方法能去掉首尾，但中间的分隔符保留
	r = "   abc  def "
	r.strip()
	r = "--abc+def++++"
	r.strip('-+')
	
	# 方法二：replace() 方法或正则表达式
	# replace() 方法只能替换一种
	r = "--abc+def++++"
	r.replace('-', '')
	
	# 方法三：re.sub方法 (重点推荐，任意次数都可以解决)
	r = "--abc+def++++"
	print re.sub('[-+]','', r)
	
	# 方法四：str.translate 和 unicode.translate
	# 原始用法：一一对应的翻译模式
	s = 'abc123023a00xyz'

	import string
	s.translate(string.maketrans('abcxyz','xyzabc'))
	
	# 衍生用法(第一个参数为None，就是删除字符集)
	s = 'abc\refg\n234\t'
	s.translate(None, '\t\r\n')
	
	# unicode的略有不同
	u = u'ni\u0301 ha\u0300o ci\u0304 fa\u0300n'
	
	print u.translate(dict.fromkeys([0x0301, 0x0300, 0x0304, 0x0300]))


- 如何判断字符串a是否以字符串b开头或结尾？


	import os, stat
	# 当前目录下的文件名
	os.listdir('.')
	[for name in os.listdir('.') if name.endswith(('.sh', '.py'))]
	# chmod的第一个参数为文件名，第二个参数为权限值
	os.chmod('e.py', os.stat('e.py').st_mode | stat.S_IXUSR)
	

- 如何调整字符串中文格式？（正则组的应用！！！）


	import re
	log = "2013-10-11 hello world"
	
	# \d 表示数字, \d{4}表示4个数字,()表示正则组, r'\3\/2/\1' 表示组3，组2，组1
	print re.sub('(\d{4})-(\d{2})-(\d{2}) (\w+) (\w+)', r'\3/\2/\1 \4-\5', log)

输出为： 11/10/2013 hello-world
	
	print re.sub('(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})', r'\g<month>/\g<day>/\g<year>', log)

**Note：**正则组能够把相应的位置替换后，然后其余的字符串都保留！


- 如何将小字符串拼接成大字符串
如果使用"+",会产生大量的临时对象，所以推荐使用join方法。


	l = ['ac', 123, 45, 'xyz']
	''.join(str(x) for x in l)
	
**Note:** 这个之所以可以其实是因为join 可以接受生成器参数，str(x) for x in l 相当于 (str(x) for x in l), 这样比列表解析的开销小很多。
	
- 如何对字符串进行左右居中对齐工整的输出dict


	d = {'Dictionsat':500, 'falsc': 477,'trilinear': 40}
	map(len, d.keys())
	w = max(map(len, d.keys()))
	
	for k in d:
		print k.ljust(w), ':', d[k]

## 第五章 文件处理（未校对）##

- 如何访问文件的状态


	import os
	os.path.
	1、文件的类型（普通文件，目录，符号链接）
	os.path.isdir('x.txt')
	os.path.islink('x.txt')
	os.path.isfile('a.txt')
	
	2、文件的访问权限
	s = os.stat('a.txt')
	s.st_mode
	os.stat?
	import stat
	stat.S_ISDIR(s.st_mode)
	stat.S_ISREG(s.st_mode)
	
	# 大于0 即真值
	s.st_mode & stat.S_IRUSR
	
	s.st_mode & stat.S_IX
	s.st_mode & stat.S_IXUSR
	
	3、文件的最后访问时间
	import time
	time.localtime(os.path.getatime('a.txt'))
	
	4、文件的大小
	os.path.getsize('a.txt')

## 第六章 文件读写（未校对）##


- 如何读写excel文件


	import xlrd, xlwt
	
	rbook = xlrd.open_workbook('demo.xlsx')
	# 得到sheet表
	rsheet = rbook.sheet_by_index(0)
	nc = rsheet.ncols
	# 在[0, nc]位置增加单元格
	rsheet.put_cell(0, nc, xlrd.XL_CELL_TEXT, u'总分', None)
	
	for row in xrange(1, rsheet.nrows):
		t = sum(rsheet)
		rsheet.put_cell(row, nc, xlrd.XL_CELL_NUMBER, t, None)
	
	# 重新写入一个表格
	wbook = xlwt.Workbook()
	wsheet = wbook.add_sheet(rsheet.name)
	style = xlwt.easyxf('align:vertical center, horizontal center')
	
	for r in xrange(rsheet.nrows):
		for c in xrange(rsheet.ncols):
			wsheet.write(r, c, rsheet.cell_value(r,c), style)
			
	wbook.save('output.xlsx')	


## 第七章 类对象 ##

- 如何派生内置不可变类型并修改其实例化行为？


	# IntTuple继承tuple，所以 IntTuple 按理是无法修改的，那么该如何处理这个问题呢？
	# __new__ 方法可以解决这个问题
	class IntTuple(tuple):
	    def __new__(self, iterable):
	        g = (x for x in iterable if isinstance(x, int) and x>0)
	        return super(IntTuple, self).__new__(self, g)
	
	    def __init__(self,iterable):
	        print self
	        super(IntTuple, self).__init__(iterable)
	
	# 完全和tuple对象一致
	t = IntTuple([-1,1,'abc',['x','y'],3])
	print t


- 如何节省内存空间？


	class Player(object):
		def __init__(self, uid, name):
			self.uid = uid
			self.name = name
	
	class Player2(object):
		__slots__=['uid', 'name']
		def __init__(self, uid, name):
			self.uid = uid
			self.name = name		
	
	import sys
	p1 = Player('0001','Jim')
	p2 = Player2('0001', 'Jim')
	# 里面其实存放的就是uid，name 这些的绑定值
	p1.__dict__
	# 如果你动态绑定值这个__dict__字典，也会绑定这个值
	p1.x = 32
	# 当然也可以换种方式动态绑定
	p1.__dict__['y'] = 78
	print p1.y
	sys.getsizeof(p1.__dict__)
	
	p2.x = 1  # 是通不过的！


- 如何创建可管理的对象属性
假如一个不可管理的类如下：


	from math import pi
	
	class Cirlce(object):
		def __init__(self, radius):
			self.radius = radius
		def getRadius(self):
			return self.radius
		def setRadius(self, value):
			if not isinstance(value,(int, float, long)):
				raise ValueError("wrong type !")
			self.radius = float(value)
		def getArea(self):
			return self.radius ** 2 * pi
		
	c = Cirlce(3.2)
	# 竟然也能通过！！！！！！！
	c.radius = 'abc'

如果，要维护一个可管理的类，定义如下：

	class Cirlce(object):
		def __init__(self, radius):
			self.radius = radius
		def getRadius(self):
			return self.radius
		def setRadius(self, value):
			if not isinstance(value,(int, float, long)):
				raise ValueError("wrong type !")
			self.radius = float(value)
		def getArea(self):
			return self.radius ** 2 * pi
			
		R = property(getRadius, setRadius)
		
	c = Cirlce(3.2)
	print c.R
	c.R = 5.9


- 支持类可以比较大小
一般而言，functools 里的 total-ordering 可以帮助简化代码的书写，方便我们写出更精简的比较代码，只用定义 __lt__ 和 __eq__ 方法。


	from functools import total_ordering
	
	@total_ordering
	class Rectangle(object):
		def __init__(self, w, h):
			self.w = w
			self.h = h
		def area(self):
			return self.w*self.h
		def __lt__(self, obj):
			return self.area() < obj.area()
		def __eq__(self, obj):
			return self.area() == obj.area()
	
	class Cirlce(object):
		def __init__(self,r):
			self.r = r
		def area(self):
			return self.r ** 2 * pi
		
	r1 = Rectangle(5,3)
	r2 = Rectangle(4,4)
	c1 = Cirlce(3)
	print r1 < r2
	print r1 <= c1
	# 不行
	print c1 <= r1

同样，可以使用抽象接口的方法，能比较的都实现这个area接口：

	from functools import total_ordering
	from abc import ABCMeta, abstractmethod
	
	class Shape(object):
	    @abstractmethod
	    def area(self):
	        pass
	    def __lt__(self, obj):
	        if not isinstance(obj, Shape):
	            raise TypeError("obj is not shape")
	        return self.area() < obj.area()
	
	    def __eq__(self, obj):
	        return self.area() == obj.area()
	
	@total_ordering
	class Rectangle(Shape):
	    def __init__(self, w, h):
	        self.w = w
	        self.h = h
	    def area(self):
	        return self.w*self.h
	
	@total_ordering
	class Cirlce(Shape):
	    def __init__(self,r):
	        self.r = r
	    def area(self):
	        return self.r ** 2 * pi
	
	r1 = Rectangle(5,3)
	r2 = Rectangle(4,4)
	c1 = Cirlce(3)
	print r1 < r2
	print r1 <= c1
	# 不行
	print c1 >= r2


- 如何使用描述符对实力属性做类型判断
可以使用描述符来解决这个问题，所谓描述符__get__()，__set__()，__delete__()方法。实际上会发生这样的事情：在另一个类中定义一个类属性，它是一个描述符的实例，那么在对它进行赋值、删除等操作时会被这些方法截获，所以这就给予我们进行类型判断的机会。


	class Attr(object):
	    def __init__(self, name, *args):
	        self.name = name
	        self.type_ = args
	
	    def __get__(self, instance, cls):
	        return instance.__dict__[self.name]
	
	    def __set__(self, instance, value):
	        if not isinstance(value, self.type_):
	            raise TypeError("expected an %s" % self.type_)
	        instance.__dict__[self.name] = value
	
	    def __delete__(self, instance):
	        del instance.__dict__[self.name]
	
	class Person(object):
	    name = Attr('name', str)
	    age = Attr('age', int)
	    height = Attr('height', float, int)
	
	p1 = Person()
	p1.name = "Bob"
	# p1.name = 13
	print p1.name
	p1.height = 14.0
	print p1.height


- 如何通过实例方法名字的字符串调用方法（未校对）

在对象上分别尝试获取这些属性，获取到就调用，获取不到就换下一个。

	def getArea(shape):
		for name in ('area', 'getArea', 'get_area'):
			# shape 对象去获取方法名字
			f = getattr(shape, name, None)
			if f:
				return f()
	
	shape1 = Cirlce(2)
	shape2 = Triangle(3,4,5)
	shape3 = Rectangle(2,4)
	
	shapes = [shape1, shape2, shape3]
	print map(getArea, shapes)

## 第九章 装饰器的用法 ##

- 装饰器的基本使用
装饰器的构成：
1、定义一个接受函数的 function
2、定义一个接受函数参数的 function


	# 这样书写更准确
	# 接受函数的 function
	def memo(func):
	    cache = {}
	    def wrap(*args):
	        for arg in args:
	            if arg not in cache:
	                cache[arg] = func(*args)
	            return cache[arg]
	    return wrap
	
	@memo
	def fib(n):
	    if n <= 1:
	        return 1
	    return fib(n-1) + fib(n-2)
	
	#fibresult = memo(fib)
	print fib(5)


- 带参数的函数装饰器
1、 外部是接受函数参数
2、 内部是个装饰器


	import time
	import logging
	from random import randint
	
	def warn(timeout):
	    def decorator(func):
	        def wrapper(*args, **kargs):
	            t1 = time.time()
	            res = func(*args, **kargs)
	            t2 = time.time() - t1
	            print t2
	            if(t2 > timeout):
	                msg = "exceed time: %s, %s, %s" %(func.__name__, t2, timeout)
	                logging.warn(msg)
	        return wrapper
	    return decorator
	
	@warn(1)
	def test():
	    print "in test"
	    while randint(0, 1):
	        time.sleep(1.5)
	
	for _ in range(30):
	    test()


