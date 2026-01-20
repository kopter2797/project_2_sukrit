import math # นำเข้าไลบรารี math สำหรับการคำนวณทางคณิตศาสตร์ (เช่น ceil)

# คลาสสำหรับ Vigenère Cipher (การเข้ารหัสแบบวิจเนียร์)
class Vigenere:
    # เมธอดสำหรับเข้ารหัส (Encrypt) ข้อมูล
    @staticmethod
    def encrypt(text, key):
        encrypted_text = [] # สร้างลิสต์ว่างสำหรับเก็บผลลัพธ์ที่เข้ารหัสแล้ว
        key_index = 0 # ตัวแปรสำหรับติดตามตำแหน่งของตัวอักษรใน Key
        key = key.upper() # แปลง Key เป็นตัวพิมพ์ใหญ่ทั้งหมดเพื่อให้ง่ายต่อการคำนวณ
        
        # วนลูปตรวจสอบทุกตัวอักษรในข้อความ (text)
        for char in text:
            if char.isalpha(): # ถ้าตัวอักษรเป็นพยัญชนะ (A-Z หรือ a-z)
                # คำนวณค่าการเลื่อน (Shift) จากตัวอักษรใน Key ตามตำแหน่งปัจจุบัน
                # ใช้ modulo (% len(key)) เพื่อวนใช้ Key ซ้ำถ้ายาวไม่พอ
                shift = ord(key[key_index % len(key)]) - ord('A')
                
                if char.isupper(): # ถ้าตัวอักษรต้นฉบับเป็นพิมพ์ใหญ่
                    # คำนวณการเลื่อนแบบวงกลม (0-25) แล้วแปลงกลับเป็น ASCII
                    encrypted_text.append(chr((ord(char) - ord('A') + shift) % 26 + ord('A')))
                else: # ถ้าตัวอักษรต้นฉบับเป็นพิมพ์เล็ก
                    # คำนวณการเลื่อนแบบวงกลม (0-25) แล้วแปลงกลับเป็น ASCII พิมพ์เล็ก
                    encrypted_text.append(chr((ord(char) - ord('a') + shift) % 26 + ord('a')))
                
                key_index += 1 # ขยับตำแหน่ง Key ไปตัวถัดไป
            else:
                # ถ้าไม่ใช่ตัวอักษร (เช่น ตัวเลข, สัญลักษณ์) ให้เก็บไว้เหมือนเดิม
                encrypted_text.append(char)
        
        return "".join(encrypted_text) # รวมลิสต์กลับเป็นข้อความสตริงและส่งคืน

    # เมธอดสำหรับถอดรหัส (Decrypt) ข้อมูล
    @staticmethod
    def decrypt(text, key):
        decrypted_text = [] # สร้างลิสต์ว่างสำหรับเก็บผลลัพธ์ที่ถอดรหัสแล้ว
        key_index = 0 # ตัวแปรสำหรับติดตามตำแหน่งของตัวอักษรใน Key
        key = key.upper() # แปลง Key เป็นตัวพิมพ์ใหญ่
        
        # วนลูปตรวจสอบทุกตัวอักษรในข้อความที่เข้ารหัสมา (text)
        for char in text:
            if char.isalpha(): # ถ้าเป็นตัวอักษร
                # คำนวณค่าการเลื่อน (Shift) จาก Key เหมือนตอนเข้ารหัส
                shift = ord(key[key_index % len(key)]) - ord('A')
                
                if char.isupper(): # ถ้าเป็นพิมพ์ใหญ่
                    # ถอยหลังค่า Shift เพื่อถอดรหัส (+26 เพื่อกันค่าติดลบก่อน Modulo)
                    decrypted_text.append(chr((ord(char) - ord('A') - shift + 26) % 26 + ord('A')))
                else: # ถ้าเป็นพิมพ์เล็ก
                    decrypted_text.append(chr((ord(char) - ord('a') - shift + 26) % 26 + ord('a')))
                
                key_index += 1 # ขยับตำแหน่ง Key
            else:
                # ถ้าไม่ใช่ตัวอักษร ให้คงค่าเดิมไว้
                decrypted_text.append(char)
        
        return "".join(decrypted_text) # ส่งคืนข้อความที่ถอดรหัสแล้ว

