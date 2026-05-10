from datetime import datetime, timedelta

from dados import RepositorioReservas


class RelatorioDiario:
    def __init__(self, repositorio=None):
        if repositorio is None:
            repositorio = RepositorioReservas()

        self.repositorio = repositorio

    def gerar(self, data):
        reservas = self.repositorio.listar_reservas_por_data(data)
        reservas_confirmadas = []

        for reserva in reservas:
            if self._reserva_esta_confirmada(reserva):
                reservas_confirmadas.append(reserva)

        if not reservas_confirmadas:
            return f"Nenhuma reserva confirmada encontrada para {data}."

        reservas_por_sala = {}

        for reserva in reservas_confirmadas:
            sala = reserva.get_sala()

            if sala not in reservas_por_sala:
                reservas_por_sala[sala] = []

            reservas_por_sala[sala].append(reserva)

        linhas = [f"Relatorio diario - {data}"]

        for sala, reservas_da_sala in reservas_por_sala.items():
            linhas.append("")
            linhas.append(str(sala))

            for reserva in reservas_da_sala:
                usuario = reserva.get_usuario()
                horario = reserva.get_horario()

                if horario is None:
                    intervalo = "Horario nao informado"
                else:
                    inicio = datetime.combine(data, horario)
                    fim = inicio + timedelta(hours=1)
                    intervalo = (
                        f"{inicio.strftime('%H:%M')} as "
                        f"{fim.strftime('%H:%M')}"
                    )

                linhas.append(
                    f"- {intervalo} - "
                    f"{usuario.get_nome()} "
                    f"({usuario.tipo()})"
                )

        return "\n".join(linhas)

    def _reserva_esta_confirmada(self, reserva):
        status = reserva.get_status()

        if status is None:
            return False

        valor_status = getattr(status, "value", status)

        return valor_status == "Confirmada"