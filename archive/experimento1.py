from aima.search import hill_climbing
from azamon_problem import AzamonProblem
from practica import generate_initial_state1
from abia_azamon import random_paquetes, random_ofertas
import time

if __name__ == '__main__':
    mean_execution_time = 0.0
    mean_heuristic = 0.0
    for _ in range(10):
        paquetes = random_paquetes(50, 1234)
        ofertas = random_ofertas(paquetes, 1.2, 1234)
        initial_state = generate_initial_state1(paquetes, ofertas)
        start_time = time.time()
        n = hill_climbing(AzamonProblem(initial_state))
        end_time = time.time()
        mean_heuristic += n.heuristic()
        mean_execution_time += end_time - start_time
    print(mean_execution_time / 10)
    print(mean_heuristic / 10)