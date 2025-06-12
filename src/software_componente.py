from abc import ABC, abstractmethod

class ComponenteSoftware(ABC):
    
    @abstractmethod
    def get_nome(self) -> str:
        pass

class SoftwareIndividual(ComponenteSoftware):
    
    def __init__(self, nome: str):
        self._nome = nome

    def get_nome(self) -> str:
        return self._nome
