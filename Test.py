import streamlit as st
from PIL import Image
import random
import os

st.set_page_config(
    page_title="Meidän ryhmä", 
    layout="centered",
    page_icon="👥"
)

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# 💡 [진짜 자동 재생 마법 코드]
# 처음엔 조용히 켜졌다가, 학생이 글자를 입력하기 위해 키보드를 누르거나 
# 화면을 건드리는 모든 자연스러운 행동을 감지해 음악 소리를 저절로 켭니다!
st.components.v1.html(
    """
    <iframe id="youtube-bgm" width="0" height="0" 
        src="https://www.youtube.com/embed/vT7_lO3VDic?autoplay=1&mute=1&loop=1&playlist=vT7_lO3VDic&enablejsapi=1" 
        title="BGM" frameborder="0" 
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
        style="position: absolute; width: 0; height: 0; border: none;">
    </iframe>

    <script>
    // 유튜브 플레이어 제어용 API
    var tag = document.createElement('script');
    tag.src = "https://www.youtube.com/iframe_api";
    var firstScriptTag = document.getElementsByTagName('script')[0];
    firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

    var player;
    function onYouTubeIframeAPIReady() {
        player = new YT.Player('youtube-bgm', {
            events: {
                'onReady': onPlayerReady
            }
        });
    }

    function onPlayerReady(event) {
        // 학생들이 문제를 풀려고 글자를 타이핑하거나 화면을 만지면 소리 잠금을 해제합니다.
        function unmuteBGM() {
            if(player && typeof player.unMute === 'function') {
                player.unMute();
                player.setVolume(50); // 소리 크기 50%
                // 소리가 켜지면 감지기 작동 중지
                window.removeEventListener('keydown', unmuteBGM);
                window.removeEventListener('input', unmuteBGM);
                window.removeEventListener('focus', unmuteBGM, true);
                window.removeEventListener('touchstart', unmuteBGM);
                window.removeEventListener('click', unmuteBGM);
            }
        }
        
        // 학생들이 할 수 있는 모든 자연스러운 행동을 감지 (키보드 치기, 입력하기 등)
        window.addEventListener('keydown', unmuteBGM);
        window.addEventListener('input', unmuteBGM);
        window.addEventListener('focus', unmuteBGM, true);
        window.addEventListener('touchstart', unmuteBGM);
        window.addEventListener('click', unmuteBGM);
    }
    </script>
    """,
    height=0,
)

st.components.v1.html(
    """
    <head>
        <meta property="og:type" content="website">
        <meta property="og:title" content="Meidän ryhmä">
        <meta property="og:description" content="Heidi opettajan B1-tasoa testaava hauska luokkatesti!">
        <meta property="og:image" content="https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=800">
        <meta property="twitter:card" content="summary_large_image">
        <meta property="twitter:title" content="Meidän ryhmä">
        <meta property="twitter:description" content="Heidi opettajan B1-tasoa testaava hauska luokkatesti!">
        <meta property="twitter:image" content="https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=800">
    </head>
    """,
    height=0,
)

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

    if 'feedback' in st.session_state:
        if st.session_state.feedback_type == "success": 
            st.success(st.session_state.feedback)
        else:
            st.error(st.session_state.feedback)
            st.markdown("""
            <div style="background-color: #FFF9E6; padding: 15px; border-left: 5px solid #FFCC00; border-radius: 5px;">
                <p style="margin: 0 0 8px 0; font-weight: bold; color: #7A5C00;">💡 Hint (Name Options):</p>
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
