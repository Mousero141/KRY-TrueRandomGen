# import large_prime_generation as primes
import sys
from operator import ge
from random import random

import pyautogui as pyautogui
import logging
import random
import hashlib
import time
import os
import inspect
import math
import prngtest
import dieharder
from cryptography.fernet import Fernet

print(os.path.dirname(inspect.getfile(inspect)) + "/site-packages")

number = 0
global generatedNumber
global last_line
global number_in_file

choose_an_action = 99

print("KRY-True-Random-Generator\n")

log_file = open('test.log', 'a')
log_file.write('------------------------------------------------------------------------------------------\n')
log_file.write(time.strftime('%d_%m_%Y--%I_%M_%S_%p\n'))
log_file.close()

logging.basicConfig(filename='test.log', level=logging.DEBUG)


def log_timestamp():
    timestamp = time.strftime('%d_%m_%Y--%I_%M_%S_%p')
    logging.info(timestamp)


def decrypt_number(encrypted_number, cipher):
    # Decrypt the encrypted number
    decrypted_number_bytes = cipher.decrypt(encrypted_number)
    # Convert decrypted bytes back to integer
    decrypted_number = int(decrypted_number_bytes.decode())
    return decrypted_number

def mouse_movement_entropy(duration):
    data = ''
    start_time = time.time()
    while (time.time() - start_time) < duration:
        x, y = pyautogui.position()
        data += f'{x},{y} '
        time.sleep(0.00001)
    print(data)
    return data


def numberControl(n):
    sts = prngtest.otm(n, None)
    if (sts[1] > 0.01):
        return True
    else:
        False


def resultPresenting(p):
    if (p > 0.01):
        print("Number is consider as RANDOM")
    else:
        print("Number is NOT RANDOM")


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


