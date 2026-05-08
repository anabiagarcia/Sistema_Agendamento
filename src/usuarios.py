from abc import ABC, abstractmethod

class Usuario(ABC):
    def __init__(self):
        self.id: int

class Professor(Usuario):
    pass

class Aluno(Usuario):
    pass

class Manutencao(Usuario):
    pass

class UsuarioFactory:
    _types = {
        "Professor": Professor,
        "Aluno": Aluno,
        "Manutenção": Manutencao,
    }

    @staticmethod
    def _create(usuario_type: str) -> Usuario:
        new = UsuarioFactory._types.get(usuario_type)
        return new