from abc import ABC, abstractmethod


class Sala(ABC):
    """
    Classe abstrata que representa uma sala do sistema.

    Toda sala possui:
    - identificador único
    - andar
    - número

    As subclasses devem implementar:
    - capacidade da sala
    - tipo da sala
    """

    proximo_id = 1

    def __init__(self, andar: int, numero: int):
        """
        Inicializa uma sala.

        Args:
            andar (int): Andar onde a sala está localizada.
            numero (int): Número identificador da sala.
        """

        self._id = Sala.proximo_id
        self._andar = andar
        self._numero = numero

        Sala.proximo_id += 1

    def get_andar(self) -> int:
        """
        Retorna o andar da sala.

        Returns:
            int: Andar da sala.
        """
        return self._andar

    def get_numero(self) -> int:
        """
        Retorna o número da sala.

        Returns:
            int: Número da sala.
        """
        return self._numero
    
    def get_id(self) -> int:
        """
        Retorna o id da sala.

        Returns:
            int: Id da sala.
        """
        return self._id

    @abstractmethod
    def capacidade(self) -> int:
        """
        Retorna a capacidade máxima da sala.

        Returns:
            int: Quantidade máxima de pessoas.
        """
        pass

    @abstractmethod
    def tipo(self) -> str:
        """
        Retorna o tipo da sala.

        Returns:
            str: Tipo da sala.
        """
        pass

    def __str__(self) -> str:
        """
        Retorna uma representação textual da sala.

        Returns:
            str: Informações formatadas da sala.
        """

        return (
            f"{self.tipo()} | "
            f"Sala {self._numero} | "
            f"Andar {self._andar}"
        )


class SalaIndividual(Sala):
    """
    Representa uma sala individual.
    """

    def capacidade(self) -> int:
        return 1

    def tipo(self) -> str:
        return "Individual"


class SalaGrupo(Sala):
    """
    Representa uma sala destinada a grupos.
    """

    def capacidade(self) -> int:
        return 30

    def tipo(self) -> str:
        return "Grupo"


class Laboratorio(Sala):
    """
    Representa um laboratório.
    """

    def capacidade(self) -> int:
        return 25

    def tipo(self) -> str:
        return "Laboratório"

#Factor
class SalaFactory:
    """
    Classe responsável pela criação de salas.

    Implementa o padrão Factory para criar
    diferentes tipos de salas dinamicamente.
    """

    _types = {
        "Sala Individual": SalaIndividual,
        "Sala Grupo": SalaGrupo,
        "Laboratório": Laboratorio,
    }

    @staticmethod
    def create(sala_type: str, andar: int, numero: int) -> Sala:
        """
        Cria uma nova sala com base no tipo informado.

        Args:
            sala_type (str): Tipo da sala.
            andar (int): Andar da sala.
            numero (int): Número da sala.

        Raises:
            ValueError: Caso o tipo da sala seja inválido.

        Returns:
            Sala: Instância do tipo de sala solicitado.
        """

        sala_class = SalaFactory._types.get(sala_type)

        if sala_class is None:
            raise ValueError("Tipo de sala inválido")

        return sala_class(andar, numero)