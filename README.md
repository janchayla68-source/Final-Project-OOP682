# 🕵️‍♀️ The Shadow of Eldoria
PYGAME
**โครงงานกลุ่มรายวิชาการเขียนโปรแกรมเชิงวัตถุ (OOP Final Team Project)**
สาขาวิทยาการข้อมูลและนวัตกรรมซอฟต์แวร์ (DSSI) 

## 👥 สมาชิกทีม 
* **สมาชิก 1:** นางสาวนางสาวจันทร์ฉาย เหล่าสาร รหัสนักศึกษา [68114540100] 
  * **หน้าที่ความรับผิดชอบ:** System Architect, Lead Programmer (Game Logic, OOP Architecture, UI/UX)

## 🎮 สิ่งที่ซอฟต์แวร์ทำได้ (Features)
- **Free Roam Navigation:** ระบบเดินสำรวจห้องต่างๆ แบบอิสระ
- **Inventory System:** ระบบเก็บหลักฐานและจัดการไอเทมในกระเป๋า
- **Cross-Examination Logic:** ระบบสืบสวนเชิงจิตวิทยา นำหลักฐานมาหักล้างคำให้การเพื่อจับโกหก
- **Multi-level System:** รองรับการเล่นหลายคดีต่อเนื่อง (คดีคฤหาสน์ และ คดีห้องสมุด)

## ⚙️ วิธีการติดตั้งและใช้งาน (Installation & Usage)

### สิ่งที่ต้องมี (Prerequisites)
- Python 3.8 หรือใหม่กว่า

### ขั้นตอนการติดตั้ง (Installation Steps)
1. โคลน Repository นี้ลงมาที่เครื่องของคุณ:
   git clone https://github.com/janchayla68-source/The-Shadow-of-Eldoria.git
2. เข้าไปในโฟลเดอร์ของโปรเจคต์:
   cd the-shadow-of-eldoria
3. ติดตั้ง Library ที่เกี่ยวข้องผ่านไฟล์ requirements.txt:
   pip install -r requirements.txt
4. รันเกมด้วยคำสั่ง:
   python main.py

   วิธีการควบคุมเกม (Controls)
คลิกซ้าย: เพื่อย้ายห้อง, คุยกับตัวละคร, หรือเก็บหลักฐาน

ปุ่ม I: เพื่อเปิด/ปิด หน้าต่างกระเป๋า (Inventory) เพื่อยื่นหลักฐานให้ตัวละคร

ปุ่ม R: เพื่อเริ่มคดีนั้นใหม่ (เมื่อเกมโอเวอร์)

ปุ่ม N: เพื่อไปยังคดีถัดไป (เมื่อเคลียร์คดีสำเร็จ)

ปุ่ม ESC: เพื่อออกจากเกม

## 🤖 Acknowledgement (การกิตติกรรมประกาศ)
โปรเจกต์นี้มีการออกแบบสถาปัตยกรรมซอฟต์แวร์และ Game Logic โดยผู้พัฒนาหลัก และมีการใช้ Generative AI เป็นเครื่องมือช่วยในการพัฒนา (AI-Assisted Development) สำหรับการเขียนโครงสร้างโค้ดบางส่วนและการ Debug เพื่อให้โปรเจกต์เสร็จสมบูรณ์ตามหลักการ OOP และ SOLID Principles