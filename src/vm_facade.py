from src.diretor import Diretor
from src.linux_vm_builder import LinuxVMBuilder
from src.windows_vm_builder import WindowsVMBuilder
from src.maquina_virtual import MaquinaVirtual

class GerenciadorVM:

    def __init__(self):
        self._diretor = Diretor()
        self._linux_builder = LinuxVMBuilder()
        self._windows_builder = WindowsVMBuilder()

    def criar_vm_desenvolvimento_linux(self) -> MaquinaVirtual:
        print("Criando VM de Desenvolvimento (Linux) via Facade...")
        return self._diretor.construir_vm_desenvolvimento(self._linux_builder)

    def criar_vm_web_server_windows(self) -> MaquinaVirtual:
        print("Criando VM de Web Server (Windows) via Facade...")
        return self._diretor.construir_vm_web_server(self._windows_builder)

    def criar_vm_banco_dados_linux(self) -> MaquinaVirtual:
        print("Criando VM de Banco de Dados (Linux) via Facade...")
        return self._diretor.construir_vm_banco_dados(self._linux_builder)

if __name__ == "__main__":
    gerenciador = GerenciadorVM()

    vm1 = gerenciador.criar_vm_desenvolvimento_linux()
    print(vm1)

    print("\n" + "="*50 + "\n") # Separador

    vm2 = gerenciador.criar_vm_web_server_windows()
    print(vm2)
