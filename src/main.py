from datetime import datetime

from dados import RepositorioReservas
from salas import SalaFactory
from usuarios import UsuarioFactory
from politicas import ProxyReserva
from relatorios import RelatorioDiario

repositorio = RepositorioReservas()
proxy = ProxyReserva()

def menu():
    print("\n=== Reserva de Salas de Estudo ===")
    print("1 - Cadastrar sala")
    print("2 - Cadastrar usuário")
    print("3 - Listar salas")
    print("4 - Listar usuários")
    print("5 - Listar salas disponíveis")
    print("6 - Criar reserva")
    print("7 - Modificar reserva")
    print("8 - Cancelar reserva")
    print("9 - Relatório diário")
    print("0 - Sair")


def cadastrar_sala():
    print("\nTipos de sala:")
    print("1 - Sala Individual")
    print("2 - Sala Grupo")
    print("3 - Laboratório")

    opcao = input("Escolha o tipo: ")

    tipos = {
        "1": "Sala Individual",
        "2": "Sala Grupo",
        "3": "Laboratório"
    }

    tipo = tipos.get(opcao)

    if tipo is None:
        print("Tipo inválido.")
        return

    andar = int(input("Andar: "))
    numero = int(input("Número da sala: "))

    sala = SalaFactory.create(tipo, andar, numero)
    repositorio.adicionar_sala(sala)
    print("Sala cadastrada.")


def cadastrar_usuario():
    print("\nTipos de usuário:")
    print("1 - Professor")
    print("2 - Aluno")
    print("3 - Manutenção")

    opcao = input("Escolha o tipo: ")

    tipos = {
        "1": "Professor",
        "2": "Aluno",
        "3": "Manutenção"
    }

    tipo = tipos.get(opcao)

    if tipo is None:
        print("Tipo inválido.")
        return

    nome = input("Nome: ")

    usuario = UsuarioFactory.create(tipo, nome)
    repositorio.adicionar_usuario(usuario)
    print("Usuário cadastrado.")


def listar_salas():
    salas = repositorio.listar_salas()

    if not salas:
        print("Nenhuma sala cadastrada.")
        return

    print("\nSalas:")

    for sala in salas:
        print(
            f"ID: {sala.get_id()}"
            f"Numero: {sala.get_numero()}"
            f"Andar: {sala.get_andar()}"
            f"Tipo: {sala.tipo()}"
        )


def listar_usuarios():
    usuarios = repositorio.listar_usuarios()

    if not usuarios:
        print("Nenhum usuário cadastrado.")
        return

    print("\nUsuários:")

    for usuario in usuarios:
        print(
            f"ID: {usuario.get_id()}"
            f"Nome: {usuario.get_nome()}"
            f"Tipo: {usuario.tipo()}"
        )


def listar_salas_disponiveis():

    data_inicio = input("Data inicial (AAAA-MM-DD): ")
    data_fim = input("Data final (AAAA-MM-DD): ")
    data_inicio = datetime.strptime(data_inicio, "%Y-%m-%d").date()
    data_fim = datetime.strptime(data_fim, "%Y-%m-%d").date()
    
    disponibilidade = repositorio.listar_horarios_disponiveis_por_periodo(data_inicio, data_fim)

    print("\nDisponibilidade por período:")

    if not disponibilidade:
        print("Período inválido ou sem disponibilidade.")
        return

    for data, salas in disponibilidade.items():
        print(f"\nData: {data}")

        if not salas:
            print("Nenhuma sala disponível.")
            continue

        for sala, horarios in salas.items():
            print(f"ID {sala.get_id()}:")

            for horario in horarios:
                print(f"  - {horario.strftime('%H:%M')}")


def criar_reserva():
    listar_salas()

    sala_id = int(input("\nID da sala: "))
    sala = repositorio.buscar_sala_por_id(sala_id)

    if sala is None:
        print("Sala não encontrada.")
        return

    listar_usuarios()
    usuario_id = int(input("\nID do usuário: "))
    usuario = repositorio.buscar_usuario_por_id(usuario_id)

    if usuario is None:
        print("Usuário não encontrado.")
        return

    data = input("Data (AAAA-MM-DD): ")
    horario = input("Horário (HH:MM): ")

    data = datetime.strptime(data, "%Y-%m-%d").date()
    horario = datetime.strptime(horario,"%H:%M").time()

    try:
        reserva = proxy.criar_reserva(sala, usuario, data, horario)

        if (reserva not in repositorio.listar_reservas()):
            repositorio.adicionar_reserva(reserva)

        print("Reserva criada.")

    except ValueError as erro:
        print(f"Erro: {erro}")

#verificar
def modificar_reserva():
    reservas = repositorio.listar_reservas()

    if not reservas:
        print("Nenhuma reserva cadastrada.")
        return

    print("\nReservas:")

    for reserva in reservas:
        print(reserva)

    reserva_id = int(input("ID da reserva: "))

    reserva = repositorio.buscar_reserva_por_id(reserva_id)
    
    if reserva is None:
        print("Reserva não encontrada.")
        return
    
    print("\nTipos de mudança:")
    print("1 - Horário")
    print("2 - Dia")
    print("3 - Sala")
    
    opcao = input("\nEscolha: ")

    if opcao == "1":

        novo_horario = input("Novo horário (HH:MM): ")
        novo_horario = datetime.strptime(novo_horario, "%H:%M").time()
        reserva.set_horario(novo_horario)
    
    elif opcao == "2":
        nova_data = input("Nova data (AAAA-MM-DD): ")
        nova_data = datetime.strptime(nova_data, "%Y-%m-%d").date()
        reserva.set_data(nova_data)

    elif opcao == "3":

        listar_salas()
        sala_id = int(input("\nNovo ID da sala: "))
        nova_sala = repositorio.buscar_sala_por_id(sala_id)

        if nova_sala is None:
            print("Sala não encontrada.")
            return
        
        reserva.set_sala(nova_sala)
        
    else:
        print("Opção inválida.")
    
    print("Reserva modificada.")


def cancelar_reserva():
    reservas = repositorio.listar_reservas()

    if not reservas:
        print("Nenhuma reserva cadastrada.")
        return

    print("\nReservas:")

    for reserva in reservas:
        print(reserva)

    reserva_id = int(input("ID da reserva: "))
    reserva = repositorio.buscar_reserva_por_id(reserva_id)

    if reserva is None:
        print("Reserva não encontrada.")
        return
    
    reserva.cancelar_reserva()
    print("Reserva cancelada.")


def gerar_relatorio_diario():

    data = input("Data do relatório (AAAA-MM-DD): ")
    data = datetime.strptime(data, "%Y-%m-%d").date()
    relatorio = RelatorioDiario()
    print("\n" + relatorio.gerar(data))


def executar():
    while True:
        menu()

        opcao = input("\nEscolha: ")

        if opcao == "1":
            cadastrar_sala()

        elif opcao == "2":
            cadastrar_usuario()

        elif opcao == "3":
            listar_salas()

        elif opcao == "4":
            listar_usuarios()

        elif opcao == "5":
            listar_salas_disponiveis()

        elif opcao == "6":
            criar_reserva()

        elif opcao == "7":
            modificar_reserva()

        elif opcao == "8":
            cancelar_reserva()

        elif opcao == "9":
            gerar_relatorio_diario()

        elif opcao == "0":
            print("Sistema encerrado.")
            break

        else:
            print("Opção inválida.")


if __name__ == "__main__":
    executar()