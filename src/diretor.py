from src.maquina_virtual_builder import MaquinaVirtualBuilder
from src.linux_vm_builder import LinuxVMBuilder
from src.windows_vm_builder import WindowsVMBuilder
from src.maquina_virtual import MaquinaVirtual
from src.software_componente import SoftwareIndividual
from src.software_composite import GrupoSoftware

class Diretor:

    def construir_vm_desenvolvimento(self, builder: MaquinaVirtualBuilder) -> MaquinaVirtual:
        dev_stack = GrupoSoftware("Dev Stack Python")
        dev_stack.adicionar(SoftwareIndividual("Python 3.9"))
        dev_stack.adicionar(SoftwareIndividual("Docker"))
        dev_stack.adicionar(SoftwareIndividual("Git"))

        return (builder
                .definir_sistema_operacional()
                .com_ram(8)
                .com_cpu(2)
                .com_disco(50)
                .instalar_software(dev_stack) 
                .configurar_rede(True)
                .get_maquina_virtual())

    def construir_vm_banco_dados(self, builder: MaquinaVirtualBuilder) -> MaquinaVirtual:
        return (builder
                .definir_sistema_operacional()
                .com_ram(16)
                .com_cpu(4)
                .com_disco(200)
                .instalar_software(SoftwareIndividual("PostgreSQL")) 
                .configurar_rede(True)
                .get_maquina_virtual())

    def construir_vm_web_server(self, builder: MaquinaVirtualBuilder) -> MaquinaVirtual:
        web_server_bundle = GrupoSoftware("Web Server Bundle")
        web_server_bundle.adicionar(SoftwareIndividual("IIS")) 
        web_server_bundle.adicionar(SoftwareIndividual("ASP.NET Core Runtime"))

        return (builder
                .definir_sistema_operacional()
                .com_ram(4)
                .com_cpu(2)
                .com_disco(100)
                .instalar_software(web_server_bundle) 
                .configurar_rede(True)
                .get_maquina_virtual())

if __name__ == "__main__":

    diretor = Diretor()
    linux_builder = LinuxVMBuilder()
    vm_dev_linux = diretor.construir_vm_desenvolvimento(linux_builder)
    print(vm_dev_linux)

    custom_linux_builder = LinuxVMBuilder()
    custom_software_bundle = GrupoSoftware("Ferramentas Customizadas")
    custom_software_bundle.adicionar(SoftwareIndividual("Nginx"))
    custom_software_bundle.adicionar(SoftwareIndividual("Certbot"))

    vm_custom = (custom_linux_builder
                 .definir_sistema_operacional()
                 .com_ram(6)
                 .com_cpu(3)
                 .com_disco(75)
                 .instalar_software(custom_software_bundle) 
                 .configurar_rede(True)
                 .get_maquina_virtual())
    print(vm_custom)
