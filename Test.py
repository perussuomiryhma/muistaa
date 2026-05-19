import streamlit as st
from PIL import Image
import random
import os
import base64

# 1. 퀴즈 데이터 세팅
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
    "Hän istuu aina takarivissä, mutta suhtautuu suomen kielen opiskeluun suurella sydämellä.": "Serhii",
    "Hän on aina Oksanan parina luokassa.": "Elena",
    "Kuka istuu Tanjan lähellä?": "Anna",
    "Hän on erittäin kiinnostunut suomen kielestä ja on aina ystävällinen.": "Elius",
    "Hän istuu aina keskirivissä ja opiskelee suomea todella ahkerasti.": "Yogendra",
    "Hänellä on aina paras ystävä vierellään. Molemmat heistä puhuvat erittäin hyvää suomea.": "Soosan"
}

# 2. 웹 브라우저용 세션 상태 초기화
if 'sanat' not in st.session_state:
    kaikki_sanat = list(Meidän_ryhmä.keys())
    eka_kysymys = kaikki_sanat[0]
    muut_kysymykset = kaikki_sanat[1:]    
    random.shuffle(muut_kysymykset)        
    st.session_state.sanat = [eka_kysymys] + muut_kysymykset 
    
    st.session_state.idx = 0
    st.session_state.pisteet = 0
    st.session_state.game_over = False
    st.session_state.show_correct_image = False

st.set_page_config(page_title="Meidän ryhmä", page_icon="🇫🇮", layout="centered")
st.title("🇫🇮 Meidän ryhmä")


