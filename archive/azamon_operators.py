class AzamonOperator(object):
    pass


class MovePaquete(AzamonOperator):
    def __init__(self, p_i: int, o_j: int, o_k: int):
        self.p_i = p_i
        self.o_j = o_j
        self.o_k = o_k

    def __repr__(self) -> str:
        return f"Move parcel {self.p_i} from container {self.o_j} to container {self.o_k}"


class SwapPaquetes(AzamonOperator):
    def __init__(self, p_i: int, p_j: int):
        self.p_i = p_i
        self.p_j = p_j

    def __repr__(self) -> str:
        return f"Swap paquetes {self.p_i} and {self.p_j}"