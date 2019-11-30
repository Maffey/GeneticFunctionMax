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

logging.basicConfig(level=logging.DEBUG, format=' %(asctime)s - %(levelname)s: %(message)s')


# This might stay out of class.
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


def display_chromosomes(chromosomes):
    for chromosome in chromosomes:
        chromosome.display()


# TODO: use it in the single epoch
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


# TODO: add a function to get function sum values

def plot_pie_chart(values):
    """
    Function used for easier debbuing. Shows how chromosomes are distributed.
    Not needed on release, but might be used to show the first and last generation.
    :param values: values of f(x) where:
    - x is the argument (chromosome's data)
    - f(x) is a function that we evaluate with.
    :return: Shows a pie chart of the chromosome distribution.
    """
    labels = []
    for value in values:
        labels.append(f"Ch: {value}")
    plt.pie(values, autopct='%1.1f%%', shadow=True, startangle=140)
    plt.legend(labels)
    plt.axis('equal')
    plt.tight_layout()
    plt.show()


def fitness_test(function, old_generation_chromosomes, new_generation_chromosomes):
    old_generation_integers = get_chromosome_arguments(old_generation_chromosomes)
    new_generation_integers = get_chromosome_arguments(new_generation_chromosomes)
    old_generation_sum = function.get_sum(old_generation_integers)
    new_generation_sum = function.get_sum(new_generation_integers)
    sum_difference = new_generation_sum - old_generation_sum
    limit = (max(new_generation_sum, old_generation_sum, 0.0000000001))  # Last value ensures no division by zero
    return sum_difference / limit


# TODO: implement this for further improvements
def fitness_test_single(function, old_generation_chromosomes, new_generation_chromosomes):
    pass


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


# Initialize function
fun = Function(-5, 2, 1, 3)  # Random values, test phase
fun.display()

# Initialize chromosomes
gen_chromosomes = initialize_chromosomes(16, 1, 31)  # Default values, test phase
print("=== STARTING CHROMOSOMES ===")
display_chromosomes(gen_chromosomes)

"""
    === MAIN LOOP ===
"""
epoch = 0  # Counts how many generations (epochs) it takes.
result = [Chromosome("00000")]  # Default value, a safe-check to avoid going through loop without initializing result.
while True:
    if epoch == 0:
        result = single_epoch(fun, gen_chromosomes)

    old_result = result
    result = single_epoch(fun, result)
    fitness_value = fitness_test(fun, old_result, result)
    logging.info(f"Fitness value for {epoch}. generation: {fitness_value}")
    if abs(fitness_value) < 0.02:
        logging.info(f"Fitness stagnates. Interrupting genetic evolution.\nTotal epochs: {epoch}")
        break
    epoch += 1

print("=== FINISHED CHROMOSOMES ===")
display_chromosomes(result)

# TODO: change fitness function to test the difference between THE BEST chromosome between epochs. Not required.
