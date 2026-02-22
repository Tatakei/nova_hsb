import requests

def get_bazaar_data():
    URL = "https://api.hypixel.net/v2/skyblock/bazaar"
    try:
        response = requests.get(URL, timeout=5)
        data = response.json()
        if data.get("success"):
            return data["products"]
    except:
        pass
    return {}

def function_grab_item_price(products, item_id):
    if not products or item_id not in products:
        return 0, 0

    product_data = products[item_id]

    sell_summary = product_data.get("sell_summary", [])
    bazaar_sell_price = sell_summary[0]["pricePerUnit"] if sell_summary else 0

    buy_summary = product_data.get("buy_summary", [])
    bazaar_buy_price = buy_summary[0]["pricePerUnit"] if buy_summary else 0

    return bazaar_sell_price, bazaar_buy_price