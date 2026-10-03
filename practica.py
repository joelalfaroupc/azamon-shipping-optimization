import config #Variable global donde guardamos la heuristica para poder hacer plots i la ponderacion de la felicidad
from abia_azamon import Paquete, Oferta
from typing import List, Generator
from azamon_operators import AzamonOperator, MovePaquete, SwapPaquetes


class StateRepresentation(object):
    def __init__(self, state: List[List[Paquete]], ofertas: List[Oferta]):
        self.state = state
        self.ofertas = ofertas
     
    
    def __str__(self) -> str:
        print("")
        print("Estat final")
        print("--------------------------------------")
        for o_i,p_i in enumerate(self.state):
            peso = 0
            for p in p_i:
                print(f"Oferta {o_i}: {p}")
                peso += p.peso
            print(f"Of_{o_i}-> peso: {peso}, p_max: {self.ofertas[o_i].pesomax}, dias: {self.ofertas[o_i].dias}, precio: {self.ofertas[o_i].precio}")
            print("")
        return ""

    def copy(self):
        # Afegim el copy per cada set!
        state_copy = [element.copy() for element in self.state]
        return StateRepresentation(state_copy, self.ofertas)
    
    
    # Utilitzarem aquesta funció auxiliar per trobar el contenidor
    # que conté un paquet determinat
    def find_oferta(self, p_i: int) -> int:
        for oferta_id in range(len(self.state)):
            if p_i in self.state[oferta_id]:
                return oferta_id
    
    #funcio per mantenir estats en espai de solucio quan apliquem canvis i que 
    # accepta paquets amb prioridad baixa a ofertes mes rapides (felicitat)
    def asignable(self, paquete, oferta):
            if paquete.prioridad == 0:
                return oferta.dias == 1
            elif paquete.prioridad == 1:
                return oferta.dias <= 3 
            elif paquete.prioridad == 2:
                return oferta.dias <=5
    

    def generate_actions(self) -> Generator[AzamonOperator, None, None]:
        # Primer calculem el pes lliure de cada oferta
        free_weights = [offer.pesomax - sum(p.peso for p in parcels)
                        for offer, parcels in zip(self.ofertas, self.state)]

        # Moure paquet de contenidor: 
        for id_oferta_i, paquetes in enumerate(self.state):
            for p_i in paquetes:
                for id_oferta_f in range(len(self.state)):
                    # Condició: contenidor diferent i té espai lliure suficient
                    if id_oferta_i != id_oferta_f and free_weights[id_oferta_f] >= p_i.peso \
                        and self.asignable(p_i, self.ofertas[id_oferta_f]):
                        yield MovePaquete(p_i, id_oferta_i, id_oferta_f)

        # Intercanviar paquets:
        for oferta_id1 in range(len(self.state)):
            for paq_i in range(len(self.state[oferta_id1])):
                for oferta_id2 in range(oferta_id1 +1, len(self.state)):
                    for paq_j in range(len(self.state[oferta_id2])):
                        p_i = self.state[oferta_id1][paq_i]
                        p_j = self.state[oferta_id2][paq_j]
                        if p_i != p_j and oferta_id1 != oferta_id2:
                            if self.asignable(p_i, self.ofertas[oferta_id2]) and self.asignable(p_j, self.ofertas[oferta_id1]):
                                if free_weights[oferta_id1] + p_i.peso >= p_j.peso and free_weights[oferta_id2] + p_j.peso >= p_i.peso:
                                    yield SwapPaquetes(p_i, p_j)
                

    def apply_action(self, action: AzamonOperator):
        new_state = self.copy()
        if isinstance(action, MovePaquete):
            p_i = action.p_i
            o_j = action.o_j
            o_k = action.o_k

            new_state.state[o_k].append(p_i)
            new_state.state[o_j].remove(p_i)


        elif isinstance(action, SwapPaquetes):
            p_i = action.p_i
            p_j = action.p_j

            o_i = new_state.find_oferta(p_i)
            o_j = new_state.find_oferta(p_j)

            new_state.state[o_i].append(p_j)
            new_state.state[o_i].remove(p_i)

            new_state.state[o_j].append(p_i)
            new_state.state[o_j].remove(p_j)
        return new_state

    #Heuristica base
    def heuristic(self) -> float:
        # Minimizacion de los costes de transporte y almacenamiento
        total = 0.0
        for id_oferta, paquetes in enumerate(self.state):
            
            dias = self.ofertas[id_oferta].dias
            coste_alm=0
            coste_transporte = 0
            for id_paq in paquetes:
                peso=id_paq.peso
                if 3<= dias <=4:
                    coste_alm += peso*0.25

                elif dias == 5:
                    coste_alm += peso*0.5
                
                coste_transporte += self.ofertas[id_oferta].precio*peso

            total += coste_transporte + coste_alm
        
        return total
    
    #Heuristica Felicidad
    def heuristic00(self) -> float:
       # Minimizacion de los costes de transporte y almacenamiento
       # Maximizacion de la felicidad de los clientes
        total = 0.0
        ponderacion_felicidad = config.ponderacion_felicidad

        for id_oferta, paquetes in enumerate(self.state):
            coste_transporte = 0
            coste_alm=0
            felicitat=0
            dias = self.ofertas[id_oferta].dias
             
            for id_paq in paquetes:
                peso=id_paq.peso
                if 3 <= dias <= 4:
                    coste_alm += peso*0.25
                    
                if dias == 5:
                    coste_alm += peso*0.5
                
                coste_transporte+=self.ofertas[id_oferta].precio * peso
                
                #Calcul de la felicitat
                dias_minim = [1,2,4]
                diferencia=max(0,dias_minim[id_paq.prioridad]-dias)
                felicitat+=diferencia

            total += coste_transporte + coste_alm - ponderacion_felicidad*felicitat
        
        return total 
    

def _initial_state(paquetes, ofertas, reverse=False):
    """Greedy feasible assignment. Failure is not a proof of infeasibility."""
    state = StateRepresentation([[] for _ in ofertas], ofertas)
    remaining = [o.pesomax for o in ofertas]
    indices = list(range(len(ofertas)))
    if reverse:
        indices.reverse()
    # Tightest deadlines and largest parcels first; original objects retained.
    for parcel in sorted(paquetes, key=lambda p: (p.prioridad, -p.peso)):
        for i in indices:
            if state.asignable(parcel, ofertas[i]) and remaining[i] >= parcel.peso:
                state.state[i].append(parcel)
                remaining[i] -= parcel.peso
                break
        else:
            raise ValueError("Greedy initialization failed: try other offers/order")
    return state

def generate_initial_state1(l_paquetes, l_ofertas):
    return _initial_state(l_paquetes, l_ofertas)

def generate_initial_state2(l_paquetes, l_ofertas):
    return _initial_state(l_paquetes, l_ofertas, reverse=True)
