import json
import os
import urllib.request
import urllib.parse

DB_FILE = "polyuz_data.json"
ADMIN_PAROL = "7777"

def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"foydalanuvchilar": {}, "tarix": []}

def save_data(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def online_tarjima(soz, hedef_til_kodi="en"):
    try:
        encoded_soz = urllib.parse.quote(soz)
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=uz&tl={hedef_til_kodi}&dt=t&q={encoded_soz}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read().decode('utf-8'))
            return res[0][0][0]
    except:
        return "Internet aloqasi yo'q."

def main():
    db = load_data()
    if "foydalanuvchilar" not in db:
        db = {"foydalanuvchilar": {}, "tarix": []}
    
    print("=" * 60)
    print("      POLYUZ: TIL VA HAYOT (UNIVERSAL TIZIM)      ")
    print("=" * 60)
    
    username = input("\nIsmingizni kiriting: ").strip()
    if not username:
        username = "Mehmon"
        
    if username.lower() == "admin":
        parol = input("Admin parolini kiriting: ").strip()
        if parol == ADMIN_PAROL:
            print("\n👑 Boshqaruv xonasiga xush kelibsiz!")
            while True:
                print("\n--- ADMIN PANEL ---")
                print("[1] Jami foydalanuvchilar")
                print("[2] So'rovlar tarixi")
                print("[3] Chiqish")
                a_tanlov = input("Tanlang (1-3): ").strip()
                if a_tanlov == '1':
                    print(f"\n📊 Jami foydalanuvchilar: {len(db['foydalanuvchilar'])}")
                    for usr, info in db['foydalanuvchilar'].items():
                        print(f" - {usr} | {info['maqsad']} | Ball: {info['ball']}")
                elif a_tanlov == '2':
                    print("\n📜 So'rovlar:")
                    for t in db['tarix'][-15:]:
                        print(f"[{t['ism']}]: {t['soz']} ➡️ {t['til']}")
                elif a_tanlov == '3':
                    break
            return
        else:
            print("❌ Xato parol!")
            return

    if username not in db["foydalanuvchilar"]:
        db["foydalanuvchilar"][username] = {"maqsad": "Nemis tili", "til_kodi": "de", "ball": 0}
        save_data(db)
        
    user = db["foydalanuvchilar"][username]
    print(f"\nXush kelibsiz, {username}! Maqsadingiz: {user['maqsad']}")
    
    while True:
        print(f"\n--- ASOSIY MENYU [Ball: {user['ball']}] ---")
        print("[1] AI Onlayn Tarjimon (So'z/gap tarjima qilish)")
        print("[2] O'qish yo'nalishini o'zgartirish")
        print("[3] Profil statistikasi")
        print("[4] Ilova haqida va Shartlar")
        print("[5] Chiqish")
        
        amal = input("Amalni tanlang (1-5): ").strip()
        
        if amal == '1':
            print("\n--- AI ONLAYN TARJIMON ---")
            soz_gap = input("O'zbek tilida so'z yoki gap yozing: ").strip()
            if soz_gap:
                natija = online_tarjima(soz_gap, user['til_kodi'])
                print(f"🌍 Tarjimasi ({user['maqsad']}): **{natija}**\n")
                db["tarix"].append({"ism": username, "soz": soz_gap, "til": user['maqsad']})
                save_data(db)
            else:
                print("⚠️ Matn kiritilmadi!")
                
        elif amal == '2':
            print("\nYo'nalishni tanlang:")
            print("[1] Nemis tili (de)")
            print("[2] Ingliz tili (en)")
            print("[3] Koreys tili (ko)")
            t_tanlov = input("Tanlov (1-3): ").strip()
            if t_tanlov == '1':
                user['maqsad'] = "Nemis tili"; user['til_kodi'] = "de"
            elif t_tanlov == '2':
                user['maqsad'] = "Ingliz tili"; user['til_kodi'] = "en"
            elif t_tanlov == '3':
                user['maqsad'] = "Koreys tili"; user['til_kodi'] = "ko"
            save_data(db)
            print(f"✅ O'zgartirildi: {user['maqsad']}")
            
        elif amal == '3':
            print(f"\n--- PROFIL ---")
            print(f"Foydalanuvchi: {username}")
            print(f"Til: {user['maqsad']}")
            print(f"Ball: {user['ball']}")
            
        elif amal == '4':
            print("\n" + "="*40)
            print(" Ilova versiyasi: v1.0.4")
            print(" Dastur ta'lim va tarjima maqsadida tuzilgan.")
            print("\n [Qo'shimcha shartlar]")
            print(" Dasturdan foydalanish jarayonida internet tarmog'i")
            print(" orqali so'rovlar almashinuvi amalga oshiriladi.")
            print(" Barcha huquqlar himoyalangan. 2026.")
            print("="*40 + "\n")
            
        elif amal == '5':
            print("Xayr!")
            break

if __name__ == "__main__":
    main()
