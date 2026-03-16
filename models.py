import pygame
from abc import ABC, abstractmethod

class GameObject(ABC):
    def __init__(self, name, description):
        self.name = name
        self.description = description
        
    @abstractmethod
    def get_info(self):
        pass

class Item(GameObject):
    def __init__(self, name, description, image_path=None):
        super().__init__(name, description)
        self.image_path = image_path
        self.image = None
        if image_path:
            try:
                self.image = pygame.image.load(image_path).convert_alpha()
                self.image = pygame.transform.scale(self.image, (40, 40))
            except:
                pass

    def get_info(self):
        return f"[หลักฐาน] {self.name}: {self.description}"

class Character(GameObject):
    def __init__(self, name, description, dialogues, reactions, weakness=None, secret_dialogue=None):
        super().__init__(name, description)
        self.__dialogues = dialogues
        self.__reactions = reactions
        self.weakness = weakness               
        self.secret_dialogue = secret_dialogue 
        self.alibi_broken = False              

    def speak(self, topic):
        return self.__dialogues.get(topic, "ฉันไม่มีอะไรจะพูดเรื่องนั้น")

    def react_to_evidence(self, item_name):
        if self.weakness and item_name == self.weakness:
            self.alibi_broken = True
            if "ความลับ" not in self.__dialogues:
                self.__dialogues["ความลับ"] = self.secret_dialogue
            return f"!!! (หน้าถอดสี) ค...คุณรู้ได้ยังไง!? (ปลดล็อคหัวข้อ 'ความลับ' แล้ว)"
            
        return self.__reactions.get(item_name, f"ฉันไม่รู้เรื่องของชิ้นนี้หรอกนะ")
        
    def get_all_topics(self):
        return list(self.__dialogues.keys())

    def get_info(self):
        return f"[ตัวละคร] {self.name} - สถานะการโกหก: {self.alibi_broken}"

class Location:
    def __init__(self, name, description, bg_path=None):
        self.name = name
        self.description = description
        self.bg_path = bg_path
        self.items = []
        self.npcs = []
        self.connections = {}

    def add_item(self, item):
        self.items.append(item)

    def add_npc(self, npc):
        self.npcs.append(npc)

    def add_connection(self, direction, location):
        self.connections[direction] = location

class Inventory:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def get_all_items(self):
        return self.items

class Player:
    def __init__(self, name):
        self.name = name
        self.inventory = Inventory()

    def collect_item(self, item):
        self.inventory.add_item(item)

class SoundManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SoundManager, cls).__new__(cls)
            cls._instance.init_sounds()
        return cls._instance
        
    def init_sounds(self):
        pygame.mixer.init()
        try:
            self.bgm = "assets/bgm.mp3"
            self.sfx = {
                "click": pygame.mixer.Sound("assets/click.wav"),
                "collect": pygame.mixer.Sound("assets/collect.wav"),
                "shock": pygame.mixer.Sound("assets/shock.wav")
            }
        except:
            self.bgm = None
            self.sfx = {}

    def play_bgm(self):
        if self.bgm:
            try:
                pygame.mixer.music.load(self.bgm)
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(0.3)
            except:
                pass

    def play_sfx(self, name):
        if name in self.sfx:
            try:
                self.sfx[name].play()
            except:
                pass