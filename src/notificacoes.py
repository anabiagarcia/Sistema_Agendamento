from abc import ABC, abstractmethod

class Observer(ABC):
	@abstractmethod
	def update(self, evento, reserva):
		pass

class ObserverUsuario(Observer):
	def __init__(self, usuario):
		self.usuario = usuario

	# pull
	def update(self, evento, reserva):
		print(f"Notificando {self.usuario.get_nome()}: "f"{evento} - Reserva {getattr(reserva, '_id', '')}")

class NotificadorReservas:
	def __init__(self):
		self.observers = []

	def adicionar_observador(self, observer):
		if observer not in self.observers:
			self.observers.append(observer)

	def remover_observer(self, observer):
		if observer in self.observers:
			self.observers.remove(observer)

	# push
	def notificar(self, evento, reserva): 
		for observer in self.observers:
			observer.update(evento, reserva)