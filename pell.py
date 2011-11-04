#!/usr/bin/env python
import math
import fractions
def fundamental(n):
    """Find a fundamental solution to pell equation. 
    Use the continous fraction form of a square root"""
    r = math.sqrt(n)
    result = [int(r)]
    r = 1 / (r - result[-1])
    while True:
        result.append(int(r))
        r = 1 / (r - result[-1])
        j = len(result)
        a, b = 1, 0
        for j in result[::-1]:
            a, b = a*j + b, a
        temp = fractions.gcd(a, b)
        a, b = a / temp, b / temp
        if a*a - n*b*b == 1:
            return a, b

def pell(n):
    """Solutions to the standard form of a pell equation. 
    That is a^2 -db^2 = 1"""
    a1, b1 = fundamental(n)
    a, b =  a1, b1
    while True:
        yield a, b
        a, b = a1*a + n*b1*b, a1*b + b1*a

def pell_k(n, k, x, y):
    """Solutions to the expension form of a pell equation.
    That is a^2 -db^2 = k(k != 1)"""
    a1, b1 = fundamental(n)
    while True:
        yield x, y
        x, y = a1*x + n*b1*y, b1*x+a1*y


def main():
    """test cases"""

    # test case 1
    print "x^2 - 2 * y^2 = 1"
    for a, b in pell(2):
        assert a*a - 2*b*b == 1
        print "%s\t\t%s" % (a, b)
        if a > 10000:
            break
    print

    # test case 2
    print "x^2 - 3 * y^2 = 1"
    for a, b in pell(3):
        assert a*a - 3*b*b == 1
        print "%s\t\t%s" % (a, b)
        if a > 10000:
            break
    print

    # test case 3
    print "x^2 - 3 * y^2 = -2"
    for a, b in pell_k(3, -2, 1, 1):
        assert a*a - 3*b*b == -2
        print "%s\t\t%s" % (a, b)
        if a > 10000:
            break

if __name__ == '__main__':
    main()
