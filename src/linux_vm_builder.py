from src.maquina_virtual_builder import MaquinaVirtualBuilder

class LinuxVMBuilder(MaquinaVirtualBuilder):
    def definir_sistema_operacional(self):
        # Implementação específica para VMs Linux
        self.maquina_virtual.sistema_operacional = "Linux (Ubuntu Server)"
        return self
    

