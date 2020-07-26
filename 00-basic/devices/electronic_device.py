class ElectronicDevice:
    """ Represent each electronic device. """

    def __init__(self, name, model, size: dict):
        """ Constructor

        Args:
            name: The name of the device.
            model: The model of the device.
            size: The size of the device. Should be a dictionary in a format of
                {'width': width, 'height': height, 'thickness': thickness}
        """
        self.name = name  # public attribute
        self.__model = model  # private attribute
        self.set_device_size(size)

    def restart(self):
        print(f'Restarting {self.name} {self.__model} device...')

    def get_device_model(self):
        return self.__model

    def set_device_size(self, size):
        # private attribute __size
        self.__size = {key: val for key, val in size.items()}

    def get_device_size(self):
        return self.__size

    def basic_info(self):
        return f'{self.name} {self.__model} (w: {self.__size["width"]}, h: {self.__size["height"]}, t: {self.__size["thickness"]})'

    def descrtion(self):
        return self.__doc__  # docstring belonging to the class