def generate_random_number(bit_length, mouse_data):
    """Generate a random number with the specified bit length."""
    # Check if bit_length is less than 128
    # Check if bit_length is less than 128
    if bit_length < 128:
        print("Using os.urandom() for generating random number.")
        num_bytes = (bit_length + 7) // 8
        hash_digest = os.urandom(num_bytes)
        combined_bytes = hash_digest

    if bit_length > 2048:
        print("Using hash function for generating random number.")
        # Determine the number of hash functions needed
        num_hashes = (bit_length + 1023) // 2048  # Each hash contributes 1024 bits, and we need at least one hash

        hash_digests = []
        for _ in range(num_hashes):
            hash_function = get_hash_function(1024)
            hash_digest = hash_function(
                mouse_data.encode() + os.urandom(16)).digest()  # Combining mouse_data with random bytes
            hash_digests.append(hash_digest)

        remaining_bit_length = bit_length - len(hash_digest) * 8
        num_bytes_needed = (remaining_bit_length + 7) // 8
        # second_half_random = os.urandom(num_bytes_needed)

        # Combine the truncated hash digest with the second half of os.urandom bytes
        combined_bytes = b''.join(hash_digests)

    else:
        # Round the bit length to the nearest hash function
        rounded_bit_length = round_to_nearest_hash_function(bit_length)
        print("Using hash function for generating random number.")
        # Pevný časový interval na základě současného času
        current_time = int(time.time())
        # duration = current_time % 10 + 5  # Pevný časový interval mezi 5 a 15 sekundami
        # duration = random.randint(0, 0) + random.random()  # Duration in seconds

        hash_function = get_hash_function(rounded_bit_length)
        hash_object = hash_function(mouse_data.encode())
        hash_digest = hash_object.digest()

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

    combined_bytes += os.urandom((bit_length - len(combined_bytes) * 8 + 7) // 8)

    # Convert the hash to an integer
    random_integer = int.from_bytes(combined_bytes, byteorder='big')
    random_integer &= (1 << bit_length) - 1

    bitRandom = bin(random_integer)[2:]
    while len(bitRandom) != bit_length and bit_length == 128:
        random_integer |= 1 << (bit_length - 1)
        bitRandom = bin(random_integer)[2:]

    return random_integer


def round_to_nearest_hash_function(bit_length):
    """Round the bit length to the nearest hash function."""
    hash_functions = [128, 256, 512, 1024]  # List of hash function bit lengths
    nearest_hash = min(hash_functions, key=lambda x: abs(x - bit_length))
    return nearest_hash

def encryptLog():
    key = Fernet.generate_key()  # Generate a Fernet key
    fernet = Fernet(key)  # Initialize a Fernet cipher object with the key
    with open("log_fernet_key.txt", "wb") as f:  # Save the key to a file
        f.write(key)
    with open("test.log", "rb") as f:
        original = f.read()
    encryptedFile = fernet.encrypt(original)

    with open("test.log", "wb") as f:
        f.write(encryptedFile)
    fileHash = hashlib.sha3_256(encryptedFile)
    print(f"Log file was successfully encrypted. Hash of the log file is: {fileHash.hexdigest()}")


def decryptLog():
    with open('log_fernet_key.txt', 'rb') as fileKey:
        key = fileKey.read()
    fernet = Fernet(key)
    with open("test.log", "rb") as f:
        encrypted = f.read()
    decryptedFile = fernet.decrypt(encrypted)

    with open("test.log", "wb") as f:
        f.write(decryptedFile)
    print("Log file was successfully DECRYPTED.")


def is_file_empty(file_path):
    return os.path.exists(file_path) and os.stat(file_path).st_size == 0


print("1 - Generate new number for testing")
print("2 - Import number from file")
print("3 - Test number")
print("4 - Export generated number to file")
print("5 - Generate number truly random number")
print("0 - Exit\n")

try:
    decryptLog()
except:
    print("File is not encrypted!")

while choose_an_action != 0:
    # V této části uživatel zadá délku prvočísla, které chce vygenerovat.
    try:
        choose_an_action = int(input("Choose what action you want to perform: "))
    except ValueError:
        logging.info("Enter only positive numbers")
    else:
        if choose_an_action == 1:
            logging.info("Chosen action -> \'Generate new number\'")
            log_timestamp()

            print("Warning: For security reasons, it is recommended to use bit lengths of 128 or more.")
            bit_length = int(input("Enter the desired bit length for the random number: "))

            logging.info("Generate a random number with the specified bit length")
            log_timestamp()
            # Generate a random number with the specified bit length
            duration = random.randint(10, 25) + random.random()  # Duration in seconds
            print(f"Gathering mouse movement data for {duration} seconds...")
            mouse_data = mouse_movement_entropy(duration)

            counter = 0
            print(time.time())
            random_number = generate_random_number(bit_length, mouse_data)
            print(time.time())
            # print(f"Random number with {bit_length} bits: {random_number}")
            if len(str(random_number)) > 199:
                print(f"Random number with {bit_length} bits: {str(random_number)[:200]}..")
                logging.info(f"Random number with {bit_length} bits: {str(random_number)[:200]}..")
                log_timestamp()
            else:
                print(f"Random number with {bit_length} bits: {random_number}")
                logging.info(f"Random number with {bit_length} bits: {str(random_number)[:200]}..")
                log_timestamp()
            generatedNumber = random_number
            continue

        elif choose_an_action == 2:
            logging.info("Chosen action -> \'Import number from a file(bin/txt)\'")
            log_timestamp()
            print("System is using generated_numbers.txt file for import/export")

            print("1 - Importing plain text number")
            print("2 - Importing encrypted number")

            chooseImport = int(input("Choose how the number should be imported"))
            if chooseImport == 1:
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
                            generatedNumber = number_in_file
                logging.info(f"Number was imported {generatedNumber}")
                log_timestamp()
                continue
            elif chooseImport == 2:
                with open("fernet_key.txt", "rb") as f:
                    key = f.read()

                cipher = Fernet(key)

                with open("encrypted_number.txt", "rb") as f:
                    for line in f:
                        # Read each line (which should contain one encrypted number)
                        encrypted_number = line.strip()
                        # Decrypt the encrypted number
                        decrypted_number = decrypt_number(encrypted_number, cipher)
                        print("Decrypted Number:", decrypted_number)
                    generatedNumber = decrypted_number
                    logging.info(f"Number was imported {generatedNumber}")
                    log_timestamp()
                continue

        elif choose_an_action == 3:
            logging.info("Chosen action -> \'Test number\'")
            log_timestamp()
            print("1 - NIST STS tests")
            print("2 - Dieharder tests")
            chooseTest = int(input("Choose what set of test you want to use: "))

            if chooseTest == 1:
                print("You choose NIST STS tests")
                try:
                    print(f"Testing number {generatedNumber}\n")
                    bitRepresent = bin(generatedNumber)[2:]

                    # The focus of this test is the proportion of zeroes and ones for the entire sequence.
                    # The purpose of this test is to determine whether the number of ones and zeros in a sequence are approximately the same as would be expected for a truly random sequence.
                    print("Frequency (Monobit) Test:")
                    logging.info("Frequency (Monobit) Test:")
                    sts = prngtest.monobit(bitRepresent)
                    print(sts)
                    resultPresenting(sts[1])
                    logging.info(sts)
                    log_timestamp()
                    print("\n")

                    # The focus of this test is the total number of runs in the sequence, where a run is an uninterrupted sequence of identical bits
                    print("Runs Test:")
                    logging.info("Runs Test:")
                    sts = prngtest.runs(bitRepresent)
                    print(sts)
                    resultPresenting(sts[1])
                    logging.info(sts)
                    log_timestamp()
                    print("\n")

                    # The focus of the test is the proportion of ones within M-bit blocks.
                    print("Block Frequency Test:")
                    logging.info("Block Frequency Test:")
                    blocksize = max(math.ceil(0.0125 * len(bitRepresent)), 4)
                    if blocksize >= 20:
                        sts = prngtest.blockfreq(bitRepresent, blocksize)
                        print(sts)
                        resultPresenting(sts[1])
                        logging.info(sts)
                        log_timestamp()
                        print("\n")
                    else:
                        print(
                            f"This number has too small blocksize for this test. Blocksize is {blocksize} needs to be 20 or more (bit length needs to be greater than 1700b)\n")

                    # The focus of this test is the peak heights in the Discrete Fourier Transform of the sequence.
                    # The purpose of this test is to detect periodic features (i.e., repetitive patterns that are near each other) in the tested sequence that would indicate a deviation from the assumption of randomness.
                    print("Discrete Fourier Transform (Spectral) Test")
                    logging.info("Discrete Fourier Transform (Spectral) Test:")
                    if len(bitRepresent) >= 1024:
                        sts = prngtest.spectral(bitRepresent)
                        print(sts)
                        resultPresenting(sts[1])
                        logging.info(sts)
                        log_timestamp()
                        print("\n")
                    else:
                        print("This number is too small for this test. Bit length needs to be greater than 1024b\n")

                    # Overlapping matches to template per block is compared to expected result
                    print("Overlapping Template Matching Test")
                    logging.info("Overlapping Template Matching Test")
                    if len(bitRepresent) >= 288:
                        sts = prngtest.otm(bitRepresent, None, None)
                        print(sts)
                        resultPresenting(sts[1])
                        logging.info(sts)
                        log_timestamp()
                        print("\n")
                    else:
                        print("This number is too small for this test. Bit length needs to be greater than 288b\n")
                    # The focus of this test is the number of bits between matching patterns.

                    print("Maurer’s “Universal Statistical” Test ")
                    logging.info("Maurer’s “Universal Statistical” Test ")
                    if len(bitRepresent) >= 400000:
                        sts = prngtest.universal(bitRepresent, None, None)
                        print(sts)
                        resultPresenting(sts[1])
                        logging.info(sts)
                        log_timestamp()
                        print("\n")
                    else:
                        print("This number is too small for this test. Bit length needs to be greater than 400000 b\n")

                    # The focus of this test is the length of a linear feedback shift register (LFSR).
                    print("Linear Complexity Test")
                    logging.info("Linear Complexity Test")
                    if len(bitRepresent) >= 1000000:
                        sts = prngtest.complexity(bitRepresent, None)
                        print(sts)
                        resultPresenting(sts[1])
                        logging.info(sts)
                        log_timestamp()
                        print("\n")
                    else:
                        print("This number is too small for this test. Bit length needs to be greater than 1mil b\n")

                    # The focus of this test is the frequency of all possible overlapping m-bit patterns across the entire sequence.
                    print("Serial Test")  # 2 OUTPUT
                    logging.info("Serial Test")
                    sts = prngtest.serial(bitRepresent, None)
                    print(sts)
                    resultPresenting(sts[0][1])
                    resultPresenting(sts[1][1])
                    logging.info(sts)
                    log_timestamp()
                    print("\n")

                    # The focus of this test is the maximal excursion (from zero) of the random walk defined by the cumulative sum of adjusted (-1, +1) digits in the sequence
                    print("Cumulative Sums (Cusum) Test")
                    logging.info("Cumulative Sums (Cusum) Test")
                    sts = prngtest.cumsum(bitRepresent, False)
                    print(sts)
                    resultPresenting(sts[1])
                    logging.info(sts)
                    log_timestamp()
                    print("\n")

                    print("Cumulative Sums (Cusum) Test - REVERSE")
                    logging.info("Cumulative Sums (Cusum) Test - REVERSE")
                    sts = prngtest.cumsum(bitRepresent, True)
                    print(sts)
                    resultPresenting(sts[1])
                    logging.info(sts)
                    log_timestamp()
                    print("\n")

                    print("Longest runs:")
                    logging.info("Longest runs:")
                    if len(bitRepresent) >= 128:
                        sts = prngtest.blockruns(bitRepresent)
                        print(sts)
                        resultPresenting(sts[1])
                        logging.info(sts)
                        log_timestamp()
                        print("\n")
                    else:
                        print("This number is too small for this test. Bit length needs to be greater than 128b\n")
                except:
                    print("Please generate or load number before testing!")

            elif chooseTest == 2:
                try:
                    print("You choose Diedharder tests\n")
                    print(f"Testing number {generatedNumber}\n")
                    bitRepresent = bin(generatedNumber)[2:]

                    print("Birthday Spacing Test")
                    logging.info("Birthday Spacing Test")
                    sts = dieharder.birthday_spacing_test(n_numbers=bit_length, range_interval=bit_length)
                    print(sts)
                    logging.info(sts)
                    log_timestamp()
                    print("\n")

                    print("Diehard Runs Test")
                    logging.info("Diehard Runs Test")
                    sts = dieharder.diehard_runs_test(bitRepresent)
                    print(sts)
                    logging.info(sts)
                    log_timestamp()
                    print("\n")

                    print("Binary Rank Test")
                    logging.info("Binary Rank Test")
                    rank = dieharder.binary_rank_test(generatedNumber, bit_length)
                    print(f"Rank: {rank}, less number is better")
                    logging.info(f"Rank: {rank}, less number is better")
                    log_timestamp()
                    print("\n")

                    print("Count Ones test")
                    logging.info("Count Ones test")
                    sts = dieharder.count_ones_test(bitRepresent)
                    print(sts)
                    logging.info(sts)
                    log_timestamp()
                    print("\n")
                except:
                    print("Please generate or load number before testing!")

            continue
        elif choose_an_action == 4:
            # Export cisla do souboru .txt, bude se muset otevrit okno File exploreru, tak jak kdyz se vybira soubor k narati treba na Moodle
            logging.info("Chosen action -> Export number to file")
            if generatedNumber == 0 or None:
                print("Number was not generated. If you want generate number press 1 or 5")
            else:
                number_to_encode = generatedNumber

                key = Fernet.generate_key()  # Generate a Fernet key
                cipher = Fernet(key)  # Initialize a Fernet cipher object with the key
                number_bytes = str(number_to_encode).encode()  # Convert number to bytes
                encrypted_number = cipher.encrypt(number_bytes)  # Encrypt the number

                with open("encrypted_number.txt", "wb") as f:  # Write the encrypted number to a file
                    f.write(encrypted_number)
                with open("fernet_key.txt", "wb") as f: # Save the key to a file
                    f.write(key)
                print("Encrypted number saved to file successfully.")

                with open("generated_numbers.txt", "a", encoding="utf-8") as f:
                    f.write("\n")
                    f.write(str(generatedNumber))
                print("Plain number saved to file successfully.")

                logging.info("{} writted into a file".format(generatedNumber))
                log_timestamp()
            continue
        elif choose_an_action == 5:
            logging.info("Chosen action -> \'Generate true random number\'")
            log_timestamp()

            print("Warning: For security reasons, it is recommended to use bit lengths of 288 or more. Otherwise the "
                  "number could not be True Random!")
            bit_length = int(input("Enter the desired bit length for the random number: "))

            counter = 0
            if (bit_length >= 288):
                # Generate a random number with the specified bit length
                # Duration in seconds
                duration = random.randint(10, 25) + random.random()
                print(f"Gathering mouse movement data for {duration} seconds...")
                mouse_data = mouse_movement_entropy(duration)
                print(time.time())
                while (True):
                    random_number = generate_random_number(bit_length, mouse_data)
                    bitRepresent = bin(random_number)[2:]
                    counter += 1
                    if numberControl(bitRepresent):
                        generatedNumber = random_number
                        print(f"Random number with {bit_length} bits: {str(random_number)[:200]}..")
                        logging.info(f"Random number with {bit_length} bits: {str(random_number)[:200]}..")
                        print(time.time())
                        break
                    elif counter > 200000:
                        generatedNumber = None
                        print(f"Not able to generate random number with {bit_length} bits")
                        logging.info(f"Not able to generate random number with {bit_length} bits")
                        break
            else:
                print("To make sure the number will be truly random,the bit length needs to be more then 288b")
                logging.info("To make sure the number will be truly random,the bit length needs to be more then 288b")
            continue
encryptLog()