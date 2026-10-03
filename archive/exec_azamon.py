from aima.search import hill_climbing
from azamon_problem import AzamonProblem
from practica import generate_initial_state1, generate_initial_state2
from abia_azamon import random_paquetes, random_ofertas, inspeccionar_ofertas, inspeccionar_paquetes
import time
import config
import matplotlib.pyplot as plt

def plotejar(x):
    #PLOTS HEURISTICA
    plt.figure(figsize=(10, 6))
    plt.plot(range(len(x)), x, marker='o', linestyle='-', color='b')
    plt.xlabel('Iteración (Paso)')
    plt.ylabel('Valor de la Heurística')
    plt.title('Progreso de Hill Climbing')
    plt.grid(True)
    plt.show()


if __name__ == '__main__':
    npaq = int(input("Numero de paquetes: "))
    semilla = int(input("Semilla aleatoria: "))
    paquetes = random_paquetes(npaq, semilla)
    ofertas = random_ofertas(paquetes, 1.2, 1234)
    inspeccionar_paquetes(paquetes)
    inspeccionar_ofertas(ofertas)
    initial_state = generate_initial_state1(paquetes, ofertas)
    start_time = time.time()
    n = hill_climbing(AzamonProblem(initial_state))
    end_time = time.time()
    print(n) # Estat final
    print(n.heuristic()) # Valor de l’estat final
    print("")
    print("Temps d'execució: ", end_time - start_time)
    plotejar(config.iterations)