# -*- coding: utf-8 -*-
# Daniel H. Stolfi and Enrique Alba. Epigenetic algorithms: A New way of building GAs based on epigenetics.
# In: Information Sciences, vol. 424, Supplement C, pp. 250–272, 2018.
# doi> 10.1016/j.ins.2017.10.005
#
# author: Daniel H. Stolfi
#

import random
import unittest

from OneMax import OneMaxProblem
from epiga.epigeneticindividual import EpigeneticIndividual
from epiga.epigeneticcell import EpigeneticCell
from epiga.epigeneticpopulation import EpigeneticPopulation


class EpigeneticPopulationTestCase(unittest.TestCase):

    def my_setUp(self, size):
        self.size = size
        self.n_cells = random.randint(1, 10)
        self.p = OneMaxProblem(10)
        self.pop = EpigeneticPopulation(self.p)
        self.pop.generate(self.size, self.n_cells)

    def test_init(self):
        for i in range(2, 50):
            with self.subTest(i=i):
                self.my_setUp(i)

                assert (self.pop.problem is self.p)
                assert (self.pop.size == i)

                for j in range(self.pop.size):
                    ind = self.pop.get(j)
                    assert (len(ind.cells) == self.n_cells)

    def test_str(self):
        for i in range(2, 50):
            with self.subTest(i=i):
                self.my_setUp(i)

                assert (str(self.pop) != "")

    def test_evaluations(self):
        for i in range(2, 50):
            with self.subTest(i=i):
                self.my_setUp(i)

                n_ev = self.n_cells * self.size
                assert (self.p.evaluations == n_ev)

                self.pop.evaluate()
                n_ev += i * self.n_cells
                assert (self.p.evaluations == n_ev)

                pop1 = EpigeneticPopulation(self.p)
                pop1.generate(10, 1)
                n_ev += 10
                assert (self.p.evaluations == n_ev)

                pop1.evaluate()
                n_ev += 10
                assert (self.p.evaluations == n_ev)

    def test_add(self):
        for i in range(2, 50):
            with self.subTest(i=i):
                self.my_setUp(i)

                i = EpigeneticIndividual(self.p, 2)
                self.pop.add(i)
                assert (self.pop.get(self.pop.size - 1) is i)

    def test_metrics(self):
        for i in range(2, 50):
            with self.subTest(i=i):
                self.my_setUp(i)

                v1 = [True] * self.p.size
                v2 = [False] * self.p.size
                c1 = EpigeneticCell(self.p, solution=v1)
                c2 = EpigeneticCell(self.p, solution=v2)
                i1 = EpigeneticIndividual(self.p, 1, [c1])
                i2 = EpigeneticIndividual(self.p, 1, [c2])
                pop1 = EpigeneticPopulation(self.p)
                pop1.add(i1)
                pop1.add(i2)
                avg_f, max_f = pop1.metrics()
                assert (avg_f == self.p.size / 2)
                assert (max_f == self.p.size)


if __name__ == '__main__':
    unittest.main(verbosity=2)
