from abc import ABC, abstractmethod
from src.maquina_virtual import MaquinaVirtual 

class ObserverVM(ABC):
    
    @abstractmethod
    def atualizar(self, vm: MaquinaVirtual, evento: str):
        pass

class SubjectVM(ABC):
    
    _observers: list[ObserverVM] 

    def __init__(self):
        self._observers = []

    def anexar(self, observer: ObserverVM):
        if observer not in self._observers:
            self._observers.append(observer)

    def desanexar(self, observer: ObserverVM):
        self._observers.remove(observer)

    def notificar(self, vm: MaquinaVirtual, evento: str):
        for observer in self._observers:
            observer.atualizar(vm, evento)

class LoggerVMObserver(ObserverVM):
    
    def atualizar(self, vm: MaquinaVirtual, evento: str):
        print(f"[LOG] {evento}: VM '{vm.sistema_operacional}' - RAM: {vm.ram_gb}GB, CPU: {vm.cpu_cores} Cores")

class MonitoramentoVMObserver(ObserverVM):
    
    def atualizar(self, vm: MaquinaVirtual, evento: str):
        print(f"[MONITORAMENTO] Alerta! Evento '{evento}' na VM {vm.sistema_operacional}. Verificar status.")
