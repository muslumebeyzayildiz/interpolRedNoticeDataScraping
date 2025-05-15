import requests
import pandas as pd
import os

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Referer": "https://www.interpol.int/",
    "Origin": "https://www.interpol.int",
    "Connection": "keep-alive",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site"
}

# Fotoğrafları kaydedeceğin klasör
photo_folder = "photos"
os.makedirs(photo_folder, exist_ok=True)

# Excel dosyasını oku
df = pd.read_excel("Interpol_Tum_KayitlarV6.xlsx")

for idx, row in df.iterrows():
    detail_url = row["detail_link"]
    entity_id = row["entity_id"]

    response = requests.get(detail_url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        image_links = data.get("_links", {}).get("images", {}).get("href", "")

        if image_links:
            img_resp = requests.get(image_links, headers=headers)

            if img_resp.status_code == 200:
                img_data = img_resp.json()
                embedded_images = img_data.get("_embedded", {}).get("images", [])

                # Birden fazla resim varsa her birini indir
                for i, img in enumerate(embedded_images):
                    picture_url = img.get("_links", {}).get("self", {}).get("href", "")
                    if picture_url:
                        pic_resp = requests.get(picture_url, headers=headers)
                        if pic_resp.status_code == 200:
                            safe_entity_id = entity_id.replace("/", "_")
                            image_path = os.path.join(photo_folder, f"{safe_entity_id}_{i + 1}.jpg")
                            with open(image_path, "wb") as file:
                                file.write(pic_resp.content)
                            print(f"{safe_entity_id}_{i + 1}.jpg indirildi.")
                        else:
                            print(f"Resim indirilemedi: {entity_id} (durum kodu {pic_resp.status_code})")
            else:
                print(f"Fotoğraf bağlantısı alınamadı: {entity_id}")
        else:
            print(f"Resim yok: {entity_id}")
    else:
        print(f"Detay sayfası açılmadı: {entity_id}")
