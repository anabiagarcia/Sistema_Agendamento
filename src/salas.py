from abc import ABC, abstractmethod

class Sala(ABC):
    def __init__(self):
        self._id: int

class SalaIndividual(Sala):
    pass

class SalaGrupo(Sala):
    pass

class Laboratorio(Sala):
    pass

class SalaFactory:
    _types = {
        "Sala Individual": SalaIndividual,
        "Sala Grupo": SalaGrupo,
        "Laboratório": Laboratorio,
    }

    @staticmethod
    def _create(sala_type: str) -> Sala:
        new = SalaFactory._types.get(sala_type)
        return new