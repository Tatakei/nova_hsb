import streamlit as st
import requests
import time

st.set_page_config(layout="wide", page_title="Bazaar NPC Flip")

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("assets/style.css")

def purple_card_row(card_items):
    cards_html = ""
    for label, page_name in card_items:
        card_html = f'<a href="./{page_name}" target="_self" class="small-purple-card">{label}</a>'
        cards_html += card_html
    st.markdown(f'<div class="card-container">{cards_html}</div>', unsafe_allow_html=True)

purple_card_row([("Zurück", "")])

def get_data():
    try:
        b_res = requests.get("https://api.hypixel.net/v2/skyblock/bazaar", timeout=5).json()
        i_res = requests.get("https://api.hypixel.net/v2/resources/skyblock/items", timeout=5).json()
        b_prod = b_res.get("products", {})
        npc_map = {i["id"]: i.get("npc_sell_price", 0) for i in i_res.get("items", [])}
        proc = []
        stts = {"1m+": 0, "500k-1m": 0, "250k-500k": 0, "100k-250k": 0, "50k-100k": 0, "0-50k": 0}
        for k, v in b_prod.items():
            # q = v.get("quick_status", {})
            bs = v.get("buy_summary")
            ss = v.get("sell_summary")
            if bs and len(bs) and ss and len(ss) > 0:
                top_buy_order = bs[0]
                top_sell_order = ss[0]

                sell_order_price = top_buy_order.get("pricePerUnit")
                sell_order_amount = top_buy_order.get("amount")

                buy_order_price = top_sell_order.get("pricePerUnit")
                buy_order_amount = top_sell_order.get("amount")

                #print(f"Product {k} | Top Price: {bp} | Amount: {ba}")
                #print(f"Product {k} | Top Price: {sp} | Amount: {sa}")

                npc = npc_map.get(k, 0)
                if npc == 0 or buy_order_price == 0 and buy_order_price == 0: continue
                p = npc - buy_order_price
                if p <= 0: continue
                if p >= 1_000_000:
                    stts["1m+"] += 1
                elif p >= 500_000:
                    stts["500k-1m"] += 1
                elif p >= 250_000:
                    stts["250k-500k"] += 1
                elif p >= 100_000:
                    stts["100k-250k"] += 1
                elif p >= 50_000:
                    stts["50k-100k"] += 1
                else:
                    stts["0-50k"] += 1
                proc.append(
                    {"id": k.replace('_', ' ').title(), "sellPrice": buy_order_price, "npc_price": npc,
                     "profit": p,
                     "sellOrders": buy_order_amount})
            else:
                abc = ""
                abc = "abc"
                #print(f"Product: {k} | No active buy summary found.")
        return proc, stts
    except:
        return [], {"1m+": 0, "500k-1m": 0, "250k-500k": 0, "100k-250k": 0, "50k-100k": 0, "0-50k": 0}


st.markdown('<h1 class="main-title">Hypixel Bazaar NPC Flip</h1>', unsafe_allow_html=True)

c1, c2 = st.columns(2)
sort_by = c1.selectbox("Sort By", ["Profit", "Demand"])
order = c2.radio("Order", ["High to Low", "Low to High"], horizontal=True)

if 'items' not in st.session_state:
    st.session_state['items'], st.session_state['stats'], st.session_state['last_sync'] = [], {"1m+": 0, "500k-1m": 0,
                                                                                               "250k-500k": 0,
                                                                                               "100k-250k": 0,
                                                                                               "50k-100k": 0,
                                                                                               "0-50k": 0}, 0

timer_place = st.empty()
s_place = st.empty()
g_place = st.empty()

while True:
    now = time.time()
    next_sync = 31 - (now % 30)

    if (now - st.session_state['last_sync']) > 5 and next_sync > 29:
        d, s = get_data()
        if d:
            st.session_state['items'], st.session_state['stats'], st.session_state['last_sync'] = d, s, now

    timer_place.markdown(
        f'''<div class="next-sync-container"><span class="next-sync-text">Next Sync: {int(next_sync)}s</span></div>''',
        unsafe_allow_html=True
    )

    stts = st.session_state['stats']
    s_place.markdown(
        f'''<div class="stats-box"><strong>Profit Brackets:</strong> 1M+ ({stts["1m+"]}) | 500k-1M ({stts["500k-1m"]}) | 250k-500k ({stts["250k-500k"]}) | 100k-250k ({stts["100k-250k"]}) | 50k-100k ({stts["50k-100k"]}) | 0-50k ({stts["0-50k"]})</div>''',
        unsafe_allow_html=True)

    curr = list(st.session_state['items'])
    if curr:
        sk = "profit" if sort_by == "Profit" else "sellOrders"
        sorted_d = sorted(curr, key=lambda x: x[sk], reverse=(order == "High to Low"))

        with g_place.container():
            for i in range(0, len(sorted_d), 4):
                cols = st.columns(4)
                for idx, item in enumerate(sorted_d[i:i + 4]):

                    p_val = item["profit"]
                    if p_val >= 50_000:
                        p_class = "gradient-green"
                    elif p_val >= 30_000:
                        p_class = "gradient-green"
                    elif p_val >= 20_000:
                        p_class = "gradient-green"
                    elif p_val >= 10_000:
                        p_class = "gradient-green"
                    else:
                        p_class = "gradient-green"

                    html_content = (
                        f'<div class="info-item-card">'
                        f'<div class="item-id-label gradient-test">{item["id"]}</div>'
                        f'<div class="price-row">Bazaar: <span class="gradient-green">{item["sellPrice"]:,.1f}</span></div>'
                        f'<div class="price-row">NPC: <span class="gradient-green">{item["npc_price"]:,.1f}</span></div>'
                        f'<hr class="card-divider">'
                        f'<div class="profit-row">Profit: <span class="{p_class}">{item["profit"]:,.1f}</span></div>'
                        f'</div>'
                    )

                    cols[idx].markdown(html_content, unsafe_allow_html=True)

    time.sleep(1)