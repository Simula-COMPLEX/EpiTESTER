# -*- coding: utf-8 -*-
# file  :  epigeneticexception.py
# author:  Daniel H. Stolfi
# date  :  2019-08-15
#
# Daniel H. Stolfi and Enrique Alba. Epigenetic algorithms: A New way of building GAs based on epigenetics.
# In: Information Sciences, vol. 424, Supplement C, pp. 250–272, 2018.
# doi> 10.1016/j.ins.2017.10.005


class EpigeneticException(Exception):
    """The Epigenetic Exception Class."""

    def __init__(self, *args: object) -> None:
        super().__init__(*args)
