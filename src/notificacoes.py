from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def update(self, evento, reserva):
        pass

class Subject(ABC):
    @abstractmethod
    def adicionar_observador(self, observer):
        pass

    @abstractmethod
    def remover_observador(self, observer):
        pass

    @abstractmethod
    def notificar(self, evento, reserva):
        pass

# observer concreto
class ObserverUsuario(Observer):
    def __init__(self, usuario):
        self.usuario = usuario

    def __eq__(self, other):
        return ( isinstance(other, ObserverUsuario) and self.usuario.get_id() == other.usuario.get_id())

    def __hash__(self):
        return hash(self.usuario.get_id())

    # pull, o observer recebe a reserva e busca nela os dados necessários.
    def update(self, evento, reserva):
        print(
            f"Notificando {self.usuario.get_nome()}: "
            f"{evento} - Reserva {reserva.get_id()}"
        )


# Subject concreto
class NotificadorReservas(Subject):
    def __init__(self):
        self.observers = []

    def adicionar_observador(self, observer):
        if observer not in self.observers:
            self.observers.append(observer)

    def remover_observador(self, observer):
        if observer in self.observers:
            self.observers.remove(observer)

    def remover_observer(self, observer):
        self.remover_observador(observer)

    def limpar_observadores(self):
        self.observers.clear()

    # push, o notificador envia o evento e a reserva para todos os observers
    def notificar(self, evento, reserva):
        for observer in list(self.observers):
            observer.update(evento, reserva)
