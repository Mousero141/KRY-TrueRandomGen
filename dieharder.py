import numpy
from scipy.stats import expon, kstest

def birthday_spacing_test(n_numbers: int, range_interval: float):

    # Generate random uniform point
    random_points = numpy.random.uniform(low=0.0, high=range_interval, size=n_numbers)

    # Calculate the spacings between the random points
    random_points = numpy.sort(random_points)
    spacings = numpy.diff(random_points)

    # Conduct Goodness-of-Fit Test (Kolmogorov-Smirnov Test in this case)
    # Fit the spacings to an exponential distribution to get the parameters
    params = expon.fit(spacings)

    # Conduct the Kolmogorov-Smirnov test to compare the empirical and theoretical distributions
    ks_statistic, p_value = kstest(spacings, 'expon', args=params)


    if p_value > 0.05:
        print(f"P-value is: {p_value}. Number is consider as RANDOM")
    else:
        print(f"P-value is: {p_value}. Number is NOT RANDOM")


def diehard_runs_test(data):
    runs = []
    current_run = 1
    for i in range(1, len(data)):
        if data[i] == data[i - 1]:
            current_run += 1
        else:
            runs.append(current_run)
            current_run = 1
    runs.append(current_run)

    n = len(data)
    expected_mean = (2 * n - 1) / 3
    expected_variance = (16 * n - 29) / 90
    pvalue = (sum(runs) - expected_mean) / (expected_variance ** 0.5)

    # Two-tailed test, assuming normal distribution
    # You can adjust the significance level (alpha) as needed
    alpha = 0.05
    critical_value = 1.96  # For alpha = 0.05

    if abs(pvalue) > critical_value:
        return print(f"P-value is: {pvalue}. Number is NOT RANDOM")
    else:
        return print(f"P-value is: {pvalue}. Number is consider as RANDOM")


def binary_rank_test(random_number, bit_length):
    # Convert the random number to its binary representation
    binary_string = bin(random_number)[2:].zfill(bit_length)

    # Count the consecutive blocks of 1s and 0s in the binary string
    ones_blocks = [len(block) for block in binary_string.split('0') if block]  # Lengths of consecutive blocks of 1s
    zeros_blocks = [len(block) for block in binary_string.split('1') if block]  # Lengths of consecutive blocks of 0s
    rank = max(max(ones_blocks, default=0), max(zeros_blocks, default=0))

    #Larger rank means worse randomness
    return rank


def count_ones_test(data):
    ones_count = data.count('1')
    n = len(data)
    expected_ones = n / 2
    variance = n / 4
    p_value = (ones_count - expected_ones) / (variance ** 0.5)

    # Two-tailed test, assuming normal distribution
    alpha = 0.05
    critical_value = 1.96  # For alpha = 0.05

    if abs(p_value) > critical_value:
        return print(f"P-value is: {p_value}. Number is NOT RANDOM")
    else:
        return print(f"P-value is: {p_value}. Number is consider as RANDOM")