# คลาสสำหรับ Caesar Cipher (การเข้ารหัสแบบซีซาร์)
class Caesar:
    # เมธอดสำหรับเข้ารหัส (Encrypt)
    @staticmethod
    def encrypt(text, shift):
        try:
            shift = int(shift) # พยายามแปลงค่า Shift เป็นตัวเลขจำนวนเต็ม
        except ValueError:
            return "ค่าการเลื่อนไม่ถูกต้อง (Invalid shift value)" # ถ้าแปลงไม่ได้ให้แจ้งเตือน
            
        encrypted_text = [] # ลิสต์เก็บผลลัพธ์
        
        # วนลูปทุกตัวอักษรในข้อความ
        for char in text:
            if char.isalpha(): # ถ้าเป็นตัวอักษร
                # กำหนดฐาน ASCII ว่าเป็นพิมพ์ใหญ่ ('A') หรือพิมพ์เล็ก ('a')
                base = ord('A') if char.isupper() else ord('a')
                # คำนวณการเลื่อนตำแหน่งตามค่า shift
                encrypted_text.append(chr((ord(char) - base + shift) % 26 + base))
            else:
                # ถ้าไม่ใช่ตัวอักษร เก็บค่าเดิม
                encrypted_text.append(char)
        
        return "".join(encrypted_text) # ส่งคืนผลลัพธ์

    # เมธอดสำหรับถอดรหัส (Decrypt)
    @staticmethod
    def decrypt(text, shift):
        try:
            shift = int(shift) # ตรวจสอบค่า Shift
        except ValueError:
            return "ค่าการเลื่อนไม่ถูกต้อง (Invalid shift value)"
        
        # การถอดรหัส Caesar คือการเข้ารหัสด้วยค่า Shift ที่เป็นลบ (-shift)
        return Caesar.encrypt(text, -shift)

# คลาสสำหรับ Number Cipher (ระบบตัวเลข A1Z26 ผสม ASCII)
class Number:
    # เมธอดสำหรับเข้ารหัส (Encrypt)
    @staticmethod
    def encrypt(text, key=0):
        # พยายามแปลง Key เป็นตัวเลข (ถ้าไม่ได้ให้เป็น 0)
        try:
            key = int(key)
        except (ValueError, TypeError):
            key = 0
            
        encrypted_text = [] # ลิสต์เก็บผลลัพธ์
        
        for char in text:
            if char.isalpha(): # ถ้าเป็นตัวอักษร (A-Z)
                # แปลงเป็นตัวเลข 1-26 (A=1, B=2...) แล้วบวกค่า Key
                num = ord(char.upper()) - ord('A') + 1 + key
                encrypted_text.append(str(num)) # เก็บเป็นข้อความตัวเลข
            elif 32 <= ord(char) <= 126: # ถ้าเป็นอักขระที่พิมพ์ได้อื่น ๆ (เช่น สัญลักษณ์)
                # ใช้ค่ารหัส ASCII ของตัวนั้น ๆ บวกค่า Key
                num = ord(char) + key
                encrypted_text.append(str(num))
            else:
                # ถ้าเป็นอักขระพิเศษอื่น ๆ (เช่น ขึ้นบรรทัดใหม่) ให้เก็บไว้เหมือนเดิม
                encrypted_text.append(char)
        
        return " ".join(encrypted_text) # ส่งคืนผลลัพธ์โดยคั่นด้วยช่องว่าง

    # เมธอดสำหรับถอดรหัส (Decrypt)
    @staticmethod
    def decrypt(text, key=0):
        # แปลง Key เป็นตัวเลข
        try:
            key = int(key)
        except (ValueError, TypeError):
            key = 0
            
        # เตรียมข้อมูล: แทนที่ขีด (-) ด้วยช่องว่าง เพื่อรองรับรูปแบบที่ใช้ขีดคั่น
        text = text.replace('-', ' ')
        
        parts = text.split(' ') # แยกข้อความด้วยช่องว่างให้เป็นชิ้นส่วน (Token)
        decrypted_text = [] # ลิสต์เก็บผลลัพธ์
        
        for part in parts:
            current_segment = ""
            # ตรวจสอบว่าชิ้นส่วนนี้เป็นตัวเลขหรือไม่ (รวมถึงเลขติดลบด้วย)
            if part.replace('-', '', 1).isdigit():
                try:
                    val = int(part) - key # ลบค่า Key ออกเพื่อหาค่าจริง
                    
                    if 1 <= val <= 26: # ถ้าค่าอยู่ในช่วง 1-26
                        # แปลงกลับเป็นตัวอักษร A-Z
                        current_segment += chr(val - 1 + ord('A'))
                    else:
                        # ถ้าไม่ใช่ 1-26 ให้ลองแปลงเป็น ASCII
                        try:
                            current_segment += chr(val)
                        except ValueError:
                            # ถ้าแปลง ASCII ไม่ได้ ให้แสดงค่าตัวเลขในวงเล็บ []
                            current_segment += f"[{val}]"
                except ValueError:
                    # ถ้าเกิดข้อผิดพลาดในการคำนวณ ให้คงค่าเดิมไว
                    current_segment += part
            else:
                # ถ้าไม่ใช่ตัวเลข (เช่น ช่องว่างที่เกินมา หรือขยะ) ให้คงค่าเดิม
                current_segment += part
            
            decrypted_text.append(current_segment) # เก็บผลลัพธ์ของส่วนนี้
        
        return "".join(decrypted_text) # รวมผลลัพธ์ทั้งหมดเป็นข้อความ

