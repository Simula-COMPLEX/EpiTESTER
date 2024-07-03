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
from SphereFunction import SphereFunctionProblem
from epiga.epigeneticpopulation import EpigeneticPopulation
from epiga.operators.binarytournamentselection import BinaryTournamentSelection


class BinaryTournamentTestCase(unittest.TestCase):

    def setUp(self):
        self.p1 = OneMaxProblem(10)
        self.p2 = SphereFunctionProblem(10, 1)
        self.bt = BinaryTournamentSelection()

    def test_select(self):
        for i in range(1, 100):
            for p in [self.p1, self.p2]:
                n_c = random.randint(1, 10)
                pop1 = EpigeneticPopulation(p)
                pop1.generate(i, n_c)

                pop2 = self.bt.select(pop1)
                assert (pop2.size == pop1.size)
                assert (pop2.problem == pop1.problem)

                for ind2 in range(pop2.size):
                    found = False
                    for ind1 in range(pop1.size):
                        if ind2 is ind1:
                            found = True
                            break
                    assert found


if __name__ == '__main__':
    unittest.main(verbosity=2)
