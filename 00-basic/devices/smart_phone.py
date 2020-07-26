from .electronic_device import ElectronicDevice


class SmartPhone(ElectronicDevice):
    """ Represent smart phones. """

    def __init__(self, name, model, size, brand):
        super().__init__(name, model, size)
        self.__brand = brand

    def connect_to_wifi(self):
        print(f'{self.name} {self.get_device_model()} is connecting to a wifi')

    def basic_info(self):
        return f'{super().basic_info()} | Designed by {self.__brand}'
