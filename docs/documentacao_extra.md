# Documentacao extra do projeto

Este documento complementa o `README.md` e o diagrama de classes em `docs/DiagramaDeClasses.png`. Ele serve como guia para novos usuarios entenderem o papel de cada modulo, classe e fluxo do sistema de reserva de salas de estudo.

## Visao geral

O projeto implementa uma aplicacao de linha de comando para reservar salas de estudo em um campus universitario. O sistema permite cadastrar salas e usuarios, consultar disponibilidade por periodo, criar reservas, modificar reservas, cancelar reservas, emitir notificacoes e gerar relatorio diario.

Os dados ficam em memoria durante a execucao. Ao encerrar o programa, as salas, usuarios e reservas cadastradas deixam de existir, pois nao ha banco de dados ou arquivo de persistencia.

## Estrutura principal

```text
src/
  main.py           Interface de linha de comando e orquestracao dos fluxos.
  salas.py          Modelos de salas e factory de criacao.
  usuarios.py       Modelos de usuarios e factory de criacao.
  reservas.py       Entidade Reserva, status e alteracoes/cancelamentos.
  politicas.py      Estrategias de reserva, proxy de validacao e decorator.
  dados.py          Repositorio singleton em memoria.
  notificacoes.py   Contratos e implementacao do Observer.
  relatorios.py     Geracao do relatorio diario.

docs/
  DiagramaDeClasses.png
  documentacao_extra.md
```

## Como o sistema funciona

1. O usuario executa `python3 src/main.py`.
2. `main.py` cria uma instancia de `RepositorioReservas`.
3. Pelo menu, o usuario cadastra salas e usuarios.
4. Ao criar uma reserva, `main.py` escolhe a estrategia adequada:
   - `PrimeiraReserva` para alunos e usuarios comuns.
   - `PrioridadeProfessor` para professores.
5. `ProxyReserva` valida data, horario e formato do horario.
6. A estrategia consulta `RepositorioReservas` para detectar colisao.
7. Se a reserva for valida, uma instancia de `Reserva` e criada ou uma reserva existente e alterada.
8. Alteracoes e cancelamentos disparam notificacoes via `NotificadorReservas`.
9. O relatorio diario consulta o repositorio e lista apenas reservas confirmadas.

## Regras de negocio

- Uma reserva usa uma sala, uma data e um horario cheio.
- Os horarios permitidos vao de `08:00` ate `17:00`.
- O horario precisa ter minuto igual a `00`.
- Nao e permitido criar reserva em data/hora passada.
- Uma sala nao pode ter duas reservas confirmadas na mesma data e horario.
- Professores possuem prioridade sobre reservas feitas por usuarios que nao sao professores.
- Um professor nao pode sobrescrever reserva de outro professor.
- Reservas canceladas nao bloqueiam a disponibilidade futura da sala.
- O relatorio diario mostra somente reservas com status `Confirmada`.

## `src/main.py`

Modulo responsavel pela interface de linha de comando. Ele nao define entidades do dominio; apenas coleta entradas do usuario, chama factories, consulta o repositorio e direciona as operacoes para as classes corretas.

### Variavel global `repositorio`

Instancia de `RepositorioReservas`. Como essa classe usa Singleton, qualquer outro ponto do projeto que chame `RepositorioReservas()` acessa a mesma instancia em memoria.

### Funcoes

- `menu()`: imprime as opcoes disponiveis no terminal.
- `cadastrar_sala()`: pergunta tipo, andar e numero; cria a sala com `SalaFactory.create()`; salva no repositorio.
- `cadastrar_usuario()`: pergunta tipo e nome; cria o usuario com `UsuarioFactory.create()`; salva no repositorio.
- `listar_salas()`: exibe todas as salas cadastradas, incluindo id, numero, andar e tipo.
- `listar_usuarios()`: exibe todos os usuarios cadastrados, incluindo id, nome e tipo.
- `listar_salas_disponiveis()`: recebe data inicial e final; chama `listar_horarios_disponiveis_por_periodo()` no repositorio; imprime os horarios livres por sala e data.
- `criar_reserva()`: recebe sala, usuario, data e horario; escolhe `PrioridadeProfessor` se o usuario for professor, caso contrario usa `PrimeiraReserva`; cria a reserva por meio de `ProxyReserva`.
- `criar_reserva_limpeza()`: cria uma reserva de limpeza usando `DecoratorLimpeza` e o usuario fixo de manutencao.
- `modificar_reserva()`: lista reservas, seleciona uma pelo id e permite alterar horario, data ou sala. A propria classe `Reserva` valida conflitos e regras de prioridade.
- `cancelar_reserva()`: seleciona uma reserva pelo id e chama `cancelar_reserva()`.
- `gerar_relatorio_diario()`: recebe uma data e imprime o resultado de `RelatorioDiario.gerar()`.
- `executar()`: loop principal do sistema. Le a opcao do menu e chama a funcao correspondente ate o usuario escolher sair.

