#import large_prime_generation as primes
import sys
import large_prime_generation as lpg
import erathostens_sieve as es
import time
import logging
import random
import os
import miller_rabin_test as miller
import fermat_test as fermat
import lucas_lehmer_primality_test as lehmer



number=0
global generatedNumber
global last_line
global number_in_file


print("ACR-Large-Primes-Generator\n")

log_file = open('test.log', 'a')
log_file.write('------------------------------------------------------------------------------------------\n')
log_file.write(time.strftime('%d_%m_%Y--%I_%M_%S_%p\n'))
log_file.close()

logging.basicConfig(filename = 'test.log', level = logging.DEBUG)
print("1 - Generate new prime number")
print("2 - Test of primality for entered number + Erathostens Sieve")
print("3 - Export generated number to file")
print("4 - Import number from file + primality test\n")

while(True):
#V této části uživatel zadá délku prvočísla, které chce vygenerovat.
    try:
        choose_an_action = int(input("Choose what action you want to perform: "))
    except ValueError:
        logging.info("Enter only positive numbers")
    else:
        if choose_an_action == 1:
            logging.info("Chosen action -> \'Generate new prime number\'")
            take_length = lpg.choose_a_length() #Definice délky
            number=lpg.generating_number(take_length) #Vygenerování lichého čísla
            print(number)
            generatedNumber=str(number)#Konverze na string
           
        elif choose_an_action == 2:
            #Aplikace 3 testů na vygenrovné liché číslo
            logging.info("Chosen action -> \'Test of primality for entered number\'\n")
            
            if(number==0):
                print("Number was not generated press 1 for generating number")
            else:
                fermat_test_solved=fermat.fermat_test1(number,3)
                if fermat_test_solved:
                        print("Number", number ,  "is a prime number according to the Fermat Primality Test")


                        miller_rabin_test_print=miller.FinalPart(number)
                        if miller_rabin_test_print:
                            print("Number", number ,  "is a prime number accoring to Miller-Rabin test")


                            lucas_lehmer_test_print=lehmer.lucas_lehmeruv(number)
                            if lucas_lehmer_test_print:
                                print("Number", number ,  "is a prime number accoring to Lucas-Lehmer test")
                                print("\nErathostens Sieve:\n")
                                print(es.poping_phase(number))
                            


                            else:
                                print("Number", number ,  "is a not prime number accoring to Lucas-Lehmer test")
                        else:
                            print("Number", number, "is not a prime number accoring to Miller-Rabin test")
                        
                else:
                    print("Number", number, "is not a prime number according to the Fermat Primality Test")
                    #V případě, že číslo neprojde biť jedním testem aplikuje se funkce naive_incremetal generator
                    naive_incremental_prime = lpg.naive_incremental_prime_generator(number)
                    number=naive_incremental_prime
                    
            
        elif choose_an_action == 3:
            #Export cisla do souboru .txt, bude se muset otevrit okno File exploreru, tak jak kdyz se vybira soubor k narati treba na Moodle
            logging.info("Chosen action -> Export number to file")
            if(number==0):
                print("Number was not generated. If you want generate number press 1")
            else:
                with open("generated_numbers.txt", "a", encoding="utf-8") as f:
                    f.write("\n")
                    f.write(generatedNumber)
                print("Generated number was written into file.")
                logging.info("{} writted into a file".format(generatedNumber))
 
        elif choose_an_action == 4:
            #Import cisla ze souboru + otestovani prvociselnosti
            logging.info("Chosen action -> \'Import number from a file(bin/txt)\'")

            def is_file_empty(file_path):
                return os.path.exists(file_path) and os.stat(file_path).st_size == 0
   
            file_path="generated_numbers.txt"
            is_empty = is_file_empty(file_path)
            if is_empty:
                print("File is empty")
            else:
                with open("generated_numbers.txt", "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    last_line = lines[-1:]

                for i in last_line:
                    if i.isdigit():
                        number_in_file=int(i)
                        print("Generated number from file: ", number_in_file)

                        fermat_test_solved=fermat.fermat_test1(number_in_file,3)
                        if fermat_test_solved:
                           print("Number", number_in_file ,  "is a prime number according to the Fermat Primality Test")
                        else:
                           print("Number", number_in_file ,  "is not a prime number according to the Fermat Primality Test")

                        
                        miller_rabin_test_print=miller.FinalPart(number_in_file)
                
                        if miller_rabin_test_print:
                            print("Number", number_in_file ,  "is a prime number accoring to Miller-Rabin test")
                        else:
                            print("Number", number_in_file, "is not a prime number accoring to Miller-Rabin test")
                        
                        lucas_lehmer_test_print = lehmer.lucas_lehmeruv(number_in_file)
                        if lucas_lehmer_test_print:
                            print("Number", number_in_file ,  "is a prime number accoring to Lucas Lehmer test")
                        else:
                            print("Number", number_in_file, "is not a prime number accoring to Lucas Lehmer test")

                    
    


    


