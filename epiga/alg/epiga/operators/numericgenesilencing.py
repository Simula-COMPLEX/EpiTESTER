# -*- coding: utf-8 -*-
# file  :  numericgenesilencing.py
# author:  Daniel H. Stolfi
# date  :  2019-08-15
#
# Daniel H. Stolfi and Enrique Alba. Epigenetic algorithms: A New way of building GAs based on epigenetics.
# In: Information Sciences, vol. 424, Supplement C, pp. 250–272, 2018.
# doi> 10.1016/j.ins.2017.10.005

import random
from .epigeneticoperator import EpigeneticOperator
import pandas as pd


class NumericGeneSilencing(EpigeneticOperator):
    """
    Numeric Gene Silencing Operator.
    Based on Chelouah et al., 2000.
    """

    def __init__(self, p_e, p_path):
        """
        Constructor.

        :param float p_e: the epigenetic probability
        """
        super().__init__(p_e)
        self.generation = 0
        self.path = p_path

        pd.DataFrame(list()).to_csv(self.path + 'silence.csv', mode='w', index=False, header=False)

    def methylate(self, pop):
        p = pop.problem
        env = p.environment
        for i in range(pop.size):
            count_c = 0
            for cell in pop.get(i).cells:
                silence = [False] * len(cell.solution)
                log = cell.solution
                r_p_l = []
                for j in range(len(cell.solution)):
                    r_p = random.random()
                    if cell.nucleosomes[j] and r_p < self._p_e:
                        v_min, v_max = p.limits(j)
                        # delta = p.delta(j)
                        delta = 0
                        r_e = random.random()
                        if r_e < env[j]:
                            delta = p.delta(j)
                            delta = -1 * delta
                            silence[j] = True
                        cell.solution[j] = max(min(cell.solution[j] + delta, v_max), v_min)
                    r_p_l.append(r_p)

                log = ['generation_{}_individual_{}_cell_{}'.format(self.generation, i, count_c)] + \
                      log + cell.nucleosomes + r_p_l + silence + cell.solution

                count_c += 1
                pd.DataFrame([log]).to_csv(self.path + 'silence.csv', mode='a', index=False, header=False)

        self.generation += 1
