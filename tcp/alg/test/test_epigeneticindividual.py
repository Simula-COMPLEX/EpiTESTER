# -*- coding: utf-8 -*-
# Daniel H. Stolfi and Enrique Alba. Epigenetic algorithms: A New way of building GAs based on epigenetics.
# In: Information Sciences, vol. 424, Supplement C, pp. 250–272, 2018.
# doi> 10.1016/j.ins.2017.10.005
#
# author: Daniel H. Stolfi
#

import unittest

from OneMax import OneMaxProblem
from epiga.epigeneticindividual import EpigeneticIndividual
from epiga.epigeneticcell import EpigeneticCell


class EpigeneticIndividualTestCase(unittest.TestCase):

    def my_setUp(self, size):
        self.size = size
        self.p = OneMaxProblem(self.size)
        self.i1 = EpigeneticIndividual(self.p, 5)
        self.i2 = EpigeneticIndividual(self.p, 10)
        self.v1 = [True] * self.p.size
        self.v2 = [False] * self.p.size
        self.c1 = EpigeneticCell(self.p, solution=self.v1)
        self.c2 = EpigeneticCell(self.p, solution=self.v2)

    def test_init_1(self):
        for i in range(2, 50):
            with self.subTest(i=i):
                self.my_setUp(i)

                assert (len(self.i1.cells) == 5)
                self.i1 = EpigeneticIndividual(self.p, 1)
                assert (len(self.i1.cells) == 1)
                assert (len(self.i2.cells) == 10)

    def test_init_2(self):
        for i in range(2, 50):
            with self.subTest(i=i):
                self.my_setUp(i)

                i4 = EpigeneticIndividual(self.p, 2, [self.c1, self.c2])
                assert (i4.get_best_cell() is self.c1)
                assert (i4.get_best_cell().fitness == self.c1.fitness)
                assert (i4.get_best_cell().solution == self.v1)
                assert (i4.get_best_fitness() == self.p.compute_fitness(self.v1))

    def test_str(self):
        for i in range(2, 50):
            with self.subTest(i=i):
                self.my_setUp(i)

                assert (str(self.i1) != "")

    def test_best_cell(self):
        for i in range(2, 50):
            with self.subTest(i=i):
                self.my_setUp(i)

                f1 = 0
                for c1 in self.i1.cells:
                    if c1.fitness >= f1:
                        f1 = c1.fitness
                        b1 = c1
                f2 = 0
                for c2 in self.i2.cells:
                    if c2.fitness >= f2:
                        f2 = c2.fitness
                        b2 = c2
                assert (self.i1.get_best_cell() is b1)
                assert (self.i2.get_best_cell() is b2)
                assert (self.i1.is_better(self.i2) == (f1 >= f2))

    def test_evaluations(self):
        self.my_setUp(10)

        assert (self.p.evaluations == 17)
        self.i1.evaluate()
        assert (self.p.evaluations == 22)
        self.i2.evaluate()
        assert (self.p.evaluations == 32)

    def test_duplicate(self):
        for i in range(2, 50):
            with self.subTest(i=i):
                self.my_setUp(i)

                i3 = self.i2.duplicate()
                assert (isinstance(i3, EpigeneticIndividual))
                assert (i3 is not self.i2)

                for j in range(len(self.i2.cells)):
                    assert (i3.cells[j] is not self.i2.cells[j])
                    assert (i3.cells[j].problem is self.i2.cells[j].problem)
                    assert (i3.cells[j].solution == self.i2.cells[j].solution)
                    assert (i3.cells[j].solution is not self.i2.cells[j].solution)
                    assert (i3.cells[j].nucleosomes == self.i2.cells[j].nucleosomes)
                    assert (i3.cells[j].nucleosomes is not self.i2.cells[j].nucleosomes)
                    assert (i3.cells[j].fitness == self.i2.cells[j].fitness)

    def test_replicate(self):
        for i in range(2, 50):
            with self.subTest(i=i):
                self.my_setUp(i)

                i1 = EpigeneticIndividual(self.p, 2, [self.c1, self.c2])
                i2 = i1.replicate()
                assert (i2.get_best_cell() is not self.c1)
                assert (i2.get_best_cell() is not self.c2)
                assert (i2.cells[0] is not i2.cells[1])
                assert (i2.cells[0].solution is not i2.cells[1].solution)
                assert (i2.cells[0].solution == i2.cells[1].solution)


if __name__ == '__main__':
    unittest.main(verbosity=2)
