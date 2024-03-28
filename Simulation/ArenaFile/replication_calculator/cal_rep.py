import numpy as np
from scipy.stats import t


def calculate_replications(average, half_width, n_initial, alpha, gamma_target):

    # Convert the target relative error to gamma prime

    gamma_prime_target = gamma_target / (1 + gamma_target)

    # Calculate the initial estimate of the population variance

    t_value_initial = t.ppf(1 - alpha / 2, n_initial - 1)

    estimated_variance = (half_width / t_value_initial) ** 2 * n_initial

    # Initialize the number of replications to check

    n_replications = n_initial

    # Calculate the relative error for the current number of replications

    relative_error = 1  # Initialize to a value greater than gamma_prime_target

    # Iterate over n_replications to find the minimum number needed for the desired relative error

    while relative_error > gamma_prime_target:

        n_replications += 1

        t_value = t.ppf(1 - alpha / 2, n_replications - 1)

        standard_error = np.sqrt(estimated_variance / n_replications)

        relative_error = (t_value * standard_error) / average

    return n_replications


# Inputs

average = 3.57  # Mean number of lost customers

half_width = 0.7  # Half-width of the confidence interval

n_initial = 10  # Initial number of replications

alpha = 0.05  # Significance level for the t-distribution

gamma_target = 0.20  # Desired relative error


# Calculate the number of replications needed

n_needed = calculate_replications(average, half_width, n_initial, alpha, gamma_target)


print(f"Number of replications needed: {n_needed}")
