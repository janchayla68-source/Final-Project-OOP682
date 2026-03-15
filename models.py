import pygame

class GameObject:
    def __init__(self, name, description):
        self.name = name
        self.description = description

class Item(GameObject):
    def __init__(self, name, description, is_clue=False, image_path=None):
        super().__init__(name, description)
        self.is_clue = is_clue
        self.image = None
        
        if image_path:
            try:
                self.image = pygame.image.load(image_path)
                self.image = pygame.transform.scale(self.image, (40, 40))
            except Exception as e:
                print(f"❌ โหลดรูปไอเทมไม่ได้: {e}")

    def examine(self):
        return f"ตรวจสอบ {self.name}: {self.description}"

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

class Inventory:
    def __init__(self):
        self.__items = [] 

    def add_item(self, item):
        self.__items.append(item)
        print(f"[System]: เก็บ {item.name} เข้ากระเป๋า")

    def get_all_items(self):
        return self.__items

class Player:
    def __init__(self, name):
        self.name = name
        self.inventory = Inventory() 

    def collect_item(self, item):
        self.inventory.add_item(item)

class Location:
    def __init__(self, name, description, bg_path=None):
        self.name = name
        self.description = description
        self.bg_path = bg_path
        self.items = []
        self.npcs = []
        self.connections = {} 

    def add_connection(self, direction, destination):
        self.connections[direction] = destination

    def add_item(self, item):
        self.items.append(item)

    def add_npc(self, npc):
        self.npcs.append(npc)

class SoundManager:
    __instance = None 

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(SoundManager, cls).__new__(cls)
            cls.__instance.__initialize() 
        return cls.__instance

    def __initialize(self):
        """ฟังก์ชันนี้จะถูกรันแค่ครั้งเดียวตอนสร้างเกม"""
        pygame.mixer.init()
        try:
            pygame.mixer.music.load("assets/bgm.mp3")
            pygame.mixer.music.set_volume(0.3)
            self.sfx_click = pygame.mixer.Sound("assets/click.wav") 
            self.sfx_collect = pygame.mixer.Sound("assets/collect.wav")
            self.sfx_shock = pygame.mixer.Sound("assets/shock.wav")
        except Exception as e:
            print(f"⚠️ ระบบเสียงมีปัญหา: {e}")
            self.sfx_click = None
            self.sfx_collect = None
            self.sfx_shock = None

    def play_bgm(self):
        try:
            pygame.mixer.music.play(-1)
        except:
            pass

    def play_sfx(self, sound_type):
        if sound_type == "click" and self.sfx_click:
            self.sfx_click.play()
        elif sound_type == "collect" and self.sfx_collect:
            self.sfx_collect.play()
        elif sound_type == "shock" and self.sfx_shock:
            self.sfx_shock.play()