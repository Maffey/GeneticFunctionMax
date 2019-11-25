#! python3
# GeneticFunctionMax - find the max value in the function, given the range of arguments (as chromosomes)

"""
standard binary notation    0bXXXXX
converting bin to int       int("binary_string", base=2)
converting int to bin       bin(number)
"""

import random
from chromosome import Chromosome
from function import Function


# This might stay out of class.
def initialize_chromosomes(number_of_chromosomes, start_range, end_range):
    list_of_chromosomes = []
    for chromosome in range(number_of_chromosomes):
        # TODO: Make sure all numbers have the same bitwise length without "0b" part.
        binary_notation = bin(random.randint(start_range, end_range))
        list_of_chromosomes.append(Chromosome(str(binary_notation)))
    return list_of_chromosomes


# TODO: Create redistribution function.
def redistribute_chromosomes(chromosomes):
    pass


# Initialize function
fun = Function(5, 1, 7, 12)
fun.display()


# Initialize chromosomes
chromos = initialize_chromosomes(6, 1, 31)  # Default values, test phase
for chromo in chromos:
    chromo.display()

# Get values of chromos into a list
values_of_chromos = []
for chromo in chromos:
    values_of_chromos.append(chromo.get_integer())



# Tests
print("=== TESTS ===")

# Get sum of values.
print("Sum of values: ", fun.get_sum(values_of_chromos))

chromos[0].display()
chromos[0].swap_bit(3)
chromos[0].display()

print("Chromos count: ", Chromosome.chromosome_count)
