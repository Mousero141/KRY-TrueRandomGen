# import large_prime_generation as primes
import sys

import pyautogui as pyautogui

import large_prime_generation as lpg
import erathostens_sieve as es
import time
import logging
import random
import os
import miller_rabin_test as miller
import fermat_test as fermat
import lucas_lehmer_primality_test as lehmer
import sympy
import hashlib
import time
import os
import inspect

print(os.path.dirname(inspect.getfile(inspect)) + "/site-packages")

number = 0
global generatedNumber
global last_line
global number_in_file

print("ACR-Large-Primes-Generator\n")

log_file = open('test.log', 'a')
log_file.write('------------------------------------------------------------------------------------------\n')
log_file.write(time.strftime('%d_%m_%Y--%I_%M_%S_%p\n'))
log_file.close()

logging.basicConfig(filename='test.log', level=logging.DEBUG)

def log_timestamp():
    timestamp = time.strftime('%d_%m_%Y--%I_%M_%S_%p')
    logging.info(timestamp)

def mouse_movement_entropy(duration):
    data = ''
    start_time = time.time()
    while (time.time() - start_time) < duration:
        x, y = pyautogui.position()
        data += f'{x},{y} '
        time.sleep(0.00001)
    print(data)
    return data

def get_hash_function(bit_length):
    """Get the appropriate hash function based on the bit length."""
    if bit_length == 128:
        return hashlib.md5
    elif bit_length == 256:
        return hashlib.sha256
    elif bit_length == 512:
        return hashlib.sha512
    elif bit_length == 1024:
        return hashlib.sha512
    else:
        raise ValueError("Unsupported bit length for hash function")
def generate_random_number(bit_length):
    """Generate a random number with the specified bit length."""
    # Check if bit_length is less than 128
    # Check if bit_length is less than 128
    if bit_length < 128:
        print("Using os.urandom() for generating random number.")
        num_bytes = (bit_length + 7) // 8
        hash_digest = os.urandom(num_bytes)
        combined_bytes=hash_digest

    else:
        # Round the bit length to the nearest hash function
        rounded_bit_length = round_to_nearest_hash_function(bit_length)
        print("Using hash function for generating random number.")
        # Pevný časový interval na základě současného času
        current_time = int(time.time())
        #duration = current_time % 10 + 5  # Pevný časový interval mezi 5 a 15 sekundami
        duration = random.randint(0, 0) + random.random()  # Duration in seconds

        print(f"Gathering mouse movement data for {duration} seconds...")
        mouse_data = mouse_movement_entropy(duration)
        hash_function = get_hash_function(rounded_bit_length)
        hash_object = hash_function(mouse_data.encode())
        hash_digest = hash_object.digest()


        # Získání první poloviny z hash digest
        # first_half_digest = hash_digest[:len(hash_digest) // 2]
        # Získání druhé poloviny z os.urandom
        # num_bytes = (bit_length + 7) // 8
        # second_half_random = os.urandom(num_bytes // 2)

        # Ensure that the hash digest is truncated or padded to match half of the desired bit length
        half_bit_length = bit_length // 2
        digest_length = (half_bit_length + 7) // 8  # Convert bit length to byte length
        truncated_digest = hash_digest[:digest_length]

        # Generate the second half of the combined bytes using os.urandom
        remaining_bit_length = bit_length - len(truncated_digest) * 8
        num_bytes_needed = (remaining_bit_length + 7) // 8
        second_half_random = os.urandom(num_bytes_needed)

        # Combine the truncated hash digest with the second half of os.urandom bytes
        combined_bytes = truncated_digest + second_half_random

    # Convert the hash to an integer
    random_integer = int.from_bytes(combined_bytes, byteorder='big')
    return random_integer

def round_to_nearest_hash_function(bit_length):
    """Round the bit length to the nearest hash function."""
    hash_functions = [128, 256, 512, 1024]  # List of hash function bit lengths
    nearest_hash = min(hash_functions, key=lambda x: abs(x - bit_length))
    return nearest_hash

def is_prime(number):
    """Check if the given number is prime."""
    return sympy.isprime(number)


print("1 - Generate new prime number")
print("2 - Generate with mouse")
print("3 - Export generated number to file")
print("4 - Import number from file + primality test\n")

while (True):
    # V této části uživatel zadá délku prvočísla, které chce vygenerovat.
    try:
        choose_an_action = int(input("Choose what action you want to perform: "))
    except ValueError:
        logging.info("Enter only positive numbers")
    else:
        if choose_an_action == 1:
            logging.info("Chosen action -> \'Generate new prime number\'")
            log_timestamp()

            print("Warning: For security reasons, it is recommended to use bit lengths of 128 or more.")
            bit_length = int(input("Enter the desired bit length for the random number: "))
            # Generate a random number with the specified bit length

            random_number = generate_random_number(bit_length)
            print(f"Random number with {bit_length} bits: {random_number}")
            break

        elif choose_an_action == 3:
            # Export cisla do souboru .txt, bude se muset otevrit okno File exploreru, tak jak kdyz se vybira soubor k narati treba na Moodle
            logging.info("Chosen action -> Export number to file")
            if (number == 0):
                print("Number was not generated. If you want generate number press 1")
            else:
                with open("generated_numbers.txt", "a", encoding="utf-8") as f:
                    f.write("\n")
                    f.write(generatedNumber)
                print("Generated number was written into file.")
                logging.info("{} writted into a file".format(generatedNumber))
                log_timestamp()
            break
        elif choose_an_action == 4:
            # Import cisla ze souboru + otestovani prvociselnosti
            logging.info("Chosen action -> \'Import number from a file(bin/txt)\'")

            def is_file_empty(file_path):
                return os.path.exists(file_path) and os.stat(file_path).st_size == 0
            file_path = "generated_numbers.txt"
            is_empty = is_file_empty(file_path)
            if is_empty:
                print("File is empty")
            else:
                with open("generated_numbers.txt", "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    last_line = lines[-1:]

                for i in last_line:
                    if i.isdigit():
                        number_in_file = int(i)
                        print("Generated number from file: ", number_in_file)
            break







