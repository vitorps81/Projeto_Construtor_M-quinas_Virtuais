from src.maquina_virtual_builder import MaquinaVirtualBuilder
from src.linux_vm_builder import LinuxVMBuilder
from src.windows_vm_builder import WindowsVMBuilder
from src.maquina_virtual import MaquinaVirtual

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

    def construir_vm_banco_dados(self, builder: MaquinaVirtualBuilder) -> MaquinaVirtual:
        return (builder
                .definir_sistema_operacional()
                .com_ram(16)
                .com_cpu(4)
                .com_disco(200)
                .instalar_software("PostgreSQL")
                .configurar_rede(True)
                .get_maquina_virtual())

    def construir_vm_web_server(self, builder: MaquinaVirtualBuilder) -> MaquinaVirtual:
        return (builder
                .definir_sistema_operacional()
                .com_ram(4)
                .com_cpu(2)
                .com_disco(100)
                .instalar_software("IIS") 
                .configurar_rede(True)
                .get_maquina_virtual())

if __name__ == "__main__":
    from src.linux_vm_builder import LinuxVMBuilder
    from src.windows_vm_builder import WindowsVMBuilder

    diretor = Diretor()

    print("--- Construindo VM de Desenvolvimento (Linux) ---")
    linux_builder = LinuxVMBuilder()
    vm_dev_linux = diretor.construir_vm_desenvolvimento(linux_builder)
    print(vm_dev_linux)

    print("\n--- Construindo VM de Web Server (Windows) ---")
    windows_builder = WindowsVMBuilder()
    vm_web_windows = diretor.construir_vm_web_server(windows_builder)
    print(vm_web_windows)

    print("\n--- Construindo VM Customizada (Linux) ---")
    custom_linux_builder = LinuxVMBuilder()
    vm_custom = (custom_linux_builder
                 .definir_sistema_operacional()
                 .com_ram(6)
                 .com_cpu(3)
                 .com_disco(75)
                 .instalar_software("Nginx")
                 .configurar_rede(True)
                 .get_maquina_virtual())
    print(vm_custom)
