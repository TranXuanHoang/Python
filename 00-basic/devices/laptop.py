from .electronic_device import ElectronicDevice


class Laptop(ElectronicDevice):
    """ Represent laptops. """

    def __init__(self, name, model, size, os):
        """ os: operating system """
        super().__init__(name, model, size)
        self.__os = os

    def connect_wired_lan(self):
        print(f'{self.__os} is connecting to a wired LAN...')