## `src/salas.py`

Modulo que representa os tipos de sala disponiveis no sistema e centraliza sua criacao.

### Classe `Sala`

Classe abstrata base para todas as salas. Define os atributos comuns:

- `_id`: identificador unico gerado automaticamente.
- `_andar`: andar onde a sala fica.
- `_numero`: numero da sala.

Metodos principais:

- `get_andar()`: retorna o andar.
- `get_numero()`: retorna o numero.
- `get_id()`: retorna o identificador unico.
- `capacidade()`: metodo abstrato que cada subtipo precisa implementar.
- `tipo()`: metodo abstrato que cada subtipo precisa implementar.
- `__str__()`: retorna uma descricao textual da sala.

### Classe `SalaIndividual`

Subclasse de `Sala` para salas individuais.

- `capacidade()`: retorna `1`.
- `tipo()`: retorna `"Individual"`.

### Classe `SalaGrupo`

Subclasse de `Sala` para salas de trabalho em grupo.

- `capacidade()`: retorna `30`.
- `tipo()`: retorna `"Grupo"`.

### Classe `Laboratorio`

Subclasse de `Sala` para laboratorios.

- `capacidade()`: retorna `25`.
- `tipo()`: retorna `"Laboratório"`.

### Classe `SalaFactory`

Implementa o padrao Factory Method para criar salas sem acoplar o menu as classes concretas.

- `_types`: dicionario que associa texto de entrada a classe concreta.
- Tipos aceitos atualmente: `"Sala Individual"`, `"Sala Grupo"` e `"Laboratório"`.
- `create(sala_type, andar, numero)`: cria e retorna a sala solicitada. Lanca `ValueError` se o tipo for invalido.

## `src/usuarios.py`

Modulo que representa os usuarios do sistema e centraliza sua criacao.

### Classe `Usuario`

Classe abstrata base para usuarios.

Atributos:

- `_id`: identificador unico gerado automaticamente.
- `_nome`: nome do usuario.

Metodos:

- `get_id()`: retorna o id.
- `get_nome()`: retorna o nome.
- `tipo()`: metodo abstrato que cada subtipo implementa.
- `__str__()`: retorna uma descricao textual do usuario.

### Classe `Professor`

Representa professor. Tem prioridade sobre reservas feitas por alunos ou manutencao.

- `tipo()`: retorna `"Professor"`.

### Classe `Aluno`

Representa estudante.

- `tipo()`: retorna `"Aluno"`.

### Classe `Manutencao`

Representa funcionario ou usuario de manutencao.

- `tipo()`: retorna `"Manutenção"`.

### Classe `UsuarioFactory`

Factory responsavel por criar usuarios.

- `_types`: mapeia `"Professor"`, `"Aluno"` e `"Manutenção"` para suas classes.
- Tipos aceitos atualmente: `"Professor"`, `"Aluno"` e `"Manutenção"`.
- `create(usuario_type, nome)`: retorna uma instancia do tipo pedido. Lanca `ValueError` se o tipo for invalido.

## `src/reservas.py`

Modulo da entidade central do sistema: a reserva.

### Enum `StatusReserva`

Define os estados possiveis:

- `CONFIRMADA`: reserva ativa.
- `CANCELADA`: reserva cancelada, nao bloqueia horario.
- `FINALIZADA`: estado previsto para reserva encerrada, embora nao seja usado no fluxo atual do menu.

### Classe `Reserva`

Representa uma reserva feita por um usuario em uma sala, data e horario.

Atributos principais:

- `_id`: identificador unico.
- `_sala`: sala reservada.
- `_usuario`: usuario responsavel.
- `_data`: data da reserva.
- `_horario`: horario inicial.
- `_status`: status da reserva.
- `_notificador`: notificador proprio da reserva.

Constantes:

- `EVENTO_ALTERADA`: texto usado em notificacoes de alteracao.
- `EVENTO_CANCELADA`: texto usado em notificacoes de cancelamento.

