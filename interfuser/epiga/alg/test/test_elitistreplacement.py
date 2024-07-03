# -*- coding: utf-8 -*-
# Daniel H. Stolfi and Enrique Alba. Epigenetic algorithms: A New way of building GAs based on epigenetics.
# In: Information Sciences, vol. 424, Supplement C, pp. 250–272, 2018.
# doi> 10.1016/j.ins.2017.10.005
#
# author: Daniel H. Stolfi
#

import unittest

from OneMax import OneMaxProblem
from SphereFunction import SphereFunctionProblem
from epiga.epigeneticpopulation import EpigeneticPopulation
from epiga.operators.elitistreplacement import ElitistReplacement


class ElitistReplacementTestCase(unittest.TestCase):

    def setUp(self):
        self.p1 = OneMaxProblem(10)
        self.p2 = SphereFunctionProblem(10, 1)
        self.er1 = ElitistReplacement(True)
        self.er2 = ElitistReplacement(False)

    def test_replace(self):
        for i in range(1, 100, 10):
            for p in [self.p1, self.p2]:
                pop1 = EpigeneticPopulation(p)
                pop1.generate(i, 10)

                pop2 = EpigeneticPopulation(p)
                pop2.generate(i, 10)

                pop3 = self.er1.replace(pop1, pop2)
                assert (pop3.size == pop1.size)
                assert (pop3.size == pop2.size)
                for i3 in range(pop3.size):
                    found = False
                    for i12 in range(pop1.size):
                        if pop3.get(i3).get_best_cell().solution == pop1.get(i12).get_best_cell().solution or \
                                pop3.get(i3).get_best_cell().solution == pop2.get(i12).get_best_cell().solution:
                            found = True
                            break
                    assert found

                # sorted
                if p is self.p1:
                    for i3 in range(1, pop3.size):
                        assert (pop3.get(i3 - 1).get_best_fitness() >= pop3.get(i3).get_best_fitness())
                else:
                    for i3 in range(1, pop3.size):
                        assert (pop3.get(i3 - 1).get_best_fitness() <= pop3.get(i3).get_best_fitness())

                if p is self.p1 and i > 50:
                    pop3 = self.er2.replace(pop1, pop2)
                    assert (pop3.size == pop1.size)
                    assert (pop3.size == pop2.size)
                    found2 = False
                    for i3 in range(pop3.size):
                        found = False
                        for i12 in range(pop1.size):
                            if pop3.get(i3).get_best_cell().solution == pop1.get(i12).get_best_cell().solution or \
                                    pop3.get(i3).get_best_cell().solution == pop2.get(i12).get_best_cell().solution:
                                found = True
                                break
                        if not found:
                            found2 = True
                    assert found2


if __name__ == '__main__':
    unittest.main(verbosity=2)
