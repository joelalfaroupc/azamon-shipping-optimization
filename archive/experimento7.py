from aima.search import simulated_annealing, exp_schedule
from azamon_problem import AzamonProblem
from practica import generate_initial_state1
from abia_azamon import random_paquetes, random_ofertas
import time
import config
import matplotlib.pyplot as plt

def plotejar(x,y,labelx,labely,title):
    #PLOTS HEURISTICA
    plt.figure(figsize=(10, 6))
    plt.plot(y, x, marker='o', linestyle='-', color='b')
    plt.xlabel(labelx)
    plt.ylabel(labely)
    plt.title(title)
    plt.grid(True)
    plt.show()

valors_c = [1,2,3,4.5,6,7,8,9,10,14,17.5,20,30]

if __name__ == '__main__':
    heuristic = []
    times = []
    for c in valors_c:
        mean_time = 0
        mean_heuristic = 0
        for _ in range(10):
            config.ponderacion_felicidad = c
            paquetes = random_paquetes(50, 1234)
            ofertas = random_ofertas(paquetes, 1.2, 1234)
            initial_state = generate_initial_state1(paquetes, ofertas) #ESCOGER
            start_time = time.time()
            n = simulated_annealing(AzamonProblem(initial_state),schedule=exp_schedule(k=5, lam=0.1, limit=500)) # mejores valores de experimento3
            end_time = time.time()
            mean_heuristic += n.heuristic()
            mean_time += end_time - start_time
        heuristic.append(mean_heuristic/10)
        times.append(mean_time/10)

    plotejar(heuristic,valors_c,"Ponderación felicidad","Heurística","Heurística en función de la ponderación de la felicidad (SA)")
    plotejar(times,valors_c,"Ponderación felicidad","Tiempo","Tiempo en función de la ponderación de la felicidad (SA)")