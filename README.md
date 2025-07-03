# Construtor de Máquinas Virtuais / Ambientes de Execução

Este projeto demonstra a aplicação prática de **Padrões de Projeto (Design Patterns)** na construção e gerenciamento de máquinas virtuais (VMs) e ambientes de execução. Ao longo de três entregas, foram implementados padrões Criacionais, Estruturais e Comportamentais para promover flexibilidade, reusabilidade e manutenibilidade do código.

---

## 1ª Entrega: Padrões Criacionais - Builder

### Qual(is) padrão(ões) foram utilizados?

Para esta primeira fase do projeto, implementamos o padrão de projeto **Builder**.

### Por que o padrão Builder foi escolhido?

A escolha do padrão **Builder** foi motivada pela complexidade na criação de objetos `MaquinaVirtual`, que podem ter uma vasta gama de configurações e componentes opcionais (sistema operacional, RAM, CPU, disco, softwares instalados, configurações de rede, etc.).

As principais razões para a escolha foram:

* **Simplificação da Construção de Objetos Complexos:** Evita construtores com muitos parâmetros, tornando o processo de criação de VMs mais legível e gerenciável.
* **Construção Passo a Passo:** Permite que a VM seja montada em etapas, adicionando características específicas conforme necessário, sem ter que passar todas as configurações de uma vez.
* **Representações Variadas:** Possibilita a criação de diferentes "tipos" de VMs (ex: VM de Desenvolvimento, VM de Banco de Dados) usando o mesmo processo de construção, mas com diferentes sequências de chamadas aos métodos do Builder.
* **Separação de Preocupações:** O processo de construção (definido nos Builders) é separado da representação final do produto (`MaquinaVirtual`), facilitando a manutenção e a adição de novas características ou tipos de VMs.

### Como foi implementado no projeto?

A implementação do padrão Builder neste projeto segue a estrutura clássica:

* **`MaquinaVirtual` (Produto):**
    Representa a máquina virtual final que está sendo construída. Possui atributos para suas características e um método `__str__` para exibir sua configuração de forma amigável.

    ```python
    # src/maquina_virtual.py
    class MaquinaVirtual:
        def __init__(self):
            self.sistema_operacional = None
            self.ram_gb = 0
            self.cpu_cores = 0
            self.disco_gb = 0
            self.softwares_instalados = []
            self.rede_configurada = False

        def __str__(self):
            softwares = ", ".join(self.softwares_instalados) if self.softwares_instalados else "Nenhum"
            rede = "Configurada" if self.rede_configurada else "Não Configurada"
            return (f"--- Configuração da Máquina Virtual ---\n"
                    f"SO: {self.sistema_operacional}\n"
                    f"RAM: {self.ram_gb} GB\n"
                    f"CPU: {self.cpu_cores} Cores\n"
                    f"Disco: {self.disco_gb} GB\n"
                    f"Softwares: {softwares}\n"
                    f"Rede: {rede}\n"
                    f"----------------------------------------")
    ```

* **`MaquinaVirtualBuilder` (Builder Abstrato):**
    Define a interface para a construção das partes da `MaquinaVirtual`. Ele contém métodos abstratos (como `definir_sistema_operacional`) que são implementados pelos builders concretos, e métodos concretos que retornam `self` para permitir o encadeamento de chamadas (fluent interface).

    ```python
    # src/maquina_virtual_builder.py
    from abc import ABC, abstractmethod
    from src.maquina_virtual import MaquinaVirtual # Import absoluto

    class MaquinaVirtualBuilder(ABC):
        def __init__(self):
            self.maquina_virtual = MaquinaVirtual()

        @abstractmethod
        def definir_sistema_operacional(self):
            pass

        def com_ram(self, ram_gb: int):
            self.maquina_virtual.ram_gb = ram_gb
            return self

        def com_cpu(self, cpu_cores: int):
            self.maquina_virtual.cpu_cores = cpu_cores
            return self
        # ... outros métodos como com_disco, instalar_software, configurar_rede
        # e o método final get_maquina_virtual()
    ```

* **Builders Concretos (`LinuxVMBuilder`, `WindowsVMBuilder`):**
    Implementam a interface `MaquinaVirtualBuilder` para construir tipos específicos de máquinas virtuais, definindo como um sistema operacional em particular é configurado.

    ```python
    # src/linux_vm_builder.py
    from src.maquina_virtual_builder import MaquinaVirtualBuilder # Import absoluto

    class LinuxVMBuilder(MaquinaVirtualBuilder):
        def definir_sistema_operacional(self):
            self.maquina_virtual.sistema_operacional = "Linux (Ubuntu Server)"
            return self
    ```

    ```python
    # src/windows_vm_builder.py
    from src.maquina_virtual_builder import MaquinaVirtualBuilder # Import absoluto

    class WindowsVMBuilder(MaquinaVirtualBuilder):
        def definir_sistema_operacional(self):
            self.maquina_virtual.sistema_operacional = "Windows Server"
            return self
    ```