# 🎵 3. 자동 무한 반복 배경음악 플레이어 (중복 확장자 완벽 대응)
def play_bgm():
    # bgm.mp3.mp3 또는 bgm.mp3 둘 다 찾아내는 스마트 추적
    file_name = None
    if os.path.exists("bgm.mp3.mp3"):
        file_name = "bgm.mp3.mp3"
    elif os.path.exists("bgm.mp3"):
        file_name = "bgm.mp3"

    if file_name:
        with open(file_name, "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
            md = f"""
                <audio id="bgm" autoplay loop>
                    <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
                </audio>
                <script>
                    var audio = document.getElementById("bgm");
                    audio.volume = 0.3; // 소리 크기 (0.0 ~ 1.0)
                    
                    // 새로고침 해도 음악이 끊김 없이 흐르게 하는 마법
                    if (localStorage.getItem("bgm_time")) {{
                        audio.currentTime = parseFloat(localStorage.getItem("bgm_time"));
                    }}
                    setInterval(function() {{
                        localStorage.setItem("bgm_time", audio.currentTime);
                    }}, 300);
                </script>
                """
            st.markdown(md, unsafe_allow_html=True)

play_bgm()


# 🏆 4. 게임 종료 및 B1 TODISTUS 출력 화면
if st.session_state.game_over:
    st.balloons()
    max_pisteet = len(Meidän_ryhmä)
    saadut_pisteet = st.session_state.pisteet
    st.success(f"🎉 Peli on päättynyt! Tuloksesi: {saadut_pisteet}/{max_pisteet}")
    
    if saadut_pisteet == max_pisteet:
        st.markdown("""
        <div style="border: 8px double #D4AF37; padding: 30px; text-align: center; background-color: #FDFBF7; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin-top: 20px;">
            <span style="font-size: 50px;">🏅</span>
            <h1 style="color: #1A365D; font-family: 'Georgia', serif; font-size: 36px; margin-bottom: 5px;">VIRALLINEN TODISTUS</h1>
            <p style="color: #666; font-size: 14px; letter-spacing: 2px; margin-top: 0;">SUOMEN KIELEN OSAAMINEN</p>
            <hr style="border: 0; height: 1px; background-image: linear-gradient(to right, rgba(0,0,0,0), rgba(212,175,55,0.75), rgba(0,0,0,0)); margin: 20px 0;">
            <p style="font-size: 18px; color: #333; font-style: italic;">Täten todistetaan, etta</p>
            <h2 style="color: #D4AF37; font-family: 'Arial', sans-serif; font-size: 32px; margin: 15px 0;">Heidi Opettaja</h2>
            <p style="font-size: 18px; color: #333; line-height: 1.6;">
                on läpäissyt "Meidän ryhmä" -tietokilpailun <br>
                <b>täydellisillä pisteillä ({saadut_pisteet}/{max_pisteet})</b> <br>
                ja saavuttanut virallisesti tason:
            </p>
            <div style="background-color: #1A365D; color: white; display: inline-block; padding: 10px 40px; font-size: 30px; font-weight: bold; border-radius: 8px; margin: 20px 0; letter-spacing: 3px; box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
                TASO: B1
            </div>
            <p style="font-size: 16px; color: #555; margin-top: 15px;">
                <i>"Onnea! Sinä olet todellinen B1-tason mestari!"</i>
            </p>
            <hr style="border: 0; height: 1px; background-image: linear-gradient(to right, rgba(0,0,0,0), rgba(212,175,55,0.75), rgba(0,0,0,0)); margin: 20px 0;">
            <p style="font-size: 12px; color: #999;">Myönnetty kunnianosoituksena luokan opiskelijoilta</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("Heidi opettaja! Sinä olet A2.2. Yritä uudelleen saadaksesi B1-todistuksen! 💪")

    if st.button("Aloita alusta (Pelaa uudelleen) 🔄"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

else:
    current_q = st.session_state.sanat[st.session_state.idx]
    oikea_vastaus = Meidän_ryhmä[current_q]
    
    # 5. 이미지 출력 로직
    img_path = None
    target_folder = "image"
    
    if os.path.exists(target_folder):
        files = os.listdir(target_folder)
        if st.session_state.show_correct_image:
            for f in files:
                name_part, _ = os.path.splitext(f)
                if name_part.lower() == oikea_vastaus.lower():
                    img_path = os.path.join(target_folder, f)
                    break
        else:
            for f in files:
                if "main" in f.lower():
                    img_path = os.path.join(target_folder, f)
                    break

    if img_path and os.path.exists(img_path):
        try:
            image = Image.open(img_path)
            st.image(image, width=300)
        except Exception:
            st.warning("⚠️ Kuvan avaamisessa on ongelma.")
    else:
        st.error(f"❌ Kuvaa ei löytynyt: image/{oikea_vastaus.lower()}")

    # 6. UI 및 입력창
    st.write(f"**Kysymys {st.session_state.idx + 1} / {len(Meidän_ryhmä)}**")
    st.info(current_q)

    if 'feedback' in st.session_state:
        if st.session_state.feedback_type == "success":
            st.success(st.session_state.feedback)
        else:
            st.error(st.session_state.feedback)

    if st.session_state.show_correct_image:
        if st.button("Seuraava kysymys ➡️"):
            st.session_state.show_correct_image = False
            st.session_state.idx += 1
            if 'feedback' in st.session_state:
                del st.session_state.feedback
            
            if st.session_state.idx >= len(st.session_state.sanat):
                st.session_state.game_over = True
            st.rerun()
    else:
        with st.form(key=f"quiz_form_{st.session_state.idx}", clear_on_submit=True):
            user_input = st.text_input("Kirjoita nimi tähän:").strip()
            submit_button = st.form_submit_button(label="Tarkista")
            
            if submit_button and user_input:
                if user_input.title() == oikea_vastaus:
                    st.session_state.feedback = "Heidi opettaja! Sinä olet B1 🎉"
                    st.session_state.feedback_type = "success"
                    st.session_state.pisteet += 1
                    st.session_state.show_correct_image = True
                    st.rerun()
                else:
                    st.session_state.feedback = f"Heidi opettaja! Sinä olet A2.2\nVinkki: {oikea_vastaus[0]}"
                    st.session_state.feedback_type = "error"
                    st.rerun()