# คลาสสำหรับ Columnar Transposition Cipher (การสลับตำแหน่งแบบคอลัมน์)
class Columnar:
    # เมธอดสำหรับเข้ารหัส (Encrypt)
    @staticmethod
    def encrypt(text, key):
        msg = text 
        # สร้างลำดับการอ่านคอลัมน์ โดยเรียงตามตัวอักษรของ Key
        # เช่น Key = "ZEBRA" -> ลำดับจะเป็น 5, 2, 1, 4, 3 (ตาม A-Z)
        key_indices = sorted(range(len(key)), key=lambda k: key[k])
        
        num_cols = len(key) # จำนวนคอลัมน์เท่ากับความยาว Key
        # คำนวณจำนวนแถวที่ต้องใช้
        num_rows = math.ceil(len(msg) / num_cols)
        
        # เติมข้อความ (Padding) ด้วย _ ให้เต็มตารางสี่เหลี่ยม
        padded_msg = msg.ljust(num_rows * num_cols, '_')
        
        grid = [] # สร้างตาราง
        for i in range(num_rows):
            # ตัดแบ่งข้อความใส่ลงในแต่ละแถว
            grid.append(padded_msg[i*num_cols : (i+1)*num_cols])
            
        encrypted_text = ""
        # อ่านข้อมูลออกจากตารางตามลำดับคอลัมน์ที่เรียงไว้ (key_indices)
        for idx in key_indices:
            for row in grid:
                encrypted_text += row[idx] # อ่านตัวอักษรในคอลัมน์นั้นจากทุกแถว
                
        return encrypted_text # ส่งคืนข้อความที่สลับตำแหน่งแล้ว

    # เมธอดสำหรับถอดรหัส (Decrypt)
    @staticmethod
    def decrypt(text, key):
        num_cols = len(key) # จำนวนคอลัมน์
        num_rows = math.ceil(len(text) / num_cols) # คำนวณจำนวนแถว
        # หาลำดับคอลัมน์ที่ถูกสลับไป เพื่อจะนำข้อมูลกลับมาใส่ให้ถูกช่อง
        key_indices = sorted(range(len(key)), key=lambda k: key[k])
        
        # สร้างตารางว่างเตรียมไว้
        grid = [['' for _ in range(num_cols)] for _ in range(num_rows)]
        
        # เติมข้อมูลลงในตารางทีละคอลัมน์ ตามลำดับ key_indices
        current_idx = 0
        for key_idx in key_indices:
            for row in range(num_rows):
                if current_idx < len(text):
                    # ใส่ตัวอักษรลงในช่องที่ถูกต้อง (แถว row, คอลัมน์ key_idx)
                    grid[row][key_idx] = text[current_idx]
                    current_idx += 1
                    
        # อ่านข้อมูลออกจากตารางทีละแถว (จากซ้ายไปขวา) เพื่อให้ได้ข้อความเดิม
        decrypted_text = ""
        for row in grid:
            decrypted_text += "".join(row)
            
        return decrypted_text.rstrip('_') # ตัดตัวอักษร Padding (_) ทิ้งที่ท้ายข้อความก่อนส่งคืน
