# Sistema_Agendamento

Sistema de agendamento de salas para uma instituição, permitindo cadastrar salas e usuários, criar, alterar e cancelar reservas, além de gerar relatórios diários.


## Funcionalidades

- Cadastro de salas
- Cadastro de usuários
- Criação de reservas
- Cancelamento de reservas
- Edição de reservas
- Consulta de disponibilidade
- Geração de relatório diário de reservas
- Listagem de salas e usuários


## Requisitos Funcionais

- RF1: Listar salas disponíveis por período em intervalos de datas selecionados, considerando apenas datas e horários válidos.

- RF2: Criar reservas informando sala, usuário, data (`AAAA-MM-DD`) e horário (`HH:MM`), respeitando os horários válidos de funcionamento (`08:00–17:00`) e duração fixa de 1 hora.

- RF2: Modificar reservas (usuário, data, horário ou sala), realizando verificação de conflitos e aplicação das regras de prioridade.

- RF2: Cancelar reservas existentes.

- RF3: Evitar conflitos de agendamento, não permitindo duas reservas para a mesma sala, data e horário, exceto quando a regra de prioridade permitir substituição.

- RF3: Aplicar política de prioridade:
  - Usuários do tipo `Professor` podem substituir reservas realizadas por usuários não professores.
  - Tentativas inválidas devem lançar mensagens de erro claras.

- RF4: Notificar usuários quando houver modificações em reservas (data, horário ou sala).

- RF5: Gerar relatório diário contendo apenas reservas confirmadas e seus respectivos horários.


## Regras de Negócio

- Reservas possuem duração fixa de 1 hora.
- Horários válidos para reservas: `08:00` às `17:00`.
- Não podem existir reservas confirmadas duplicadas para a mesma sala, data e horário.
- Professores possuem prioridade sobre usuários não professores.


## Tecnologias Utilizadas

- Python 3.10+
- Programação Orientada a Objetos (POO)


## Conceitos Utilizados

- Encapsulamento
- Herança
- Polimorfismo
- Classes Abstratas
- Factory
- Strategy
- Proxy
- Observer



## Executando Localmente

Execute o programa:

```bash
python3 src/main.py
```

O menu interativo permite cadastrar salas e usuários, criar/modificar/cancelar reservas e gerar relatórios.


## Estrutura do projeto

- `src/` - código-fonte
	- `main.py` - interface de linha de comando
	- `dados.py` - repositório e lógica de disponibilidade
	- `salas.py` - modelos de salas e factory
	- `usuarios.py` - modelos de usuários e factory
	- `reservas.py` - lógica da reserva e notificações
	- `politicas.py` - proxy/strategy para criação de reservas
	- `relatorios.py` - geração de relatórios diários
	- `notificacoes.py` - mecanismo de observadores/notifications


## Exemplos de uso

- Cadastrar uma sala: menu → `1` → escolha tipo, andar, número

- Cadastrar usuário: menu → `2` → escolha tipo, nome

- Criar reserva: menu → `6` → informe `ID` da sala, `ID` do usuário, data e horário


## Exemplo de Menu

```text
1 - Cadastrar sala
2 - Cadastrar usuário
3 - Listar salas
4 - Listar usuários
5 - Listar salas disponíveis
6 - Criar reserva
7 - Modificar reserva
8 - Cancelar reserva
9 - Relatório diário
10 - Cadastrar Limpeza
0 - Sair
```


## Notas de Desenvolvimento

- As validações e regras de prioridade entre usuários estão implementadas em `politicas.py`.
- O sistema de notificações de mudanças utiliza o padrão Observer.
- A criação de usuários e salas utiliza Factory.
- As estratégias e regras de prioridade utilizam Strategy e Proxy.


## Autores

- Ana Beatriz Ribeiro Garcia
- Pedro Marx Amaral Abreu 