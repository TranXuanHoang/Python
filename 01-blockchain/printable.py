class Printable:
    """ A general class for other child class to inherit and
    get printed out as dictionaries. """

    def __repr__(self):
        return str(self.__dict__)
