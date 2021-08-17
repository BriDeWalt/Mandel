from math import sqrt
def findfactors(n):
    factors = set()
    if n%2 == 0:
        for i in range(1,int(sqrt(n))+1):
            if n % i == 0:
                factors.add(i)
                factors.add(n//i)
    else:
        for i in range(1,int(sqrt(n)+1),2):
            if n%i == 0:
                factors.add(i)
                factors.add(n//i)
    return factors
def findprimefactors(n):
    factors = []
    expo = []
    count = 0
    while n%2 == 0:
        factors.append(2)
        count += 1
        factors.append(2)
        n //= 2
        if (2, count - 1) in expo:
            expo[-1] = (2, count)
        else:
            expo.append((2, 1))
    d = 3
    while d*d <= n:
        count = 0
        while n%d == 0:
            count += 1
            factors.append(d)
            n //= d
            if (d,count-1) in expo:
                expo[expo.index((d,count-1))] = (d,count)
            else:
                expo.append((d,1))
        d += 2
    if n > 1 :
        factors.append(n)
        if (n, count - 1) in expo:
            expo[expo.index((n, count - 1))] = (n, count)
        else:
            expo.append((n, 1))

    return factors, str(expo)






