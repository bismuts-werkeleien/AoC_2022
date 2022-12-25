import sys

def build_base(num):
    base = [1]
    for i in range(20):
        base.append(base[-1]*5)
    return base

with open(sys.argv[1]) as file:
    snafu_list = file.read().split('\n')[:-1]
    snafu_list = [list(map(lambda s: int(s) if s.isdigit() else -1 if s == '-' else -2, snafu)) for snafu in snafu_list]

snafu_base = build_base(5)

def snafu_2_decimal(snafu, base):
    decimal_products = [s*b for s,b in zip(snafu[::-1], base)]
    return(sum(decimal_products))

def decimal_2_snafu(dec, base):
    remainder = dec
    snafu = ""
    started = False
    for b in base[::-1]:
        if abs(remainder) / b < 1 and not started:
            continue  # start at smaller base pos
        else:
            started = True
            if abs(abs(remainder)-2*b) < abs(abs(remainder) - b):
                if remainder > 0:
                    snafu += "2"
                    remainder -= (2*b)
                else:
                    snafu += "="
                    remainder += 2*b
                continue
            elif abs(abs(remainder) - b) < abs(remainder):
                if remainder > 0:
                    snafu += "1"
                    remainder -= b
                else:
                    snafu += "-"
                    remainder += b
                continue
            else:
                snafu += "0"
    return snafu


decimal_list = [snafu_2_decimal(n, snafu_base) for n in snafu_list]
decimal_sum = sum(decimal_list)
print(f"The decimal number of needed fuel is {decimal_sum}")

# now convert back
print(f"The SNAFU number to supply to Bob's console is {decimal_2_snafu(decimal_sum, snafu_base)}")

