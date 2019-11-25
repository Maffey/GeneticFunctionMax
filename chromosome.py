import random


class Chromosome:
    """
    Class that carries all the information of a chromosome and operations needed to mutate, cross and age it.
    """
    chromosome_count = 0

    def __init__(self, binary: str) -> None:
        self.binary = binary
        Chromosome.chromosome_count += 1

    def display(self):
        print(f"||Chromosome|| id: {id(self)} --- bin: {self.binary} --- int: {int(self.binary, base=2)}")

    def get_integer(self):
        return int(self.binary, base=2)

    def swap_bit(self, index):
        if self.binary[index] == "0":
            # TODO: Make sure it concatenates string correctly.
            self.binary = self.binary[:index] + "1" + self.binary[index + 1:]
        else:
            self.binary = self.binary[:index] + "0" + self.binary[index + 1:]

    def mutate(self, mutation_parameter: float) -> None:
        """
        By a random chance, we decide whether or not we will initiate mutation.

        If we do, select random index of a bit for a chromosome.
        Since Python has a notation of "0b" at the beginning,
        we exclude it by selecting number from a range of <2, 6>
        """
        if random.random < mutation_parameter:
            self.swap_bit(random.randint(2, 6))

    def cross(self, chromosome, cross_parameter: float) -> None:
        """
        By a random chance, we decide whether or not we will initiate crossing.

        If we do, select random index of a bit for a chromosome.
        Since Python has a notation of "0b" at the beginning,
        we exclude it by selecting number from a range of <2, 5>

        The selected point will indicate the last bit of the part that will NOT be changed.
        Now, we swap the latter part of two chromosomes together.
        Notice that crossing is a method object, which means the it goes like this:
        chromosome_dad(chromosome_mom, cross_parameter)
        """
        if random.random < cross_parameter:
            # Select L parameter (bit index)
            cross_point = random.randint((2, 5))
            # Save the parts that won't be changed
            frozen_part_chromosome_one = self.binary[:cross_point + 1]
            frozen_part_chromosome_two = chromosome.binary[:cross_point + 1]
            # Save the parts to be crossed (swapped)
            crossing_part_chromosome_one = self.binary[cross_point + 1:]
            crossing_part_chromosome_two = chromosome.binary[cross_point + 1:]
            # Perform the crossing
            self.binary = frozen_part_chromosome_one + crossing_part_chromosome_two
            chromosome.binary = frozen_part_chromosome_two + crossing_part_chromosome_one
