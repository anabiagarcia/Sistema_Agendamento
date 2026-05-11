from abc import ABC, abstractmethod
from datetime import date, time, datetime

from salas import Sala
from usuarios import Usuario, Professor, UsuarioFactory
from reservas import Reserva
from dados import RepositorioReservas

#Strategy
class StrategyReserva(ABC):
    """
    Interface para as estratégias de criação ou alteração de reservas.

    Cada estratégia define uma regra diferente para lidar com reservas
    já existentes em uma mesma sala, data e horário.
    """

    @abstractmethod
    def nova_reserva(self, sala: Sala, usuario: Usuario, data: date, horario: time) -> Reserva | None:
        """
        Cria ou altera uma reserva conforme a estratégia escolhida.

        Args:
            sala (Sala): Sala desejada para a reserva.
            usuario (Usuario): Usuário que deseja reservar.
            data (date): Data da reserva.
            horario (time): Horário da reserva.

        Returns:
            Reserva | None: Reserva criada/alterada ou None caso não seja possível.
        """
        pass


class PrimeiraReserva(StrategyReserva):
    """
    Estratégia padrão: cria uma reserva quando não há conflito de horário.
    """

    def nova_reserva(self, sala: Sala, usuario: Usuario, data: date, horario: time) -> Reserva:
        """
        Cria uma nova reserva.

        Returns:
            Reserva: Nova reserva criada.
        """
        reserva = GetReserva.get_reserva(sala, data, horario)

        if reserva is None:
            return Reserva(sala, usuario, data, horario)
        
        else:
            raise ValueError("Sala já reservada")


class PrioridadeProfessor(StrategyReserva):
    """
    Estratégia em que professores possuem prioridade sobre uma reserva existente.

    Caso já exista uma reserva naquele horário, o professor substitui
    o usuário anterior da reserva.
    """

    def nova_reserva(self, sala: Sala, usuario: Usuario, data: date, horario: time) -> Reserva | None:
        """
        Substitui o usuário da reserva existente por um professor.

        Returns:
            Reserva | None: Reserva alterada ou None se não existir reserva.
        """
        reserva = GetReserva.get_reserva(sala, data, horario)

        if reserva is None:
            return Reserva(sala, usuario, data, horario)

        if isinstance(reserva.get_usuario(), Professor):
            raise ValueError("Sala reservada por outro professor")

        reserva.set_usuario(usuario)
        return reserva


class ProxyReserva:

    def __init__(self, strategy: StrategyReserva):
        self.strategy = strategy

    def alterar_strategy(self, nova_strategy: StrategyReserva):
        self.strategy = nova_strategy

    def criar_reserva(self, sala: Sala, usuario: Usuario, data: date, horario: time) -> Reserva | None:

        if data < date.today() or (data == date.today() and horario <= datetime.now().time()):
            raise ValueError("Data e hora inválidos")

        if horario.hour < 8 or horario.hour > 17 or horario.minute != 0:
            raise ValueError("Horário inválido")

        return self.strategy.nova_reserva(sala, usuario, data, horario)


class GetReserva:
    """
    Classe responsável por buscar reservas existentes.
    """

    @staticmethod
    def get_reserva(sala: Sala, data: date, horario: time) -> Reserva | None:
        """
        Busca uma reserva existente para a mesma sala, data e horário.

        Args:
            sala (Sala): Sala pesquisada.
            data (date): Data pesquisada.
            horario (time): Horário pesquisado.

        Returns:
            Reserva | None: Reserva encontrada ou None.
        """

        repositorio = RepositorioReservas()
        return repositorio.buscar_reserva_por_sala_data_horario(sala, data, horario)
    
#Decorator
class DecoratorLimpeza(StrategyReserva):
    """
    Decorator que envolve outra `StrategyReserva` e cria reservas em nome
    de um usuário fixo de limpeza (`Manutenção` - "Limpeza").

    """

    user_limpeza = UsuarioFactory.create("Manutenção", "Limpeza")

    def __init__(self, strategy: StrategyReserva):
        self._strategy = strategy

    def nova_reserva(self, sala: Sala, usuario: Usuario, data: date, horario: time) -> Reserva | None:

        if data < date.today() or (data == date.today() and horario <= datetime.now().time()):
            raise ValueError("Data e hora inválidos")

        if horario.hour < 8 or horario.hour > 17 or horario.minute != 0:
            raise ValueError("Horário inválido")

        if GetReserva.get_reserva(sala, data, horario) is not None:
            raise ValueError("Data e hora já estão ocupados")

        return self._strategy.nova_reserva(sala, self.user_limpeza, data, horario)