Metodos de consulta:

- `get_usuario()`: retorna o usuario responsavel.
- `get_sala()`: retorna a sala.
- `get_data()`: retorna a data.
- `get_horario()`: retorna o horario.
- `get_id()`: retorna o id.
- `get_status()`: retorna o status.

Metodos de observacao:

- `adicionar_observador(observer)`: adiciona um observador interessado na reserva.
- `remover_observador(observer)`: remove um observador.
- `_notificar(evento)`: notifica observadores da reserva e tambem observadores globais do repositorio.
- `_adicionar_observador_usuario(usuario)`: cria um `ObserverUsuario` para o usuario informado.

Metodos de alteracao:

- `cancelar_reserva()`: muda o status para `CANCELADA` e notifica os envolvidos.
- `set_usuario(usuario)`: troca o usuario responsavel, registra observadores e notifica alteracao.
- `set_sala(sala)`: tenta mover a reserva para outra sala. Se houver conflito, so permite a troca quando o usuario atual for professor e a reserva conflitante nao for de professor.
- `set_horario(horario)`: tenta alterar o horario com a mesma regra de conflito.
- `set_data(data)`: tenta alterar a data com a mesma regra de conflito.

Metodos auxiliares:

- `_validar_data_horario(data, horario)`: impede data/hora passada e horarios fora de `08:00` a `17:00`.
- `__str__()`: retorna a reserva formatada para exibicao no terminal.

## `src/politicas.py`

Modulo das politicas de criacao de reserva. Ele concentra Strategy, Proxy e Decorator.

### Classe `StrategyReserva`

Interface abstrata para estrategias de reserva.

- `nova_reserva(sala, usuario, data, horario)`: metodo que as estrategias concretas implementam.

### Classe `PrimeiraReserva`

Estrategia padrao: a primeira reserva valida ocupa o horario.

- Consulta `GetReserva.get_reserva()`.
- Se nao houver reserva conflitante, cria uma nova `Reserva`.
- Se houver conflito, lanca `ValueError("Sala ja reservada")`.

### Classe `PrioridadeProfessor`

Estrategia para professores.

- Se nao houver conflito, cria uma nova `Reserva`.
- Se a reserva existente tambem for de professor, lanca erro.
- Se a reserva existente for de outro tipo de usuario, troca o usuario da reserva existente para o professor.

### Classe `ProxyReserva`

Proxy usado antes da estrategia concreta.

Responsabilidades:

- Guardar a estrategia atual.
- Permitir troca em tempo de execucao com `alterar_strategy()`.
- Validar se data/hora nao estao no passado.
- Validar se o horario esta entre `08:00` e `17:00` e se os minutos sao `00`.
- Delegar a criacao para `strategy.nova_reserva()`.

Metodos:

- `__init__(strategy)`: recebe a estrategia inicial.
- `alterar_strategy(nova_strategy)`: troca a estrategia.
- `criar_reserva(sala, usuario, data, horario)`: valida e cria a reserva.

### Classe `GetReserva`

Classe utilitaria para consultar conflito de reserva.

- `get_reserva(sala, data, horario)`: busca no `RepositorioReservas` uma reserva ativa para a mesma sala, data e horario.

### Classe `DecoratorLimpeza`

Decorator usado para criar reserva de limpeza como extensao opcional.

- `user_limpeza`: usuario fixo de `"Manutenção"` chamado `"Limpeza"`.
- `__init__(strategy)`: recebe uma estrategia base.
- `nova_reserva(sala, usuario, data, horario)`: valida data e horario, impede conflito e delega para a estrategia base usando `user_limpeza`, ignorando o usuario recebido como argumento.

## `src/dados.py`

Modulo do repositorio em memoria. Ele usa Singleton para manter uma unica instancia compartilhada por todo o sistema.

### Classe `RepositorioReservas`

Responsavel por armazenar salas, usuarios, reservas e observadores globais.

Atributos de classe:

- `_instance`: guarda a instancia unica.
- `_lock`: lock usado no `__new__()` para criacao thread-safe.
- `HORARIOS_DISPONIVEIS`: lista dos horarios padrao de reserva.

Atributos da instancia:

- `salas`: lista de salas cadastradas.
- `usuarios`: lista de usuarios cadastrados.
- `reservas`: lista de reservas criadas.
- `_notificador`: notificador global de eventos de reserva.
- `_data_lock`: lock reentrante para proteger acesso aos dados.

