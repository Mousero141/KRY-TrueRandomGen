import math
import logging
logging.basicConfig(filename = 'test.log', level = logging.DEBUG)

def Mersenne(input): #Kontrola zda jde o Mersenovo prvočíslo
    i = 0
    while True:
        temp = 2 ** i - 1
        if temp == input:
            return True
        if temp > input:
            logging.info("{} not a prime number".format(input))
            return False
        i += 1

def lucas_lehmeruv(input):
    trueorfalse = Mersenne(input)
    if trueorfalse == True: #Číslo se testuje jen v případě, že jde o Mersenovo prvočíslo
        vo = 4
        list = []
        while True:
            temp = (vo ** 2 - 2) % input
            list.append(temp)
            if temp == 0:
                logging.info("{} is prime number".format(input))
                return True
            if list.count(temp) > 1:
                return False
            vo = temp
    else:
        return False

