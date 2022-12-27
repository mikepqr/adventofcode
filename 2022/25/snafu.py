import pytest


def snafu_digit_to_int(c: str):
    if c in {"0", "1", "2"}:
        return int(c)
    elif c == "=":
        return -2
    elif c == "-":
        return -1
    else:
        raise ValueError(c)


def snafu(x: int) -> str:
    s = []
    carry = 0
    while x:
        x, mod = divmod(x, 5)
        mod = carry + mod
        if mod <= 2:
            s.append(str(mod))
            carry = 0
        if mod == 3:
            s.append("=")
            carry = 1
        if mod == 4:
            s.append("-")
            carry = 1
    if carry:
        s.append("1")
    return "".join(s[::-1])


def decimal(s: str) -> int:
    return sum(snafu_digit_to_int(c) * 5 ** i for i, c in enumerate(s[::-1]))


def compute1(fname):
    with open(fname) as f:
        snafus = [line.strip() for line in f.readlines()]
    return snafu(sum(decimal(s) for s in snafus))


TESTS = (
    ("1=-0-2", 1747),
    ("12111", 906),
    ("2=0=", 198),
    ("21", 11),
    ("2=01", 201),
    ("111", 31),
    ("20012", 1257),
    ("112", 32),
    ("1=-1=", 353),
    ("1-12", 107),
    ("12", 7),
    ("1=", 3),
    ("122", 37),
)


@pytest.mark.parametrize("s, x", TESTS)
def test_decimal(s, x):
    assert decimal(s) == x


@pytest.mark.parametrize("s, x", TESTS)
def test_snafu(s, x):
    assert snafu(x) == s
