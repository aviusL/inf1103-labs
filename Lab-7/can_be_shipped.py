from abc import ABC, abstractmethod


class CanBeShipped(ABC):
    #interface: any class that signs this contract must be able to calculate shipping

    @abstractmethod
    def calculate_shipping_cost(self):
        #return the shipping cost in dollars
        pass
