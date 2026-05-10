import threading
from datetime import time, timedelta

# Singleton 
class RepositorioReservas:
    _instance = None
    _lock = threading.Lock() # evitar problemas de concorrência

    HORARIOS_DISPONIVEIS = [
        time(8, 0),
        time(9, 0),
        time(10, 0),
        time(11, 0),
        time(12, 0),
        time(13, 0),
        time(14, 0),
        time(15, 0),
        time(16, 0),
        time(17, 0),
    ]# lista para horarios disponiveis de reserva

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance._inicializar()
            return cls._instance

    def _inicializar(self):
        self.salas = []
        self.usuarios = []
        self.reservas = []

    def adicionar_sala(self, sala):
        self.salas.append(sala)

    def adicionar_usuario(self, usuario):
        self.usuarios.append(usuario)

    def adicionar_reserva(self, reserva):
        self.reservas.append(reserva)

    def listar_salas(self):
        return self.salas

    def listar_usuarios(self):
        return self.usuarios

    def listar_reservas(self):
        return self.reservas

    def buscar_sala_por_id(self, sala_id):
        for sala in self.salas:
            if sala.get_id() == sala_id:
                return sala
        return None

    def buscar_usuario_por_id(self, usuario_id):
        for usuario in self.usuarios:
            if usuario.get_id() == usuario_id:
                return usuario
        return None

    def buscar_reserva_por_id(self, reserva_id):
        for reserva in self.reservas:
            if reserva.get_id() == reserva_id:
                return reserva
        return None

    def buscar_reserva_por_sala_data_horario(self, sala, data, horario):
        for reserva in self.reservas:
            if self._reserva_bloqueia_horario(reserva, sala, data, horario):
                return reserva
        return None

    def listar_reservas_por_data(self, data):
        reservas_do_dia = []

        for reserva in self.reservas:
            if reserva.get_data() == data:
                reservas_do_dia.append(reserva)

        return reservas_do_dia

    def listar_reservas_por_sala(self, sala):
        reservas_da_sala = []

        for reserva in self.reservas:
            if reserva.get_sala() == sala:
                reservas_da_sala.append(reserva)

        return reservas_da_sala

    def sala_esta_disponivel(self, sala, data, horario):
        for reserva in self.reservas:
            if self._reserva_bloqueia_horario(reserva, sala, data, horario):
                return False
        return True

    def listar_salas_disponiveis(self, data_inicio, data_fim, horario):
        if data_inicio > data_fim:
            return {}

        salas_disponiveis = {}
        data_atual = data_inicio

        while data_atual <= data_fim:
            salas_disponiveis[data_atual] = []

            for sala in self.salas:
                if self.sala_esta_disponivel(sala, data_atual, horario):
                    salas_disponiveis[data_atual].append(sala)

            data_atual += timedelta(days=1)

        return salas_disponiveis

    def listar_horarios_disponiveis_por_periodo(self, data_inicio, data_fim):
        if data_inicio > data_fim:
            return {}

        disponibilidade = {}
        data_atual = data_inicio

        while data_atual <= data_fim:
            disponibilidade[data_atual] = {}

            for sala in self.salas:
                horarios_livres = []

                for horario in self.HORARIOS_DISPONIVEIS:
                    if self.sala_esta_disponivel(sala, data_atual, horario):
                        horarios_livres.append(horario)

                if horarios_livres:
                    disponibilidade[data_atual][sala] = horarios_livres

            data_atual += timedelta(days=1)

        return disponibilidade

    def _reserva_bloqueia_horario(self, reserva, sala, data, horario):
        mesma_sala = reserva.get_sala() == sala
        mesma_data = reserva.get_data() == data
        mesmo_horario = reserva.get_horario() == horario
        cancelada = self._reserva_esta_cancelada(reserva)

        return mesma_sala and mesma_data and mesmo_horario and not cancelada

    def _reserva_esta_cancelada(self, reserva):
        status = reserva.get_status()
        valor_status = getattr(status, "value", status)

        return valor_status == "Cancelada"

    def limpar(self):
        self.salas.clear()
        self.usuarios.clear()
        self.reservas.clear()