import itertools


class Computer:

    def __init__(self, a: int, b: int, c: int):
        self.a, self.b, self.c = a, b, c
        self.ptr = 0
        self.opcode_to_f = {
            0: self.adv,
            1: self.bxl,
            2: self.bst,
            3: self.jnz,
            4: self.bxc,
            5: self.out,
            6: self.bdv,
            7: self.cdv,
        }

    def __repr__(self):
        return f"{self.a=}, {self.b=}, {self.c=}, {self.ptr=}"

    def run(self, program: tuple[int, ...]):
        while self.ptr < len(program):
            output = self.opcode_to_f[program[self.ptr]](program[self.ptr + 1])
            if output is not None:
                yield output

    def op_to_combo(self, op):
        if 0 <= op < 4:
            return op
        elif op == 4:
            return self.a
        elif op == 5:
            return self.b
        elif op == 6:
            return self.c
        else:
            raise ValueError

    def adv(self, op):
        self.a //= 2 ** self.op_to_combo(op)
        self.ptr += 2

    def bxl(self, op):
        self.b ^= op
        self.ptr += 2

    def bst(self, op):
        self.b = self.op_to_combo(op) % 8
        self.ptr += 2

    def jnz(self, op):
        if self.a == 0:
            self.ptr += 2
        else:
            self.ptr = op

    def bxc(self, _):
        self.b ^= self.c
        self.ptr += 2

    def out(self, op):
        output = self.op_to_combo(op) % 8
        self.ptr += 2
        return output

    def bdv(self, op):
        self.b = self.a // 2 ** self.op_to_combo(op)
        self.ptr += 2

    def cdv(self, op):
        self.c = self.a // 2 ** self.op_to_combo(op)
        self.ptr += 2


def part1():
    c = Computer(47792830, 0, 0)
    program = (2, 4, 1, 5, 7, 5, 1, 6, 4, 3, 5, 5, 0, 3, 3, 0)
    result = c.run(program)
    # for r, p in itertools.zip_longest(result, program):
    #     print(r, p)
    return ",".join(str(r) for r in result)


def part2():
    program = (2, 4, 1, 5, 7, 5, 1, 6, 4, 3, 5, 5, 0, 3, 3, 0)
    # program = (0, 3, 5, 4, 3, 0)
    import tqdm

    for a in tqdm.tqdm(
        itertools.count(),
        bar_format="{n_fmt} iterations | {rate_fmt} | Elapsed: {elapsed}",
    ):
        c = Computer(a * 8, 0, 0)
        result = c.run(program)
        if all(r == p for r, p in itertools.zip_longest(result, program)):
            return a * 8
