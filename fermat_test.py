import random
import os
import logging
logging.basicConfig(filename = 'test.log', level = logging.DEBUG)


def fermat_test1(n, k):  #n = possible_prime  #k = iterations
    #Je-li n=1,2 nebo 3 tak je provčíslo. Je=li n%mod 2 = 0 -> není prvočíslo
    if n == 1:
        return True

    if n == 2:
        return True

    if n == 3:
        return True

    if n % 2 == 0:
        return False

    for i in range(k): # k je počet iterací.
        a = random.randint(1, n-1) #Náhodně vygenerovat číslo - prvočílo-1
        if pow(a^(n-1) % n) != 1:
            logging.info("Fermat\'s test -> False")
            return False
                
    logging.info("Fermat\'s test -> True")
    return True









