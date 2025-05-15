from functools import wraps, lru_cache
import logging
import time
import inspect
from collections.abc import Sequence


def log(obj=None, *, level=logging.INFO): # * means all following arguments are keyword only
    def decorator(target):
        if inspect.isclass(target):
            return _log_class(target, level)
        elif inspect.isfunction(target):
            return _log_func(target, level)
        else:
            raise TypeError("@log can only be used on classes or functions")

    if obj is None:
        return decorator
    else:
        return decorator(obj)

def _log_class(c, level):
    logger = logging.getLogger(c.__module__)
    og_init = c.__init__

    @wraps(og_init) # so __name__ and __doc__ work correctly
    def wrapper(self, *args, **kwargs):
        logger.log(level, f'Creating an instance of {c.__name__} with args = {args}, kwargs = {kwargs}')
        og_init(self, *args, **kwargs)

    c.__init__ = wrapper
    return c


def _log_func(f, level):
    logger = logging.getLogger(f.__module__)

    @wraps(f)
    def wrapper(*args, **kwargs):
        begin_time = time.time()
        logger.log(level, f'Function {f.__name__} started with args = {args}, kwargs = {kwargs}')
        result = f(*args, **kwargs)
        duration = time.time() - begin_time
        logger.log(level, f'Function {f.__name__} returned {result} after {duration}')
        return result

    return wrapper

def acronym(words: list):
    return '' if not words else words[0][0].upper() + acronym(words[1:])

def test_acronym():
    print(acronym(['Zaklad', 'Ubezpieczen', 'Socjalnych']))


def median(numbers: list):
    if not numbers:
        return None

    nums = sorted(numbers)
    return _median_sorted(nums)

def _median_sorted(nums: list):
    n = len(nums)
    return nums[0] if n == 1 else (
        (nums[0] + nums[1]) / 2 if n == 2 else _median_sorted(nums[1:-1])
    )


def test_median():
    print(median([1, 2, 3, 4, 5]))
    print(median([1, 2, 3, 4, 5, 6]))
    print(median([]))


def pierwiastek(x, epsilon, y=1):
    return y if abs(y * y - x) < epsilon else pierwiastek(x, epsilon, 0.5 * (y + x / y))

def test_pierwiastek():
    print(pierwiastek(3, 0.1))
    print(pierwiastek(4, 0.1))
    print(pierwiastek(19, 0.01))


def make_alpha_dict(text: str):
    words = text.split()
    keys = list(filter(lambda c: not c.isspace(), text))

    return {
        key: list(filter(lambda word: key in word, words))
        for key in keys
    }

def test_alpha_dict():
    print(make_alpha_dict('ona i on'))
    print(make_alpha_dict('adam lubi placki'))


def flatten(lst: list):
    if not lst:
        return []
    if isinstance(lst[0], Sequence):
        return flatten(lst[0]) + flatten(lst[1:])
    else:
        return [lst[0]] + flatten(lst[1:])

def test_flatten():
    print(flatten([1, [2, 3], [[4, 5], 6]]))
    print(flatten([1, 2]))
    print(flatten([1, [2, 3], (4, 5), range(6, 8)]))

def _gen_maker(f):
    it = 0
    def generator():
        nonlocal it
        it+=1
        return f(it)
    return generator

def make_generator(f):
    return _gen_maker(f)

def make_generator_memoized(f):
    f_cache = lru_cache(maxsize=128)(f)
    return _gen_maker(f_cache)


def fibo(n):
    match n:
        case 0:
            return 0
        case 1:
            return 1
        case n:
            return fibo(n-1) + fibo(n-2)

@lru_cache(maxsize=128)
def fibo_mem(n):
    match n:
        case 0:
            return 0
        case 1:
            return 1
        case n:
            return fibo(n-1) + fibo(n-2)

def test_4_fib():
    gen = make_generator(fibo)

    for _ in range(10):
        print(gen())

def test_4_lambda():
    gen = make_generator(lambda x: x+1)

    for _ in range(10):
        print(gen())

def test_5():
    gen = make_generator_memoized(fibo)

    for _ in range(10):
        print(gen())

def test_5_fibo_mem():
    for i in range(1, 11):
        print(fibo_mem(i))

def test_6(caplog): #needs to be run with command pytest functions.py -s to work properly (-s enables print output into console)
    @log
    class TestClass:
        def __init__(self, num, kwnum=999):
            self.num = num
            self.kwnum=kwnum

    @log
    def test_print(x, y, kw=13):
        print(f"Testing {x}, {y}, {kw}")

    caplog.set_level(logging.INFO)
    TestClass(12, kwnum=567)
    print(caplog.text)
    caplog.clear()
    test_print(1, 2, kw=55)
    print(caplog.text)



def main():
    test_6()

if __name__ == '__main__':
    main()