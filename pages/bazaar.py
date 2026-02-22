import streamlit as st
import requests
import time

st.set_page_config(layout="wide", page_title="Bazaar NPC Flip")

def local_css():
    st.markdown("""
    <style>
        .main-title { color: #ffd700; text-align: center; text-shadow: 0 0 10px rgba(255, 215, 0, 0.6); margin-bottom: 20px; }
        .stats-container { background: rgba(26, 26, 46, 0.95); padding: 15px; border-radius: 8px; border: 1px solid #00ffff; margin-bottom: 20px; text-align: center; }
        .item-card { background: #1a1a2e; border-radius: 10px; padding: 20px; border: 1px solid rgba(255, 255, 255, 0.1); margin-bottom: 20px; height: 100%; text-align: center; }
        .item-id { color: #ffd700; font-size: 1.1rem; font-weight: bold; margin-bottom: 10px; display: block; width: 100%; }
        .price-val { color: #00ff99; font-weight: bold; }
        .profit-val { color: #00ffff; font-weight: bold; font-size: 1.2rem; }
        hr { border: 0; border-top: 1px solid #333; margin: 10px auto; width: 80%; }
        div[data-testid="stMetricValue"] { text-align: center !important; }
        div[data-testid="stMetricLabel"] { text-align: center !important; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

local_css()

def get_data():
    try:
        b_res = requests.get("https://api.hypixel.net/v2/skyblock/bazaar", timeout=5).json()
        i_res = requests.get("https://api.hypixel.net/v2/resources/skyblock/items", timeout=5).json()
        b_prod = b_res.get("products", {})
        npc_map = {i["id"]: i.get("npc_sell_price", 0) for i in i_res.get("items", [])}
        
        proc = []
        stts = {"1m+": 0, "500k-1m": 0, "250k-500k": 0, "100k-250k": 0, "50k-100k": 0, "0-50k": 0}

        for k, v in b_prod.items():
            q = v.get("quick_status", {})
            npc = npc_map.get(k, 0)
            if npc == 0 or (q.get("buyOrders") == 0 and q.get("sellOrders") == 0): continue
            p = npc - q.get("sellPrice", 0)
            if p <= 0: continue
            
            if p >= 1_000_000: stts["1m+"] += 1
            elif p >= 500_000: stts["500k-1m"] += 1
            elif p >= 250_000: stts["250k-500k"] += 1
            elif p >= 100_000: stts["100k-250k"] += 1
            elif p >= 50_000: stts["50k-100k"] += 1
            else: stts["0-50k"] += 1
            
            proc.append({
                "id": k.replace('_', ' ').title(),
                "sellPrice": q.get("sellPrice", 0),
                "npc_price": npc,
                "profit": p,
                "sellOrders": q.get("sellOrders", 0)
            })
        return proc, stts
    except:
        return [], {"1m+": 0, "500k-1m": 0, "250k-500k": 0, "100k-250k": 0, "50k-100k": 0, "0-50k": 0}

st.markdown('<h1 class="main-title">Hypixel Bazaar NPC Flip</h1>', unsafe_allow_html=True)

c1, c2 = st.columns(2)
sort_by = c1.selectbox("Sort By", ["Profit", "Demand"])
order = c2.radio("Order", ["High to Low", "Low to High"], horizontal=True)

t_place = st.empty()
s_place = st.empty()
g_place = st.empty()

if 'items' not in st.session_state:
    st.session_state['items'] = []
    st.session_state['stats'] = {"1m+": 0, "500k-1m": 0, "250k-500k": 0, "100k-250k": 0, "50k-100k": 0, "0-50k": 0}
    st.session_state['last_sync'] = 0

while True:
    now = time.time()
    next_sync = 31 - (now % 30)
    
    if (now - st.session_state['last_sync']) > 5 and next_sync > 29:
        d, s = get_data()
        if d:
            st.session_state['items'] = d
            st.session_state['stats'] = s
            st.session_state['last_sync'] = now

    t_place.metric("Next Sync In", f"{int(next_sync)}s")

    stts = st.session_state['stats']
    s_place.markdown(f"""
    <div class="stats-container">
        <strong>Profit Brackets:</strong> 1M+ ({stts['1m+']}) | 500k-1M ({stts['500k-1m']}) | 
        250k-500k ({stts['250k-500k']}) | 100k-250k ({stts['100k-250k']}) | 
        50k-100k ({stts['50k-100k']}) | 0-50k ({stts['0-50k']})
    </div>
    """, unsafe_allow_html=True)

    curr = list(st.session_state['items'])
    if curr:
        sk = "profit" if sort_by == "Profit" else "sellOrders"
        sorted_d = sorted(curr, key=lambda x: x[sk], reverse=(order == "High to Low"))
        
        with g_place.container():
            for i in range(0, len(sorted_d), 4):
                cols = st.columns(4)
                chunk = sorted_d[i:i + 4]
                for idx, item in enumerate(chunk):
                    cols[idx].markdown(f"""
                    <div class="item-card">
                        <span class="item-id">{item['id']}</span>
                        <div style="font-size:0.9rem; color:#aaa;">
                            Bazaar: <span class="price-val">{item['sellPrice']:,.1f}</span><br>
                            NPC: <span class="price-val">{item['npc_price']:,.1f}</span><br>
                            <hr>
                            Profit: <span class="profit-val">{item['profit']:,.1f}</span><br>
                            <span style="font-size:11px; color:#666;">Orders: {item['sellOrders']:,}</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
    
    time.sleep(1)