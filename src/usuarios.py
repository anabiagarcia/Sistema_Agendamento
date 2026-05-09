from abc import ABC, abstractmethod


class Usuario(ABC):
    """
    Classe abstrata que representa um usuário do sistema.
    """

    proximo_id = 1

    def __init__(self, nome: str):
        """
        Inicializa um usuário.

        Args:
            nome (str): Nome do usuário.
        """

        self._id = Usuario.proximo_id
        self._nome = nome

        Usuario.proximo_id += 1

    def get_id(self) -> int:
        """
        Retorna o id do usuário.

        Returns:
            int: Id do usuário.
        """
        return self._id
    
    def get_nome(self) -> str:
        """
        Retorna o nome do usuário.

        Returns:
            str: Nome do usuário.
        """
        return self._nome

    @abstractmethod
    def tipo(self) -> str:
        """
        Retorna o tipo do usuário.

        Returns:
            str: Tipo do usuário.
        """
        pass

    def __str__(self) -> str:
        """
        Retorna representação textual do usuário.

        Returns:
            str: Informações do usuário.
        """

        return (
            f"{self.tipo()} | "
            f"Nome: {self._nome}"
        )


class Professor(Usuario):
    """
    Representa um professor.
    """

    def tipo(self) -> str:
        return "Professor"


class Aluno(Usuario):
    """
    Representa um aluno.
    """

    def tipo(self) -> str:
        return "Aluno"


class Manutencao(Usuario):
    """
    Representa um funcionário da manutenção.
    """

    def tipo(self) -> str:
        return "Manutenção"


class UsuarioFactory:
    """
    Factory responsável pela criação de usuários.
    """

    _types = {
        "Professor": Professor,
        "Aluno": Aluno,
        "Manutenção": Manutencao,
    }

    @staticmethod
    def create(usuario_type: str, nome: str) -> Usuario:
        """
        Cria um usuário com base no tipo informado.

        Args:
            usuario_type (str): Tipo do usuário.
            nome (str): Nome do usuário.

        Raises:
            ValueError: Caso o tipo seja inválido.

        Returns:
            Usuario: Instância do usuário criado.
        """

        usuario_class = UsuarioFactory._types.get(usuario_type)

        if usuario_class is None:
            raise ValueError("Tipo de usuário inválido")

        return usuario_class(nome)