def acronym(words: list):
    return '' if not words else words[0][0].upper() + acronym(words[1:])


print(acronym(['Zaklad', 'Ubezpieczen', 'Socjalnych']))


def median(numbers: list):
    def sorted_copy(lst):
        return sorted(lst)

    nums = sorted_copy(numbers)

    return None if not nums else (
        nums[0] if len(nums) == 1 else (
            (nums[0] + nums[1]) / 2 if len(nums) == 2 else median(nums[1:-1])
        )
    )


print(median([1, 2, 3, 4, 5]))
print(median([1, 2, 3, 4, 5, 6]))
print(median([]))


def pierwiastek(x, epsilon, y=1):
    return y if abs(y * y - x) < epsilon else pierwiastek(x, epsilon, 0.5 * (y + x / y))


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


print(make_alpha_dict('ona i on'))
print(make_alpha_dict('adam lubi placki'))


def flatten(lst: list):
    if not lst:
        return []
    if isinstance(lst[0], list):
        return flatten(lst[0]) + flatten(lst[1:])
    else:
        return [lst[0]] + flatten(lst[1:])


print(flatten([1, [2, 3], [[4, 5], 6]]))
print(flatten([1, 2]))
