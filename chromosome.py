import logging
import random


class Chromosome:
    """
    Class that carries all the information of a chromosome and operations needed to mutate, cross and age it.
    """
    chromosome_count = 0
    crossing_parameter = 0.4
    mutation_parameter = 0.05

    def __init__(self, binary: str) -> None:
        self.binary = binary
        Chromosome.chromosome_count += 1

    def display(self):
        print(f"||Chromosome|| id: {id(self)} --- bin: {self.binary} --- int: {self.get_integer()}")

    def display_length(self):
        return len(f"||Chromosome|| id: {id(self)} --- bin: {self.binary} --- int: {self.get_integer()}")

    def get_integer(self):
        return int(self.binary, base=2)

    def swap_bit(self, index):
        logging.debug(f"Chromosome to mutate: {self.binary}. Swapping bit at index {index}.")
        if self.binary[index] == "0":
            self.binary = self.binary[:index] + "1" + self.binary[index + 1:]
        else:
            self.binary = self.binary[:index] + "0" + self.binary[index + 1:]
        logging.debug(f"Mutation effect: {self.binary}")

    def mutate(self) -> None:
        """
        By a random chance, we decide whether or not we will initiate mutation.

        If we do, select random index of a bit for a chromosome in range <0, 4>
        """
        if random.random() < Chromosome.mutation_parameter:
            logging.debug(f"Mutation accepted for {self.binary} : {self.get_integer()}.")
            self.swap_bit(random.randint(0, 4))

    def cross(self, chromosome) -> None:
        """
        By a random chance, we decide whether or not we will initiate crossing.

        If we do, select random index of a bit for a chromosome in range <0, 3>

        The selected point will indicate the last bit of the part that will NOT be changed.
        Now, we swap the latter part of two chromosomes together.
        Notice that crossing is a method object, which means the it goes like this:
        chromosome_dad(chromosome_mom, cross_parameter)
        """
        if random.random() < Chromosome.crossing_parameter:
            logging.debug(f"Crossing accepted for {self.binary} : {self.get_integer()}.")
            # Select L parameter (bit index)
            cross_point = random.randint(0, 3)
            # Save the parts that won't be changed
            frozen_part_chromosome_one = self.binary[:cross_point + 1]
            frozen_part_chromosome_two = chromosome.binary[:cross_point + 1]
            # Save the parts to be crossed (swapped)
            crossing_part_chromosome_one = self.binary[cross_point + 1:]
            crossing_part_chromosome_two = chromosome.binary[cross_point + 1:]
            # Perform the crossing
            logging.debug(f"Crossing performed between A: {self.binary} and B: {chromosome.binary}."
                          f"Bits after '|' are the ones that were swapped.\n"
                          f"A: {frozen_part_chromosome_one} | {crossing_part_chromosome_two}\n"
                          f"B: {frozen_part_chromosome_two} | {crossing_part_chromosome_one}")
            self.binary = frozen_part_chromosome_one + crossing_part_chromosome_two
            chromosome.binary = frozen_part_chromosome_two + crossing_part_chromosome_one
