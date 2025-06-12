from src.maquina_virtual_builder import MaquinaVirtualBuilder

class WindowsVMBuilder(MaquinaVirtualBuilder):
    def definir_sistema_operacional(self):
        # Implementação específica para VMs Windows
        self.maquina_virtual.sistema_operacional = "Windows Server"
        return self
    

