"""Custom list implementation"""


class List(list):
    """List with add operation"""
    def __add__(self, other):
        result = []
        for i in range(max(len(self), len(other))):
            first = self[i] if i < len(self) else 0
            second = other[i] if i < len(other) else 0
            result.append(first + second)
        return result

    def __lt__(self, other):
        return sum(self) < sum(other)

    def __le__(self, other):
        return sum(self) <= sum(other)

    def __eq__(self, other):
        return sum(self) == sum(other)

    def __gt__(self, other):
        return sum(self) > sum(other)

    def __ge__(self, other):
        return sum(self) >= sum(other)


if __name__ == '__main__':
    a = List([1, 2, 3])
    b = List([4, 7, 11, 2])
    c = List()
    d = List([4, 8, 1])
    print(a + d, b + c, b + a)
    print(b > a, d == c, a <= d, c < b, )