* **`Diretor` (Director):**
    (Opcional, mas utilizada) Esta classe orquestra a construção de configurações predefinidas de VMs. Ela recebe um objeto `Builder` e invoca seus métodos em uma sequência específica para criar VMs padronizadas (ex: VM para Desenvolvimento, VM para Banco de Dados).

    ```python
    # src/diretor.py
    from src.maquina_virtual_builder import MaquinaVirtualBuilder # Import absoluto
    from src.maquina_virtual import MaquinaVirtual # Import absoluto
    # ... outros imports absolutos necessários para o diretor

    class Diretor:
        def construir_vm_desenvolvimento(self, builder: MaquinaVirtualBuilder) -> MaquinaVirtual:
            return (builder
                    .definir_sistema_operacional()
                    .com_ram(8)
                    .com_cpu(2)
                    .com_disco(50)
                    .instalar_software("Python 3.9")
                    .instalar_software("Docker")
                    .configurar_rede(True)
                    .get_maquina_virtual())
        # ... outros métodos de construção (construir_vm_banco_dados, construir_vm_web_server)
    ```

---

### Passo 4: Como Executar o Projeto

Agora que tudo está configurado, siga estas instruções no seu terminal para rodar os testes e o exemplo:

#### Como Rodar os Testes:

Para rodar os testes unitários e verificar se tudo está funcionando como esperado, navegue até a **pasta raiz do seu projeto** no terminal (por exemplo, `C:\Users\VITORSARAIVADESOUZA\Documents\Construtor_Máquinas_Virtuais`) e execute o seguinte comando:

```bash
# Primeiro, navegue até a pasta raiz do seu projeto
cd C:\Users\VITORSARAIVADESOUZA\Documents\Construtor_Máquinas_Virtuais

# Em seguida, execute os testes
python -m unittest discover test

---

## 2ª Entrega: Padrões Estruturais - Composite e Facade

Nesta segunda fase do projeto, foram adicionados os padrões estruturais **Composite** e **Facade** para aumentar a flexibilidade na composição de softwares e simplificar a interface de uso do subsistema de construção de VMs.

### Padrão Composite: Gerenciamento Flexível de Softwares

* **Por que foi escolhido?**
    O padrão Composite foi escolhido para lidar com a complexidade da instalação de softwares em máquinas virtuais. Uma VM pode precisar de softwares individuais (ex: "Python") ou de um conjunto de softwares que funcionam como uma unidade (ex: "Stack LAMP"). O Composite permite tratar tanto softwares individuais quanto grupos de softwares de forma uniforme, sem que o cliente precise distinguir entre eles.

* **Como foi implementado?**
    1.  **`ComponenteSoftware` (Interface):** Uma classe abstrata (`src/software_componente.py`) que define a interface comum (`get_nome()`) para todos os componentes de software.
    2.  **`SoftwareIndividual` (Folha):** Uma classe concreta (`src/software_componente.py`) que implementa `ComponenteSoftware` e representa um único software.
    3.  **`GrupoSoftware` (Composite):** Uma classe (`src/software_composite.py`) que também implementa `ComponenteSoftware` e pode conter uma coleção de outros `ComponenteSoftware` (folhas ou outros composites). Seu método `get_nome()` agrega os nomes de seus filhos.
    4.  A classe `MaquinaVirtual` foi modificada para armazenar objetos `ComponenteSoftware` em sua lista `softwares_instalados`.
    5.  O método `instalar_software` no `MaquinaVirtualBuilder` agora aceita objetos `ComponenteSoftware`.
    6.  O `Diretor` utiliza `SoftwareIndividual` e `GrupoSoftware` para compor as configurações de software das VMs predefinidas (ex: "Dev Stack Python").

    ```python
    # Exemplo de uso do Composite no Diretor
    from src.software_componente import SoftwareIndividual
    from src.software_composite import GrupoSoftware

    dev_stack = GrupoSoftware("Dev Stack Python")
    dev_stack.adicionar(SoftwareIndividual("Python 3.9"))
    dev_stack.adicionar(SoftwareIndividual("Docker"))
    # ...

    builder.instalar_software(dev_stack)
    ```

### Padrão Facade: Simplificando a Interação com o Subsistema

* **Por que foi escolhido?**
    O padrão Facade foi escolhido para simplificar a interface para o subsistema complexo de construção de VMs. O cliente não precisa interagir diretamente com o `Diretor`, `Builders` específicos ou a `MaquinaVirtual` para criar uma VM comum. A Facade oferece um conjunto de métodos de alto nível para operações frequentemente usadas.

* **Como foi implementado?**
    1.  **`GerenciadorVM` (Facade):** Uma nova classe (`src/vm_facade.py`) que encapsula a complexidade do subsistema de construção de VMs.
    2.  Possui métodos simples como `criar_vm_desenvolvimento_linux()`, `criar_vm_web_server_windows()`, etc.
    3.  Internamente, a `GerenciadorVM` utiliza instâncias do `Diretor` e dos `Builders` para realizar as operações, escondendo os detalhes de implementação do cliente.

    ```python
    # Exemplo de uso da Facade
    from src.vm_facade import GerenciadorVM

    gerenciador = GerenciadorVM()
    vm_dev = gerenciador.criar_vm_desenvolvimento_linux()
    print(vm_dev)
    ```

---

### Como Rodar os Testes:

Para rodar os testes unitários e verificar se tudo está funcionando como esperado, navegue até a **pasta raiz do seu projeto** no terminal (por exemplo, `C:\Users\VITORSARAIVADESOUZA\Documents\Construtor_Máquinas_Virtuais`) e execute o seguinte comando:

```bash
# Primeiro, navegue até a pasta raiz do seu projeto
cd C:\Users\VITORSARAIVADESOUZA\Documents\Construtor_Máquinas_Virtuais

