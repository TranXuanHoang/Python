from devices.electronic_device import ElectronicDevice
from devices.laptop import Laptop
from devices.tablet import Tablet
from devices.smart_phone import SmartPhone


class Devices:
    """ Create and manage devices. """

    def __init__(self):
        self.devices = []
        self.create_laptops()
        self.create_tablets()
        self.create_smartphones()

    def create_laptops(self):
        l1 = Laptop('Dell', 'Inspiron', {'width': 1366,
                                         'height': 768, 'thickness': 10}, 'Windows 10')
        l2 = Laptop('Apple MacBook', 'Pro', {'width': 2880,
                                             'height': 1800, 'thickness': 12}, 'macOS Catalina')
        l1.restart()
        print(l1.basic_info())
        l1.connect_wired_lan()
        l2.restart()
        print(l2.basic_info())
        l2.connect_wired_lan()
        print('__' * 40)
        self.devices.extend([l1, l2])

    def create_tablets(self):
        t1 = Tablet('Apple iPad', 'Mini', {'width': 768,
                                           'height': 1024, 'thickness': 8}, 66)
        t2 = Tablet('Microsoft Surface', 'Pro', {'width': 2736,
                                                 'height': 1824, 'thickness': 11}, 13)
        t1.restart()
        print(t1.basic_info())
        t2.restart()
        print(t2.basic_info())
        print('__' * 40)
        self.devices.extend([t1, t2])

    def create_smartphones(self):
        sp1 = SmartPhone('iPhone', 12, {'width': 828,
                                        'height': 1792, 'thickness': 8}, 'Apple')
        sp2 = SmartPhone('Pixel', 'XL', {'width': 411,
                                         'height': 731, 'thickness': 8}, 'Google')
        sp1.restart()
        sp1.connect_to_wifi()
        print(sp1.basic_info())
        sp2.restart()
        sp2.connect_to_wifi()
        print(sp2.basic_info())
        print('__' * 40)
        self.devices.extend([sp1, sp2])


dv = Devices()
devices = dv.devices
for device in devices:
    if isinstance(device, Laptop):
        print(device.basic_info(), ' is a laptop')
    elif isinstance(device, Tablet):
        print(device.basic_info(), ' is a tablet')
    elif isinstance(device, SmartPhone):
        print(device.basic_info(), ' is a smart phone')
    else:
        print(device.basic_info(), ' is an electronic device')
