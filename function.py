class Function:
    """
    Class that carries all information of fourth degree polynomial
    """

    def __init__(self, a: float, b: float, c: float, d: float) -> None:
        """
        Generator for function. Creates a function based on standard parameters for fourth degree polynomial.
        :param a: coefficient of x to the power of three.
        :param b: coefficient of x to the power of two.
        :param c: coefficient of x to the power of one.
        :param d: coefficient of x to the power of zero.
        """
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def display(self):
        print(f"{self.a}x^3 + {self.b}x^2 + {self.c}x + {self.d}")

    def get_value(self, x):
        return self.a * (x ** 3) + self.b * (x ** 2) + self.c * x + self.d

    # TODO: try to optimize that.
    def get_values_list(self, list_of_x):
        list_of_values = []
        for x in list_of_x:
            list_of_values.append(self.get_value(x))
        return list_of_values

    def get_sum(self, list_of_x):
        return sum(self.get_values_list(list_of_x))
