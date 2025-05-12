
def forall(pred, iterable):
    return all(map(pred, iterable))

def exists(pred, iterable):
    return any(map(pred, iterable))

def atleast(n, pred, iterable):
    return sum(map(pred, iterable)) >= n

def atmost(n, pred, iterable):
    return sum(map(pred, iterable)) <= n


print(forall(lambda x: x < 5, range(10)))
print(forall(lambda x: x < 15, range(10)))

print(exists(lambda x: x < 5, range(10)))
print(exists(lambda x: x > 15, range(10)))

print(atleast(5, lambda x: x < 4, range(10)))
print(atleast(5, lambda x: x < 6, range(10)))

print(atmost(5, lambda x: x < 4, range(10)))
print(atmost(5, lambda x: x < 6, range(10)))

