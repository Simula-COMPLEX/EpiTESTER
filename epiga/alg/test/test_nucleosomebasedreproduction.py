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
from epiga.epigeneticcell import EpigeneticCell
from epiga.epigeneticindividual import EpigeneticIndividual
from epiga.epigeneticpopulation import EpigeneticPopulation
from epiga.operators.nucleosomebasedreproduction import NucleosomeBasedReproduction


class NucleosomeBasedReproductionTestCase(unittest.TestCase):

    def setUp(self):
        self.p1 = OneMaxProblem(10)
        self.p2 = SphereFunctionProblem(10, 1)
        self.v1 = [True] * 10
        self.v2 = [False] * 10
        self.v3 = [True, True, True, True, True, False, False, False, False, False]
        self.v4 = [False, False, False, False, False, True, True, True, True, True]

    def test_binary_1(self):
        c1 = EpigeneticCell(self.p1, solution=self.v1, nucleosomes=self.v2)
        c2 = EpigeneticCell(self.p1, solution=self.v2, nucleosomes=self.v2)

        pop = EpigeneticPopulation(self.p1)
        i1 = EpigeneticIndividual(self.p1, 1, [c1])
        i2 = EpigeneticIndividual(self.p1, 1, [c2])
        pop.add(i1)
        pop.add(i2)

        nbr = NucleosomeBasedReproduction()
        nbr.reproduction(pop)

        assert (i1.get_best_cell().solution == self.v2)
        assert (i2.get_best_cell().solution == self.v1)

    def test_binary_2(self):
        c1 = EpigeneticCell(self.p1, solution=self.v1, nucleosomes=self.v1)
        c2 = EpigeneticCell(self.p1, solution=self.v2, nucleosomes=self.v1)

        pop = EpigeneticPopulation(self.p1)
        i1 = EpigeneticIndividual(self.p1, 1, [c1])
        i2 = EpigeneticIndividual(self.p1, 1, [c2])
        pop.add(i1)
        pop.add(i2)

        nbr = NucleosomeBasedReproduction()
        nbr.reproduction(pop)

        assert (i1.get_best_cell().solution == self.v1)
        assert (i2.get_best_cell().solution == self.v2)

    def test_binary_3(self):
        c1 = EpigeneticCell(self.p1, solution=self.v1, nucleosomes=self.v3)
        c2 = EpigeneticCell(self.p1, solution=self.v2, nucleosomes=self.v4)

        pop = EpigeneticPopulation(self.p1)
        i1 = EpigeneticIndividual(self.p1, 1, [c1])
        i2 = EpigeneticIndividual(self.p1, 1, [c2])
        pop.add(i1)
        pop.add(i2)

        nbr = NucleosomeBasedReproduction()
        nbr.reproduction(pop)

        assert (i1.get_best_cell().solution == self.v1)
        assert (i2.get_best_cell().solution == self.v2)

    def test_binary_4(self):
        c1 = EpigeneticCell(self.p1, solution=self.v1, nucleosomes=self.v3)
        c2 = EpigeneticCell(self.p1, solution=self.v2, nucleosomes=self.v3)

        pop = EpigeneticPopulation(self.p1)
        i1 = EpigeneticIndividual(self.p1, 1, [c1])
        i2 = EpigeneticIndividual(self.p1, 1, [c2])
        pop.add(i1)
        pop.add(i2)

        nbr = NucleosomeBasedReproduction()
        nbr.reproduction(pop)

        assert (i1.get_best_cell().solution == self.v3)
        assert (i2.get_best_cell().solution == self.v4)

    def test_binary_5(self):
        c1 = EpigeneticCell(self.p1, solution=self.v1, nucleosomes=self.v4)
        c2 = EpigeneticCell(self.p1, solution=self.v2, nucleosomes=self.v4)

        pop = EpigeneticPopulation(self.p1)
        i1 = EpigeneticIndividual(self.p1, 1, [c1])
        i2 = EpigeneticIndividual(self.p1, 1, [c2])
        pop.add(i1)
        pop.add(i2)

        nbr = NucleosomeBasedReproduction()
        nbr.reproduction(pop)

        assert (i1.get_best_cell().solution == self.v4)
        assert (i2.get_best_cell().solution == self.v3)

    def test_float_1(self):
        c1 = EpigeneticCell(self.p2, nucleosomes=self.v2)
        c2 = EpigeneticCell(self.p2, nucleosomes=self.v2)

        vf1 = c1.solution[:]
        vf2 = c2.solution[:]

        pop = EpigeneticPopulation(self.p2)
        i1 = EpigeneticIndividual(self.p2, 1, [c1])
        i2 = EpigeneticIndividual(self.p2, 1, [c2])
        pop.add(i1)
        pop.add(i2)

        nbr = NucleosomeBasedReproduction()
        nbr.reproduction(pop)

        assert (i1.get_best_cell().solution == vf2)
        assert (i2.get_best_cell().solution == vf1)

    def test_float_2(self):
        vf1 = EpigeneticCell(self.p2, nucleosomes=self.v2).solution[:]
        vf2 = EpigeneticCell(self.p2, nucleosomes=self.v2).solution[:]

        c1 = EpigeneticCell(self.p2, solution=vf1, nucleosomes=self.v1)
        c2 = EpigeneticCell(self.p2, solution=vf2, nucleosomes=self.v1)

        pop = EpigeneticPopulation(self.p2)
        i1 = EpigeneticIndividual(self.p2, 1, [c1])
        i2 = EpigeneticIndividual(self.p2, 1, [c2])
        pop.add(i1)
        pop.add(i2)

        nbr = NucleosomeBasedReproduction()
        nbr.reproduction(pop)

        assert (i1.get_best_cell().solution == vf1)
        assert (i2.get_best_cell().solution == vf2)

    def test_float_3(self):
        vf1 = EpigeneticCell(self.p2, nucleosomes=self.v2).solution[:]
        vf2 = EpigeneticCell(self.p2, nucleosomes=self.v2).solution[:]

        c1 = EpigeneticCell(self.p2, solution=vf1, nucleosomes=self.v3)
        c2 = EpigeneticCell(self.p2, solution=vf2, nucleosomes=self.v4)

        pop = EpigeneticPopulation(self.p2)
        i1 = EpigeneticIndividual(self.p2, 1, [c1])
        i2 = EpigeneticIndividual(self.p2, 1, [c2])
        pop.add(i1)
        pop.add(i2)

        nbr = NucleosomeBasedReproduction()
        nbr.reproduction(pop)

        assert (i1.get_best_cell().solution == vf1)
        assert (i2.get_best_cell().solution == vf2)


if __name__ == '__main__':
    unittest.main(verbosity=2)
