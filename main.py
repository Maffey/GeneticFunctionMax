#! python3
# GeneticFunctionMax - find the max value in the function, given the range of arguments (as chromosomes)

"""
standard binary notation    0bXXXXX
converting bin to int       int("binary_string", base=2)
converting int to bin       bin(number)
"""

import copy
import logging
import random

import matplotlib.pyplot as plt

from chromosome import Chromosome
from function import Function

logging.basicConfig(level=logging.INFO, format=' %(asctime)s - %(levelname)s: %(message)s')

# The range of chromosome arguments for our algorithm.
# Since the algorithm has no flexible change of arguments implemented it is not recommended to change those values.
ARGUMENTS_START_RANGE = 0
ARGUMENTS_END_RANGE = 31
FITNESS_CHANGE_PARAM = 0.02


def get_function_sum(function, chromosomes):
    chromosome_arguments = get_chromosome_arguments(chromosomes)
    return function.get_sum(chromosome_arguments)


def initialize_chromosomes(number_of_chromosomes, start_range, end_range):
    list_of_chromosomes = []
    for chromosome in range(number_of_chromosomes):
        binary_notation = str(bin(random.randint(start_range, end_range)))
        binary_notation = binary_notation[2:].rjust(5, '0')
        list_of_chromosomes.append(Chromosome(str(binary_notation)))
    return list_of_chromosomes


def redistribute_chromosomes(chromosomes, chromosome_values):
    offset = min(chromosome_values)
    return random.choices(population=chromosomes, weights=[w - offset + 1 for w in chromosome_values],
                          k=len(chromosomes))


def display_chromosomes(chromosomes, message="CHROMOSOMES"):
    print(message.upper().center(chromosomes[0].display_length(), "="))
    for chromosome in chromosomes:
        chromosome.display()


def get_chromosome_arguments(chromosomes):
    chromosome_arguments = []
    for chromosome in chromosomes:
        chromosome_arguments.append(chromosome.get_integer())
    return chromosome_arguments


def copy_chromosomes(chromosomes):
    copied_chromosomes = []
    for chromo in chromosomes:
        chromo_copy = copy.copy(chromo)
        copied_chromosomes.append(chromo_copy)
    return copied_chromosomes


def find_best_chromosome(function, chromosomes):
    current_best_chromosome = None
    current_max_value = float('-inf')
    for chromosome in chromosomes:
        chromosome_value = chromosome.get_value(function)
        if chromosome.get_value(function) > current_max_value:
            current_max_value = chromosome_value
            current_best_chromosome = chromosome
    return current_best_chromosome


def plot_pie_chart(values):
    """
    Function used for easier debbuging. Shows how chromosomes are distributed.
    Not needed on release, but might be used to show the first and last generation.
    :param values: values of f(x) where:
    - x is the argument (chromosome's data)
    - f(x) is a function that we evaluate with.
    :return: Shows a pie chart of the chromosome distribution.
    """
    labels = []
    for value in values:
        labels.append(f"Ch: {value}")
    plt.pie(values, autopct="%1.1f%%", shadow=True, startangle=140)
    plt.legend(labels)
    plt.axis('equal')
    plt.tight_layout()
    plt.show()


def plot_line_chart(values):
    plot_epochs = range(len(values))
    plt.plot(plot_epochs, values, "go-")
    plt.grid(color='b', linestyle='--', linewidth=1)
    plt.show()


def fitness_test(function, old_generation_chromosomes, new_generation_chromosomes):
    old_generation_integers = get_chromosome_arguments(old_generation_chromosomes)
    new_generation_integers = get_chromosome_arguments(new_generation_chromosomes)
    old_generation_sum = function.get_sum(old_generation_integers)
    new_generation_sum = function.get_sum(new_generation_integers)
    limit = (max(new_generation_sum, old_generation_sum, 0.0000000001))  # Last value ensures no division by zero
    return (new_generation_sum - old_generation_sum) / limit


def fitness_test_single(function, old_generation_chromosomes, new_generation_chromosomes):
    old_generation_max = max(chromosome.get_value(function) for chromosome in old_generation_chromosomes)
    new_generation_max = max(chromosome.get_value(function) for chromosome in new_generation_chromosomes)
    logging.debug(f"Max value of old generation: {old_generation_max} and the new: {new_generation_max}")
    limit = (max(new_generation_max, old_generation_max, 0.0000000001))  # Last value ensures no division by zero
    return (new_generation_max - old_generation_max) / limit


