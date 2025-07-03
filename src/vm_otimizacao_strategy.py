from abc import ABC, abstractmethod
from src.maquina_virtual import MaquinaVirtual 

class EstrategiaOtimizacaoVM(ABC):
    
    @abstractmethod
    def aplicar(self, vm: MaquinaVirtual):
        pass

class OtimizacaoDesempenhoStrategy(EstrategiaOtimizacaoVM):
    
    def aplicar(self, vm: MaquinaVirtual):
        print(f"Aplicando estratégia de Otimização para DESEMPENHO em {vm.sistema_operacional}...")
        vm.cpu_cores = max(vm.cpu_cores, 4) 
        vm.ram_gb = max(vm.ram_gb, 16) 
        vm.disco_gb = max(vm.disco_gb, 80) 

class OtimizacaoEconomiaStrategy(EstrategiaOtimizacaoVM):
    
    def aplicar(self, vm: MaquinaVirtual):
        print(f"Aplicando estratégia de Otimização para ECONOMIA em {vm.sistema_operacional}...")
        vm.cpu_cores = min(vm.cpu_cores, 2) 
        vm.ram_gb = min(vm.ram_gb, 4) 
        vm.disco_gb = max(vm.disco_gb, 150) 
