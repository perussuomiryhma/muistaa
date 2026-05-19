import streamlit as st
from PIL import Image
import random
import os

# 1. 퀴즈 데이터 세팅
Meidän_ryhmä = {
    "Kuka on luokkamme opettaja?": "Heidi", 
    "Kuka on luokkamme insinööri?": "Migara",
    "Kuka on luokkamme toinen insinööri?": "Sana",
    "Kuka on luokkamme vilkkain opiskelija?": "Tanja",
    "Hän tuli luokallemme kesken kurssin, kun se oli jo alkanut.": "Mbuyi",
    "Hän vastaa aina erittäin aktiivisesti tunneilla.": "Hamza",
    "Hän osasi jo ensimmäisellä tunnilla paljon sanoja ja puhui hyvää suomea.": "Sunita",
    "Hän ymmärsi opettajaa ja vastasi hienosti heti ensimmäisestä tunnista lähtien.": "Antony",
    "Hän tuli luokallemme noin elokuussa. Puhuu hyvää suomea ja haaveilee vaatesuunnittelijan urasta.": "Khali",
    "Hän on pieni mutta vahva. Hän on aina erittäin ystävällinen.": "Sakineh",
    "Hänestä oli heti alusta asti paljon huhuja, että hän puhuu erittäin hyvää suomea.": "Oksana",
    "Hän oli erittäin aktiivinen ensiapuohjelmassa.": "Andrii",
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
    st.session_state.game_started = False  # 게임 시작 여부 확인용

st.set_page_config(page_title="Meidän ryhmä", page_icon="🇫🇮", layout="centered")


# 🎵 3. 보이지 않는 플레이어 (시작 버튼을 누르면 유튜브 음악 재생 시작)
if st.session_state.game_started and not st.session_state.game_over:
    st.markdown("""
        <iframe width="1" height="1" 
            src="https://www.youtube.com/embed/5w3pMAsgR08?autoplay=1&loop=1&playlist=5w3pMAsgR08&mute=0" 
            frameborder="0" 
            allow="autoplay; encrypted-media" 
            style="position:absolute; top:-100px; left:-100px;">
        </iframe >
    """, unsafe_allow_html=True)


st.title("🇫🇮 Meidän ryhmä")

# 🎮 대기 화면: 아직 게임 시작 버튼을 안 눌렀을 때
if not st.session_state.game_started:
    st.write("### Tervetuloa peliin! (게임을 환영합니다!)")
    st.info("Klikkaa alla olevaa painiketta aloittaaksesi pelin musiikin kanssa. 🎉\n(아래 버튼을 누르면 음악과 함께 게임이 시작됩니다.)")
    
    # 메인 퀴즈 표지 이미지 띄우기
    target_folder = "image"
    if os.path.exists(target_folder):
        for f in os.listdir(target_folder):
            if "main" in f.lower():
                st.image(Image.open(os.path.join(target_folder, f)), width=350)
                break
                
    if st.button("▶️ Aloita peli (게임 시작)", type="primary", use_container_width=True):
        st.session_state.game_started = True
        st.rerun()

# 🏆 게임 완료 화면 (B1 증서)
elif st.session_state.game_over:
    st.balloons()
    max_pisteet = len(Meidän_ryhmä)
    saadut_pisteet = st.session_state.pisteet
    st.success(f"🎉 Peli on päättynyt! Tuloksesi: {saadut_pisteet}/{max_pisteet}")
    
    if saadut_pisteet == max_pisteet:
        st.markdown(f"""
        <div style="border: 8px double #D4AF37; padding: 30px; text-align: center; background-color: #FDFBF7; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin-top: 20px;">
            <span style="font-size: 50px;">🏅</span>
            <h1 style="color: #1A365D; font-family: 'Georgia', serif; font-size: 36px; margin-bottom: 5px;">VIRALLINEN TODISTUS</h1>
            <p style="color: #666; font-size: 14px; letter-spacing: 2px; margin-top: 0;">SUOMEN KIELEN OSAAMINEN</p>
            <hr style="border: 0; height: 1px; background-image: linear-gradient(to right, rgba(0,0,0,0), rgba(212,175,55,0.75), rgba(0,0,0,0)); margin: 20px 0;">
            <p style="font-size: 18px; color: #333; font-style: italic;">Talten todistetaan, että</p>
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

# 📝 진행 화면: 게임 중일 때
else:
    current_q = st.session_state.sanat[st.session_state.idx]
    oikea_vastaus = Meidän_ryhmä[current_q]
    
    # 이미지 출력 로직
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
        st.error(f"❌ Kuvaa ei löytynyt: image/{document.vastaus.lower()}")

    # UI 및 입력창
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