Metodos de ciclo de vida:

- `__new__()`: garante que so exista uma instancia.
- `_inicializar()`: inicializa listas, notificador e lock de dados.
- `limpar()`: limpa salas, usuarios, reservas e observadores. E util para testes ou reinicio manual do estado.

Metodos de cadastro:

- `adicionar_sala(sala)`: salva uma sala.
- `adicionar_usuario(usuario)`: salva um usuario.
- `adicionar_reserva(reserva)`: salva uma reserva.

Metodos de observadores:

- `adicionar_observador(observer)`: adiciona observador global.
- `remover_observador(observer)`: remove observador global.
- `notificar_evento_reserva(evento, reserva)`: dispara evento pelo notificador global.

Metodos de listagem:

- `listar_salas()`: retorna copia da lista de salas.
- `listar_usuarios()`: retorna copia da lista de usuarios.
- `listar_reservas()`: retorna copia da lista de reservas.
- `listar_reservas_por_data(data)`: retorna reservas da data informada.
- `listar_reservas_por_sala(sala)`: retorna reservas da sala informada.

Metodos de busca:

- `buscar_sala_por_id(sala_id)`: retorna sala pelo id ou `None`.
- `buscar_usuario_por_id(usuario_id)`: retorna usuario pelo id ou `None`.
- `buscar_reserva_por_id(reserva_id)`: retorna reserva pelo id ou `None`.
- `buscar_reserva_por_sala_data_horario(sala, data, horario)`: retorna uma reserva que bloqueia aquele horario ou `None`.

Metodos de disponibilidade:

- `sala_esta_disponivel(sala, data, horario)`: retorna `True` quando nenhuma reserva ativa bloqueia o horario.
- `listar_salas_disponiveis(data_inicio, data_fim, horario)`: lista salas livres em um horario fixo ao longo de um periodo.
- `listar_horarios_disponiveis_por_periodo(data_inicio, data_fim)`: lista horarios livres por sala e por data.

Metodos auxiliares:

- `_reserva_bloqueia_horario(reserva, sala, data, horario)`: verifica se uma reserva ativa ocupa a mesma sala, data e horario.
- `_reserva_esta_cancelada(reserva)`: identifica se a reserva esta cancelada.

## `src/notificacoes.py`

Modulo que implementa o padrao Observer.

### Classe `Observer`

Interface abstrata para observadores.

- `update(evento, reserva)`: metodo chamado quando ocorre uma alteracao.

### Classe `Subject`

Interface abstrata para objetos observaveis.

- `adicionar_observador(observer)`: registra observador.
- `remover_observador(observer)`: remove observador.
- `notificar(evento, reserva)`: envia evento aos observadores.

### Classe `ObserverUsuario`

Observer concreto associado a um usuario.

- `__init__(usuario)`: guarda o usuario que sera notificado.
- `__eq__(other)`: evita observadores duplicados para o mesmo usuario.
- `__hash__()`: permite comparacao baseada no id do usuario.
- `update(evento, reserva)`: imprime a notificacao no terminal. O metodo recebe o evento e a reserva, entao combina push e pull: o evento chega pronto e o observer tambem consulta dados da reserva.

### Classe `NotificadorReservas`

Subject concreto que mantem uma lista de observadores.

- `__init__()`: inicializa a lista de observers.
- `adicionar_observador(observer)`: adiciona se ainda nao existir.
- `remover_observador(observer)`: remove se existir.
- `remover_observer(observer)`: alias para `remover_observador()`.
- `limpar_observadores()`: remove todos os observers.
- `notificar(evento, reserva)`: chama `update()` em cada observer.

## `src/relatorios.py`

Modulo responsavel por gerar relatorios textuais.

### Classe `RelatorioDiario`

Gera o relatorio diario de reservas confirmadas.

- `__init__(repositorio=None)`: usa o repositorio recebido ou cria/acessa o `RepositorioReservas` singleton.
- `gerar(data)`: busca reservas da data, filtra as confirmadas, agrupa por sala e monta uma string com intervalos de uma hora.
- `_reserva_esta_confirmada(reserva)`: retorna `True` apenas quando o status da reserva e `"Confirmada"`.

## Padroes de projeto aplicados

### Factory Method

Usado em:

- `SalaFactory`
- `UsuarioFactory`

Objetivo: criar objetos com base em um tipo textual sem espalhar `if/else` e conhecimento das classes concretas pelo sistema.