def single_epoch(function, chromosomes):
    # Create a list of integer values of chromosomes
    chromosomes_integers = get_chromosome_arguments(chromosomes)

    # Get values resulting from evaluating over function and sum of them
    function_values = function.get_values_list(chromosomes_integers)

    # Redistribute chromosomes by random selection (roulette)
    chromosomes = redistribute_chromosomes(chromosomes, function_values)

    # Make a pie chart of redistributed chromosomes. Not required
    # plot_pie_chart(function_values)  # DEBUG

    # Make copies of chromosomes to dereference them
    chromosomes = copy_chromosomes(chromosomes)

    # Cross pairs of chromosomes
    for i in range(0, len(chromosomes), 2):
        chromosomes[i].cross(chromosomes[i + 1])

    # Mutate chromosomes
    for chromosome in chromosomes:
        chromosome.mutate()

    return chromosomes


def user_input():
    print("Configuring parameters...")
    a = float(input("Enter 'a' parameter for the function: "))
    b = float(input("Enter 'b' parameter for the function: "))
    c = float(input("Enter 'c' parameter for the function: "))
    d = float(input("Enter 'd' parameter for the function: "))
    number_of_chromosomes = int(input("Enter desired number of chromosomes for each generation: "))
    Chromosome.crossing_parameter = float(input("Enter desired crossing parameter: "))
    Chromosome.mutation_parameter = float(input("Enter desired mutation parameter: "))
    return a, b, c, d, number_of_chromosomes


# Get user input
run_mode = input("If you want to run the script in normal mode, press ENTER. "
                 "If you want to enter default values, type 'd' and then press ENTER.")
if run_mode == "d":
    run_parameters = (-1, 1, 1, 1, 16)  # Default values
else:
    run_parameters = user_input()

# Initialize function
fun = Function(run_parameters[0], run_parameters[1], run_parameters[2], run_parameters[3])
fun.display()

# Initialize chromosomes
gen_chromosomes = initialize_chromosomes(run_parameters[4], ARGUMENTS_START_RANGE, ARGUMENTS_END_RANGE)

# Display the initialized chromosomes
display_chromosomes(gen_chromosomes, "initialized chromosomes")

"""
    === MAIN LOOP ===
"""
epochs = 0  # Counts how many generations (epochs) it takes to quit genetic algorithm
result = [Chromosome("00000")]  # Default value, a safe-check to avoid going through loop without initializing result
epoch_total_sums = []  # Tracks how the sum changes for each epoch
best_chromosomes = []  # Stores best chromosome for each epoch
fitness_count = 0  # Stores how many times fitness test stagnated

while True:
    if epochs == 0:
        result = single_epoch(fun, gen_chromosomes)
        epoch_total_sums.append(get_function_sum(fun, gen_chromosomes))

    # Store the previous generation for fitness tests
    old_result = result

    # Perform new evolution
    result = single_epoch(fun, result)

    # Save the total sum for the line graph
    epoch_total_sums.append(get_function_sum(fun, result))

    # Find the best chromosome in this epoch
    best_chromosomes.append(find_best_chromosome(fun, result))

    # Perform two fitness tests for total generation values and single-best chromosome
    fitness_value = fitness_test(fun, old_result, result)
    fitness_value_single = fitness_test_single(fun, old_result, result)

    logging.info(f"Fitness value for {epochs}. generation || full estimation: {fitness_value}, "
                 f"single element estimation: {fitness_value_single}")
    # If fitness of our generation is pretty bad and 10 iterations have already been done, quit the loop
    if (abs(fitness_value) < FITNESS_CHANGE_PARAM and abs(fitness_value_single) < FITNESS_CHANGE_PARAM) and epochs > 5:
        if fitness_count >= 5:
            logging.info(f"Fitness stagnates. Interrupting genetic evolution.\nTotal epochs: {epochs}")
            break
        else:
            fitness_count += 1
    else:
        fitness_count = 0

    # Saves the amount of iterations (epochs) we do
    epochs += 1

# Display the chromosomes we finished with
display_chromosomes(result, "finished chromosomes")

# Finds the best chromosome across all epochs
best_chromosome = find_best_chromosome(fun, best_chromosomes)
logging.debug(f"List of best chromosomes across epochs: {best_chromosomes}")
# Shows the information about the chromosome
logging.info(f"Best chromosome: {best_chromosome.binary} ({best_chromosome.get_integer()}) | "
             f"f(x) = {best_chromosome.get_value(fun)}")

# Plot chart of progress across epochs
logging.debug(f"All sums for each epoch: {epoch_total_sums}")
plot_line_chart(epoch_total_sums)
