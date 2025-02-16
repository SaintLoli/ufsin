from winreg import *


REGISTRY = ConnectRegistry(None, HKEY_LOCAL_MACHINE)


class PCInfo:
    def __init__(self):
        self.processor = ''
        self.motherboard = ''
        self.video_card = ''
        self.ram = ''
        self.year = ''
        self.other = []

        """
        вызов функций на получение информации из регистра
        """
        self.get_processor_info()
        self.get_video_card_info()
        self.get_motherboard_info()

    def get_processor_info(self):
        key = OpenKey(REGISTRY, r"HARDWARE\DESCRIPTION\System\CentralProcessor\0")
        self.processor = QueryValueEx(key, "ProcessorNameString")[0]

    def get_video_card_info(self):
        path_to_video_card = QueryValueEx(OpenKey(REGISTRY, r"HARDWARE\DEVICEMAP\VIDEO"), "\Device\Video0")[0]
        path_to_video_card = path_to_video_card.replace("\Registry\Machine\System", "")
        path_to_video_card = r"SYSTEM" + path_to_video_card
        self.video_card = QueryValueEx(OpenKey(REGISTRY, path_to_video_card), "DriverDesc")[0]

    def get_motherboard_info(self):
        key = OpenKey(REGISTRY, r"HARDWARE\DESCRIPTION\System\BIOS")
        self.motherboard = QueryValueEx(key, "BaseBoardManufacturer")[0] + " " + \
                           QueryValueEx(key, "BaseBoardProduct")[0]

    def __repr__(self):
        return f"Процессор: {self.processor}\n" \
               f"Материнская плата: {self.motherboard}\n" \
               f"Видеоадаптер: {self.video_card}\n"


def get_pc_name():
    key = OpenKey(REGISTRY, r"SYSTEM\CurrentControlSet\Control\ComputerName\ComputerName")
    return QueryValueEx(key, "ComputerName")[0]


if __name__ == "__main__":
    PC = PCInfo()
    print(PC)
    print(get_pc_name())
