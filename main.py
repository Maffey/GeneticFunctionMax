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


# This might stay out of class.
def initialize_chromosomes(number_of_chromosomes, start_range, end_range):
    list_of_chromosomes = []
    for chromosome in range(number_of_chromosomes):
        binary_notation = str(bin(random.randint(start_range, end_range)))
        binary_notation = binary_notation[2:].rjust(5, '0')
        list_of_chromosomes.append(Chromosome(str(binary_notation)))
    return list_of_chromosomes


# TODO: recreate redistribution function.
def redistribute_chromosomes(chromosomes, chromosomes_values, number_of_chromosomes):
    return random.choices(population=chromosomes, weights=chromosomes_values, k=number_of_chromosomes)


# Initialize function
fun = Function(5, 1, 7, 12)
fun.display()

# Initialize chromosomes
chromos = initialize_chromosomes(6, 1, 31)  # Default values, test phase

# Display all chromosomes, create a list of integer values of them and create labels list for pie chart.
args_of_chromos = []  # Get values of chromos into a list
labels = []  # Needed for our sweet cake!
i = 0  # I'm too focused on the algorithm itself to put it more nicely, figure it out later.
for chromo in chromos:
    chromo.display()
    int_form = chromo.get_integer()
    args_of_chromos.append(int_form)
    labels.append(f"Ch{i}: {int_form}")
    i += 1

print("Chromos count: ", Chromosome.chromosome_count)

# TODO: Put all that shit into functions. and a loop.
# Get values and its sum
fun_values = fun.get_values_list(args_of_chromos)
fun_sum = fun.get_sum(args_of_chromos)
print("Sum of values: ", fun_sum)

# Plot a tasty pie chart
plt.pie(fun_values, autopct='%1.1f%%', shadow=True, startangle=140)
plt.legend(labels)
plt.axis('equal')
plt.tight_layout()
plt.show()

redistributed_chromos = redistribute_chromosomes(chromos, fun_values, 6)

# If there is any code deserving a Code of Shame trophy, it's this one below.
# Make copies of chromosomes to allow for smooth crossing and mutations.
temp_chromos = []
for chromo in redistributed_chromos:
    chromo_copy = copy.copy(chromo)
    temp_chromos.append(chromo_copy)
redistributed_chromos = temp_chromos

# Redistribution: OK
print("REDISTRIBUTED CHROMOSOMES")
for chromo in redistributed_chromos:
    chromo.display()

# Cross chromosomes

for i in range(0, len(redistributed_chromos), 2):
    redistributed_chromos[i].cross(redistributed_chromos[i + 1])

print("CROSSED CHROMOSOMES")
for chromo in redistributed_chromos:
    chromo.display()

# Mutate chromosomes
print("MUTATED CHROMOSOMES")
for chromo in redistributed_chromos:
    chromo.mutate()
    chromo.display()
