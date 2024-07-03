# -*- coding: utf-8 -*-
# file  :  epiga.py
# author:  Daniel H. Stolfi
# date  :  2019-08-15
#
# Daniel H. Stolfi and Enrique Alba. Epigenetic algorithms: A New way of building GAs based on epigenetics.
# In: Information Sciences, vol. 424, Supplement C, pp. 250–272, 2018.
# doi> 10.1016/j.ins.2017.10.005

from .epigeneticpopulation import EpigeneticPopulation
from .operators.nucleosomegenerator import NucleosomeGenerator
from .operators.selectionoperator import SelectionOperator
from .operators.reproductionoperator import ReproductionOperator
from .operators.epigeneticoperator import EpigeneticOperator
from .operators.replacementoperator import ReplacementOperator
from .problems.problem import Problem


class EpiGA:
    """epiGenetic Algorithm."""

    def __init__(self, problem, n_individuals, n_cells, nucleosomes, selection, reproduction, epigenetic, replacement):
        """
        Constructor.

        :param Problem problem: the problem.
        :param int n_individuals: the number of individuals.
        :param int n_cells: the number of cells.
        :param NucleosomeGenerator nucleosomes: the nucleosome generator.
        :param SelectionOperator selection: the selection operator.
        :param ReproductionOperator reproduction: the reproduction operator.
        :param EpigeneticOperator epigenetic: the epigenetic operator.
        :param ReplacementOperator replacement: the replacement operator.
        """
        self.__problem = problem
        self.__n_individuals = n_individuals
        self.__n_cells = n_cells

        self.__nucleosomes = nucleosomes
        self.__selection = selection
        self.__reproduction = reproduction
        self.__epigenetic = epigenetic
        self.__replacement = replacement

    def run(self, n_evaluations, verbosity=0, solution_file=None, stat_file=None):
        """
        Begins the execution and returns the best fitness.

        :param int n_evaluations: the maximum number of evaluations.
        :param int verbosity: the verbosity level [0 -- 4].
        :param str solution_file: the solution file.
        :param str stat_file: the stats file (convergence data).
        :return: the best fitness.
        :rtype: float
        """
        f_stat = None
        if stat_file:
            f_stat = open(stat_file, "w")

        if verbosity > 1:
            print(self.__problem)
            print()

        pop = EpigeneticPopulation(self.__problem)
        pop.generate(self.__n_individuals, self.__n_cells)

        if verbosity > 3:
            self.__debug("Initialization", pop)

        gen = 1
        ev = self.__problem.evaluations
        while ev <= n_evaluations:

            if verbosity > 3:
                self.__debug("New generation", pop)

            temp = self.__selection.select(pop)
            self.__nucleosomes.generate(temp)

            if verbosity > 3:
                self.__debug("Selection and Nucleosomes", temp)

            self.__reproduction.reproduction(temp)

            if verbosity > 3:
                self.__debug("Reproduction", temp)

            self.__epigenetic.methylate(temp)
            temp.evaluate()

            if verbosity > 3:
                self.__debug("Methylation", temp)

            pop = self.__replacement.replace(temp, pop)
            ev = self.__problem.evaluations

            if verbosity > 3:
                self.__debug("Evaluation and Replacement", pop)

            if verbosity > 0 or f_stat:
                avg, best = pop.metrics()
                # print(pop)
                if verbosity > 0:
                    print("Generations: {:6d}  Evaluations: {:6d}  Average Fitness: {:12.3f}  Best Fitness: {:12.3f}".
                          format(gen, ev, avg, best))
                if f_stat:
                    f_stat.write("{}\t{}\t{}\t{}\n".format(gen, ev, avg, best))

            gen += 1

        best_cell = pop.best_individual().get_best_cell()
        if verbosity > 2:
            print()
            print(best_cell)
        if f_stat:
            f_stat.close()
        if solution_file:
            f_sol = open(solution_file, "w")
            for i in best_cell.solution:
                f_sol.write(str(i))
                f_sol.write(" ")
            f_sol.write("\n")
            f_sol.close()

        return pop.best_individual().get_best_cell().fitness

    @staticmethod
    def __debug(title, pop):
        print(title)
        print(pop)
