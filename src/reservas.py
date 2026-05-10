from datetime import date, time, datetime
from enum import Enum
from notificacoes import NotificadorReservas, ObserverUsuario
from salas import Sala
from usuarios import Usuario, Professor
from dados import RepositorioReservas


class StatusReserva(Enum):
    """
    Representa os possíveis estados de uma reserva.
    """

    CONFIRMADA = "Confirmada"
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
    EVENTO_ALTERADA = "Reserva alterada"
    EVENTO_CANCELADA = "Reserva cancelada"

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
        self._status = StatusReserva.CONFIRMADA
        self._notificador = NotificadorReservas()
        self._adicionar_observador_usuario(usuario)

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

    def adicionar_observador(self, observer):
        """Adiciona um observador interessado nas mudanças desta reserva"""
        self._notificador.adicionar_observador(observer)

    def remover_observador(self, observer):
        """Remove um observador desta reserva"""
        self._notificador.remover_observador(observer)

    def cancelar_reserva(self):
        """
        Cancela a reserva.
        """

        self._status = StatusReserva.CANCELADA
        self._notificar(Reserva.EVENTO_CANCELADA)

    def set_usuario(self, usuario: Usuario):
        """
        Altera o usuário responsável pela reserva.

        Args:
            usuario (Usuario): Novo usuário.
        """
        self._adicionar_observador_usuario(self._usuario)
        self._adicionar_observador_usuario(usuario)
        self._usuario = usuario
        self._notificar(Reserva.EVENTO_ALTERADA)

    def set_sala(self, sala: Sala):
        """
        Altera a sala da reserva.

        Args:
            sala (Sala): Nova sala.
        """

        self._validar_data_horario(self.get_data(), self.get_horario())

        repositorio = RepositorioReservas()
        conflito = repositorio.buscar_reserva_por_sala_data_horario(
            sala, self.get_data(), self.get_horario()
        )

        if conflito is None:
            self._sala = sala
            self._notificar(Reserva.EVENTO_ALTERADA)
        elif isinstance(self._usuario, Professor) and not isinstance(conflito.get_usuario(), Professor):
            self._sala = sala
            self._notificar(Reserva.EVENTO_ALTERADA)
            conflito.cancelar_reserva()
        else:
            raise ValueError("Modificação Inválida")

    def set_horario(self, horario: time):
        """
        Altera o horário da reserva.

        Args:
            horario (time): Novo horário.
        """
        self._validar_data_horario(self.get_data(), horario)

        repositorio = RepositorioReservas()
        conflito = repositorio.buscar_reserva_por_sala_data_horario(
            self.get_sala(), self.get_data(), horario
        )

        if conflito is None:
            self._horario = horario
            self._notificar(Reserva.EVENTO_ALTERADA)
        elif isinstance(self._usuario, Professor)and not isinstance(conflito.get_usuario(), Professor):
            self._horario = horario
            self._notificar(Reserva.EVENTO_ALTERADA)
            conflito.cancelar_reserva()
        else:
            raise ValueError("Modificação Inválida")
        
        

    def set_data(self, data: date):
        """
        Altera a data da reserva.

        Args:
            data (date): Nova data.
        """
        self._validar_data_horario(data, self.get_horario())

        repositorio = RepositorioReservas()
        conflito = repositorio.buscar_reserva_por_sala_data_horario(
            self.get_sala(), data, self.get_horario()
        )

        if conflito is None:
            self._data = data
            self._notificar(Reserva.EVENTO_ALTERADA)
        elif isinstance(self._usuario, Professor) and not isinstance(conflito.get_usuario(), Professor):
            self._data = data
            self._notificar(Reserva.EVENTO_ALTERADA)
            conflito.cancelar_reserva()
        else:
            raise ValueError("Modificação Inválida")
        
        

    def _notificar(self, evento):
        self._notificador.notificar(evento, self)

    def _adicionar_observador_usuario(self, usuario):
        self._notificador.adicionar_observador(ObserverUsuario(usuario))

    def _validar_data_horario(self, data: date, horario: time):
        if data < date.today() or (data == date.today() and horario <= datetime.now().time()):
            raise ValueError("Data e hora inválidos")

        if horario.hour < 8 or horario.hour > 17 or horario.minute != 0:
            raise ValueError("Horário inválido")
    
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