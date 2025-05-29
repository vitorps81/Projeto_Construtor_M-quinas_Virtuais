import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from src.maquina_virtual import MaquinaVirtual
from src.linux_vm_builder import LinuxVMBuilder
from src.windows_vm_builder import WindowsVMBuilder
from src.diretor import Diretor 

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
              .instalar_software("SQL Server")
              .instalar_software("Visual Studio")
              .configurar_rede(True)
              .get_maquina_virtual())

        self.assertIsInstance(vm, MaquinaVirtual)
        self.assertEqual(vm.sistema_operacional, "Windows Server")
        self.assertEqual(vm.ram_gb, 8)
        self.assertEqual(vm.cpu_cores, 4)
        self.assertEqual(vm.disco_gb, 120)
        self.assertIn("SQL Server", vm.softwares_instalados)
        self.assertIn("Visual Studio", vm.softwares_instalados)
        self.assertTrue(vm.rede_configurada)

    def test_diretor_builds_dev_vm(self):
        diretor = Diretor()
        builder = LinuxVMBuilder() 
        vm_dev = diretor.construir_vm_desenvolvimento(builder)

        self.assertIsInstance(vm_dev, MaquinaVirtual)
        self.assertEqual(vm_dev.sistema_operacional, "Linux (Ubuntu Server)")
        self.assertEqual(vm_dev.ram_gb, 8)
        self.assertEqual(vm_dev.cpu_cores, 2)
        self.assertEqual(vm_dev.disco_gb, 50)
        self.assertIn("Python 3.9", vm_dev.softwares_instalados)
        self.assertIn("Docker", vm_dev.softwares_instalados)
        self.assertTrue(vm_dev.rede_configurada)

if __name__ == '__main__':
    unittest.main()
