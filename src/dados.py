import threading


class RepositorioReservas:
    _instance = None
    _lock = threading.Lock() # evitar problemas de concorrência

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
            if getattr(sala, "_id", None) == sala_id:
                return sala
        return None

    def buscar_usuario_por_id(self, usuario_id):
        for usuario in self.usuarios:
            if getattr(usuario, "_id", None) == usuario_id:
                return usuario
        return None

    def buscar_reserva_por_id(self, reserva_id):
        for reserva in self.reservas:
            if getattr(reserva, "_id", None) == reserva_id:
                return reserva
        return None

    def listar_reservas_por_data(self, data):
        reservas_do_dia = []

        for reserva in self.reservas:
            if getattr(reserva, "_data", None) == data:
                reservas_do_dia.append(reserva)

        return reservas_do_dia

    def listar_reservas_por_sala(self, sala):
        reservas_da_sala = []

        for reserva in self.reservas:
            if reserva.get_sala() == sala:
                reservas_da_sala.append(reserva)

        return reservas_da_sala

    def limpar(self): # limpa dados (testes)
        self.salas.clear()
        self.usuarios.clear()
        self.reservas.clear()
