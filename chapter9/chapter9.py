# -*- coding: UTF-8 -*-
# fib 数列的典型应用（无参数装饰器）
def memo(func):
    cache = {}
    def f(*args, **kwargs):
        if args not in cache.keys():
            cache[args] = func(*args)
        return cache[args]
    return f

@memo
def fib(num):
    if num <= 1:
        return 1
    else:
        return fib(num-1) + fib(num-2)

print fib(5)

# 有参数构造，现在希望在执行期间能加个“开始执行”或是“hello”的问候句
def memo(message):
    print message
    def decrate(func):
        cache = {}
        def f(*args, **kwargs):
            if args not in cache.keys():
                cache[args] = func(*args)
            return cache[args]
        return f
    return decrate

@memo("开始执行！")
def fib(num):
    if num <= 1:
        return 1
    else:
        return fib(num-1) + fib(num-2)

print fib(5)