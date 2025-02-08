#!C:\Users\Chirag\AppData\Local\Programs\Python\Python310\python.exe

from domain import Lecture, TimeTable, generate_problem
from constraints import define_constraints,isOverlapping
from optapy import get_class
import optapy.config
from optapy.types import Duration
from optapy import solver_factory_create

solver_config = optapy.config.solver.SolverConfig() \
    .withEntityClasses(get_class(Lecture)) \
    .withSolutionClass(get_class(TimeTable)) \
    .withConstraintProviderClass(get_class(define_constraints)) \
    .withTerminationSpentLimit(Duration.ofSeconds(30))
    

solver = solver_factory_create(solver_config).buildSolver()
    
solution = solver.solve(generate_problem())

print(solution)

for i in range(len(solution)):
    for j in range(i,len(solution)):
        if isOverlapping(i, j):
            print(i)
            print(j)