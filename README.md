# Construtor de Máquinas Virtuais / Ambientes de Execução

Este projeto demonstra a aplicação do padrão de projeto **Builder** para a construção incremental e flexível de máquinas virtuais (VMs) e ambientes de execução.

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

