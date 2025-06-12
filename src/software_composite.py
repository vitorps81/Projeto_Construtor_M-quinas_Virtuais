from src.software_componente import ComponenteSoftware 

class GrupoSoftware(ComponenteSoftware):
    
    def __init__(self, nome_grupo: str):
        self._nome_grupo = nome_grupo
        self._componentes = []

    def adicionar(self, componente: ComponenteSoftware):
        self._componentes.append(componente)

    def remover(self, componente: ComponenteSoftware):
        self._componentes.remove(componente)

    def get_nome(self) -> str:
        nomes_componentes = [comp.get_nome() for comp in self._componentes]
        return f"{self._nome_grupo} ({', '.join(nomes_componentes)})"
    