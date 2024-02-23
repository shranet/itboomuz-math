import math
from decimal import Decimal, getcontext

# Aniqlik darajasi
getcontext().prec = 25


def my_sin(x):
    result = 0
    fact = 1
    for i in range(30):
        power = 2 * i + 1
        if i > 0:
            fact *= (2 * i) * power

        if i % 2 == 0:
            result += x ** power / fact
        else:
            result -= x ** power / fact

    return result


def my_pi():
    result = 0
    for i in range(10000000):
        k = 2 * i + 1
        if i % 2 == 0:
            result += 1 / k
        else:
            result -= 1 / k

    return 4 * result


def my_pi2():
    fact4 = 1
    fact = 1
    sum_result = Decimal(0)
    for k in range(5):
        if k > 0:
            # 4 * 3 * 2 * 1
            # keyingi siklda 8 * 7 * 6 * 5
            # natija 4k!
            fact4 *= (4 * k) * (4 * k - 1) * (4 * k - 2) * (4 * k - 3)
            fact *= k

        sum_result += Decimal(fact4 * (1103 + 26390 * k)) / Decimal(fact ** 4 * 396 ** (4 * k))

    return 1 / (Decimal(2 * math.sqrt(2)) / 9801 * sum_result)


print("   sin(pi / 4) =", math.sin(math.pi / 4))
print("my_sin(pi / 4) =", my_sin(math.pi / 4))

print("   sin(pi / 5) =", math.sin(math.pi / 5))
print("my_sin(pi / 5) =", my_sin(math.pi / 5))

print()
print(" math.pi =", math.pi)
print(" my_pi() =", my_pi())
print("my_pi2() =", my_pi2())


