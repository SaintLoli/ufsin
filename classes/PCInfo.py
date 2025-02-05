from winreg import *


class PCInfo:
    def __init__(self):
        self.processor = ''
        self.motherboard = ''
        self.ram = ''
        self.video_card = ''
        self.other = []

        self.registry = ConnectRegistry(None, HKEY_LOCAL_MACHINE)


        """
        вызов функций на получение информации из регистра
        """
        self.get_processor_info()
        self.get_video_card_info()
        self.get_motherboard_info()

    def get_processor_info(self):
        key = OpenKey(self.registry, r"HARDWARE\DESCRIPTION\System\CentralProcessor\0")
        self.processor = QueryValueEx(key, "ProcessorNameString")[0]

    def get_video_card_info(self):
        path_to_video_card = QueryValueEx(OpenKey(self.registry, r"HARDWARE\DEVICEMAP\VIDEO"), "\Device\Video0")[0]
        path_to_video_card = path_to_video_card.replace("\Registry\Machine\System", "")
        path_to_video_card = r"SYSTEM" + path_to_video_card
        self.video_card = QueryValueEx(OpenKey(self.registry, path_to_video_card), "HardwareInformation.AdapterString")[0]

    def get_motherboard_info(self):
        key = OpenKey(self.registry, r"HARDWARE\DESCRIPTION\System\BIOS")
        self.motherboard = QueryValueEx(key, "BaseBoardManufacturer")[0] + " " + \
                           QueryValueEx(key, "BaseBoardProduct")[0]

    def get_pc_processor(self):
        return self.processor

    def get_pc_video_card(self):
        return self.video_card

    def get_pc_motherboard(self):
        return self.processor

    def __repr__(self):
        return f"Процессор: {self.processor}\n" \
               f"Материнская плата: {self.motherboard}\n" \
               f"Видеоадаптер: {self.video_card}\n"



if __name__ == "__main__":
    PC = PCInfo()
    print(PC)