### Strategy

Usado em:

- `StrategyReserva`
- `PrimeiraReserva`
- `PrioridadeProfessor`

Objetivo: permitir trocar a politica de tratamento de conflitos em tempo de execucao. O menu escolhe a estrategia com base no tipo de usuario.

### Observer

Usado em:

- `Observer`
- `Subject`
- `ObserverUsuario`
- `NotificadorReservas`
- Integracao com `Reserva`

Objetivo: notificar usuarios ou servicos interessados quando uma reserva for alterada ou cancelada.

### Singleton

Usado em:

- `RepositorioReservas`

Objetivo: manter um unico repositorio em memoria compartilhado entre os modulos.

### Proxy

Usado em:

- `ProxyReserva`

Objetivo: centralizar validacoes comuns antes de chamar a estrategia de criacao de reserva.

### Decorator

Usado em:

- `DecoratorLimpeza`

Objetivo: adicionar o comportamento de reserva de limpeza sem alterar as strategies existentes.

## Fluxos importantes

### Criacao de reserva comum

```text
main.criar_reserva()
  -> busca sala e usuario no RepositorioReservas
  -> escolhe PrimeiraReserva ou PrioridadeProfessor
  -> ProxyReserva.criar_reserva()
  -> StrategyReserva.nova_reserva()
  -> Reserva(...)
  -> RepositorioReservas.adicionar_reserva()
```

### Alteracao de reserva

```text
main.modificar_reserva()
  -> RepositorioReservas.buscar_reserva_por_id()
  -> Reserva.set_horario(), Reserva.set_data() ou Reserva.set_sala()
  -> validacao de data/horario
  -> busca de conflito no RepositorioReservas
  -> alteracao ou erro
  -> notificacao dos observadores
```

### Cancelamento de reserva

```text
main.cancelar_reserva()
  -> RepositorioReservas.buscar_reserva_por_id()
  -> Reserva.cancelar_reserva()
  -> status muda para CANCELADA
  -> notificacao dos observadores
```

### Consulta de disponibilidade

```text
main.listar_salas_disponiveis()
  -> RepositorioReservas.listar_horarios_disponiveis_por_periodo()
  -> RepositorioReservas.sala_esta_disponivel()
  -> ignora reservas canceladas
  -> retorna horarios livres por data e sala
```

### Relatorio diario

```text
main.gerar_relatorio_diario()
  -> RelatorioDiario.gerar(data)
  -> RepositorioReservas.listar_reservas_por_data(data)
  -> filtra status Confirmada
  -> agrupa por sala
  -> retorna texto do relatorio
```

## Como adicionar novos recursos

### Novo tipo de sala

1. Criar uma subclasse de `Sala` em `salas.py`.
2. Implementar `capacidade()` e `tipo()`.
3. Adicionar a classe no dicionario `SalaFactory._types`.
4. Adicionar uma opcao em `main.cadastrar_sala()`.

### Novo tipo de usuario

1. Criar uma subclasse de `Usuario` em `usuarios.py`.
2. Implementar `tipo()`.
3. Adicionar a classe em `UsuarioFactory._types`.
4. Adicionar uma opcao em `main.cadastrar_usuario()`.

### Nova politica de reserva

1. Criar uma classe em `politicas.py` herdando de `StrategyReserva`.
2. Implementar `nova_reserva()`.
3. Escolher em qual ponto do menu ou fluxo ela sera usada.
4. Passar a nova estrategia para `ProxyReserva` ou chamar `alterar_strategy()`.

### Novo observador

1. Criar uma classe que herde de `Observer`.
2. Implementar `update(evento, reserva)`.
3. Registrar o observador em uma `Reserva` ou no `RepositorioReservas`.

## Pontos de atencao para novos usuarios

- O projeto usa imports simples como `from dados import RepositorioReservas`, portanto o comando recomendado e executar a partir da raiz com `python3 src/main.py`.
- O estado e em memoria. Cadastros precisam ser refeitos a cada execucao.
- IDs de salas, usuarios e reservas sao sequenciais e gerados por variaveis de classe.
- Algumas mensagens e nomes internos usam acentos; ao alterar factories, mantenha os textos iguais aos usados pelo menu.
- `RepositorioReservas.limpar()` limpa os dados, mas nao reinicia automaticamente os contadores de id das classes.
- A classe `StatusReserva` possui `FINALIZADA`, mas o menu atual nao oferece fluxo para finalizar reservas.
