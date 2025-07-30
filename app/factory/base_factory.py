from abc import ABC, abstractmethod

class PessoaFactory(ABC):
    @abstractmethod
    def criar(self, **kwargs):
        pass
