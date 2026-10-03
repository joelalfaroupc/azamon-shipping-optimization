import unittest
import config
from abia_azamon import Paquete, Oferta
from practica import StateRepresentation, generate_initial_state1
from azamon_operators import MovePaquete

class SearchTests(unittest.TestCase):
    def test_empty_offer_can_receive_parcel(self):
        parcel=Paquete(1,2)
        state=StateRepresentation([[parcel],[]],[Oferta(2,5,5),Oferta(2,1,1)])
        actions=list(state.generate_actions())
        self.assertTrue(any(isinstance(a,MovePaquete) and a.o_k==1 for a in actions))
        child=state.apply_action(next(a for a in actions if isinstance(a,MovePaquete)))
        self.assertEqual(state.state,[[parcel],[]])
        self.assertLess(child.heuristic(),state.heuristic())

    def test_candidate_construction_does_not_log_iterations(self):
        config.iterations.clear()
        StateRepresentation([[]],[Oferta(1,1,1)]).copy()
        self.assertEqual(config.iterations,[])

    def test_initialization_allows_early_delivery(self):
        parcel=Paquete(1,2)
        state=generate_initial_state1([parcel],[Oferta(2,1,1)])
        self.assertEqual(state.state,[[parcel]])

    def test_failed_greedy_assignment_is_explicit(self):
        with self.assertRaises(ValueError):
            generate_initial_state1([Paquete(3,0)],[Oferta(1,1,1)])

if __name__=='__main__': unittest.main()