# Em seguida, execute os testes (inclui testes para Composite e Facade)
python -m unittest discover test

## 3ª Entrega: Padrões Comportamentais - Strategy e Observer

Nesta última fase do projeto, foram adicionados os padrões comportamentais **Strategy** e **Observer** para introduzir comportamentos flexíveis e um mecanismo de notificação de eventos, aprimorando a interatividade e a capacidade de extensão do sistema.

### Padrão Strategy: Estratégias de Otimização da VM

* **Por que foi escolhido?**
    O padrão Strategy foi selecionado para permitir que diferentes algoritmos de otimização de recursos (RAM, CPU, Disco) sejam aplicados a uma `MaquinaVirtual` de forma intercambiável em tempo de execução. Isso evita a necessidade de criar múltiplas subclasses de VM para cada combinação de otimização, promovendo flexibilidade e reusabilidade.

* **Como foi implementado?**
    1.  **`EstrategiaOtimizacaoVM` (Interface):** Uma classe abstrata (`src/vm_otimizacao_strategy.py`) que define o método `aplicar(vm: MaquinaVirtual)` para todas as estratégias.
    2.  **`OtimizacaoDesempenhoStrategy` e `OtimizacaoEconomiaStrategy` (Estratégias Concretas):** Classes (`src/vm_otimizacao_strategy.py`) que implementam a interface, definindo regras específicas para otimização de desempenho ou economia de recursos.
    3.  A classe `GerenciadorVM` (Facade) foi estendida para aceitar uma `EstrategiaOtimizacaoVM` opcional ao criar VMs, aplicando a estratégia antes de finalizar a construção.

    ```python
    # Exemplo de uso do Strategy na Facade
    from src.vm_otimizacao_strategy import OtimizacaoDesempenhoStrategy

    gerenciador = GerenciadorVM()
    estrategia_desempenho = OtimizacaoDesempenhoStrategy()
    vm_dev = gerenciador.criar_vm_desenvolvimento_linux(estrategia_desempenho)
    # A VM 'vm_dev' terá seus recursos ajustados pela estratégia de desempenho
    ```

### Padrão Observer: Notificações de Eventos da VM

* **Por que foi escolhido?**
    O padrão Observer foi implementado para criar um mecanismo de notificação para eventos importantes do ciclo de vida das VMs, como sua criação. Isso permite que múltiplos componentes do sistema (como loggers, sistemas de monitoramento) reajam a esses eventos de forma desacoplada, sem que o objeto `MaquinaVirtual` ou a Facade precise saber sobre eles diretamente.

* **Como foi implementado?**
    1.  **`ObserverVM` (Interface):** Uma classe abstrata (`src/vm_observer.py`) que define o método `atualizar(vm: MaquinaVirtual, evento: str)` para todos os observadores.
    2.  **`SubjectVM` (Interface):** Uma classe abstrata (`src/vm_observer.py`) que define métodos para anexar, desanexar e notificar observadores. A classe `GerenciadorVM` herda de `SubjectVM`.
    3.  **`LoggerVMObserver` e `MonitoramentoVMObserver` (Observadores Concretos):** Classes (`src/vm_observer.py`) que implementam a interface `ObserverVM` e simulam o registro de logs e alertas de monitoramento, respectivamente.
    4.  A classe `GerenciadorVM` (Facade) foi adaptada para atuar como o "Subject" que notifica seus observadores cada vez que uma VM é criada ou seu estado relevante é alterado.

    ```python
    # Exemplo de uso do Observer na Facade
    from src.vm_observer import LoggerVMObserver, MonitoramentoVMObserver
    from src.vm_facade import GerenciadorVM

    gerenciador = GerenciadorVM()
    logger = LoggerVMObserver()
    monitor = MonitoramentoVMObserver()

    gerenciador.anexar(logger)
    gerenciador.anexar(monitor)

    vm_criada = gerenciador.criar_vm_desenvolvimento_linux()
    # Ao final da criação, o logger e o monitor serão notificados automaticamente.
    ```

---

### Como Rodar os Testes:

Para rodar os testes unitários e verificar se tudo está funcionando como esperado, navegue até a **pasta raiz do seu projeto** no terminal (por exemplo, `C:\Users\SEU_USUARIO\Documents\Construtor_Máquinas_Virtuais`) e execute o seguinte comando:

```bash
# Primeiro, navegue até a pasta raiz do seu projeto
cd C:\Users\SEU_USUARIO\Documents\Construtor_Máquinas_Virtuais

# Em seguida, execute os testes (inclui testes para todos os padrões)
python -m unittest discover test
