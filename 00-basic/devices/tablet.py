from .electronic_device import ElectronicDevice


class Tablet(ElectronicDevice):
    """ Represent tablets. """

    def __init__(self, name, model, size, popularity=1):
        super().__init__(name, model, size)
        self.__popurarity = popularity

    def basic_info(self):
        return f'{super().basic_info()} | Popularity = {self.__popurarity}'
