import streamlit as st
import streamlit.components.v1 as components
from PIL import Image
import random
import os

# =========================================================================
# [필수 수정] 카카오톡/슬랙 등에 링크를 보냈을 때 뜨게 할 사진 주소를 넣어주세요.
# 내부 경로(예: "image/main.png")는 안 되며, 인터넷 주소(http...)여야 합니다.
# =========================================================================
OG_IMAGE_URL = "YOUR_IMAGE_URL_HERE" 
PAGE_TITLE = "Meidän ryhmä"
PAGE_DESC = "Heidi opettajan B1-tasoa testaava hauska luokkatesti!"

# 1. 페이지 기본 설정 (무조건 코드의 최상단에 위치해야 에러가 나지 않습니다)
st.set_page_config(
    page_title=PAGE_TITLE, 
    layout="centered",
    page_icon="👥"
)

# 2. 링크 미리보기용 Open Graph 메타태그 강제 주입
components.html(
    f"""
    <head>
        <!-- Open Graph / Facebook / Kakao -->
        <meta property="og:type" content="website">
        <meta property="og:title" content="{PAGE_TITLE}">
        <meta property="og:description" content="{PAGE_DESC}">
        <meta property="og:image" content="{OG_IMAGE_URL}">

        <!-- Twitter -->
        <meta property="twitter:card" content="summary_large_image">
        <meta property="twitter:title" content="{PAGE_TITLE}">
        <meta property="twitter:description" content="{PAGE_DESC}">
        <meta property="twitter:image" content="{OG_IMAGE_URL}">
    </head>
    """,
    height=0, # 화면 레이아웃을 해치지 않도록 높이를 0으로 설정
)
# =========================================================================

# 퀴즈 데이터 정의
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
    "Hän istuu aina keskirivissä og opiskelee suomea todella ahkerasti.": "Yogendra",
    "Hänellä on aina paras ystävä vierellään. Molemmat heistä puhuvat erittäin hyvää suomea.": "Soosan"
}

# 세션 상태(Session State) 초기화
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

st.title("Meidän ryhmä")

if st.session_state.game_over:
    st.balloons()
    max_pisteet = len(Meidän_ryhmä)
    saadut_pisteet = st.session_state.pisteet
    
    st.success(f"🎉 Lopputesti on päättynyt! Tuloksesi: {saadut_pisteet}/{max_pisteet}")
    
    if saadut_pisteet == max_pisteet:
        st.markdown(f"""
        <div style="border: 8px double #D4AF37; padding: 30px; text-align: center; background-color: #FDFBF7; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); margin-top: 20px;">
            <span style="font-size: 50px;">🏅</span>
            <h1 style="color: #1A365D; font-family: 'Georgia', serif; font-size: 36px; margin-bottom: 5px;">VIRALLINEN TODISTUS</h1>
            <p style="color: #666; font-size: 14px; letter-spacing: 2px; margin-top: 0;">SUOMEN KIELEN OSAAMINEN</p>
            <hr style="border: 0; height: 1px; background-image: linear-gradient(to right, rgba(0,0,0,0), rgba(212,175,55,0.75), rgba(0,0,0,0)); margin: 20px 0;">
            <p style="font-size: 18px; color: #333; font-style: italic;">Täten todistetaan, että</p>
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

    if st.button("Aloita alusta 🔄"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

else:
    current_q = st.session_state.sanat[st.session_state.idx]
    oikea_vastaus = Meidän_ryhmä[current_q]
    
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
