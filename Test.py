import streamlit as st
from PIL import Image
import random
import os

# 1. 페이지 설정
st.set_page_config(
    page_title="Meidän ryhmä", 
    layout="centered",
    page_icon="👥"
)

# 2. 왓츠앱/팀즈 메신저용 절대 깨지지 않는 1번 퀴즈 일러스트 사진 등록
st.components.v1.html(
    """
    <head>
        <meta property="og:type" content="website">
        <meta property="og:title" content="Meidän ryhmä">
        <meta property="og:description" content="Heidi opettajan B1-tasoa testaava hauska luokkatesti!">
        <meta property="og:image" content="https://pub-static.fotor.com/assets/projects/pages/d9f78310-8bde-11ed-bd68-d326f63459c7_55eef501-f2f2-4467-8d89-9dbb3b4bf2da_w.jpg">
        <meta property="twitter:card" content="summary_large_image">
        <meta property="twitter:title" content="Meidän ryhmä">
        <meta property="twitter:description" content="Heidi opettajan B1-tasoa testaava hauska luokkatesti!">
        <meta property="twitter:image" content="https://pub-static.fotor.com/assets/projects/pages/d9f78310-8bde-11ed-bd68-d326f63459c7_55eef501-f2f2-4467-8d89-9dbb3b4bf2da_w.jpg">
    </head>
    """,
    height=0,
)

# 퀴즈 데이터
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

if 'questions' not in st.session_state:
    all_questions = list(Meidän_ryhmä.keys())
    st.session_state.questions = [all_questions[0]] + random.sample(all_questions[1:], len(all_questions)-1)
    st.session_state.current_idx = 0
    st.session_state.score = 0
    st.session_state.game_over = False
    st.session_state.show_correct_image = False

st.title("Meidän ryhmä")

if st.session_state.game_over:
    st.balloons()
    st.success(f"🎉 Lopputesti on päättynyt! Tuloksesi: {st.session_state.score}/{len(Meidän_ryhmä)}")
    if st.button("Aloita alusta 🔄"):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()
else:
    current_q = st.session_state.questions[st.session_state.current_idx]
    correct_answer = Meidän_ryhmä[current_q]
    
    img_path = None
    for folder in ["image", "pic"]:
        if os.path.exists(folder):
            files = os.listdir(folder)
            for f in files:
                if (st.session_state.show_correct_image and os.path.splitext(f)[0].lower() == correct_answer.lower()) or (not st.session_state.show_correct_image and "main" in f.lower()):
                    img_path = os.path.join(folder, f)
                    break
        if img_path: break

    if img_path and os.path.exists(img_path):
        try: st.image(Image.open(img_path), width=300)
        except: pass

    st.write(f"**Kysymys {st.session_state.current_idx + 1} / {len(Meidän_ryhmä)}**")
    st.info(current_q)

    # 💡 틀렸을 때 선생님이 주신 명단을 예쁘게 정렬해서 힌트창에 띄워줍니다.
    if 'feedback' in st.session_state:
        if st.session_state.feedback_type == "success": 
            st.success(st.session_state.feedback)
        else:
            st.error(st.session_state.feedback)
            st.markdown("""
            <div style="background-color: #FFF9E6; padding: 15px; border-left: 5px solid #FFCC00; border-radius: 5px;">
                <p style="margin: 0 0 8px 0; font-weight: bold; color: #7A5C00;">💡 Vinkki (Nimivaihtoehdot):</p>
                <p style="margin: 0; color: #555; font-size: 14px; line-height: 1.6;">
                    Heidi, Anna, Mbuyi, Migara, Sana, Tanja, Hamza, Sunita, Antony, <br>
                    Khali, Sakineh, Oksana, Andrii, Serhii, Elena, Elius, Yogendra, Soosan
                </p>
            </div>
            """, unsafe_allow_html=True)

    if st.session_state.show_correct_image:
        if st.button("Seuraava kysymys ➡️"):
            st.session_state.show_correct_image = False
            st.session_state.current_idx += 1
            if 'feedback' in st.session_state: del st.session_state.feedback
            if st.session_state.current_idx >= len(st.session_state.questions): st.session_state.game_over = True
            st.rerun()
    else:
        with st.form(key=f"quiz_form_{st.session_state.current_idx}", clear_on_submit=True):
            user_input = st.text_input("Kirjoita nimi tähän:").strip()
            if st.form_submit_button(label="Tarkista") and user_input:
                if user_input.title() == correct_answer:
                    st.session_state.feedback = "Heidi opettaja! Sinä olet B1 🎉"
                    st.session_state.feedback_type = "success"
                    st.session_state.score += 1
                    st.session_state.show_correct_image = True
                else:
                    st.session_state.feedback = "Heidi opettaja! Sinä olet A2.2 ❌"
                    st.session_state.feedback_type = "error"
                st.rerun()
