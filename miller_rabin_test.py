import math
import logging
logging.basicConfig(filename = 'test.log', level = logging.DEBUG)


def Part1(n):# V části 'Part1' volime r a s
    s = 0
    r = 1
    while ((2 ** s * r + 1) <= n):
        while ((2 ** s * r + 1) <= n):
            if (2 ** s * r + 1) == n:
                return s, r
            r += 2
        s += 1
        r = 1


def Part2(n,a): #a je vybrano na zaklade podminky <1,(n-1)> 
    while(True):
        if (a >= 1 and a <= (n-1)):
            return a
        a += 1

def FinalPart(n):
    temp = 0
    a = Part2(n,temp)
    s, r = Part1(n)

    test = False
    while (test == False):
        if(a**r % n == 1):
            test = False
            temp += 1
            a = Part2(n, temp)
        else:
            test = True
    i = 0

    if test == True:
        while True:
            if i <= s-1 and i <= 4:
                if (a**((2**i)*r)) % n == (n-1):
                    logging.info("{} Miller Rabin\'s test-> True".format(n))
                    return True #Pokud rovnice v if platé jde o prvočíslo
                else:
                    i += 1 #Jinak se test opakuje pro i-čka, nevýše však 4x.
            else:
                logging.info("{} Miller Rabin\'s test-> False".format(n))
                return False #Neplatí-li nejedná se o provčíslo




