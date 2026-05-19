import streamlit as st
import streamlit.components.v1 as components
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

# 🎵 3. 무한 반복 배경음악 플레이어 (새로고침되어도 유지되는 비밀 코드)
# 크롬 브라우저 정책상 사용자가 웹사이트 아무 곳이나 한 번 클릭해야 소리가 나기 시작합니다!
st.markdown("""
    <iframe src="https://colab.research.google.com/" style="display:none;" id="dummy"></iframe>
    <audio id="bgm" autoplay loop>
        <source src="app/static/bgm.mp3" type="audio/mp3">
    </audio>
    <script>
        // 무한 반복 및 페이지 이동 시 기억 장치 작동
        var audio = document.getElementById("bgm");
        audio.volume = 0.4; // 볼륨 조절 (0.0 ~ 1.0)
        
        // 페이지 새로고침 시 음악이 끊기지 않은 것처럼 이어 붙이는 마법
        if (localStorage.getItem("bgm_time")) {
            audio.currentTime = parseFloat(localStorage.getItem("bgm_time"));
        }
        setInterval(function() {
            localStorage.setItem("bgm_time", audio.currentTime);
        }, 300);
    </script>
""", unsafe_allow_html=True)


if st.session_state.game_over:
    st.balloons()
    st.success(f"🎉 Peli on päättynyt! Tuloksesi: {st.session_state.pisteet}/{len(Meidän_ryhmä)}")
    st.info("Heidi opettaja, sinä olet B1, tämä on B1 todistus! 📜")
    if st.button("Aloita alusta (Pelaa uudelleen)"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.erase()
        st.rerun()

else:
    current_q = st.session_state.sanat[st.session_state.idx]
    oikea_vastaus = Meidän_ryhmä[current_q]
    
    # 4. 이미지 출력 로직
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

    # 5. UI 및 입력창
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
