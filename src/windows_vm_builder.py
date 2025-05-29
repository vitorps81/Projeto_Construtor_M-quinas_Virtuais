from src.maquina_virtual_builder import MaquinaVirtualBuilder

class WindowsVMBuilder(MaquinaVirtualBuilder):
    def definir_sistema_operacional(self):
        self.maquina_virtual.sistema_operacional = "Windows Server"
        return self
    

