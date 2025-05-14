import functools
import logging
import time
import inspect

def log(obj):
    def wrapper(level=logging.INFO):
        if inspect.isclass(obj):
            _log_class(obj, level)
        elif inspect.isfunction(obj):
            _log_func(obj, level)
        else:
            raise TypeError("@log can only be used on classes or functions")

    return wrapper

def _log_class(c, level):
    logger = logging.getLogger(c.__module__)

    @functools.wraps(c.__init__) # so __name__ and __doc__ work correctly
    def wrapper(self, *args, **kwargs):
        logger.log(level, f'Creating an instance of {c.__name__}')
        c(self, *args, **kwargs)

    c.__init__ = wrapper
    return c


def _log_func(f, level):
    logger = logging.getLogger(f.__module__)

    @functools.wraps(f)
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
    def sorted_copy(lst): # funkcja wywolujaca funkcje?
        return sorted(lst)

    nums = sorted_copy(numbers)

    return None if not nums else (
        nums[0] if len(nums) == 1 else (
            (nums[0] + nums[1]) / 2 if len(nums) == 2 else median(nums[1:-1])
        )
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
        for key in keys # uzywany for
    }

def test_alpha_dict():
    print(make_alpha_dict('ona i on'))
    print(make_alpha_dict('adam lubi placki'))


def flatten(lst: list):
    if not lst:
        return []
    if isinstance(lst[0], list): # moga byc tez sekwencje
        return flatten(lst[0]) + flatten(lst[1:])
    else:
        return [lst[0]] + flatten(lst[1:])

def test_flatten():
    print(flatten([1, [2, 3], [[4, 5], 6]]))
    print(flatten([1, 2]))

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
    f_cache = functools.lru_cache(maxsize=128)(f)
    return _gen_maker(f_cache)


def fibo(n):
    match n:
        case 0:
            return 0
        case 1:
            return 1
        case n:
            return fibo(n-1) + fibo(n-2)

@functools.lru_cache(maxsize=128)
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

def main():
    test_5_fibo_mem()

if __name__ == '__main__':
    main()