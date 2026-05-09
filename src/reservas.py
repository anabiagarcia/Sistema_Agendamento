from datetime import date, time
from enum import Enum
from salas import Sala
from usuarios import Usuario


class StatusReserva(Enum):
    """
    Representa os possíveis estados de uma reserva.
    """

    ATIVA = "Ativa"
    CANCELADA = "Cancelada"
    FINALIZADA = "Finalizada"


class Reserva:
    """
    Representa uma reserva de sala realizada por um usuário.

    Cada reserva possui:
    - um identificador único;
    - uma sala;
    - um usuário responsável;
    - uma data;
    - um horário;
    - um status.
    """

    proximo_id = 1

    def __init__(self, sala: Sala, usuario: Usuario, data: date, horario: time):
        """
        Inicializa uma nova reserva.

        Args:
            sala (Sala): Sala reservada.
            usuario (Usuario): Usuário responsável pela reserva.
            data (date): Data da reserva.
            horario (time): Horário da reserva.
        """

        self._id = Reserva.proximo_id
        self._sala = sala
        self._usuario = usuario
        self._data = data
        self._horario = horario
        self._status = StatusReserva.ATIVA

        Reserva.proximo_id += 1

    def get_usuario(self) -> Usuario:
        """
        Retorna o usuário responsável pela reserva.

        Returns:
            Usuario: Usuário da reserva.
        """

        return self._usuario

    def get_sala(self) -> Sala:
        """
        Retorna a sala reservada.

        Returns:
            Sala: Sala da reserva.
        """

        return self._sala
    
    def get_data(self) -> date:
        """
        Retorna a data da reserva.

        Returns:
            date: Data da reserva.
        """

        return self._data
    
    def get_horario(self) -> time:
        """
        Retorna o horario da reserva.

        Returns:
            time: Horario da reserva.
        """

        return self._horario
    
    def get_id(self) -> int:
        """
        Retorna o id da reserva.

        Returns:
            int: Id da reserva.
        """

        return self._id
    
    def get_status(self) -> StatusReserva:
        """
        Retorna o status da reserva.

        Returns:
            StatusReserva: Status da reserva.
        """
        return self._status

    def cancelar_reserva(self):
        """
        Cancela a reserva.

        Futuramente deverá notificar os observadores.
        """

        self._status = StatusReserva.CANCELADA

    def set_usuario(self, usuario: Usuario):
        """
        Altera o usuário responsável pela reserva.

        Args:
            usuario (Usuario): Novo usuário.
        """

        #adicionar observer
        self._usuario = usuario

    def set_sala(self, sala: Sala):
        """
        Altera a sala da reserva.

        Args:
            sala (Sala): Nova sala.
        """

        #adicionar observer
        self._sala = sala

    def set_horario(self, horario: time):
        """
        Altera o horário da reserva.

        Args:
            horario (time): Novo horário.
        """

        #adicionar observer
        self._horario = horario

    def set_data(self, data: date):
        """
        Altera a data da reserva.

        Args:
            data (date): Nova data.
        """

        #adicionar observer
        self._data = data
    
    def __str__(self) -> str:
        """
        Retorna uma representação textual da reserva.

        Returns:
            str: Informações formatadas da reserva.
        """

        return (
            f"{self._id} | "
            f"Sala {self._sala.get_numero()} | "
            f"Tipo da Sala {self._sala.tipo()} | "
            f"Andar {self._sala.get_andar()} | "
            f"Usuário {self._usuario.get_nome()} | "
            f"Tipo Usuário {self._usuario.tipo()} | "
            f"Data {self._data} | "
            f"Hora {self._horario} | "
            f"Status {self._status.value}"
        )

