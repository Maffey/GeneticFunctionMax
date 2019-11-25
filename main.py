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
import matplotlib.pyplot as plt


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

# TODO: optimize this shit
args_of_chromos = []  # Get values of chromos into a list
labels = []  # Needed for our sweet cake!
i = 0
for chromo in chromos:
    chromo.display()
    int_form = chromo.get_integer()
    args_of_chromos.append(int_form)
    labels.append(f"Ch{i}: {int_form}")
    i += 1

# Get values and its sum
fun_sum = fun.get_sum(args_of_chromos)
print("Sum of values: ", fun_sum)

# Plot a tasty pie chart
sizes = fun.get_values_list(args_of_chromos)

# Plot
plt.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=140)
plt.axis('equal')
plt.show()

print("Chromos count: ", Chromosome.chromosome_count)
