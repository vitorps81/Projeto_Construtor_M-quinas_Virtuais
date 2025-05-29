class MaquinaVirtual:
    def __init__(self):
        self.sistema_operacional = None
        self.ram_gb = 0
        self.cpu_cores = 0
        self.disco_gb = 0
        self.softwares_instalados = []
        self.rede_configurada = False

    def __str__(self):
        softwares = ", ".join(self.softwares_instalados) if self.softwares_instalados else "Nenhum"
        rede = "Configurada" if self.rede_configurada else "Não Configurada"
        return (f"--- Configuração da Máquina Virtual ---\n"
                f"SO: {self.sistema_operacional}\n"
                f"RAM: {self.ram_gb} GB\n"
                f"CPU: {self.cpu_cores} Cores\n"
                f"Disco: {self.disco_gb} GB\n"
                f"Softwares: {softwares}\n"
                f"Rede: {rede}\n"
                f"----------------------------------------")
    