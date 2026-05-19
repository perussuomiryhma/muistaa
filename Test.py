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
        <meta property="og:type" content="website">
        <meta property="og:title" content="{PAGE_TITLE}">
        <meta property="og:description" content="{PAGE_DESC}">
        <meta property="og:image" content="{OG_IMAGE_URL}">

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
    "Hän istuu aina keskirivissä ja opiskelee suomea todella ahkerasti.": "Yogendra",
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

classic_bgm = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3"

if not st.session_state.game_over:
    st.markdown(f"""
        <audio id="bg
