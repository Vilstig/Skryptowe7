import random
import string


class PasswordGenerator:
    def __init__(self, length, count, charset=None):
        self.length = length
        self.charset = charset if charset is not None else string.ascii_letters + string.digits
        self.count = count
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= self.count:
            raise StopIteration

        self.index += 1
        return ''.join(random.choices(self.charset, k=self.length))

generator1 = PasswordGenerator(length=8, count=5, charset='abcABC123')

for password in generator1:
    print(password)

generator2 = PasswordGenerator(length=8, count=3)

print(next(generator2))
print(next(generator2))
print(next(generator2))
print(next(generator2))
