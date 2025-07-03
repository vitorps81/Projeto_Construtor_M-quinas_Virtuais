from src.diretor import Diretor
from src.linux_vm_builder import LinuxVMBuilder
from src.windows_vm_builder import WindowsVMBuilder
from src.maquina_virtual import MaquinaVirtual
from src.vm_otimizacao_strategy import EstrategiaOtimizacaoVM, OtimizacaoDesempenhoStrategy, OtimizacaoEconomiaStrategy
from src.vm_observer import SubjectVM, LoggerVMObserver, MonitoramentoVMObserver 

class GerenciadorVM(SubjectVM): 
    
    def __init__(self):
        super().__init__() 
        self._diretor = Diretor()
        self._linux_builder = LinuxVMBuilder()
        self._windows_builder = WindowsVMBuilder()

    def _criar_e_notificar(self, vm_type: str, builder, estrategia: EstrategiaOtimizacaoVM = None) -> MaquinaVirtual:
        vm = None
        if vm_type == "dev_linux":
            vm = self._diretor.construir_vm_desenvolvimento(builder)
        elif vm_type == "web_windows":
            vm = self._diretor.construir_vm_web_server(builder)
        elif vm_type == "db_linux":
            vm = self._diretor.construir_vm_banco_dados(builder)

        if vm and estrategia:
            estrategia.aplicar(vm)

        if vm:
            self.notificar(vm, f"VM {vm_type.replace('_', ' ').title()} Criada")
        return vm

    def criar_vm_desenvolvimento_linux(self, estrategia: EstrategiaOtimizacaoVM = None) -> MaquinaVirtual:
        print("Criando VM de Desenvolvimento (Linux) via Facade...")
        return self._criar_e_notificar("dev_linux", self._linux_builder, estrategia)

    def criar_vm_web_server_windows(self, estrategia: EstrategiaOtimizacaoVM = None) -> MaquinaVirtual:
        print("Criando VM de Web Server (Windows) via Facade...")
        return self._criar_e_notificar("web_windows", self._windows_builder, estrategia)

    def criar_vm_banco_dados_linux(self, estrategia: EstrategiaOtimizacaoVM = None) -> MaquinaVirtual:
        print("Criando VM de Banco de Dados (Linux) via Facade...")
        return self._criar_e_notificar("db_linux", self._linux_builder, estrategia)


if __name__ == "__main__":
    gerenciador = GerenciadorVM()

    logger = LoggerVMObserver()
    monitor = MonitoramentoVMObserver()
    gerenciador.anexar(logger)
    gerenciador.anexar(monitor)

    print("--- Teste com Estratégia de Desempenho ---")
    estrategia_desempenho = OtimizacaoDesempenhoStrategy()
    vm1 = gerenciador.criar_vm_desenvolvimento_linux(estrategia_desempenho)
    print(vm1)

    print("\n" + "="*50 + "\n") 

    print("--- Teste com Estratégia de Economia ---")
    estrategia_economia = OtimizacaoEconomiaStrategy()
    vm2 = gerenciador.criar_vm_web_server_windows(estrategia_economia)
    print(vm2)

    print("\n" + "="*50 + "\n") 

    print("--- Teste sem Estratégia Específica ---")
    vm3 = gerenciador.criar_vm_banco_dados_linux() 
    print(vm3)

    gerenciador.desanexar(logger)
    print("\nLogger desanexado. Criando outra VM...")
    vm4 = gerenciador.criar_vm_desenvolvimento_linux(estrategia_economia)
    print(vm4)
