# -*- coding: utf-8 -*-
# Daniel H. Stolfi and Enrique Alba. Epigenetic algorithms: A New way of building GAs based on epigenetics.
# In: Information Sciences, vol. 424, Supplement C, pp. 250–272, 2018.
# doi> 10.1016/j.ins.2017.10.005
#
# author: Daniel H. Stolfi
#

import random
import unittest

from EggholderFunction import EggholderFunctionProblem
from OneMax import OneMaxProblem
from SphereFunction import SphereFunctionProblem
from TSP import TSP
from epiga.epiga import EpiGA
from epiga.operators.binarygenesilencing import BinaryGeneSilencing
from epiga.operators.binarytournamentselection import BinaryTournamentSelection
from epiga.operators.elitistreplacement import ElitistReplacement
from epiga.operators.nucleosomebasedreproduction import NucleosomeBasedReproduction
from epiga.operators.nucleosomegenerator import NucleosomeGenerator
from epiga.operators.numericgenesilencing import NumericGeneSilencing
from epiga.operators.permutationgenesilencing import PermutationGeneSilencing


class EpiGATestCase(unittest.TestCase):

    def setUp(self):
        random.seed(1)

    def test_onemax(self):
        L = 1000
        p = OneMaxProblem(L)
        alg = EpiGA(p, 20, 1, NucleosomeGenerator(3 / L, int(round(L / 8))), BinaryTournamentSelection(),
                    NucleosomeBasedReproduction(), BinaryGeneSilencing(8 / L), ElitistReplacement(duplicates=False))
        assert (alg.run(500, 0) == 644)

    def test_egg_holder_function(self):
        p = EggholderFunctionProblem(10)
        alg = EpiGA(p, 100, 1, NucleosomeGenerator(0.5, 0), BinaryTournamentSelection(),
                    NucleosomeBasedReproduction(), NumericGeneSilencing(0.5), ElitistReplacement(duplicates=False))
        assert (alg.run(3500, 0) == -959.579671903256)

    def test_sphere_function(self):
        L = 20
        EV = 500
        p = SphereFunctionProblem(L, int(round(EV / 1800)))
        alg = EpiGA(p, 100, 10, NucleosomeGenerator(1 / L, 2), BinaryTournamentSelection(),
                    NucleosomeBasedReproduction(), NumericGeneSilencing(2 / L), ElitistReplacement(duplicates=False))
        assert (alg.run(EV, 0) == 2457509.627718172)

    def test_tsp(self):
        M = [
            [0, 2, 4, 6, 7, 10],
            [2, 0, 6, 5, 4, 3],
            [4, 6, 0, 3, 5, 1],
            [6, 5, 3, 0, 7, 3],
            [7, 4, 5, 7, 0, 9],
            [10, 3, 1, 3, 9, 0],
        ]
        p = TSP(M)
        alg = EpiGA(p, 100, 1, NucleosomeGenerator(3 / len(M[0]), 2), BinaryTournamentSelection(),
                    NucleosomeBasedReproduction(), PermutationGeneSilencing(1 / len(M[0])),
                    ElitistReplacement(duplicates=False))
        assert (alg.run(100, 0) == 21)


if __name__ == '__main__':
    unittest.main(verbosity=2)
