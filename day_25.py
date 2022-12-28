from time import perf_counter

D_MAP = {
    0: '0',
    1: '1',
    2: '2',
    -2: '=',
    -1: '-'
}
S_MAP = {
    '0': 0,
    '1': 1,
    '2': 2,
    '=': -2,
    '-': -1
}


def decimal_to_snafu(decimal):
    snafu = ''
    while True:
        s = decimal % 5
        if s > 2: s -= 5
        snafu = D_MAP.get(s) + snafu
        s = (decimal - s) // 5
        if s == 0: break
        decimal = s
    return snafu


def snafu_to_decimal(string):
    decimal = 0
    for p, s in enumerate(string[::-1]):
        decimal += S_MAP.get(s) * (5 ** p)
    return decimal


def main():
    with open('input_day_25.txt', 'r') as f:
        input_lines = f.read().splitlines()

    decimal_total = sum(snafu_to_decimal(line) for line in input_lines)
    print(decimal_total)
    print('SNAFU number:', decimal_to_snafu(decimal_total))


if __name__ == "__main__":
    start = perf_counter()
    main()
    end = perf_counter()
    print('Completed in:', round((end - start) * 1000, 2), 'ms')
