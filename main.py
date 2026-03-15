import pygame
import sys
from models import Item, Character, Location, Player, SoundManager

SCREEN_WIDTH = 1280  
SCREEN_HEIGHT = 720 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50, 180) 

class DetectiveGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("The Shadow of Eldoria - Mystery Game")
        self.clock = pygame.time.Clock()
        
        try:
            self.font = pygame.font.Font("assets/Sarabun-Regular.ttf", 24)
            self.big_font = pygame.font.Font("assets/Sarabun-Regular.ttf", 72) 
            self.title_font = pygame.font.Font("assets/Sarabun-Regular.ttf", 50)
        except Exception as e:
            print(f"⚠️ หาไฟล์ฟอนต์ไม่เจอ โหลดฟอนต์สำรองแทน: {e}")
            self.font = pygame.font.SysFont("leelawadee", 24)
            self.big_font = pygame.font.SysFont("leelawadee", 72, bold=True)
            self.title_font = pygame.font.SysFont("leelawadee", 50, bold=True)
        
        self.sound_manager = SoundManager()
        self.sound_manager.play_bgm() 
        
        self.player = Player("เอลรอน")
        self.current_location = None
        self.current_npc = None
        self.nav_buttons = {}      
        self.choice_buttons = {}   
        self.inv_buttons = {} 
        self.menu_buttons = {} 
        
        self.show_inventory_ui = False
        self.game_state = "MENU" 
        self.current_dialogue = "ยินดีต้อนรับนักสืบ... คลิกที่ตัวละครหรือสำรวจห้องเพื่อหาเบาะแส"
        self.is_running = True

        self.current_level = 1
        self.setup_level_1()


    def draw_main_menu(self):
        self.screen.fill(BLACK) 

        title_text = self.title_font.render("The Shadow of Eldoria", True, (220, 20, 20)) 
        self.screen.blit(title_text, (SCREEN_WIDTH//2 - title_text.get_width()//2, 100))

        subtitle = self.font.render("Mystery Game - OOP Project", True, (150, 150, 150))
        self.screen.blit(subtitle, (SCREEN_WIDTH//2 - subtitle.get_width()//2, 170))

        mouse_pos = pygame.mouse.get_pos()

        buttons = ["เริ่มเกม (Start)", "วิธีเล่น (How to Play)", "ออก (Exit)"]
        self.menu_buttons = {}
        y_pos = 300
        
        for text in buttons:
            btn_rect = pygame.Rect(SCREEN_WIDTH//2 - 150, y_pos, 300, 50)
            
            if btn_rect.collidepoint(mouse_pos):
                pygame.draw.rect(self.screen, (150, 30, 30), btn_rect)
            else:
                pygame.draw.rect(self.screen, (20, 20, 20), btn_rect) 
                
            pygame.draw.rect(self.screen, (200, 0, 0), btn_rect, 2) 
            
            text_surf = self.font.render(text, True, WHITE)
            self.screen.blit(text_surf, (btn_rect.centerx - text_surf.get_width()//2, btn_rect.centery - 15))
            
            self.menu_buttons[text] = btn_rect
            y_pos += 80


    def draw_instructions(self):
        self.screen.fill(BLACK)
        title = self.big_font.render("HOW TO PLAY", True, WHITE)
        self.screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 50))

        instructions = [
            "1. สำรวจห้องต่างๆ เพื่อค้นหา 'หลักฐาน' ที่ซ่อนอยู่",
            "2. พูดคุยกับผู้ต้องสงสัยเพื่อจับผิด 'คำให้การ'",
            "3. กด 'I' เพื่อเปิดกระเป๋า และยื่นหลักฐานให้ NPC ดู",
            "4. เมื่อมั่นใจและมีหลักฐานครบ 2 ชิ้น ให้กด 'ชี้ตัว'",
            "   (ระวัง: หากชี้ตัวผิดคน เกมจะจบทันที!)"
        ]
        
        y_pos = 200
        for line in instructions:
            text_surf = self.font.render(line, True, (200, 255, 200))
            self.screen.blit(text_surf, (100, y_pos))
            y_pos += 50

        back_btn = pygame.Rect(SCREEN_WIDTH//2 - 100, 500, 200, 50)
        pygame.draw.rect(self.screen, (100, 50, 50), back_btn)
        pygame.draw.rect(self.screen, WHITE, back_btn, 2)
        back_text = self.font.render("กลับ (Back)", True, WHITE)
        self.screen.blit(back_text, (back_btn.centerx - back_text.get_width()//2, back_btn.centery - 15))
        self.menu_buttons["Back"] = back_btn


    def setup_level_1(self):
        self.living_room = Location("ห้องนั่งเล่น", "ศพท่านเคานต์นอนอยู่ มีรอยเท้าโคลนเปื้อนพรม", bg_path="assets/bg_livingroom.png")
        self.kitchen = Location("ห้องครัว", "ห้องครัวที่ดูสะอาด... แต่มีบางอย่างซ่อนอยู่", bg_path="assets/bg_kitchen.png")
        self.garden = Location("สวนหลังบ้าน", "มืดมิด ฝนตกหนัก มีแอ่งโคลนเละเทะ", bg_path="assets/bg_garden.png")
        self.bedroom = Location("ห้องนอน", "ห้องนอนของอลิซ ที่ปลอดภัยที่สุดในบ้าน", bg_path="assets/bg_bedroom.png")

        rooms = [self.living_room, self.kitchen, self.garden, self.bedroom]
        for current_room in rooms:
            for target_room in rooms:
                if current_room != target_room:
                    current_room.add_connection(target_room.name, target_room)

        self.kitchen.add_item(Item(
            "ใบแจ้งหนี้สีแดง", 
            "ยอดหนี้พนันจำนวนมหาศาล ระบุชื่อผู้กู้คือ 'เจมส์'", 
            image_path="assets/red_bill.png"  
        ))
        
        self.garden.add_item(Item(
            "กระดุมเสื้อพ่อบ้าน", 
            "ตกจมอยู่ในแอ่งโคลน มีตราประจำตระกูลสลักไว้", 
            image_path="assets/butler_button.png"  
        ))
        james_dialogues = {
            "ทั่วไป": "ผมชงชาอยู่ในครัวตลอดครับ ไม่ได้ออกไปตากฝนที่สวนแน่นอน",
            "เสื้อผ้า": "อ้อ... วันนี้อากาศอ้าวๆ ผมเลยไม่ได้ใส่สูทตัวนอกน่ะครับ",
            "เวลา": "เที่ยงคืนผมกำลังต้มน้ำร้อน ไม่เห็นใครเดินผ่านครัวเลย",
            "ชี้ตัว": "คุณจะหาว่าผมเป็นฆาตกรเหรอ!? มีหลักฐานมัดตัวผมหรือไง!"
        }
        james_reactions = {
            "ใบแจ้งหนี้สีแดง": "นั่นมันของส่วนตัวผมนะ! ถึงผมจะเป็นหนี้ แต่ก็ไม่ได้แปลว่าผมต้องฆ่าเจ้านายตัวเองนี่!",
            "กระดุมเสื้อพ่อบ้าน": "!!!" 
        }
        self.james = Character(
            "พ่อบ้านเจมส์", "ผู้ต้องสงสัย", james_dialogues, james_reactions,
            weakness="กระดุมเสื้อพ่อบ้าน", 
            secret_dialogue="ก...กระดุมเสื้อผม! ไปตกอยู่ตรงนั้นได้ยังไง... ยอมรับก็ได้ครับ! ท่านเคานต์จับได้ว่าผมขโมยเงินไปใช้หนี้ ผมเลยพลั้งมือ... แล้วแอบหนีออกไปทางสวนหลังบ้าน!"
        )
        self.kitchen.add_npc(self.james)

        tom_dialogues = {
            "ทั่วไป": "เมื่อคืนฝนตกหนัก โคลนในสวนเละไปหมดเลยครับ ใครเดินย่ำต้องเปื้อนแน่ๆ",
            "เสื้อผ้า": "ผมเห็นนะว่าเมื่อเย็นเจมส์ยังใส่สูทเต็มยศอยู่เลย ทำไมตอนนี้ถอดออกล่ะ?",
            "ชี้ตัว": "ผมแค่คนสวนแก่ๆ จะไปมีปัญญาฆ่าใครได้ครับ"
        }
        tom_reactions = {
            "ใบแจ้งหนี้สีแดง": "เจมส์ติดหนี้พนันก้อนโตเลยครับ ช่วงนี้เขาดูเครียดๆ ลุกลี้ลุกลนชอบกล",
            "กระดุมเสื้อพ่อบ้าน": "เอ๊ะ นี่มันกระดุมเสื้อสูทของเจมส์นี่ครับ? ผมจำตราสัญลักษณ์ได้แม่นเลย!"
        }
        self.tom = Character("ลุงทอม คนสวน", "พยานปากเอก", tom_dialogues, tom_reactions)
        self.garden.add_npc(self.tom)

        rose_dialogues = {
            "ทั่วไป": "โธ่... สามีที่รักของฉัน ทำไมถึงด่วนจากไปแบบนี้ (ซับน้ำตา)",
            "เสื้อผ้า": "เจมส์แปลกไปนะ ปกติเขาเจ้าระเบียบจะตาย ต้องใส่สูทตลอด แต่วันนี้กลับใส่แค่เสื้อเชิ้ต?",
            "ชี้ตัว": "คุณกล้าสงสัยภรรยาที่กำลังโศกเศร้าอย่างฉันเหรอคะ!?"
        }
        rose_reactions = {
            "ใบแจ้งหนี้สีแดง": "หนี้พนัน? มิน่าล่ะ ช่วงนี้เงินในบัญชีตระกูลถึงหายไปแปลกๆ",
            "กระดุมเสื้อพ่อบ้าน": "นั่นมันกระดุมสูทของพ่อบ้านนี่คะ! ทำไมไปตกอยู่ข้างนอกล่ะ?"
        }
        self.rose = Character("มาดามโรส", "ภรรยาผู้โศกเศร้า", rose_dialogues, rose_reactions)
        self.living_room.add_npc(self.rose)

        alice_dialogues = {
            "ทั่วไป": "คุณพ่อบุญธรรมใจดีกับหนูมากค่ะ... (เสียงสั่น)",
            "รอยเท้า": "ตอนเที่ยงคืน หนูแอบเห็นรอยเท้าเปื้อนโคลน เดินจากสวนเข้ามาในห้องนั่งเล่นค่ะ...",
            "ชี้ตัว": "หนูเปล่านะคะ! หนูเป็นแค่เด็กกำพร้าที่คุณพ่อเก็บมาเลี้ยง..."
        }
        alice_reactions = {
            "ใบแจ้งหนี้สีแดง": "หนูเคยเห็นพ่อบ้านเจมส์แอบคุยโทรศัพท์เรื่องเงินด้วยท่าทางน่ากลัวค่ะ",
            "กระดุมเสื้อพ่อบ้าน": "หนูจำได้! เมื่อเช้าเสื้อของพ่อบ้านเจมส์กระดุมหายไปเม็ดนึงค่ะ!"
        }
        self.alice = Character("อลิซ", "ลูกสาวบุญธรรม", alice_dialogues, alice_reactions)
        self.bedroom.add_npc(self.alice) 

        self.current_location = self.living_room

        self.bg_images = {}
        for loc in [self.living_room, self.kitchen, self.garden, self.bedroom]:
            try:
                img = pygame.image.load(loc.bg_path).convert_alpha()
                self.bg_images[loc.name] = pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))
            except Exception as e:
                print(f"โหลดรูปฉากหลัง {loc.name} ไม่ได้: {e}")
                self.bg_images[loc.name] = None

        self.npc_images = {}
        self.npc_rects = {}
        
        npc_configs = {
            "พ่อบ้านเจมส์": {
                "path": "assets/npc_james.png",
                "height": int(SCREEN_HEIGHT * 0.65), 
                "pos_x": SCREEN_WIDTH - 150,         
                "pos_y": 750                        
            },
            "ลุงทอม คนสวน": {
                "path": "assets/npc_tom.png",
                "height": int(SCREEN_HEIGHT * 0.50), 
                "pos_x": SCREEN_WIDTH - 400,         
                "pos_y": 700                         
            },
            "มาดามโรส": {
                "path": "assets/npc_rose.png",
                "height": int(SCREEN_HEIGHT * 0.75), 
                "pos_x": SCREEN_WIDTH - 150,         
                "pos_y": 750             
            },
            "อลิซ": {
                "path": "assets/npc_alice.png",      
                "height": int(SCREEN_HEIGHT * 0.55), 
                "pos_x": SCREEN_WIDTH - 1150,         
                "pos_y": 650
            }
        }

        for name, config in npc_configs.items():
            try:
                img = pygame.image.load(config["path"]).convert_alpha() 
                orig_rect = img.get_rect()
                target_height = config["height"]
                ratio = target_height / orig_rect.height
                target_width = int(orig_rect.width * ratio)
                
                img = pygame.transform.scale(img, (target_width, target_height))
                self.npc_images[name] = img
                self.npc_rects[name] = img.get_rect(midbottom=(config["pos_x"], config["pos_y"])) 
                
            except Exception as e:
                print(f"โหลดรูป {name} ไม่ได้: {e}")
                self.npc_images[name] = None
                self.npc_rects[name] = pygame.Rect(550, 200, 150, 250)


    def setup_level_2(self):
        self.library = Location("ห้องสมุด", "เงียบสงบ แต่มีกองเลือดบนพื้น", bg_path="assets/bg_library.png")
        self.hallway = Location("โถงทางเดิน", "ทางเดินหน้าห้องสมุด", bg_path="assets/bg_hallway.png")

        rooms = [self.library, self.hallway]
        for current_room in rooms:
            for target_room in rooms:
                if current_room != target_room:
                    current_room.add_connection(target_room.name, target_room)

        self.library.add_item(Item("แว่นตาที่แตกหัก", "แว่นตาของอาจารย์ ถูกเหยียบพัง", image_path="assets/broken_glasses.png"))
        self.hallway.add_item(Item("หน้ากระดาษที่ถูกฉีก", "มีรอยจดเลคเชอร์ด้วยหมึกสีแดง", image_path="assets/torn_page.png"))

        david_dialogues = {
            "ทั่วไป": "ผมอ่านหนังสือเตรียมสอบอยู่มุมในสุด ไม่ได้ยินเสียงอะไรเลยครับ",
            "เวลา": "ตอนเกิดเหตุผมไม่ได้ลุกไปไหนเลยจริงๆ นะครับ",
            "ชี้ตัว": "ผมเป็นนักศึกษาดีเด่นนะ! จะไปทำร้ายอาจารย์ทำไม!"
        }
        david_reactions = {
            "แว่นตาที่แตกหัก": "น่ากลัวจังครับ... หวังว่าอาจารย์จะปลอดภัยนะ",
            "หน้ากระดาษที่ถูกฉีก": "!!!" 
        }
        self.david = Character(
            "เดวิด (นักศึกษา)", "ผู้ต้องสงสัย", david_dialogues, david_reactions,
            weakness="หน้ากระดาษที่ถูกฉีก",
            secret_dialogue="น...นั่นมันกระดาษเลคเชอร์ของผมนี่! ยอมรับก็ได้ครับ... ผมแอบเข้าไปขโมยข้อสอบ แต่อาจารย์มาเจอพอดี ผมตกใจเลยพลั้งมือผลักเขา!"
        )
        self.library.add_npc(self.david)

        self.current_location = self.library
        
        self.player = Player("เอลรอน") 
        
        self.current_npc = None
        self.current_dialogue = "[คดีที่ 2] เกิดเหตุทำร้ายร่างกายในห้องสมุด... จงหาหลักฐานมางัดข้ออ้างผู้ต้องสงสัย!"

        self.bg_images = {}
        for loc in [self.library, self.hallway]:
            try:
                img = pygame.image.load(loc.bg_path).convert_alpha()
                self.bg_images[loc.name] = pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))
            except:
                self.bg_images[loc.name] = None

        self.npc_images = {}
        self.npc_rects = {}
        try:
            img = pygame.image.load("assets/npc_david.png").convert_alpha()
            orig_rect = img.get_rect()
            target_height = int(SCREEN_HEIGHT * 0.70)
            ratio = target_height / orig_rect.height
            img = pygame.transform.scale(img, (int(orig_rect.width * ratio), target_height))
            self.npc_images["เดวิด (นักศึกษา)"] = img
            self.npc_rects["เดวิด (นักศึกษา)"] = img.get_rect(midbottom=(SCREEN_WIDTH - 250, 700))
        except:
            self.npc_rects["เดวิด (นักศึกษา)"] = pygame.Rect(550, 200, 150, 250)

    def draw_dialogue_box(self, text):
        max_chars = 65
        lines = []
        temp_text = text
        while len(temp_text) > 0:
            lines.append(temp_text[:max_chars])
            temp_text = temp_text[max_chars:]
            
        text_surfaces = []
        max_width = 0
        line_height = 35
        
        for line in lines:
            surf = self.font.render(line, True, WHITE)
            text_surfaces.append(surf)
            if surf.get_width() > max_width:
                max_width = surf.get_width()
                
        padding_x = 40 
        padding_y = 30 
        
        box_width = max_width + padding_x
        if box_width < 300: 
            box_width = 300
            
        box_height = (len(text_surfaces) * line_height) + padding_y
        
        box_x = 50
        box_y = SCREEN_HEIGHT - box_height - 40 
        
        rect = pygame.Rect(box_x, box_y, box_width, box_height)
        pygame.draw.rect(self.screen, GRAY, rect)
        pygame.draw.rect(self.screen, WHITE, rect, 2)
        
        if self.current_npc:
            speaker_name = self.font.render(self.current_npc.name, True, (100, 255, 100)) 
            speaker_rect = speaker_name.get_rect(bottomleft=(box_x + 10, box_y - 5))
            bg_rect = speaker_rect.inflate(20, 10) 
            
            pygame.draw.rect(self.screen, BLACK, bg_rect)
            pygame.draw.rect(self.screen, WHITE, bg_rect, 2)
            self.screen.blit(speaker_name, speaker_rect)
            
        current_y = box_y + (padding_y // 2)
        for surf in text_surfaces:
            self.screen.blit(surf, (box_x + (padding_x // 2), current_y))
            current_y += line_height

    def draw_navigation_buttons(self):
        self.nav_buttons = {}
        y_pos = 50 
        for direction, loc in self.current_location.connections.items():
            btn_rect = pygame.Rect(50, y_pos, 250, 40)
            pygame.draw.rect(self.screen, (100, 100, 255), btn_rect)
            pygame.draw.rect(self.screen, WHITE, btn_rect, 2)
            
            nav_text = self.font.render(f"ไปยัง: {loc.name}", True, WHITE)
            self.screen.blit(nav_text, (60, y_pos + 5))
            
            self.nav_buttons[direction] = (btn_rect, loc)
            y_pos += 50 

    def draw_choice_menu(self):
        self.choice_buttons = {}
        if self.current_npc:
            topics = self.current_npc.get_all_topics()
            for i, topic in enumerate(topics):
                color = (200, 100, 50)
                if topic == "ชี้ตัว": color = (200, 50, 50) 
                
                btn_rect = pygame.Rect(550, 50 + (i * 55), 200, 45)
                pygame.draw.rect(self.screen, color, btn_rect)
                pygame.draw.rect(self.screen, WHITE, btn_rect, 2)
                
                choice_text = self.font.render(topic, True, WHITE)
                self.screen.blit(choice_text, (570, 60 + (i * 55)))
                self.choice_buttons[topic] = btn_rect

    def draw_inventory(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(230)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        title = self.big_font.render("INVENTORY", True, WHITE)
        self.screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 30))
        
        self.inv_buttons = {} 
        items = self.player.inventory.get_all_items()
        
        if not items:
            msg = self.font.render("กระเป๋าว่างเปล่า...", True, GRAY)
            self.screen.blit(msg, (SCREEN_WIDTH//2 - msg.get_width()//2, 200))
        else:
            y = 120
            for item in items:
                btn_rect = pygame.Rect(100, y, 1050, 50) 
                pygame.draw.rect(self.screen, (70, 70, 90), btn_rect)
                pygame.draw.rect(self.screen, WHITE, btn_rect, 2)
                
                text_start_x = 120 
                if item.image:
                    self.screen.blit(item.image, (110, y + 5))
                    text_start_x = 160 

                action_text = ""
                if self.current_npc:
                    action_text = " [คลิกเพื่อยื่นหลักฐาน]"
                    
                text = self.font.render(f"- {item.name}: {item.description}{action_text}", True, WHITE)
                self.screen.blit(text, (text_start_x, y + 10))
                
                self.inv_buttons[item.name] = (btn_rect, item)
                y += 60
                
        close_msg = self.font.render("กด I อีกครั้ง หรือคลิกที่ว่างเพื่อปิด", True, GRAY)
        self.screen.blit(close_msg, (SCREEN_WIDTH//2 - close_msg.get_width()//2, 530))

    def draw_ending(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))
        
        if self.game_state == "WON":
            msg = "MISSION COMPLETE"
            color = (0, 255, 0)
            sub_msg = "คุณจับคนร้ายตัวจริงได้สำเร็จ!"
            
            if self.current_level == 1:
                retry_msg_text = "กด N เพื่อเล่นคดีที่ 2 หรือ ESC เพื่อออก"
            else:
                retry_msg_text = "คุณเคลียร์ครบทุกคดีแล้ว! สุดยอดมาก! กด ESC เพื่อออก"
        else:
            msg = "GAME OVER"
            color = (255, 0, 0)
            sub_msg = "คุณจับผิดคน คนร้ายตัวจริงหนีไปได้..."
            retry_msg_text = "กด R เพื่อเริ่มคดีนี้ใหม่ หรือ ESC เพื่อออก"

        text_surf = self.big_font.render(msg, True, color)
        sub_surf = self.font.render(sub_msg, True, WHITE)
        self.screen.blit(text_surf, (SCREEN_WIDTH//2 - text_surf.get_width()//2, 200))
        self.screen.blit(sub_surf, (SCREEN_WIDTH//2 - sub_surf.get_width()//2, 320))
        
        retry_msg = self.font.render(retry_msg_text, True, GRAY)
        self.screen.blit(retry_msg, (SCREEN_WIDTH//2 - retry_msg.get_width()//2, 500))

    def run(self):
        while self.is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                
                if event.type == pygame.KEYDOWN:
                    if self.game_state in ["WON", "LOST"]:
                        if event.key == pygame.K_r: 
                            if self.current_level == 1: self.setup_level_1()
                            else: self.setup_level_2()
                            self.game_state = "PLAYING"
                            
                        if event.key == pygame.K_n and self.game_state == "WON" and self.current_level == 1:
                            self.current_level = 2
                            self.setup_level_2()
                            self.game_state = "PLAYING"
                            
                        if event.key == pygame.K_ESCAPE: 
                            self.is_running = False
                    
                    elif self.game_state == "PLAYING":
                        if event.key == pygame.K_i:
                            self.show_inventory_ui = not self.show_inventory_ui

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.game_state == "MENU":
                        for text, rect in self.menu_buttons.items():
                            if rect.collidepoint(event.pos):
                                self.sound_manager.play_sfx("click")
                                if text == "เริ่มเกม (Start)":
                                    self.game_state = "PLAYING"
                                elif text == "วิธีเล่น (How to Play)":
                                    self.game_state = "HOW_TO_PLAY"
                                elif text == "ออก (Exit)":
                                    self.is_running = False
                    
                    elif self.game_state == "HOW_TO_PLAY":
                        if self.menu_buttons.get("Back") and self.menu_buttons["Back"].collidepoint(event.pos):
                            self.sound_manager.play_sfx("click")
                            self.game_state = "MENU"

                    elif self.game_state == "PLAYING":
                        if self.show_inventory_ui:
                            clicked_item = False
                            for item_name, (rect, item) in self.inv_buttons.items():
                                if rect.collidepoint(event.pos):
                                    self.sound_manager.play_sfx("click")
                                    if self.current_npc:
                                        self.current_dialogue = self.current_npc.react_to_evidence(item.name)
                                        self.sound_manager.play_sfx("shock")
                                    else:
                                        self.current_dialogue = f"คุณกำลังดู: {item.name}"
                                    self.show_inventory_ui = False 
                                    clicked_item = True
                                    break
                            
                            if not clicked_item:
                                self.show_inventory_ui = False 
                                
                        else:
                            clicked_choice = False
                            if self.current_npc:
                                for topic, rect in self.choice_buttons.items():
                                    if rect.collidepoint(event.pos):
                                        self.sound_manager.play_sfx("click")
                                        
                                        if topic == "ชี้ตัว":
                                            real_killer = "พ่อบ้านเจมส์" if self.current_level == 1 else "เดวิด (นักศึกษา)"
                                            
                                            if self.current_npc.name == real_killer:
                                                if self.current_npc.alibi_broken: 
                                                    self.game_state = "WON"
                                                    self.sound_manager.play_sfx("shock")
                                                else:
                                                    self.current_dialogue = "คุณไม่มีหลักฐานมัดตัวผมหรอกครับนักสืบ!"
                                            else:
                                                self.game_state = "LOST"
                                                self.sound_manager.play_sfx("shock")
                                        else:
                                            self.current_dialogue = self.current_npc.speak(topic)
                                            
                                        clicked_choice = True
                                        break

                            if not clicked_choice:
                                for direction, (rect, loc) in self.nav_buttons.items():
                                    if rect.collidepoint(event.pos):
                                        self.sound_manager.play_sfx("click")
                                        self.current_location = loc
                                        self.current_npc = None
                                        self.current_dialogue = f"คุณเข้ามาใน {loc.name}"
                                        break

                                for npc in self.current_location.npcs:
                                    npc_rect = self.npc_rects.get(npc.name)
                                    if npc_rect and npc_rect.collidepoint(event.pos):
                                        self.sound_manager.play_sfx("click")
                                        self.current_npc = npc
                                        self.current_dialogue = f"คุณกำลังคุยกับ {npc.name} (กด I เพื่อยื่นหลักฐาน)"

                                if self.current_location.items:
                                    for i, item in enumerate(self.current_location.items):
                                        item_rect = pygame.Rect(350 + (i * 60), 350, 40, 40)
                                        if item_rect.collidepoint(event.pos):
                                            self.sound_manager.play_sfx("collect")
                                            collected_item = self.current_location.items.pop(i)
                                            self.player.collect_item(collected_item)
                                            self.current_dialogue = f"พบหลักฐานใหม่: {collected_item.name}!"
                                            break

            if self.game_state == "MENU":
                self.draw_main_menu()
            elif self.game_state == "HOW_TO_PLAY":
                self.draw_instructions()
            elif self.game_state == "PLAYING":
                self.screen.fill(BLACK)
                
                current_bg = self.bg_images.get(self.current_location.name)
                if current_bg: 
                    self.screen.blit(current_bg, (0, 0))

                title = self.font.render(f"สถานที่: {self.current_location.name}", True, (0, 255, 0))
                self.screen.blit(title, (20, 10))

                for npc in self.current_location.npcs:
                    npc_img = self.npc_images.get(npc.name)
                    npc_rect = self.npc_rects.get(npc.name)

                    if npc_img:
                        self.screen.blit(npc_img, npc_rect)
                    else:
                        if npc.name == "พ่อบ้านเจมส์": color = (200, 0, 0)
                        elif npc.name == "ลุงทอม คนสวน": color = (0, 0, 200)
                        else: color = (150, 0, 150) 
                        pygame.draw.rect(self.screen, color, npc_rect)

                    role_text = f"{npc.name} ({npc.description})" 
                    name_surf = self.font.render(role_text, True, (255, 255, 0)) 
                    
                    name_rect = name_surf.get_rect(midbottom=(npc_rect.centerx, npc_rect.top - 10))
                    bg_rect = name_rect.inflate(20, 10)
                    
                    if bg_rect.right > SCREEN_WIDTH - 10:    
                        bg_rect.right = SCREEN_WIDTH - 10    
                        name_rect.center = bg_rect.center    
                    
                    pygame.draw.rect(self.screen, BLACK, bg_rect)
                    pygame.draw.rect(self.screen, WHITE, bg_rect, 2)
                    self.screen.blit(name_surf, name_rect)

                if not self.show_inventory_ui:
                    for i, item in enumerate(self.current_location.items):
                        item_x = 350 + (i * 60) 
                        item_y = 350
                        if item.image:
                            self.screen.blit(item.image, (item_x, item_y))
                        else:
                            pygame.draw.rect(self.screen, (255, 255, 0), (item_x, item_y, 40, 40))

                    self.draw_navigation_buttons()
                    self.draw_dialogue_box(self.current_dialogue)
                    self.draw_choice_menu()
                else:
                    self.draw_inventory()
            else:
                self.draw_ending()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = DetectiveGame()
    game.run()