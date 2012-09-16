= README =
This file is supposed to explain how the genetic_programming.py file works.

Basically, there's a Gene class with the properties code and cost, and the
methods mutate, calcCost, and mate.

1. mutate introduces one random up or down mutation in one of the code's chars
2. calcCost returns the sum of the squares of the difference between the
   target's char and the gene's code at an index.
3. mate combines the first part of one gene with the second part of the second
   gene, and vice versa, creating two children.

Then there's the Population class. It tells its members when and whom to mate,
and when to mutate.

For now, the initial gene's start out with a fixed code (all As).