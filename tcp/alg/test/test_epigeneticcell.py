# -*- coding: utf-8 -*-
# Daniel H. Stolfi and Enrique Alba. Epigenetic algorithms: A New way of building GAs based on epigenetics.
# In: Information Sciences, vol. 424, Supplement C, pp. 250–272, 2018.
# doi> 10.1016/j.ins.2017.10.005
#
# author: Daniel H. Stolfi
#

import unittest

from OneMax import OneMaxProblem
from epiga.epigeneticcell import EpigeneticCell


class EpigeneticCellTestCase(unittest.TestCase):

    def my_setUp(self, size):
        self.size = size
        self.p = OneMaxProblem(self.size)
        self.c1 = EpigeneticCell(self.p)
        self.c2 = EpigeneticCell(self.p)

    def test_init_1(self):
        for i in range(2, 50):
            with self.subTest(i=i):
                self.my_setUp(i)

                assert (self.c1.problem is self.p)
                assert (len(self.c1.solution) == self.size)
                assert (len(self.c1.nucleosomes) == self.size)

    def test_init_2(self):
        for i in range(2, 50):
            with self.subTest(i=i):
                self.my_setUp(i)

                v = [True] * self.size
                c3 = EpigeneticCell(self.p, solution=v)
                assert (c3.fitness == self.p.compute_fitness(v))
                n = [False] * self.p.size
                c4 = EpigeneticCell(self.p, solution=v, nucleosomes=n, fitness=-1)
                assert (c4.fitness == -1)
                assert (c4.solution == v)
                assert (c4.nucleosomes == n)
                assert (c4.solution is not v)
                assert (c4.nucleosomes is not n)

    def test_str(self):
        for i in range(2, 50):
            with self.subTest(i=i):
                self.my_setUp(i)

                assert (str(self.c1) != "")

    def test_is_better(self):
        for i in range(2, 50):
            with self.subTest(i=i):
                self.my_setUp(i)

                assert (self.c1.is_better(self.c2) == (self.c1.fitness >= self.c2.fitness))

    def test_generate_nucleosomes(self):
        for i in range(2, 50):
            with self.subTest(i=i):
                self.my_setUp(i)

                self.c1.generate_nucleosomes(1.0, 1)
                assert (all(self.c1.nucleosomes))
                self.c1.generate_nucleosomes(1.0, i)
                assert (all(self.c1.nucleosomes))
                self.c1.generate_nucleosomes(0.0, i)
                assert (not any(self.c1.nucleosomes))
                self.c1.generate_nucleosomes(1.0, 0)
                assert (any(self.c1.nucleosomes))

    def test_evaluations(self):
        self.my_setUp(10)

        assert (self.p.evaluations == 2)
        self.c1.evaluate()
        assert (self.p.evaluations == 3)
        self.c2.evaluate()
        assert (self.p.evaluations == 4)
        self.c2.evaluate()
        assert (self.p.evaluations == 5)

    def test_duplicate(self):
        for i in range(2, 50):
            with self.subTest(i=i):
                self.my_setUp(i)

                c = self.c1.duplicate()
                assert (isinstance(c, EpigeneticCell))
                assert (c.fitness == self.c1.fitness)
                assert (c.nucleosomes == self.c1.nucleosomes)
                assert (c.solution == self.c1.solution)
                assert (c.problem is self.c1.problem)
                assert (c.solution is not self.c1.solution)
                assert (c.nucleosomes is not self.c1.nucleosomes)

    def test_compute_fitness(self):
        for i in range(2, 50):
            with self.subTest(i=i):
                self.my_setUp(i)

                v = [True] * self.size
                c = EpigeneticCell(self.p, solution=v)
                assert (c.fitness == self.p.compute_fitness(v))


if __name__ == '__main__':
    unittest.main(verbosity=2)
