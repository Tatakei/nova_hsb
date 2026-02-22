import streamlit as st
import time
from features.item_price import get_bazaar_data, function_grab_item_price

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.set_page_config(layout="wide")
local_css("assets/style.css")

st.title("Bat Firework")

col1, col2, col3 = st.columns(3)
col11, = st.columns(1)

with col1:
    gc_box = st.container(key="blue_container")
with col2:
    pc_box = st.container(key="red_container")
with col3:
    calc_box = st.container(key="green_container")
with col11:
    next_box = st.container(key="purple_container")

gc_text = gc_box.empty()
pc_text = pc_box.empty()
calc_text = calc_box.empty()
next_text = next_box.empty()

while True:
    data = get_bazaar_data()

    if data:
        gc_sell, gc_buy = function_grab_item_price(data, "GREEN_CANDY")
        pc_sell, pc_buy = function_grab_item_price(data, "PURPLE_CANDY")
        total_value = gc_sell * 100
        min_value = pc_buy * 5
        avg_value = pc_buy * 11.1099
        max_value = pc_buy * 64

        with gc_text.container():
            st.markdown("### Green Candy")
            st.metric("Sell", f"{gc_sell:,.1f}")
            st.metric("Buy", f"{gc_buy:,.1f}")

        with pc_text.container():
            st.markdown("### Purple Candy")
            st.metric("Sell", f"{pc_sell:,.1f}")
            st.metric("Buy", f"{pc_buy:,.1f}")

        with calc_text.container():
            st.markdown("### Stack Value")
            st.metric("100x Green Candies", f"{total_value:,.1f}")
            st.metric("5x Purple Candies", f"{min_value:,.1f}")
            st.metric("11.1099x Purple Candies", f"{avg_value:,.1f}")
            st.metric("64x Purple Candies", f"{max_value:,.1f}")

    for i in range(30, 0, -1):
        with next_text.container():
            st.markdown("### Next Update")
            st.metric("Refreshing in...", f"{i}s")
        time.sleep(1)