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


def redistribute_chromosomes(chromosomes, chromosomes_values):
    # TODO: It's possible we need to offset weight so it's not negative in case of negative values.
    return random.choices(population=chromosomes, weights=chromosomes_values, k=len(chromosomes))


def display_chromosomes(chromosomes):
    for chromosome in chromosomes:
        chromosome.display()


# TODO: use it in the single epoch
def get_chromosome_arguments(chromosomes):
    chromosome_arguments = []
    for chromosome in chromosomes:
        chromosome_arguments.append(chromosome.get_integer())
    return chromosome_arguments


# TODO: add a function to get function sum values

def plot_piechart(values, labels):
    # Plot a tasty pie chart
    plt.pie(values, autopct='%1.1f%%', shadow=True, startangle=140)
    plt.legend(labels)
    plt.axis('equal')
    plt.tight_layout()
    plt.show()


def fitness_test(function, old_generation_chromosomes, new_generation_chromosomes):
    # TODO: implement dealing with negative numbers
    old_generation_integers = get_chromosome_arguments(old_generation_chromosomes)
    new_generation_integers = get_chromosome_arguments(new_generation_chromosomes)
    old_generation_sum = function.get_sum(old_generation_integers)
    new_generation_sum = function.get_sum(new_generation_integers)
    sum_difference = new_generation_sum - old_generation_sum
    limit = (max(new_generation_sum, old_generation_sum))
    # TODO: ensure good fitness test
    return sum_difference / limit


def single_epoch(function, chromosomes):
    # Display all chromosomes, create a list of integer values of them and create labels list for pie chart.
    chromosomes_integers = []  # Get values of chromos into a list
    chromosome_labels = []  # PIE CHART
    # print("=== CHROMOSOMES STARTER PACK ===")
    for i in range(len(chromosomes)):
        int_form = chromosomes[i].get_integer()
        chromosomes_integers.append(int_form)
        chromosome_labels.append(f"Ch{i}: {int_form}")  # PIE CHART
    # Get values and its sum
    function_values = function.get_values_list(chromosomes_integers)

    # Plot a tasty pie chart DEBUG
    # plot_piechart(fun_values, chromos_labels)

    chromosomes = redistribute_chromosomes(chromosomes, function_values)

    # If there is any code deserving a Code of Shame trophy, it's this one below.
    # Make copies of chromosomes to allow for smooth crossing and mutations.
    temp_chromos = []
    for chromo in chromosomes:
        chromo_copy = copy.copy(chromo)
        temp_chromos.append(chromo_copy)
    chromosomes = temp_chromos

    # Cross chromosomes
    for i in range(0, len(chromosomes), 2):
        chromosomes[i].cross(chromosomes[i + 1])

    # Mutate chromosomes
    for chromo in chromosomes:
        chromo.mutate()

    return chromosomes


# Initialize function
fun = Function(-0.5, 2, 1, 12)  # Random values, test phase
fun.display()

# Initialize chromosomes
chromos = initialize_chromosomes(32, 1, 31)  # Default values, test phase
print("=== STARTING CHROMOSOMES ===")
display_chromosomes(chromos)

# MAIN LOOP  - WORK IN PROGRESS
epoch = 0
result = [Chromosome("00000")]
while True:
    if epoch == 0:

        result = single_epoch(fun, chromos)

    old_result = result
    result = single_epoch(fun, result)
    fitness_value = fitness_test(fun, old_result, result)
    logging.info(f"Fitness value for {epoch}. generation: {fitness_value}")
    if abs(fitness_value) < 0.01:
        logging.info(f"Fitness stagnates. Interrupting genetic evolution.\nTotal epochs: {epoch}")
        break
    epoch += 1

print("=== FINISHED CHROMOSOMES ===")
display_chromosomes(result)

# TODO: change fitness function to test the difference between the HIGHEST VALUE chromosome between epochs.
#  Might be the key idea.

# TODO: This algorithm hates negative values. Solve it out.
