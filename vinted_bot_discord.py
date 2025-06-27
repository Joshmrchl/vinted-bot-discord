import requests
import time

# === CONFIGURATION ===

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1388204246540882121/KmVLeeTL5DYxJJVW-gibBpIF93kx44veFnKdomDyLIDK15TuGZEgk-iueIKZwQ2lmwCx"

SEARCH_URLS = [
    "https://www.vinted.fr/api/v2/catalog/items?search_text=nike%20air%20max&size_id=40&price_to=60"
]

CHECK_INTERVAL = 300  # toutes les 5 minutes

# === FIN CONFIGURATION ===

seen_items = set()

def send_discord_alert(title, price, url, image_url):
    data = {
        "embeds": [
            {
                "title": title,
                "url": url,
                "description": f"**Prix :** {price} €",
                "image": {"url": image_url},
                "color": 0x57F287
            }
        ]
    }
    requests.post(DISCORD_WEBHOOK_URL, json=data)

def check_vinted(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        items = response.json().get("items", [])
        for item in items:
            item_id = item["id"]
            if item_id not in seen_items:
                seen_items.add(item_id)
                title = item['title']
                price = item['price']
                item_url = f"https://www.vinted.fr{item['url']}"
                image_url = item['photo']['url']
                send_discord_alert(title, price, item_url, image_url)
    except Exception as e:
        print(f"Erreur : {e}")

def main():
    while True:
        for url in SEARCH_URLS:
            check_vinted(url)
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()

