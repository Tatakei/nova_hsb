import streamlit as st

st.set_page_config(
    layout="wide",
    initial_sidebar_state="collapsed",
    page_title="Nova"
)

def local_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"CSS Datei nicht gefunden unter: {file_name}")

local_css("assets/style.css")

st.markdown('<h1 class="main-title">Nova</h1>', unsafe_allow_html=True)

def purple_card_row(card_items):
    cards_html = ""
    for label, page_name, img_path in card_items:
        card_html = (
            f'<a href="./{page_name}" target="_self" class="purple-card">'
            f'<img src="{img_path}" class="card-img">'
            f'<div class="card-label">{label}</div>'
            f'</a>'
        )
        cards_html += card_html

    layout_html = f'<div class="card-container">{cards_html}</div>'
    st.markdown(layout_html, unsafe_allow_html=True)

purple_card_row([
    ("NPC", "npc", "app/static/images/npc/builder.png"),
    ("Bazaar", "bazaar", "app/static/images/npc/bazaar.png"),
    ("Auction", "auction_house", "app/static/images/npc/auction_master.png")
])