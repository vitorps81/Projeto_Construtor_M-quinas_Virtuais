from abc import ABC, abstractmethod
from src.maquina_virtual import MaquinaVirtual
from src.software_componente import ComponenteSoftware 

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

    def com_disco(self, disco_gb: int):
        self.maquina_virtual.disco_gb = disco_gb
        return self

    def instalar_software(self, software: ComponenteSoftware):
        self.maquina_virtual.softwares_instalados.append(software)
        return self

    def configurar_rede(self, configurado: bool):
        self.maquina_virtual.rede_configurada = configurado
        return self

    def get_maquina_virtual(self) -> MaquinaVirtual:
        return self.maquina_virtual
    