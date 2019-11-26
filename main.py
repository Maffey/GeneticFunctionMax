#! python3
# GeneticFunctionMax - find the max value in the function, given the range of arguments (as chromosomes)

"""
standard binary notation    0bXXXXX
converting bin to int       int("binary_string", base=2)
converting int to bin       bin(number)
"""

import copy
import random

import matplotlib.pyplot as plt

from chromosome import Chromosome
from function import Function


# logging.basicConfig()

# This might stay out of class.
def initialize_chromosomes(number_of_chromosomes, start_range, end_range):
    list_of_chromosomes = []
    for chromosome in range(number_of_chromosomes):
        binary_notation = str(bin(random.randint(start_range, end_range)))
        binary_notation = binary_notation[2:].rjust(5, '0')
        list_of_chromosomes.append(Chromosome(str(binary_notation)))
    return list_of_chromosomes


# TODO: remve number_of_chromosomes, just stick with len(chromosomes)
def redistribute_chromosomes(chromosomes, chromosomes_values):
    return random.choices(population=chromosomes, weights=chromosomes_values, k=len(chromosomes))


def plot_piechart(values, labels):
    # Plot a tasty pie chart
    plt.pie(values, autopct='%1.1f%%', shadow=True, startangle=140)
    plt.legend(labels)
    plt.axis('equal')
    plt.tight_layout()
    plt.show()


def single_epoch(function, chromosomes):
    # Display all chromosomes, create a list of integer values of them and create labels list for pie chart.
    chromosomes_integers = []  # Get values of chromos into a list
    chromosome_labels = []  # ARBEIT MACHT FREI
    # print("=== CHROMOSOMES STARTER PACK ===")
    for i in range(len(chromosomes)):
        int_form = chromosomes[i].get_integer()
        chromosomes_integers.append(int_form)
        chromosome_labels.append(f"Ch{i}: {int_form}")  # PIE CHART
    # Get values and its sum
    function_values = function.get_values_list(chromosomes_integers)

    # Plot a tasty pie chart DEBUG
    # plot_piechart(fun_values, chromos_labels)

    redistributed_chromos = redistribute_chromosomes(chromosomes, function_values)

    # If there is any code deserving a Code of Shame trophy, it's this one below.
    # Make copies of chromosomes to allow for smooth crossing and mutations.
    temp_chromos = []
    for chromo in redistributed_chromos:
        chromo_copy = copy.copy(chromo)
        temp_chromos.append(chromo_copy)
    redistributed_chromos = temp_chromos

    # Cross chromosomes
    for i in range(0, len(redistributed_chromos), 2):
        redistributed_chromos[i].cross(redistributed_chromos[i + 1])

    # Mutate chromosomes
    for chromo in redistributed_chromos:
        chromo.mutate()

    return redistributed_chromos


# Initialize function
fun = Function(5, 1, 7, 12)  # Random values, test phase
fun.display()

# Initialize chromosomes
# TODO: PRINT THIS SHIT OUT AT THE BEGINNING
# TODO: number of chromosomes doesn't change anythin, figure out why
chromos = initialize_chromosomes(100, 1, 31)  # Default values, test phase

# MAIN LOOP  - WORK IN PROGRESS
for epoch in range(300):
    if epoch == 0:
        result = single_epoch(fun, chromos)
    result = single_epoch(fun, result)

print("=== FINISHED CHROMOSOMES ===")
for c in result:
    c.display()
