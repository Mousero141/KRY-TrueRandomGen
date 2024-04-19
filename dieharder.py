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

    print("KS Statistic:", ks_statistic)
    print("P-value:", p_value)

    if p_value > 0.05:
        print(
            "We fail to reject the null hypothesis, this means that the random generator produces uniformly distributed spacings")
    else:
        print("The random generator is not random")