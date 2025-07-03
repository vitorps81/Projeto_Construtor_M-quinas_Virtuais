import unittest
from src.maquina_virtual import MaquinaVirtual
from src.linux_vm_builder import LinuxVMBuilder
from src.windows_vm_builder import WindowsVMBuilder
from src.diretor import Diretor
from src.software_componente import SoftwareIndividual 
from src.software_composite import GrupoSoftware     
from src.vm_facade import GerenciadorVM              
from src.vm_otimizacao_strategy import OtimizacaoDesempenhoStrategy, OtimizacaoEconomiaStrategy
from src.vm_observer import LoggerVMObserver, MonitoramentoVMObserver, SubjectVM 

class TestMaquinaVirtualBuilder(unittest.TestCase):

    def test_linux_vm_builder_basic_config(self):
        builder = LinuxVMBuilder()
        vm = (builder
              .definir_sistema_operacional()
              .com_ram(4)
              .com_cpu(2)
              .get_maquina_virtual())

        self.assertIsInstance(vm, MaquinaVirtual)
        self.assertEqual(vm.sistema_operacional, "Linux (Ubuntu Server)")
        self.assertEqual(vm.ram_gb, 4)
        self.assertEqual(vm.cpu_cores, 2)
        self.assertEqual(vm.disco_gb, 0) 
        self.assertEqual(vm.softwares_instalados, [])
        self.assertFalse(vm.rede_configurada)

    def test_windows_vm_builder_full_config(self):
        builder = WindowsVMBuilder()
        vm = (builder
              .definir_sistema_operacional()
              .com_ram(8)
              .com_cpu(4)
              .com_disco(120)
              .instalar_software(SoftwareIndividual("SQL Server")) 
              .instalar_software(SoftwareIndividual("Visual Studio")) 
              .configurar_rede(True)
              .get_maquina_virtual())

        self.assertIsInstance(vm, MaquinaVirtual)
        self.assertEqual(vm.sistema_operacional, "Windows Server")
        self.assertEqual(vm.ram_gb, 8)
        self.assertEqual(vm.cpu_cores, 4)
        self.assertEqual(vm.disco_gb, 120)
        
        installed_software_names = [s.get_nome() for s in vm.softwares_instalados]
        self.assertIn("SQL Server", installed_software_names)
        self.assertIn("Visual Studio", installed_software_names)
        self.assertTrue(vm.rede_configurada)

    def test_composite_software_installation(self):
        python_soft = SoftwareIndividual("Python 3.9") 
        docker_soft = SoftwareIndividual("Docker")
        git_soft = SoftwareIndividual("Git")

        dev_tools = GrupoSoftware("Dev Stack Python")
        dev_tools.adicionar(python_soft)
        dev_tools.adicionar(docker_soft)
        dev_tools.adicionar(git_soft)

        self.assertEqual(dev_tools.get_nome(), "Dev Stack Python (Python 3.9, Docker, Git)")

        builder = LinuxVMBuilder()
        vm = (builder
              .definir_sistema_operacional()
              .com_ram(8)
              .instalar_software(dev_tools) 
              .get_maquina_virtual())

        self.assertEqual(len(vm.softwares_instalados), 1)
        self.assertIsInstance(vm.softwares_instalados[0], GrupoSoftware)

        self.assertIn("Dev Stack Python (Python 3.9, Docker, Git)", vm.__str__())

    def test_diretor_builds_dev_vm(self):
        diretor = Diretor()
        builder = LinuxVMBuilder()
        vm_dev = diretor.construir_vm_desenvolvimento(builder)

        self.assertIsInstance(vm_dev, MaquinaVirtual)
        self.assertEqual(vm_dev.sistema_operacional, "Linux (Ubuntu Server)")
        self.assertEqual(vm_dev.ram_gb, 8)
        self.assertEqual(vm_dev.cpu_cores, 2)
        self.assertEqual(vm_dev.disco_gb, 50)
        self.assertTrue(vm_dev.rede_configurada)

        self.assertEqual(len(vm_dev.softwares_instalados), 1) 
        dev_stack_group = vm_dev.softwares_instalados[0]
        self.assertIsInstance(dev_stack_group, GrupoSoftware)
        self.assertIn("Python 3.9", dev_stack_group.get_nome())
        self.assertIn("Docker", dev_stack_group.get_nome())
        self.assertIn("Git", dev_stack_group.get_nome()) 

    def test_facade_creates_dev_vm(self):
        gerenciador = GerenciadorVM()
        vm_dev = gerenciador.criar_vm_desenvolvimento_linux() 

        self.assertIsInstance(vm_dev, MaquinaVirtual)
        self.assertEqual(vm_dev.sistema_operacional, "Linux (Ubuntu Server)")
        self.assertEqual(vm_dev.ram_gb, 8)
        self.assertIn("Dev Stack Python (Python 3.9, Docker, Git)", vm_dev.__str__())

    def test_facade_creates_web_server_vm(self):
        gerenciador = GerenciadorVM()
        vm_web = gerenciador.criar_vm_web_server_windows() 

        self.assertIsInstance(vm_web, MaquinaVirtual)
        self.assertEqual(vm_web.sistema_operacional, "Windows Server")
        self.assertEqual(vm_web.ram_gb, 4)
        self.assertIn("Web Server Bundle (IIS, ASP.NET Core Runtime)", vm_web.__str__())

    def test_vm_optimization_strategy_performance(self):
        builder = LinuxVMBuilder()
        vm = (builder
              .definir_sistema_operacional()
              .com_ram(4)  
              .com_cpu(2)  
              .com_disco(40) 
              .get_maquina_virtual())

        strategy = OtimizacaoDesempenhoStrategy()
        strategy.aplicar(vm)

        self.assertEqual(vm.ram_gb, 16) 
        self.assertEqual(vm.cpu_cores, 4) 
        self.assertEqual(vm.disco_gb, 80) 

    def test_vm_optimization_strategy_economy(self):
        builder = WindowsVMBuilder()
        vm = (builder
              .definir_sistema_operacional()
              .com_ram(32) 
              .com_cpu(8)  
              .com_disco(50) 
              .get_maquina_virtual())

        strategy = OtimizacaoEconomiaStrategy()
        strategy.aplicar(vm)

        self.assertEqual(vm.ram_gb, 4) 
        self.assertEqual(vm.cpu_cores, 2) 
        self.assertEqual(vm.disco_gb, 150) 

    def test_facade_applies_strategy(self):
        gerenciador = GerenciadorVM()
        strategy_desempenho = OtimizacaoDesempenhoStrategy()
        
        vm = gerenciador.criar_vm_desenvolvimento_linux(strategy_desempenho)
        
        self.assertEqual(vm.ram_gb, 16)
        self.assertEqual(vm.cpu_cores, 4)
        self.assertEqual(vm.disco_gb, 80) 

    def test_vm_observer_notification(self):
        gerenciador = GerenciadorVM()
        mock_logger = MockObserver()
        mock_monitor = MockObserver()

        gerenciador.anexar(mock_logger)
        gerenciador.anexar(mock_monitor)

        vm_dev = gerenciador.criar_vm_desenvolvimento_linux()

        self.assertTrue(mock_logger.notified)
        self.assertTrue(mock_monitor.notified)
        self.assertEqual(mock_logger.last_event, "VM Dev Linux Criada")
        self.assertEqual(mock_monitor.last_event, "VM Dev Linux Criada")
        self.assertIs(mock_logger.last_vm, vm_dev)

        gerenciador.desanexar(mock_logger)
        mock_logger.reset() 

        vm_web = gerenciador.criar_vm_web_server_windows() 
        
        self.assertFalse(mock_logger.notified) 
        self.assertTrue(mock_monitor.notified) 
        self.assertEqual(mock_monitor.last_event, "VM Web Windows Criada")
        self.assertIs(mock_monitor.last_vm, vm_web)

class MockObserver(LoggerVMObserver): 
    def __init__(self):
        self.notified = False
        self.last_vm = None
        self.last_event = None

    def atualizar(self, vm: MaquinaVirtual, evento: str):
        self.notified = True
        self.last_vm = vm
        self.last_event = evento

    def reset(self):
        self.notified = False
        self.last_vm = None
        self.last_event = None

if __name__ == '__main__':
    unittest.main()
