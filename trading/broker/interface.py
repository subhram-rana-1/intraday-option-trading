from abc import ABC, abstractmethod


class IBroker(ABC):
    @abstractmethod
    def Buy(self):
        ...

    @abstractmethod
    def Sell(self):
        ...
