import numpy as np
import matplotlib.pyplot as plt


class Ant:
    """."""

    def __init__(self, threshold: int, x: int, y: int):
        """."""

        self._threshold = threshold
        self._x = x
        self._y = y
        if self.sum_digits(x) + self.sum_digits(y) > self._threshold:
            print(f'Муравей не может находится в этой точке: {x}:{y}')
            exit()

        self._move2start(x, y)
        self._max_distance = None

    @property
    def max_distance(self) -> list:
        """."""

        if self._max_distance:
            return self._max_distance

        counter = self._x
        while self.sum_nums_digits(counter, self._y) <= self._threshold:
            counter += 1

        counter -= 1
        max_distance = []
        while counter != 0:
            max_distance.append(counter % 10)
            counter //= 10

        self._max_distance = max_distance
        return self._max_distance

    @staticmethod
    def sum_digits(num: int) -> int:
        """."""

        s = 0
        while num:
            s += num % 10
            num //= 10
        return s

    def _move2start(self, x: int, y: int):
        """."""

        while True:
            cond_x = (x - 1 >= 0
                      and self.sum_nums_digits(x - 1, y) <= self._threshold)
            cond_y = (y - 1 >= 0
                      and self.sum_nums_digits(x, y - 1) <= self._threshold)
            if cond_x:
                x -= 1
            elif not cond_x and not cond_y:
                if x > y:
                    self._x = x
                    self._y = y
                else:
                    self._x = y
                    self._y = x
                return
            else:
                return self._move2start(y, x)

    def _get_f(self, index: int) -> int:
        """."""

        try:
            return self.max_distance[index]
        except IndexError:
            return 0

    def _calc_recursive(
            self,
            f_index: int,
            prev_x: int,
            prev_y: int,
            prev_shift: int
    ) -> int:
        """."""

        res = 0
        shift = self._get_f(f_index + 1) - (prev_x + prev_y) + prev_shift
        fraction = self._get_f(f_index) - self.sum_digits(self._x)
        for x in range(10):
            if x > fraction + shift:
                break
            for y in range(10):
                if x + y > fraction + shift:
                    break

                if f_index != 0:
                    res += self._calc_recursive(f_index - 1, x, y, shift)
                else:
                    res += 1

        return res

    def sum_nums_digits(self, num1: int, num2: int) -> int:
        """."""

        return self.sum_digits(num1) + self.sum_digits(num2)

    def create_image(self, dimensions: int):
        """."""

        matrix = np.empty((dimensions, dimensions), dtype=int)
        for i in range(dimensions):
            for j in range(dimensions):
                summ = self.sum_nums_digits(i, j)
                value = 1 if summ <= self._threshold else 0
                matrix[i, j] = value

        fig, ax = plt.subplots(figsize=(20, 20), dpi=200)
        ax.matshow(matrix)
        plt.savefig(f'images/{self._threshold}.png')

    def total_steps(self) -> int:
        """."""

        return self._calc_recursive(len(self.max_distance) - 1, 0, 0, 0)


if __name__ == "__main__":
    ant = Ant(25, 1000, 1000)
    print(ant.max_distance, '\n')
    print(ant.total_steps(), '\n')
