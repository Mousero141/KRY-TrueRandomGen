import random
import logging
import math
import fermat_test as test1
import miller_rabin_test as test2
import lucas_lehmer_primality_test as test3


logging.basicConfig(filename = 'test.log', level = logging.DEBUG)


def choose_a_length():
    """Function that takes input of <int> type for determining length of prime to generate"""
    while True:
        try:
            length = int(input("Enter bit-length of prime you want to generate: "))
            if(length>0 and type(length) == int):
                logging.info("LENGTH OF DESIRED PRIME NUMBER:{}".format(length))
                return length
            raise ValueError
        except ValueError:
            print("Enter whole possitive numbers only")
            logging.info("Enter whole possitive numbers only")
        except Exception:
            print("Error occured")
            logging.info("Error occured")

                   
def generating_number(length):

    """Generating number, of selected length"""
    while(True):
        possible_prime = random.SystemRandom().getrandbits(length)
        if((possible_prime%2) == 0):
            generating_number(length)
        else:
             return possible_prime # number of user-defined length

def II_pregeneration():
    II = 2
    for num in range(2, 30):
        if num % 2 != 0:
            II*=num
    return II
        

def naive_incremental_prime_generator(possible_prime):
    II = II_pregeneration()
    while(True):
        if(math.gcd(possible_prime,II) == 1):
            #Fáze inkrementace
            while(True):
                prime = possible_prime+II
                if(test1.fermat_test1 == True):
                    if(test2.FinalPart== True):
                        if(test3.lucas_lehmeruv == True):
                            return prime

        
            
            
        