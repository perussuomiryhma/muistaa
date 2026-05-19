import sys
import os
import subprocess
import tkinter as tk
from tkinter import messagebox
import random
import winsound

# 1. 인코딩 및 환경 설정
os.environ["PYTHONIOENCODING"] = "utf-8"

# 2. 필수 라이브러리 설치
try:
    from PIL import Image, ImageTk
except ModuleNotFoundError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pillow"])
    from PIL import Image, ImageTk

# 3. 설정
IMAGE_FOLDER_PATH = r"C:\Users\Work-1\Desktop\image"

Meidän_ryhmä = {
    "Kuka on luokkamme opettaja?": "Heidi", 
    "Kuka on luokkamme insinööri?": "Migara",
    "Kuka on luokkamme toinen insinööri?": "Sana",
    "Kuka on luokkamme vilkkain opiskelija?": "Tanja",
    "Hän tuli luokallemme kesken kurssin, kun se oli jo alkanut.": "Mbuyi",
    "Hän vastaa aina erittäin aktiivisesti tunneilla.": "Hamza",
    "Hän osasi jo ensimmäisellä tunnilla paljon sanoja ja puhui hyvää suomea.": "Sunita",
    "Hän ymmärsi opettajaa ja vastasi hienosti heti ensimmäisestä tunnista lähtien.": "Antoni",
    "Hän tuli luokallemme noin elokuussa. Puhuu hyvää suomea ja haaveilee vaatesuunnittelijan urasta.": "Khali",
    "Hän on pieni mutta vahva. Hän on aina erittäin ystävällinen.": "Sakineh",
    "Hänestä oli heti alusta asti paljon huhuja, että hän puhuu erittäin hyvää suomea.": "Oksana",
    "Hän oli erittäin aktiivinen ensiapuohjelmassa.": "Andri",
    "Hän istuu aina takarivissä, mutta suhtautuu suomen kielen opiskeluun suurella sydämellä.": "Sergi",
    "Hän on aina Oksanan parina luokassa.": "Elena",
    "Kuka istuu Tanjan lähellä?": "Anna",
    "Hän on erittäin kiinnostunut suomen kielestä ja on aina ystävällinen.": "Elius",
    "Hän istuu aina keskirivissä ja opiskelee suomea todella ahkerasti.": "Yogendra",
    "Hänellä on aina paras ystävä vierellään. Molemmat heistä puhuvat erittäin hyvää suomea.": "Soosan"
}

kaikki_sanat = list(Meidän_ryhmä.keys())
eka_kysymys = kaikki_sanat[0]
muut_kysymykset = kaikki_sanat[1:]    
random.shuffle(muut_kysymykset)        
sanat = [eka_kysymys] + muut_kysymykset 

nykyinen_numero = 0
pisteet = 0
g_keep_image = None 

# 4. 함수 정의
def find_any_matching_image(filename_without_ext, is_main=False):
    if not os.path.exists(IMAGE_FOLDER_PATH): return None
    valid_extensions = (".jpg", ".jpeg", ".png", ".bmp", ".gif")
    files = os.listdir(IMAGE_FOLDER_PATH)
    if is_main:
        for f in files:
            if ("quiz_main" in f.lower() or "main" in f.lower()) and f.lower().endswith(valid_extensions):
                return os.path.join(IMAGE_FOLDER_PATH, f)
    else:
        for f in files:
            name_part, ext_part = os.path.splitext(f)
            if name_part.lower() == filename_without_ext.lower() and ext_part.lower() in valid_extensions:
                return os.path.join(IMAGE_FOLDER_PATH, f)
    return None

def set_label_image_by_logic(name_without_ext, is_main=False):
    global g_keep_image
    final_path = find_any_matching_image(name_without_ext, is_main)
    try:
        if final_path:
            img = Image.open(final_path)
            img.thumbnail((260, 260))  
            g_keep_image = ImageTk.PhotoImage(img)
            kuva_label.config(image=g_keep_image, text="")
        else:
            kuva_label.config(image="", text="Kuvaa ei löytynyt")
    except Exception:
        kuva_label.config(image="", text="Virhe kuvan lataamisessa")

def tarkista_vastaus():
    global nykyinen_numero, pisteet
    user_input = syotto.get().strip()
    if not user_input: return
    kayttajan_vastaus = user_input.title()
    nykyinen_sana = sanat[nykyinen_numero]
    oikea_vastaus = Meidän_ryhmä[nykyinen_sana]
    
    set_label_image_by_logic(oikea_vastaus.lower(), is_main=False)
    ikkuna.update() 
    
    if kayttajan_vastaus == oikea_vastaus:
        winsound.Beep(523, 150)
        messagebox.showinfo("Oikein!", "Heidi opettaja! Sinä olet B1 🎉")
        pisteet += 1
        set_label_image_by_logic("quiz_main", is_main=True)
        ikkuna.update()
        nykyinen_numero += 1
        syotto.delete(0, tk.END)
        seuraava_kysymys()
    else:
        winsound.Beep(220, 500)
        hint = oikea_vastaus[0]
        messagebox.showerror("Väärin", f"Heidi opettaja! Sinä olet A2.2\nVinkki: {hint}")
        set_label_image_by_logic("quiz_main", is_main=True)
        ikkuna.update()
        syotto.delete(0, tk.END)
        syotto.focus()

def seuraava_kysymys():
    if nykyinen_numero < len(sanat):
        teksti_kysymys.config(text=sanat[nykyinen_numero])
        if nykyinen_numero == 0: set_label_image_by_logic("quiz_main", is_main=True)
    else:
        # [마지막 문구 적용]
        messagebox.showinfo("Peli ohi", f"Heidi opettaja, sinä olet B1, tämä on B1 todistus! 🎉\nTuloksesi: {pisteet}/{len(Meidän_ryhmä)}")
        ikkuna.destroy()

# 5. UI 디자인
ikkuna = tk.Tk()
ikkuna.title("Meidän ryhmä")
ikkuna.geometry("550x550")
ikkuna.config(bg="#f4f7f6")
kuva_label = tk.Label(ikkuna, bg="#f4f7f6", fg="red", justify="center", font=("Helvetica", 10, "bold"), wraplength=500)
kuva_label.pack(pady=20)
teksti_kysymys = tk.Label(ikkuna, text="", font=("Helvetica", 14, "bold"), bg="#f4f7f6", fg="#003580", wraplength=500, justify="center")
teksti_kysymys.pack(pady=15)
syotto = tk.Entry(ikkuna, font=("Helvetica", 13), width=20, justify="center", bd=2, relief="groove")
syotto.pack(pady=5)
syotto.focus()
painike_tarkista = tk.Button(ikkuna, text="Tarkista", font=("Helvetica", 11, "bold"), bg="#003580", fg="white", width=15, height=1, relief="flat", command=tarkista_vastaus)
painike_tarkista.pack(pady=15)
ikkuna.after(10, seuraava_kysymys)
ikkuna.mainloop()
