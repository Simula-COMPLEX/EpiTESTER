Epigenetic Algorithm (epiGA)
============================

Evolutionary algorithm for combinatorial optimization.

Python implementation. **JAVA** version available [here](https://gitlab.com/dhstolfi/epiGA/).

Daniel H. Stolfi and Enrique Alba.
**Epigenetic algorithms: A New way of building GAs based on epigenetics.**
*In: Information Sciences, vol. 424, Supplement C, pp. 250–272, 2018.*
doi> 10.1016/j.ins.2017.10.005

Contents:
---------

- /alg: examples and source code.
- /alg/docs: documentation.
- /alg/epiga: source code.
- /alg/test: test cases.
- /docs: docs source.

Examples:
---------

```
cd alg
./TSP.py                # Traveling Salesman Problem (Minimization, Permutation Representation).
./OneMax.py             # OneMax problem (Maximization, Binary Representation).
./SphereFunction.py     # Sphere Function problem (Minimization, Float Representation).
./EggholderFunction.py  # Eggholder Function problem (Minimization, Integer Representation).
```