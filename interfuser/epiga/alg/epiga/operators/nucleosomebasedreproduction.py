# -*- coding: utf-8 -*-
# file  :  nucleosomebasedreproduction.py
# author:  Daniel H. Stolfi
# date  :  2019-08-15
#
# Daniel H. Stolfi and Enrique Alba. Epigenetic algorithms: A New way of building GAs based on epigenetics.
# In: Information Sciences, vol. 424, Supplement C, pp. 250–272, 2018.
# doi> 10.1016/j.ins.2017.10.005

from .reproductionoperator import ReproductionOperator


class NucleosomeBasedReproduction(ReproductionOperator):
    """NucleosomeBasedReproduction Operator."""

    def reproduction(self, pop):
        for i in range(0, pop.size, 2):
            c1 = pop.get(i).get_best_cell()
            c2 = pop.get(i + 1).get_best_cell()
            for j in range(len(c1.solution)):
                if not c1.nucleosomes[j] and not c2.nucleosomes[j]:
                    temp = c1.solution[j]
                    c1.solution[j] = c2.solution[j]
                    c2.solution[j] = temp
