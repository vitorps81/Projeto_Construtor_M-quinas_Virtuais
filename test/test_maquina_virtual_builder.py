import unittest
from src.maquina_virtual import MaquinaVirtual
from src.linux_vm_builder import LinuxVMBuilder
from src.windows_vm_builder import WindowsVMBuilder
from src.diretor import Diretor
from src.software_componente import SoftwareIndividual 
from src.software_composite import GrupoSoftware     
from src.vm_facade import GerenciadorVM              

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

        softwares_str = vm_dev.__str__() 

        self.assertEqual(len(vm_dev.softwares_instalados), 1) 

        dev_stack_group = vm_dev.softwares_instalados[0]
        self.assertIsInstance(dev_stack_group, GrupoSoftware)
        self.assertIn("Python 3.9", dev_stack_group.get_nome())
        self.assertIn("Docker", dev_stack_group.get_nome())
        self.assertIn("Git", dev_stack_group.get_nome()) 

        self.assertIn("Dev Stack Python (Python 3.9, Docker, Git)", softwares_str)

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
        python = SoftwareIndividual("Python")
        docker = SoftwareIndividual("Docker")
        git = SoftwareIndividual("Git")

        dev_tools = GrupoSoftware("Ferramentas de Dev")
        dev_tools.adicionar(python)
        dev_tools.adicionar(docker)
        dev_tools.adicionar(git)

        self.assertEqual(dev_tools.get_nome(), "Ferramentas de Dev (Python, Docker, Git)")

        builder = LinuxVMBuilder()
        vm = (builder
              .definir_sistema_operacional()
              .com_ram(8)
              .instalar_software(dev_tools)
              .get_maquina_virtual())

        self.assertIn("Ferramentas de Dev (Python, Docker, Git)", vm.__str__())
        self.assertEqual(len(vm.softwares_instalados), 1) 

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

if __name__ == '__main__':
    unittest.main()
